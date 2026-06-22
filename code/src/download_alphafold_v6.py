#!/usr/bin/env python3
"""
D11.1 worker — Download 27 AlphaFold DB v6 PDB structures
Gene list: v10 final 27-gene canonical set (HM-43 + HM-54)
"""
import urllib.request, os, sys, time, json
from pathlib import Path

# v10 final 27 genes → UniProt accession
# Multimer-capable (9): AF2-multimer should be used (but we use v6 monomer as a baseline,
# multimer prediction requires custom AlphaFold-Multimer run, not in DB v6)
# Monomer pLDDT proxy (18): AF v6 monomer
GENE_MAP = {
    # Multimer-capable (9)
    "SLC35G1":     ("Q96EN7", "multimer"),
    "ST6GAL1":     ("P15907", "multimer"),
    "ST3GAL4":     ("Q11206", "multimer"),
    "ST6GALNAC1":  ("Q9NSC7", "multimer"),
    "STAT1":       ("P42224", "multimer"),
    "CD274":       ("Q9NZQ7", "multimer"),
    "CD8A":        ("P01732", "multimer"),
    "CD44":        ("P16070", "multimer"),
    "MUC1":        ("P15941", "multimer"),
    # Monomer pLDDT proxy (18)
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

PDB_DIR = Path("/Users/chen/.mavis/agents/mavis/workspace/genomics_exploration/17_v8_feature_driven/50_paper_v11_D11_MD/D11.1_systems/pdbs")
PDB_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = PDB_DIR.parent / "logs" / "download_log.json"

# AF v6 PDB URL pattern
AF_V6_URL = "https://alphafold.ebi.ac.uk/files/AF-{acc}-F1-model_v6.pdb"


def download_pdb(gene, acc, kind, retries=3):
    url = AF_V6_URL.format(acc=acc)
    out = PDB_DIR / f"{gene}_{acc}.pdb"
    if out.exists() and out.stat().st_size > 1000:
        return {"gene": gene, "acc": acc, "kind": kind, "url": url, "path": str(out), "status": "exists", "size": out.stat().st_size}
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (D11.1 worker)"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
            out.write_bytes(data)
            return {"gene": gene, "acc": acc, "kind": kind, "url": url, "path": str(out), "status": "ok", "size": len(data), "attempts": attempt + 1}
        except Exception as e:
            err = f"{type(e).__name__}: {e}"
            if attempt < retries - 1:
                time.sleep(2 + attempt * 2)
            else:
                return {"gene": gene, "acc": acc, "kind": kind, "url": url, "path": str(out), "status": "failed", "error": err, "attempts": attempt + 1}


def main():
    results = []
    for gene, (acc, kind) in GENE_MAP.items():
        r = download_pdb(gene, acc, kind)
        results.append(r)
        flag = "✓" if r["status"] in ("ok", "exists") else "✗"
        size_kb = r.get("size", 0) // 1024
        print(f"{flag} {gene:14s} {acc} {kind:8s} {size_kb:5d}KB {r.get('error', '')}")
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOG_FILE.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    ok = sum(1 for r in results if r["status"] in ("ok", "exists"))
    fail = sum(1 for r in results if r["status"] == "failed")
    print(f"\n=== Downloaded {ok}/{len(results)} PDB files ({fail} failed) ===")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
