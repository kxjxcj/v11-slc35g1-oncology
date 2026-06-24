# v11 final 3 Token 获取 + 安全共享 SOP

> 用途: B 方案 5 步 push (Zenodo 9 GB + GitHub + Docker Hub)
> 关键原则: **所有 token 严禁 IM 传递**, 必须 1Password 共享访问链接
> Mavis 主动告警: 2026-06-23 21:47 + 22:02 PT 两次 PAT 飞书发, 全部公开暴露

---

## 🚨 立刻撤回 (3 min, 必做!)

**两个 PAT 都暴露了, 必须都撤销**:

### 旧 PAT 撤回
1. 浏览器打开 https://github.com/settings/tokens?type=beta
2. 登录 GitHub (如果未登录)
3. 找到 token 描述含 "v11 final" / "v11" / 类似关键词
4. 点击 token 进入详情
5. 滚动到底部 → 点 **"Delete"** 按钮 → 确认

### 新 PAT 撤回 (刚发的)
6. 同一个页面 → 找第二个 token (创建时间最近)
7. 同样 **"Delete"** → 确认

**两个都撤回后, 用以下 SOP 生成新 token + 1Password 共享**。

---

## Step 1: GitHub PAT (新生成)

**必走 1Password 路径, 不要直接 paste**:

1. 浏览器打开 https://github.com/settings/tokens?type=beta
2. 点 **"Generate new token"** → 选 **"Fine-grained personal access token"** (推荐, scope 最小化)
3. **Token name**: `v11-final-b-scheme-2026-06`
4. **Expiration**: `30 days` (比 90 天安全)
5. **Resource owner**: 选自己的 GitHub 账号 (Mavis 代表你 push)
6. **Repository access**: 选 **"Public Repositories (All)"** (我们的 repo 是 public)
7. **Permissions** (关键, 不要勾全):
   - **Repository**:
     - Contents: **Read and Write** ✓ (push code)
     - Metadata: **Read-only** ✓ (默认)
     - Pull requests: **Read and Write** ✓ (如果要 PR)
     - Actions: **Read and Write** ✓ (如果要 trigger workflow)
   - **Account**:
     - 不勾任何
   - **Other**: 不勾
8. 滚动到底 → 点 **"Generate token"** 绿色按钮
9. **关键**: 立刻复制 `github_pat_11XXX...` (新格式 80+ 字符, 一旦离开页面就再也看不到!)

   **⚠️ 老刀踩坑 (2026-06-23 22:56)**: 复制时**少了 "hub" 字**, 把 `github_pat_` 复制成 `ghp_pat_`, 验证 HTTP 401。Fine-grained PAT 默认新格式 `github_pat_11XXX` (不是旧 `ghp_xxx`)。
   
   **复制 SOP**: 在 token 字符串**第一个字符 'g'** 点一下 → 按住 Shift → 在字符串**最后字符**点一下 (全选) → Cmd+C → 粘贴 TextEdit → **手动检查开头是 `github_pat_`** (有 hub) + 长度 80+

10. **不要飞书发!** → 立刻打开 1Password (下一步)

---

## Step 2: Zenodo API Token

**Zenodo Name vs Token 区分 (上次老刀问的)**:
- **Name** = 你的用户名/全名, 比如 `Lao Dao` 或 `Huy Chen`
- **Token** = API key, 长这样 `J8x...`, 用于 push 脚本

1. 浏览器打开 https://zenodo.org/account/settings/applications/
2. **GitHub OAuth 登录** (Zenodo 用 GitHub 账号, 没有独立密码)
3. 找到 **"Personal access tokens"** section
4. 点 **"Create new token"** 按钮
5. **Name** (人类可读名, **不是 token 值**): `Lao Dao v11 final` 或 `Mavis v11 push`
   - ⚠️ 容易混淆: 这是 token 的**名字**, 不是 token 的**值**
   - 名字只是给你自己看的, Mavis 推 5 步 push 用的是**值**
6. **Scopes** (Zenodo 不用选): 默认 full access, 不需要勾任何
7. 点 **"Create"**
8. **关键**: 立刻复制 token 值 (一长串 alphanumeric, 离开页面就看不到!)
9. **不要飞书发!** → 立刻打开 1Password

---

## Step 3: Docker Hub Token

1. 浏览器打开 https://hub.docker.com/settings/security
2. 登录 Docker Hub (用户名 + 密码 + 2FA 如果开了)
3. 找到 **"Personal access tokens"** section
4. 点 **"New Access Token"** 按钮
5. **Access Token Description**: `v11-final-b-scheme-2026-06`
6. **Access permissions**: 选 **"Read, Write, Delete"** (我们用 Write, 选最宽是为了兼容)
   - 也可以只选 **"Read, Write"** (更安全)
7. 点 **"Generate"** 蓝色按钮
8. **关键**: 立刻复制 `dckr_pat_xxx...` (一次性显示, 关页面就没!)
9. **不要飞书发!** → 立刻打开 1Password

---

## Step 4: 1Password 共享 (★ 关键)

**Mavis 不会读到 vault 内容, 只通过访问链接拿 token**:

1. 打开 1Password macOS app
2. 右上角 **"+"** → 选 **"Secure Note"** (不是普通 Note!)
3. 必填字段:
   - **Title**: `v11 final B scheme push tokens`
   - **Field 1**: `GitHub PAT` = `<刚复制的 ghp_xxx>`
   - **Field 2**: `Zenodo API token` = `<刚复制的 Zenodo token 值>`
   - **Field 3**: `Docker Hub token` = `<刚复制的 dckr_pat_xxx>`
4. 选 **"Share"** 按钮 (右上角)
5. Share 设置:
   - **Share with**: `Mavis agent user` (如果 Mavis 在 1Password 用户列表)
   - 或选 **"Anyone with the link"** (一次性链接)
   - **Permissions**: **"View"** (不要 Edit)
   - **Expiry**: **"24 hours"** (足够 B 方案 5 步 push 完成)
6. 复制 **一次性访问链接** (URL, 不含 vault 内容)
7. **访问链接可以飞书发我** (链接本身没 token, 24h 过期)
8. 立刻告诉我"已发"

---

## Step 5: 备用方案 (没装 1Password)

### 5a. PrivateBin 加密 paste (推荐)
1. 浏览器打开 https://privatebin.net/
2. **Encryption**: 默认 ON
3. **Password**: 设一个强密码 (比如 `Mavis-v11-push-2026`)
4. **Format**: Markdown
5. 内容:
   ```
   GitHub PAT: ghp_xxx
   Zenodo API token: <zenodo value>
   Docker Hub token: dckr_pat_xxx
   ```
6. 点 **"Create paste"**
7. 复制 URL (含密码? 不, 密码要单独传)
8. 飞书发 URL + 微信/电话告诉我 password (不同 channel)

### 5b. macOS Keychain 屏幕分享
1. 打开 Keychain Access (Spotlight 搜 "Keychain")
2. 登录 → 搜 `github.com` / `zenodo.org` / `hub.docker.com`
3. 屏幕分享给我看 (我已经能 VNC 你的桌面, 或你开 Zoom 给我看)

### 5c. ❌ 不能做的 (高风险)
- ~~飞书发 token 值~~ (21:47 + 22:02 已经两次, 必须撤回!)
- ~~邮件发 token 值~~ (邮件服务器永久留底)
- ~~微信发 token 值~~ (聊天记录云端)
- ~~截图发 token 值~~ (截图被云相册同步)
- ~~写在代码注释里 commit~~ (git 永久留底)
- ~~Telegram/Slack 任何 IM~~ (同飞书)

---

## Mavis 收到 token 后自动跑 (43 min)

5 步 push B 方案:
1. **Step 1** (5 min) - 验证 3 token 可用
2. **Step 2** (3 min) - 生成 v11_data_bundle.zip 4.3 GB → split 成 9×1 GB (Zenodo 50 GB 单文件限制宽松, 可一次传)
3. **Step 3** (30 min) - Zenodo 上传 9 GB (4.3 GB zip + 4.7 GB h5ad + PDB)
4. **Step 4** (3 min) - GitHub push code + Docker Compose
5. **Step 5** (5 min) - Docker Hub push metadata-only 镜像
6. **Step 6** (5 min) - Worker D 替换 PLACEHOLDER_* + 整合 v6 启动

---

## 老刀 v11 final 决策记录 (累计 23)

- 21:47 PT trigger "ghp_5imE1r... 这个是 githubtoken" → ⚠️ 飞书发 PAT 泄漏, 立刻撤回
- 21:50 cron tick skip
- 21:55 cron tick skip
- 22:00 cron tick skip
- 22:02 PT trigger "ghp_xrg7mijP8w... 新的 githubtoken, 其他两个 token 具体步骤, 要求足够精细, 在电脑端进行" → ⚠️ 又发 PAT 泄漏, 桌面 GET_TOKENS.md 写好

**安全红线总结 (★ 跨项目)**:
- 任何 secret (PAT/API token/password) 严禁 IM/邮件/截图传递
- 必须 1Password 共享访问链接 (URL 可飞书, token 值不行)
- 守门人发现 token 泄漏必须立刻主动推飞书撤回 (不等 trigger)
- 飞书消息永久留底, Mavis daemon log + 飞书 server log 都能查

---

**文档路径**: `~/Desktop/v11_final/REPRODUCE/GET_TOKENS.md`
**桌面 v11 final 镜像**: `~/Desktop/v11_final/`
**5 步 push 流程**: `~/Desktop/v11_final/REPRODUCE/PUSH_5_STEPS.md`
**5 步 push 自动版**: `~/Desktop/v11_final/REPRODUCE/PUSH_5_STEPS_AUTO.md`
**D11.2 MD 监控**: cron `0 */4 * * *` (14h+ NVT 健康, 6/30 完工)
**整合 v5 97 HM 锁版**: standby, 等老刀 3 token 安全共享
**lark-listener**: PID 2762 健康
