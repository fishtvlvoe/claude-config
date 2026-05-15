# lessons-products.md — 產品專屬踩坑

> 載入時機：碰到對應產品（BuyGo+1、huashu-design、three-ai、Electron 桌面 App）時讀取。
> 核心通則見 `~/.claude/lessons.md`。

## BuyGo+1 / WP 外掛系列

| # | 規則 | 觸發情境 |
|---|------|---------|
| L054 | 為產品寫行銷文案/影片腳本前，MUST 先讀產品代碼和文件，搞清楚：(1) 產品到底解決什麼痛點 (2) 目標用戶是誰 (3) 核心功能 (4) 技術棧。禁止憑產品名稱猜測用途。已踩坑：把 BuyGo+1（LINE 社群賣家訂單管理系統）寫成「WooCommerce 結帳頁加購外掛」。 | 產品行銷內容製作 |
| L055 | 影片/行銷內容禁止使用 emoji。視覺元素用 SVG icon 或文字描述。 | 影片/行銷內容製作 |
| L058 | BuyGo+1 部署規則：只推 GitHub，不手動 rsync 到主機。主機（buygo.instawp.xyz）的角色是「讓 Claude 看代碼和 SSH debug」，不是 deploy 目標。手動 rsync 會：(1) 建備份目錄被 WP 掃成第二個 plugin 列表項導致版本混亂；(2) 排除規則跟正式 build 不同步；(3) Fish 不知道哪個版本是對的。 | BuyGo+1 部署 |
| L060 | WordPress 外掛 push 前 MUST bump 版本號。改三處：(1) 主檔 plugin header `Version: X.Y.Z` (2) `define('..._VERSION', 'X.Y.Z')` (3) `package.json` 的 `version`。bug fix = patch（+0.0.1）、新功能 = minor（+0.1.0）、breaking change = major（+1.0.0）。commit message 用 `chore(release): bump version to vX.Y.Z`。適用所有 8-外掛/ 下的 WP 外掛。 | WP 外掛 push 前 |

## huashu-design Skill

| # | 規則 | 觸發情境 |
|---|------|---------|
| L056 | 用 huashu-design 做簡報前 MUST 先問交付格式（瀏覽器 / PDF / 可編輯 PPTX）。要可編輯 PPTX → 從第一行 HTML 就按 4 條硬約束寫（960×540pt body、文字包 p/h 標籤、背景在 div 不在文字標籤、用 img 不用 background-image），用多檔架構（每頁獨立 HTML）。 | huashu-design 簡報 |
| L057 | 用 huashu-design 的 deck-stage 單檔架構時，section 標籤禁止設 display 屬性（flex/grid/block 都不行）。排版用的 display 必須放在 section 內部的子 div（如 .cover-inner）上。原因：deck-stage shadow DOM 用 `::slotted(section) { display: none }` 控制顯示，外層 CSS 設 display:flex 會覆蓋 shadow DOM 的 display:none，導致所有頁面同時顯示。 | huashu-design deck-stage |

## three-ai / Electron + Next.js 桌面 App

| # | 規則 | 觸發情境 |
|---|------|---------|
| L062 | Electron + Next.js 在 GitHub Actions CI 用 `npm ci --ignore-scripts` 會殺掉 native 模組編譯。`--ignore-scripts` 同時擋 puppeteer chromium 下載和 better-sqlite3 prebuild postinstall，導致 build 階段 `Could not locate the bindings file`。正解：移除 `--ignore-scripts`，改用環境變數 `PUPPETEER_SKIP_DOWNLOAD=true` + `PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true` 精準擋掉 chromium 下載即可。讓 better-sqlite3 自己跑 prebuild。 | Electron CI install |
| L063 | `next build` 在 standalone 模式會把部分 npm 套件做成 symlink 放到 `.next/standalone/.next/node_modules/`（如 pdfjs-dist），electron-builder packaging 階段對 symlink stat 會 ENOENT 失敗。正解：next build 之後、electron-builder 之前，跑 `node scripts/materialize-standalone-symlinks.js` 把 symlink 攤平成實體檔案。 | Electron + Next.js standalone packaging |
| L064 | electron-builder Mac 同時 build arm64 + x64 時，artifactName 沒設 `${arch}` → 兩個 dmg 同名 → 後 build 的 x64 覆蓋掉 arm64。GitHub Releases log 看到 `overwrite published file ... reason=already exists` 就是這個。正解：`mac.artifactName: "${name}-${version}-${arch}.${ext}"`。 | electron-builder 多 arch dmg |
| L065 | electron-updater 的 `provider: 'generic'` + 自訂 license-server URL 會綁死部署位址。改 GitHub Releases 後若 updater code 沒同步改成 `provider: 'github'`，舊版客戶會永遠檢查不到新版。正解：electron-builder.json 的 publish 跟 electron/updater.ts 的 setFeedURL 必須同時改、同一個 commit。 | electron-updater + publish provider |
