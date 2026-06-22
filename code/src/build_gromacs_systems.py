#!/usr/bin/env python3
"""
D11.1 — Build GROMACS systems for 27 AlphaFold DB v6 proteins
- pdbfixer: add missing atoms, hydrogens
- pdb2gmx: topology (AMBER99SB-ILDN, available in conda; CHARMM36 not in conda-forge gromacs)
- Solvate: TIP3P, dodecahedron, 1.0 nm margin
- Ions: 0.15 M NaCl
- EM: steepest descent 5000 steps, Fmax < 1000 kJ/mol/nm
"""
import os, sys, json, time, subprocess, shutil
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

# --- Configuration ---
BASE = Path("/Users/chen/.mavis/agents/mavis/workspace/genomics_exploration/17_v8_feature_driven/50_paper_v11_D11_MD/D11.1_systems")
PDB_DIR = BASE / "pdbs"
SYS_DIR = BASE / "systems"
LOG_DIR = BASE / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# AMBER99SB-ILDN force field (CHARMM36 not bundled in conda-forge gromacs)
FORCE_FIELD = "amber99sb-ildn"
WATER_MODEL = "tip3p"
EM_STEPS = 5000
ION_CONC_M = 0.15  # 0.15 M NaCl
BOX_MARGIN_NM = 1.0
BOX_TYPE = "dodecahedron"
FMAX_TOLERANCE_KJ = 1000.0

# 27 v10 final gene → UniProt accession (corrected SLC35G1 → Q2M3R5)
GENE_MAP = {
    "SLC35G1":     ("Q2M3R5", "multimer"),
    "ST6GAL1":     ("P15907", "multimer"),
    "ST3GAL4":     ("Q11206", "multimer"),
    "ST6GALNAC1":  ("Q9NSC7", "multimer"),
    "STAT1":       ("P42224", "multimer"),
    "CD274":       ("Q9NZQ7", "multimer"),
    "CD8A":        ("P01732", "multimer"),
    "CD44":        ("P16070", "multimer"),
    "MUC1":        ("P15941", "multimer"),
    "ST3GAL1":     ("Q11201", "monomer"),
    "ST3GAL2":     ("Q16842", "monomer"),
    "ST3GAL3":     ("Q11203", "monomer"),
    "ST3GAL5":     ("Q9UNP4", "monomer"),
    "ST3GAL6":     ("Q9Y274", "monomer"),
    "TP53":        ("P04637", "monomer"),
    "KRAS":        ("P01116", "monomer"),
    "BRAF":        ("P15056", "monomer"),
    "EGFR":        ("P00533", "monomer"),
    "MYC":         ("P01106", "monomer"),
    "CCND1":       ("P24385", "monomer"),
    "CDK4":        ("P11802", "monomer"),
    "CDK6":        ("Q00534", "monomer"),
    "RB1":         ("P06400", "monomer"),
    "VIM":         ("P08670", "monomer"),
    "CDH1":        ("P12830", "monomer"),
    "IFNG":        ("P01579", "monomer"),
    "FOXP3":       ("Q9BZS1", "monomer"),
}

# GROMACS prefix
GMX = "/Users/chen/miniconda3/envs/md/bin/gmx"
PYTHON = "/Users/chen/miniconda3/envs/md/bin/python3"


def _gmx(args, cwd=None, input_str=None, log_file=None, timeout=None):
    """Run gmx command and capture stdout/stderr. EM mdrun gets longer timeout (3600s)."""
    if timeout is None:
        # EM mdrun is the slow step; bump default
        timeout = 1800 if "mdrun" in args else 600
    cmd = [GMX] + args
    if input_str:
        proc = subprocess.run(cmd, input=input_str, capture_output=True, text=True, cwd=cwd, timeout=timeout)
    else:
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=timeout)
    if log_file:
        log_file.write(f"\n>>> {' '.join(cmd)}\n")
        if input_str:
            log_file.write(f"<<< stdin: {input_str!r}\n")
        log_file.write(f"--- stdout ---\n{proc.stdout}\n")
        if proc.returncode != 0:
            log_file.write(f"--- stderr ---\n{proc.stderr}\n")
    if proc.returncode != 0:
        raise RuntimeError(f"gmx {' '.join(args)} failed in {cwd}: {proc.stderr[-500:]}")
    return proc


def fix_pdb(in_pdb: Path, out_pdb: Path):
    """Use pdbfixer + OpenMM to add missing atoms/H, fix non-standard residues."""
    from pdbfixer import PDBFixer
    from openmm.app import PDBFile
    fixer = PDBFixer(filename=str(in_pdb))
    fixer.findNonstandardResidues()
    if fixer.nonstandardResidues:
        fixer.replaceNonstandardResidues()
    fixer.findMissingResidues()
    fixer.findMissingAtoms()
    fixer.addMissingAtoms()
    fixer.addMissingHydrogens(7.0)  # pH 7.0
    with open(out_pdb, "w") as f:
        PDBFile.writeFile(fixer.topology, fixer.positions, f)
    return out_pdb


def pLDDT_score(pdb: Path):
    """Extract B-factor (pLDDT) summary from AF PDB."""
    bfactors = []
    with open(pdb) as f:
        for line in f:
            if line.startswith("ATOM"):
                try:
                    bfactor = float(line[60:66])
                    bfactors.append(bfactor)
                except ValueError:
                    pass
    if not bfactors:
        return None
    mean_plddt = sum(bfactors) / len(bfactors)
    n_total = len(bfactors)
    n_very_high = sum(1 for b in bfactors if b > 90)  # pLDDT > 90
    n_confident = sum(1 for b in bfactors if 70 <= b <= 90)
    n_low = sum(1 for b in bfactors if 50 <= b < 70)
    n_very_low = sum(1 for b in bfactors if b < 50)
    return {
        "mean_pLDDT": round(mean_plddt, 2),
        "n_atoms": n_total,
        "frac_very_high": round(n_very_high / n_total, 3),
        "frac_confident": round(n_confident / n_total, 3),
        "frac_low": round(n_low / n_total, 3),
        "frac_very_low": round(n_very_low / n_total, 3),
    }


def build_system(gene, acc, kind):
    """Build GROMACS system for one protein. Returns stats dict."""
    work = SYS_DIR / f"{gene}_{acc}"
    work.mkdir(parents=True, exist_ok=True)
    log = open(LOG_DIR / f"{gene}_{acc}.log", "w")
    stats = {"gene": gene, "acc": acc, "kind": kind, "work": str(work)}
    t0 = time.time()
    try:
        # 1. Fix PDB
        in_pdb = PDB_DIR / f"{gene}_{acc}.pdb"
        fixed_pdb = work / f"{gene}_fixed.pdb"
        fix_pdb(in_pdb, fixed_pdb)
        stats["pdb_fixed_size"] = fixed_pdb.stat().st_size
        stats["pLDDT"] = pLDDT_score(in_pdb)
        log.write(f"=== D11.1 build: {gene} ({acc}, {kind}) ===\n")
        log.write(f"Step 1 (pdbfixer): OK, size={fixed_pdb.stat().st_size} bytes\n")
        log.write(f"pLDDT: {stats['pLDDT']}\n")

        # 2. pdb2gmx — generate topology with AMBER99SB-ILDN + TIP3P
        _gmx([
            "pdb2gmx",
            "-f", str(fixed_pdb),
            "-o", str(work / f"{gene}_processed.gro"),
            "-p", str(work / f"{gene}_topol.top"),
            "-i", str(work / "posre.itp"),
            "-ff", FORCE_FIELD,
            "-water", WATER_MODEL,
            "-ignh",  # ignore hydrogens (we already added via pdbfixer)
            "-missing",  # keep missing atoms
        ], cwd=work, log_file=log)
        stats["pdb2gmx"] = "ok"
        log.write(f"Step 2 (pdb2gmx): OK\n")

        # 3. Define box — dodecahedron, 1.0 nm margin
        _gmx([
            "editconf",
            "-f", str(work / f"{gene}_processed.gro"),
            "-o", str(work / f"{gene}_boxed.gro"),
            "-c",  # center in box
            "-d", str(BOX_MARGIN_NM),  # margin
            "-bt", BOX_TYPE,
        ], cwd=work, log_file=log)
        log.write(f"Step 3 (editconf): OK\n")

        # 4. Solvate with TIP3P
        _gmx([
            "solvate",
            "-cp", str(work / f"{gene}_boxed.gro"),
            "-cs", "spc216.gro",  # standard pre-equilibrated water box
            "-o", str(work / f"{gene}_solvated.gro"),
            "-p", str(work / f"{gene}_topol.top"),
        ], cwd=work, log_file=log)
        log.write(f"Step 4 (solvate): OK\n")

        # 5. Add ions (0.15 M NaCl) — use grompp + genion
        # Create ions.mdp
        mdp_content = """; D11.1 ions.mdp
integrator      = steep
nsteps          = 0
cutoff-scheme   = Verlet
nstlist         = 10
"""
        (work / "ions.mdp").write_text(mdp_content)
        _gmx([
            "grompp",
            "-f", str(work / "ions.mdp"),
            "-c", str(work / f"{gene}_solvated.gro"),
            "-p", str(work / f"{gene}_topol.top"),
            "-o", str(work / "ions.tpr"),
            "-maxwarn", "2",
        ], cwd=work, log_file=log)
        # Replace solvent with ions
        _gmx([
            "genion",
            "-s", str(work / "ions.tpr"),
            "-o", str(work / f"{gene}_ionized.gro"),
            "-p", str(work / f"{gene}_topol.top"),
            "-pname", "NA",
            "-nname", "CL",
            "-neutral",  # first neutralize
            "-conc", str(ION_CONC_M),  # then add 0.15 M
        ], cwd=work, input_str="SOL\n", log_file=log)
        log.write(f"Step 5 (genion 0.15M NaCl): OK\n")

        # 6. Energy minimization
        em_mdp = """; D11.1 em.mdp
integrator      = steep
nsteps          = 5000
emtol           = 1000.0
emstep          = 0.01
cutoff-scheme   = Verlet
nstlist         = 10
coulombtype     = PME
rcoulomb        = 1.0
rvdw            = 1.0
pbc             = xyz
"""
        (work / "em.mdp").write_text(em_mdp)
        _gmx([
            "grompp",
            "-f", str(work / "em.mdp"),
            "-c", str(work / f"{gene}_ionized.gro"),
            "-p", str(work / f"{gene}_topol.top"),
            "-o", str(work / "em.tpr"),
            "-maxwarn", "2",
        ], cwd=work, log_file=log)
        _gmx([
            "mdrun",
            "-v",
            "-deffnm", str(work / "em"),
            "-nt", "1",  # single thread
            "-nb", "cpu",
            "-maxh", "1.0",  # hard 1-hour cap
        ], cwd=work, log_file=log, timeout=3600)
        log.write(f"Step 6 (EM 5000 steps): OK\n")

        # 7. Parse EM results from em.log (GROMACS writes "Steepest Descents converged" line)
        final_energy, fmax = None, None
        em_converged = False
        if (work / "em.log").exists():
            with open(work / "em.log") as f:
                txt = f.read()
            # Look for "Steepest Descents converged to Fmax < ... in N steps" + "Maximum force"
            for line in txt.splitlines():
                if "Steepest Descents converged" in line:
                    em_converged = True
            # Parse Potential Energy and Maximum force (last occurrences)
            import re
            epot_matches = re.findall(r"Potential Energy\s*=\s*(-?\d+\.?\d*(?:[eE][+-]?\d+)?)", txt)
            fmax_matches = re.findall(r"Maximum force\s*=\s*(\d+\.?\d*(?:[eE][+-]?\d+)?)", txt)
            if epot_matches:
                final_energy = float(epot_matches[-1])
            if fmax_matches:
                fmax = float(fmax_matches[-1])

        stats["em_final_energy"] = round(final_energy, 2) if final_energy is not None else None
        stats["em_fmax"] = round(fmax, 2) if fmax is not None else None
        # Trust em.log's "Steepest Descents converged to Fmax < 1000 in N steps" message;
        # fall back to the Fmax threshold check.
        stats["em_converged"] = em_converged or (fmax is not None and fmax < FMAX_TOLERANCE_KJ)
        log.write(f"Step 7 (parse EM): Epot={stats['em_final_energy']} kJ/mol, Fmax={stats['em_fmax']} kJ/mol/nm, converged={stats['em_converged']}\n")

        # 8. Compute system size from gro
        n_atoms = 0
        n_wat = 0
        n_prot = 0
        n_ion = 0
        gro_file = work / f"{gene}_ionized.gro" if (work / f"{gene}_ionized.gro").exists() else work / "em.gro"
        with open(gro_file) as f:
            next(f)  # title
            n_atoms = int(next(f).strip())
        stats["n_atoms"] = n_atoms
        log.write(f"Step 8: total atoms = {n_atoms}\n")

        stats["status"] = "ok"
        stats["wall_time_sec"] = round(time.time() - t0, 1)
        log.write(f"\n=== {gene}: BUILD OK ({stats['wall_time_sec']}s) ===\n")
        return stats
    except Exception as e:
        stats["status"] = "failed"
        stats["error"] = f"{type(e).__name__}: {str(e)[:300]}"
        stats["wall_time_sec"] = round(time.time() - t0, 1)
        log.write(f"\n=== {gene}: BUILD FAILED — {stats['error']} ===\n")
        return stats
    finally:
        log.close()


def main():
    # Test on one system first
    print("=" * 60)
    print("D11.1 worker — GROMACS system build for 27 v10 final proteins")
    print(f"Force field: {FORCE_FIELD} (CHARMM36 not in conda-forge gromacs)")
    print(f"Water: {WATER_MODEL}, Ions: 0.15 M NaCl, EM: 5000 steps steepest descent")
    print("=" * 60)

    # Build all 27 in parallel (4 workers to keep CPU manageable on M4)
    items = list(GENE_MAP.items())
    results = []

    with ProcessPoolExecutor(max_workers=4) as ex:
        futures = {ex.submit(build_system, gene, acc, kind): gene for gene, (acc, kind) in items}
        for fut in as_completed(futures):
            gene = futures[fut]
            try:
                r = fut.result()
            except Exception as e:
                r = {"gene": gene, "status": "exception", "error": str(e)}
            results.append(r)
            flag = "✓" if r.get("status") == "ok" else "✗"
            n = r.get("n_atoms", "?")
            fmax = r.get("em_fmax", "?")
            print(f"  {flag} {gene:14s} atoms={n:>7} Fmax={fmax} {r.get('wall_time_sec', '?')}s")

    # Write summary
    summary = {
        "n_systems_attempted": len(results),
        "n_ok": sum(1 for r in results if r.get("status") == "ok"),
        "n_failed": sum(1 for r in results if r.get("status") != "ok"),
        "force_field": FORCE_FIELD,
        "water_model": WATER_MODEL,
        "ion_conc_M": ION_CONC_M,
        "em_steps": EM_STEPS,
        "results": results,
    }
    out = LOG_DIR / "build_summary.json"
    out.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print("\n" + "=" * 60)
    print(f"Built {summary['n_ok']}/{summary['n_systems_attempted']} systems, {summary['n_failed']} failed")
    print(f"Summary: {out}")
    print("=" * 60)
    return 0 if summary["n_failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
