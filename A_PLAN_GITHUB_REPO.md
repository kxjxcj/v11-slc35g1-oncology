# A 方案: 老刀 GitHub 创建空 repo 详细步骤

> **老刀 01:30 PT trigger**: A 方案需要我做的具体流程
> **老刀时间**: ~1 min 创建空 repo
> **我时间**: ~8 min 自动重跑 Step 3-6
> **总墙时**: 老刀 1 min + 我 8 min = 9 min 完工

---

## 为什么需要老刀创建空 repo

**问题**: 5 步 push PID 25947 Step 4 失败, 因为 Fine-grained PAT `github_pat_11XXX` 缺 **Administration: Write** scope, 无法 `POST /user/repos` 创建新 repo (HTTP 403)。

**解决**: 老刀用 GitHub Web UI 手动创建空 repo (Web UI 不需 PAT scope), 我直接 `git push` 推 (PAT 有 Contents: Read and Write, 够 push 现有 repo)。

---

## 🚨 老刀必做: 1 步 (1 min)

### Step 1: GitHub Web UI 创建空 repo

1. **浏览器打开**: https://github.com/new
2. **登录**: 确认登录到 `kxjxcj` 账号 (右上角头像显示 kxjxcj)
3. **Owner**: 自动选 `kxjxcj` (如果登录正确)
4. **Repository name**: 输入 **`v11-slc35g1-oncology`** (注意 4 个单词用 3 个 `-` 连接)
   - ⚠️ 必须完全一致, 不然我 git push 会失败
   - ⚠️ 不要加后缀如 `-v1` `-data` `-paper`
5. **Description (可选)**: `SLC35G1-stratified sialylation precision oncology v11 final reproducibility (97 HM, 5-anchor panel, 7-dim triangulation)`
6. **Public** ✓ (必须 public, 不要选 Private)
7. ⚠️ **不要勾** "Add a README file" (我们自己有 README.md)
8. ⚠️ **不要勾** "Add .gitignore" (我们自己有 .gitignore)
9. ⚠️ **不要勾** "Choose a license" (我们后面加 MIT LICENSE)
10. 点 **绿色 "Create repository" 按钮** (页面底部)

### 验证创建成功

跳转到 https://github.com/kxjxcj/v11-slc35g1-oncology 页面:
- **应该看到**: "Quick setup — if you've done this kind of thing before" + 空 repo 提示
- **不应该看到**: 任何文件 (README, .gitignore, LICENSE 都不应该有)

### 飞书回执 (老刀发)

```
已创建: https://github.com/kxjxcj/v11-slc35g1-oncology
```

---

## 🚀 我自动重跑 (8 min, 老刀 0 操作)

收到老刀飞书回 "已创建" 后, 我立刻:

### Step 3 (重跑): Zenodo 拆 4.2 GB zip + 分批上传

```bash
cd /Users/chen/.mavis/agents/mavis/workspace/genomics_exploration/17_v8_feature_driven/52_paper_v11_reproducibility/

# 拆 4.2 GB 成 9 个 ~500 MB 块
mkdir -p /tmp/zen_split
split -b 500m v11_data_bundle.zip /tmp/zen_split/zen_chunk_

# 创建 Zenodo deposition (复用之前的 ID 20825905, 或新建)
ZENODO_DEPOSITION=$(curl -s -X POST \
    -H "Authorization: Bearer $ZEN_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"metadata": {...}}' \
    https://zenodo.org/api/deposit/depositions | jq -r '.id')

# 分批上传 (9 chunks × ~3 min @ 5 MB/s)
for chunk in /tmp/zen_split/zen_chunk_*; do
    curl -H "Authorization: Bearer $ZEN_TOKEN" \
         --upload-file "$chunk" \
         "https://zenodo.org/api/deposit/depositions/$ZENODO_DEPOSITION/files"
done

# Publish + 拿 DOI
curl -X POST -H "Authorization: Bearer $ZEN_TOKEN" \
     "https://zenodo.org/api/deposit/depositions/$ZENODO_DEPOSITION/actions/publish"
```

### Step 4 (重跑): GitHub push

```bash
cd /Users/chen/.mavis/agents/mavis/workspace/genomics_exploration/17_v8_feature_driven/52_paper_v11_reproducibility/

# git remote 已加 (从之前失败尝试保留)
git push -u origin main --force
```

### Step 5 (重跑): Docker Hub metadata-only

```bash
# 创建 minimal Alpine image (metadata only, ~5 MB)
# 跳过 build 大镜像 (B 方案 metadata-only)
mkdir -p /tmp/docker_meta
cat > /tmp/docker_meta/Dockerfile <<EOF
FROM alpine:3.19
LABEL org.opencontainers.image.title="v11-slc35g1-oncology"
LABEL org.opencontainers.image.description="SLC35G1-stratified sialylation precision oncology v11 final reproducibility (97 HM)"
LABEL org.opencontainers.image.source="https://github.com/kxjxcj/v11-slc35g1-oncology"
COPY README.md /README.md
EOF

docker build -t iuadbciacn/v11-slc35g1-oncology:v1.0 /tmp/docker_meta/
echo "$DH_TOKEN" | docker login -u iuadbciacn --password-stdin
docker push iuadbciacn/v11-slc35g1-oncology:v1.0
```

### Step 6 (重跑): Worker D 替换 + 整合 v6

```bash
bash /Users/chen/Desktop/v11_final/REPRODUCE/do_post_push_replace.sh \
    https://github.com/kxjxcj/v11-slc35g1-oncology \
    $ZENODO_DOI \
    https://hub.docker.com/r/iuadbciacn/v11-slc35g1-oncology
```

---

## 🎯 完工时间表

| 时间 | 步骤 | 老刀操作 | 我操作 |
|------|------|---------|--------|
| 01:30 | 老刀拍 A | "A 方案" | 写流程文档 |
| 01:31 | 老刀创建 GitHub repo | 1 min | 等 |
| 01:32 | 老刀飞书回 "已创建" | 1 min | 准备 |
| 01:33 | Step 3 Zenodo 拆 9 块 + 分批上传 | 0 | 6 min |
| 01:39 | Step 4 GitHub push | 0 | 1 min |
| 01:40 | Step 5 Docker Hub metadata-only | 0 | 1 min |
| 01:41 | Step 6 Worker D 替换 + 整合 v6 | 0 | 1 min |
| 01:42 | 5 步 push 全部完工 | 0 | 推老刀汇总 |

**总墙时**: 老刀 2 min + 我 9 min = 11 min

---

## 🛑 可能踩的坑

### GitHub repo 名打错
- 必须完全 `v11-slc35g1-oncology` (4 单词 3 短横线)
- 错一个字符我 git push 失败
- 老刀截图或 copy URL 给我确认

### 创建时勾了 README/.gitignore/LICENSE
- 我 git push 会 conflict (本地 README + 远端 README)
- 老刀删远端 README/.gitignore/LICENSE, 或我 --force push (会覆盖)

### repo 创建后立刻 git push
- 我 git remote 已 add (从失败尝试保留)
- 第一次 push 是 git push -u origin main --force (覆盖)

### Zenodo 拆 zip 慢
- 4.2 GB split ~3 min
- 9 chunks 上传 ~6 min @ 5 MB/s
- 总 9 min (vs 之前 4.2 GB 单文件 413 失败)

---

## 📞 飞书回执格式 (老刀发)

```
已创建: https://github.com/kxjxcj/v11-slc35g1-oncology
```

或者包含更多上下文:
```
GitHub repo 已创建 (空, public, 没 README/.gitignore/LICENSE)
URL: https://github.com/kxjxcj/v11-slc35g1-oncology
开始重跑 5 步 push
```

---

## 🎬 完工后

老刀收到我汇总飞书后:
1. Review 3 URL + DOI (GitHub + Zenodo + Docker Hub)
2. 桌面 ~/Desktop/key 文件我自动 mavis-trash 移到回收站
3. 24h 内 review v11 final 100 HM 锁版 (97 + 3 D11.2 推 HM)
4. 投 1 区 (Gut / Nat Commun / Cancer Cell)
5. 8/1 deadline 必达 🎯

---

## 🔒 安全提醒

桌面 ~/Desktop/key 文件包含 3 token plaintext, 5 步 push 完工后我自动:
```bash
mavis-trash ~/Desktop/key  # 移到回收站, 可恢复
```

Token 本身保留在 /tmp/gh_token.txt + /tmp/zenodo_token.txt + /tmp/dh_token.txt (600 权限), 5 步 push 完后我清掉 /tmp token 文件。