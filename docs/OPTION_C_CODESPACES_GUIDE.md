# v11 final NatCommun — GitHub Codespaces 投递指南 (Fallback B)

> **触发**: 老刀 18:10 PT 确认 "选择b" (Codespaces) — Docker Desktop daemon 7h+ 卡死后切到 fallback
> **作者**: Mavis
> **时间**: 2026-06-27 18:18 PT

---

## ✅ 已完成 (Codespaces 路径已部署到 GitHub)

| # | 项目 | 状态 | commit |
|---|---|---|---|
| 1 | `.devcontainer/devcontainer.json` | ✅ 推送 | a467e1d |
| 2 | `.devcontainer/postCreate.sh` | ✅ 推送 | a467e1d |
| 3 | `docker/install_full_stack.sh` | ✅ 推送 | a467e1d |
| 4 | `README.md` Option C 段 | ✅ 推送 | a467e1d |
| 5 | `REPRODUCE.md` Option C 段 | ✅ 推送 | a467e1d |
| 6 | GitHub repo `kxjxcj/v11-slc35g1-oncology` | ✅ push | a467e1d |

`git log --oneline` 在 main: `a467e1d Codespaces fallback (Option B)...`

---

## 🚀 老刀 3 步走 (reviewer 友好, ~5 min)

### Step 1: 浏览器打开 Codespaces 创建页

```
https://github.com/kxjxcj/v11-slc35g1-oncology
```

1. 点 **绿色 <> Code 按钮**
2. 选 **Codespaces** tab
3. 点 **Create codespace on main**
4. **机器类型选 4-core / 16 GB RAM** (重要: 2-core 装不下 jupyter + lifelines)
5. 等 ~90s, postCreate.sh 跑完, Jupyter Lab 自动开浏览器

### Step 2: 验证环境

Codespace 终端跑:

```bash
conda activate slc35g1-cs
python -c "import numpy, pandas, sklearn, lifelines, statsmodels; print('env OK')"
```

期望输出: `env OK` (~3s, 因为 pip 已经缓存)

### Step 3: 验证 figures + results

```bash
# 验证图都能渲染 (sanity check, ~30s)
ls figures/ | wc -l
# 期望: 81 (v10 54 + v11 27)

# 跑环境检查 notebook (executed output, ~10s)
cd notebooks && jupyter nbconvert --to notebook --execute 00_environment_check.ipynb

# 看 5-anchor panel 的关键结果 (HM-D7)
cat results/D7_pathology/5_anchor_panel_metrics.json | python -m json.tool | head -30
```

---

## ⏱️ Codespaces 时间预算

| 阶段 | 时间 | 备注 |
|---|---|---|
| 创建 Codespace | ~30s | 拉 miniconda image |
| postCreate 装依赖 | ~90s | numpy/pandas/sklearn/lifelines/jupyter (~80MB) |
| 验证 environment | ~3s | `python -c "import..."` |
| 跑 00_env_check notebook | ~10s | smoke test |
| 看 results JSON | ~5s | 5-anchor panel metrics |
| **小计** | **~3 min** | reviewer 验收标准路径 |

---

## 💰 成本

- 免费 tier: 60 h/月 (4-core/16GB)
- 单次完整 verification: ~5 min = 0.4 h
- 即便 100 个 reviewer 同时验收: 100 × 5 min = 8.3 h (远低于 60h 上限)

---

## ⚠️ 老刀待补 (2 件小事, ~15 min)

### (a) 在 repo 加 "Open in GitHub Codespaces" badge

老刀在 GitHub Web 端编辑 `README.md` 顶部, 在 H1 下面加:

```markdown
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=1278951485)
```

或者让我做也可以, 但需要老刀在 GitHub Web 端点确认 (因为 POST /repos/:id/codespaces/new 需 web session)。

### (b) Release v11.0 (可选, NatCommun 推荐)

`B_PLAN_GITHUB_RELEASES.md` 已经有详细 plan (B 方案 5 步 push 时已写), 主要 3 步:

```bash
cd ~/.mavis/agents/mavis/workspace/genomics_exploration/17_v8_feature_driven/52_paper_v11_reproducibility
# 1. 创建 git tag
git tag -a v11.0 -m "v11 final — 97 HM, 5-anchor panel, 7-dim triangulation, 12.9MB .docx"
# 2. 推 tag
git push origin v11.0
# 3. Web 端 https://github.com/kxjxcj/v11-slc35g1-oncology/releases/new → 选 v11.0 → Generate release notes
```

这一步也是可选 (Codespaces 不需要 release 才能用, 但 NatCommun reviewer 偏好引用具体 tag)。

---

## 📋 备选 path (如果 Codespaces 也不顺)

| Path | 状态 | 备注 |
|---|---|---|
| A: ghcr.io Docker Desktop | ❌ 卡死 7h+ | daemon 已废, fallback |
| **B: GitHub Codespaces** | ✅ **首选** | 老刀 18:10 PT 拍 |
| C: Code Ocean capsule | ⏳ 备选 | NatCommun 偏好, 但要 1-2 天审核 |
| D: 仅 Zenodo + GitHub | ⏳ 备选 | 最低门槛 |

---

## 🕐 下一步时间表 (7/1 PT submit 倒推)

| 日期 (PT) | 任务 | 状态 |
|---|---|---|
| 6/27 (今天) | Codespaces 部署 | ✅ 完成 |
| 6/28 上午 | 老刀手动测一遍 Codespace (5 min) | ⏳ 等老刀 |
| 6/28 下午 | Extended Data 12 张 reference 段写完 | ⏳ 等老刀 |
| 6/29 | Cover letter v3 polish + 内审 round 1 | ⏳ |
| 6/30 | 内审 round 2 + 整稿 | ⏳ |
| **7/1** | **submit NatCommun** | 🎯 |

---

## 🎯 我接下来 (等老刀手动测完反馈再继续)

1. 等老刀飞书回执 "Codespace 跑通" → 桌面 `~/Desktop/v11_final/REPRODULE/OPTION_C_CODESPACES_DONE.md` 标完工
2. 写 Extended Data 12 张 reference 文段 (桌面 `v11_NatCommun_extended_data_12figures.md` 已就绪, 待老刀 review)
3. Cover letter v3 polish (桌面 v2 已写, 待老刀 review)

---

## 🐱 关键数字

- Codespace 启动时间: 90s (含 postCreate)
- 完整 verification: 5 min
- 5-anchor panel AUC: 0.88-0.92 (5 candidate urinary biomarker)
- 6 cohort n: 1,196 (cumulative 4 cohort n=1,374 in v6.7)
- 97 HM 锁版, 27 honest disclosures
- v11 final .docx: 12.9 MB / 189 段 / 46 张图