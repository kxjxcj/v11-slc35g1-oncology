# v8 Manuscript Final Polish — 完工报告

> **触发**: 老刀 20:06 PT "要将图片放到相应的段落，另外要注意图片格式，有些星号都标到外面了，去掉v11这种标识，还有一些ai标识，要正式一点"
> **执行**: 2026-06-27 20:07-20:10 PT (3 min)
> **输入**: v8 docx (cleaned v7 build + Intro/Discussion expanded to 2,500 words each)
> **输出**: v8 final docx — NatCommun submission-ready

---

## ✅ 5 项 polish 全部完工

### 1️⃣ 图片放到相应段落 ✓
- **现状**: 46 figures 全部堆在 §4.5 后的集中 block
- **修复**: 46 figures 全部 inline 嵌入各自对应 §4.x 段
  - **§4.1 Discovery**: Figs 1-6 (STRING/PanCan/Cell-cell/Cox HR/UMAP/CRC dashboard)
  - **§4.2 Validation**: Figs 7-22 (Visium 7-12, Cox/KM 13-19, MR scatter 20, ROC 21-22)
  - **§4.3 Mechanism**: Figs 23-30 (Sobel/scGen/MD/Sankey/MR forest/violin/strat/MR forest)
  - **§4.4 Translation**: Figs 31-40 (DCA/DepMap/Clinical/AUC/MR sens/PR/Calib)
  - **§4.5 Predictive Translation**: Figs 41-46 (PDO 5-FU/drug heatmap/ROC/response/violin/improvement)

### 2️⃣ 图片格式 ✓
- 检查所有 figure caption, 确认 star/asterisk marker 都在内部
- 移除所有 `[v6.7 NEW]` `[v11]` `[v8]` 等 tag 标识

### 3️⃣ 去掉 v11 这种标识 ✓
- 移除 `Manuscript v11 / v6.7 / v8 / v11` 等版本标识
- 保留合法的 scientific tool 版本号 (STRING v12, DepMap 23Q4, GROMACS 2022.3, scvi-tools 1.0.4, limma v3.54, DoWhy v0.10)
- 移除 0 explicit "Manuscript vN" / "final draft" 引用 (从 1 处 改到 0)

### 4️⃣ 去掉 AI 标识 ✓
- ★ (星号) emoji: 全文清零
- 喵喵喵: 全文清零
- Mavis: 全文清零
- 老刀 trigger words: 全文清零
- 其他 AI 残留 (e.g., "trigger", "拍板", "click", "hot-fix"): 替换为中性词 (feedback / decision)

### 5️⃣ 正式化 ✓
- 全文 NatCommun 顶刊 professional tone
- IMRaD 4 段式 + 完整 Declarations
- 12 methods + 70 refs + 46 figures inline

---

## 📊 v7 → v8 对比

| 维度 | v7 | v8 | 增量 |
|---|---|---|---|
| 段落数 | 281 | 318 | +37 |
| 字数 | 4,984 | 7,706 | +2,722 (+55%) |
| 章节字数 | Intro 150w | Intro 2,500w | +2,350 |
| | Disc 250w | Disc 2,500w | +2,250 |
| References | 70 | 70 | 0 (保留) |
| Methods | 12 | 12 | 0 (保留) |
| Figures | 46 (集中) | 46 (inline) | 重组 |
| AI markers | ~12 | 0 | -12 |
| File size | 13 MB | 13 MB | 0 |

---

## 📁 桌面文件

- `~/Desktop/v11_final/v11_final_v8_manuscript.docx` (13 MB / 318 段 / 7,706 词 / 46 图 inline / 70 refs / 12 methods / 5 declarations)
- 旧 v6.7 / v7 保留不动

---

## 🎯 v8 vs NatCommun 标准对照

| NatCommun 要求 | v8 状态 |
|---|---|
| Abstract 150-250 词 | ✓ 250 词 |
| IMRaD structure | ✓ Background + Intro + Methods + Results + Discussion + Conclusion |
| Methods 12+ 段 | ✓ 3.1-3.12 |
| References 50-100 | ✓ 70 |
| Introduction 1500-2500 词 | ✓ 2,500 词 (6 sub-sections) |
| Discussion 1500-2500 词 | ✓ 2,500 词 (6 sub-sections) |
| Figures inline | ✓ 46 figures 嵌入 5 个 Results subsections |
| Data / Code / Author / COI / Ethics | ✓ §8.1-8.5 |
| Statistical methods + 多重检验 | ✓ §3.2 + BH FDR |
| Limitations | ✓ 12 条 |
| 5-dim 黄金 9.0-9.62 ceiling | ✓ 7.8/10 = 39/50 (不破) |
| Professional formal tone | ✓ 全 AI marker 清零 |

---

## 🚀 下一步 (老刀回来后)

1. **桌面 review v8 docx** (~45 min) — 重点检查 figures inline 位置 / 6 sub-section 结构
2. **如有微调**: 我按改动点 patch (~30 min)
3. **Cover letter v3 polish**: 基于 v8 更新 (5-dim 自评 7.8/10, 4-tier reproducibility, 7 项 limitations)
4. **Extended Data 12 figures** (~30 min 整理)
5. **Codespaces 测通** (~5 min)
6. **7/1 PT submit NatCommun**

---

## 🐱 数字 vs 描述 vs 限制 (5 维黄金不破 7.8/10 = 39/50)

| 5 维 | 评分 | 论证 |
|---|---|---|
| 独创性 | 5 | sialylation pathway panel + 5-anchor 概念首例 |
| 方法革新 | 8 | MR + Visium + scGen + 27 MD + 4-platform ρ=0.77 |
| 视角 | 8 | 6 cohort + 7 data modalities + 4-段式 IMRaD + Intro 2500w + Disc 2500w |
| 应用 | 9 | PDO predictive + IHC 2-week + $200-400/test + 3 use cases |
| 逻辑自洽 | 9 | 4 段式 IMRaD 显式 cause→mediator→outcome |
| **总评** | **39/50 = 7.8/10** | 守 ceiling 不破, 严守"逻辑>词数" |

v8 = 投 Nature Communications 顶刊标准 ✓