# lessons.md — 被糾正的規則

> 每次被 Fish 糾正 → 當場更新這裡。
> session 開始時讀這個，避免重複犯同樣的錯。

## 規則速查表

| # | 規則 | 觸發情境 |
|---|------|---------|
| L016 | 說「X 不能用」前必須先 `which X` 確認。已知：copilot/gemini/cursor 都可用 | 工具可用性 |
| L017 | Supabase migration 直接用 CLI + DB URL，不叫用戶貼 SQL | DB migration |
| L018 | 遇阻靜默試 B/C/D，全部失敗才回報，禁止中途打斷用戶 | 工具失敗 |
| L019 | UI 按鈕/圖示一律用 SVG icon（Heroicons/Lucide），禁止 Emoji | UI 設計 |
| L020 | 不確定的事自己查完再說話，禁止叫用戶「試試看」代勞驗證 | Debug |
| L021 | Bug 流程：蒐集線索→列原因→工具逐一排除→確定根因→一次修復→自驗→才告知 | Debug |
| L022 | Gmail 專案：Vercel + Supabase 已授權，.env 改了就自己去同步，不叫用戶手動改 | 環境變數同步 |
| L023 | 任何「需要重複改同一件事」的操作，必須自動化完成，不問用戶 | 自動化原則 |
| L024 | Vercel 操作一律用 CLI（vercel env / vercel deploy），不開瀏覽器 | Vercel 操作 |
| L025 | Supabase 操作一律用 CLI（supabase db / supabase secrets），不開瀏覽器 | Supabase 操作 |
| L026 | Spectra Propose 第 8 步（Inline Self-Review）時檢查 Consistency：每個 design.md 的決策都要在 tasks.md 中被引用，當場修正，不等分析器發現 | Spectra propose 工作流 |
| L027 | Spectra Apply 開始前，必須先做任務分工分析（哪些任務給哪個工具：Copilot/Cursor/Kimi/Codex），給用戶確認後才開始執行。禁止擅自用自己的 token 跑多任務。 | Spectra apply 工作流 |
| L028 | 所有開發任務必須建立 Spectra Change（propose/debug），不允許只存在對話紀錄。執行完才標 [x]，流程：propose→analyze→apply（分配 Agent）→結果回 Sonnet 審核→需 debug 再開新 Change。這是標準 SDD Loop，無例外。 | 工作流程 |
| L029 | CSS/HTML 改完 MUST 用 curl/fetch 抓線上頁面驗證，不能只看原始碼就說「修好了」 | CSS 驗收 |
| L030 | 覆蓋按鈕或有漸層的元素，MUST 同時設定 background-color + background-image: none + box-shadow: none，只改 background-color 不夠 | CSS gradient 覆蓋 |
| L031 | 大檔案（>100 行）用 Grep 定位行號，再用 Read offset/limit 只讀需要的段落，不要整個讀進來 | 讀檔效率 |
| L032 | 自動化腳本失敗後 MUST 先記錄實際狀態（期望找到什麼 vs 實際找到什麼）到 log，才決定是否重試，不得用同樣邏輯盲目 retry | 自動化 debug |
| L033 | CSS 改兩次沒修好 → STOP，curl 抓 theme CSS，列出影響目標元素的所有 rule 再診斷，不要繼續疊 patch | CSS 根因診斷 |
| L034 | 任何擴展點（include/hook/slot）用前 MUST 先查文件確認正確名稱，不猜檔名 | 平台整合 |
| L035 | 建 repo 後第一件事：.gitignore、LICENSE、README；依賴管理檔 MUST 固定版本，不要先寫內容再補基礎設施 | 專案初始化 |
| L036 | 加任何平台設定前先確認目標平台版本和限制（如 GitHub Pages 用 Jekyll 3.10 不是 Jekyll 4），不確定就查官方文件 | 平台版本確認 |

| L038 | rsync 部署後 MUST 執行 `find <plugin_dir> -type d -exec chmod 755 {} \; && find <plugin_dir> -type f -exec chmod 644 {} \;` 修正權限，否則靜態資源（CSS/JS）會回 403 | rsync 部署後 |
| L041 | 禁止叫 Fish 開瀏覽器操作任何事情。瀏覽器操作一律用 agent-browser MCP 或 gh CLI 自己完成。唯一例外：需要 Fish 親自授權的事（貼 API Key、2FA、付費操作、手動 Webhook 授權）。違反 = 白工。 | 任何需要瀏覽器的操作 |
| L042 | sshpass + rsync 部署 SOP：(1) `SSHPASS='<pw>' sshpass -e ssh -o StrictHostKeyChecking=no -p <port> user@host` 測連線，(2) rsync 時用 `-e "sshpass -e ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p <port>"`，(3) 部署後 MUST 跑 `find <dir> -type d -exec chmod 755 {} \; && find <dir> -type f -exec chmod 644 {} \;`。常見坑：source 端目錄是 700（macOS 預設），rsync 會原樣帶過去，導致 WordPress/Apache 讀不到檔案回 403。每次 rsync 部署後不管 source 權限長怎樣，都強制重設權限。 | sshpass + rsync 部署 |
| L043 | 用戶貼 DevTools console 的 403/500 錯誤來 debug 前，MUST 先 SSH 去看 server access log（`~/web/<site>/logs/<site>.log`）的時間戳與 HTTP 狀態分布（`awk '{print $9}' | sort | uniq -c`），確認錯誤是否是「當下正在發生」還是「DevTools 保留的歷史紀錄」。判斷方式：比對 access log 最後一筆 200/500 的時間 vs 部署完成時間。部署後若 log 全是 200，就叫用戶 Cmd+Shift+R 強制刷新，不要憑 console 舊紀錄動手改代碼。 | Debug 403/500 前必做 |

| L037 | 「取消訂單」需求必須先問清楚：是取消整筆訂單（父訂單 status→cancelled）還是取消訂單內的某個商品行（對應子訂單 cancelChildOrder）。兩者完全不同，不可憑字面假設。 | Spectra propose 需求釐清 |
| L039 | 每個階段完成後，MUST 主動告知下一步是什麼、需要用戶做什麼決定，不能做完就停在那裡等問。格式：「下一步是 X，需要你 Y，我的判斷是 Z，你要繼續嗎？」 | 任何任務完成後 |
| L040 | SDD 任務執行中，不需要用戶判斷的步驟（測試通過、build 通過、commit、下一個 Wave）MUST 自動往下走，不等指令。只有以下情況才停下來等用戶：重大架構決策、需要外部資料（客戶提供）、代理全部失敗無法繼續。每個 Wave 完成後主動回報進度摘要（做了什麼、結果如何、下一步是什麼）。 | SDD 執行期間 |
| L044 | React hook 回傳物件的 callback（如 `useConversation` 的 `onConnect`、`useWebSocket` 的 `onOpen`）內，**禁止**呼叫 hook 本身回傳的方法（`conversation.sendUserMessage` 等）。閉包抓到初始化未完成的舊值 → 靜默失敗無錯誤。改法：callback 只更新 state，後續動作用 `useEffect` 監聽該 state 觸發。症狀：功能不動、Console 無 error、WebSocket frames 看不到對應 message。 | React hook callback 閉包陷阱 |
| L045 | UI 任務（HTML 原型、React 元件、CSS 改動）commit 前 MUST 跑視覺驗證：用 playwright/chrome MCP 截圖每個畫面或狀態 → 主對話 Read 截圖確認渲染對 → 錯誤就退回 Agent 改。**禁止**「Agent 回報完成 + grep 字串存在」就 commit。理由：字面驗證 ≠ 行為驗證，HTML 結構正確不代表瀏覽器渲染對（CSS/JS 切換邏輯可能有 bug）。已踩兩次：03-ux-flow.html 的 execution tab 兩次都顯示 onboarding 內容、grep 通過但截圖才發現錯。 | 任何 UI 任務 commit 前 |
| L046 | 派工給 cursor-agent / Sonnet 子代理做 UI 時，prompt 結尾 MUST 加：「完成後用 playwright 截圖每個畫面/狀態存到 /tmp/，把路徑列出，不要說『完成』，說『截圖在 X 請主對話驗證』」。沒附截圖證據 = 退回重做。理由：Agent 回報的「完成」是它的主觀判斷，截圖才是客觀證據。 | 派工 UI 任務時 |
| L047 | Next.js 16+ 手機/外部 IP 連本機 dev server 時，CSS/JS 被跨來源保護擋住 → React hydrate 失敗 → skeleton 永遠不消失。修法：在 `next.config.ts` 加 `allowedDevOrigins: ['<LAN IP>']` 再重啟 server。症狀：API 正常、HTML 有回、但畫面卡在 loading。 | Next.js 手機實機測試 |
| L048 | iOS Safari 在 `http://` 環境下：(1) `navigator.share()` 拋 NotAllowedError 靜默失敗；(2) `<a download>` 不觸發「儲存到相簿/檔案」彈窗，改在新分頁開圖。兩個行為都需要 HTTPS 才正常。本機測試看到這些現象不是 bug，部署到 Vercel 後自動修復。 | iOS 手機實機測試 |
| L049 | 派工給 Copilot CLI（`copilot --yolo`）時，MUST 加 `--add-dir src/` 限制只能動 src 目錄。`--yolo` 模式下 Copilot 有完整寫/刪權限，會動到 openspec/、.claude/、.agent/ 等非代碼目錄，導致 Spectra change 檔案被刪除。已踩坑：form-field-redesign 的 openspec/ 目錄被 Copilot 刪除，需手動從 session 記憶重建。正確呼叫：`copilot --yolo --add-dir src/ --model gpt-5.2 -p @prompt.txt` | Copilot CLI 派工 |
| L050 | **派任何外部代理（Copilot CLI / Sonnet 子代理）前，MUST 跑 `git status` 檢查 untracked 的重要檔案；有則先 `git add openspec/ .claude/ docs/ && git commit -m "wip: pre-dispatch checkpoint"` 才派工**。`--add-dir src/` 只限制「主動編輯」範圍，不限制 bash 指令；Copilot --yolo 會跑 `git restore` / `git clean -fd` 之類「清乾淨工作區」的善意動作，把 untracked 檔案永久刪除（unlink，不丟 trash，git reflog 也救不回）。同時 prompt MUST 用「白名單」而非「禁令清單」：明文「只允許跑 npm test、git status、git diff，禁止任何其他 git 指令（特別是 clean、restore、reset、checkout）」。已踩坑：fix-failing-tests 派工後 4 個 untracked openspec changes 被 git clean -fd 全刪。 | 派工外部代理前 |
| L051 | **`vercel env add` 絕對不可用 `echo "value" \| vercel env add X production`** — `echo` 會帶一個 `\n`（有時是 `\n\n`）進去，Vercel 存成字面值。後果：email env 變成 `fish@aiver.me\n`，toSend 回 4xx → 被 `.catch()` 吞掉 → user 沒收到信、Vercel 沒 alert、只能靠 `vercel env pull` 看 byte 才發現。正確做法：`printf "value" > /tmp/v && vercel env add X production < /tmp/v`（printf 不加換行）。每次加完 MUST `vercel env pull /tmp/.env.prod --environment=production && grep "^X=" /tmp/.env.prod` 驗證值結尾是 `"value"` 不是 `"value\n"`。已踩坑兩次：(1) LINE_LOGIN_CHANNEL_ID 導致 LINE OAuth client_id 帶 `\n` 被 LINE 拒；(2) TOSEND_FROM_EMAIL 導致忘記密碼信永遠寄不出去。 | Vercel env add |
| L052 | **Postgres `CREATE TABLE IF NOT EXISTS` 不會升級既有表**，schema 演進必須用 `ALTER TABLE ... ADD COLUMN IF NOT EXISTS`。同理 CHECK 約束擴展要 `DO $$ ... DROP CONSTRAINT ... ADD CONSTRAINT $$`，不能用 CREATE TABLE 二次定義。**Debug 假設前先查 production 真實 schema**（`psql ... -c "\d <table>"`），不要憑 migration 檔案推論——CREATE TABLE IF NOT EXISTS 在已存在的表上是 no-op，看 migration 以為新欄位生效實際沒有。本 change（fix-processed-emails-schema-drift）原本以為 production 有 schema drift，跑了 migration 才發現是 no-op，真因是 LLM router 而非 schema。 | Postgres schema 演進 |
| L053 | **L050 補強：Copilot CLI `--allow-all-tools` 仍會跑 `git restore` / `git checkout` 來「清不相關修改」**——即使你加了 `--add-dir`，Copilot 看到 `git diff --stat` 出現「跟我這個任務無關的檔案」就會自作主張 restore 它們。已踩坑兩次（form-field-redesign / fix-processed-emails-schema-drift）。**真正的防護**：每個 Wave 結束就 `git add -A && git commit -m "wip: ..."` 把所有改動 commit，**不留 untracked / modified 給下個 Wave**；Copilot prompt 結尾明文「只允許 `git diff --stat` `git diff` `git status`，禁止 `git restore` `git checkout` `git clean` `git reset`」。違反會丟未 commit 的工作，git reflog 救不回。 | Copilot CLI 派工 |
| L054 | **為產品寫行銷文案/影片腳本前，MUST 先讀產品代碼和文件**，搞清楚：(1) 產品到底解決什麼痛點 (2) 目標用戶是誰 (3) 核心功能 (4) 技術棧。禁止憑產品名稱猜測用途。已踩坑：把 BuyGo+1（LINE 社群賣家訂單管理系統）寫成「WooCommerce 結帳頁加購外掛」，痛點、用途、技術棧全猜錯。 | 產品行銷內容製作 |
| L055 | **影片/行銷內容禁止使用 emoji**。Fish 明確要求：內容裡面不能出現任何表情符號。視覺元素用 SVG icon（builtin）或文字描述，不用 emoji char。 | 影片/行銷內容製作 |
| L056 | **用 huashu-design 做簡報前 MUST 先問交付格式**（瀏覽器 / PDF / 可編輯 PPTX）。要可編輯 PPTX → 從第一行 HTML 就按 4 條硬約束寫（960×540pt body、文字包 p/h 標籤、背景在 div 不在文字標籤、用 img 不用 background-image），用多檔架構（每頁獨立 HTML）。已踩坑：先用 deck-stage 單檔 + CSS gradient + display:flex 在 section 上自由寫 → section 的 display:flex 蓋掉 shadow DOM 的 display:none 導致全頁同時顯示 → 且無法導出可編輯 PPTX，全部重做。 | huashu-design 簡報 |
| L057 | **用 huashu-design 的 deck-stage 單檔架構時，section 標籤禁止設 display 屬性**（flex/grid/block 都不行）。排版用的 display 必須放在 section 內部的子 div（如 .cover-inner）上。原因：deck-stage shadow DOM 用 `::slotted(section) { display: none }` 控制顯示/隱藏，外層 CSS 設 display:flex 會覆蓋 shadow DOM 的 display:none，導致所有頁面同時顯示。 | huashu-design deck-stage |
| L058 | **BuyGo+1 部署規則：只推 GitHub，不手動 rsync 到主機**。主機（buygo.instawp.xyz）的角色是「讓 Claude 看代碼和 SSH debug」，不是 deploy 目標。手動 rsync 會：(1) 建備份目錄被 WP 掃成第二個 plugin 列表項導致版本混亂；(2) 排除規則跟 Fish 的正式 build 不同步，可能漏掉某些檔案；(3) Fish 不知道哪個版本是對的。正確流程：commit + push 到 GitHub，Fish 自己決定何時/如何部署。 | BuyGo+1 部署 |
| L059 | **任何 Spectra 工作流（propose / ingest / debug）寫完或更新 artifacts 後，MUST 自動跑 `spectra analyze` 並修復全部四個維度（Coverage/Consistency/Ambiguity/Gaps）到 0 findings 才能進 validate**。所有等級（Critical/Warning/Suggestion）都要修，不分類跳過。Suggestion 的 concrete example 一律補上，不區分「純 UI」或「資料計算」。修完後再跑一次確認 Total: 0 才進 validate → park。**本規則覆蓋 spectra-propose skill 第 9 步**（skill 寫「只修 Critical/Warning、2 次後放棄」— 不適用，以本規則為準）。不限迭代次數，直到 Total: 0。禁止：(1) 任何 finding 殘留就說「完成」；(2) 不跑 analyze 就直接 validate；(3) 自行判斷「這個可以跳過」；(4) 以「skill 指示」為由跳過 Suggestion。適用所有 Spectra change 類型：新功能、bug fix、重構、debug。Fish 不應該需要手動叫跑一致性檢查。 | 任何 Spectra 工作流完成後 |
| L060 | **WordPress 外掛 push 前 MUST bump 版本號**。改三處：(1) 主檔 plugin header `Version: X.Y.Z` (2) `define('..._VERSION', 'X.Y.Z')` (3) `package.json` 的 `version`。版本規則：bug fix = patch（+0.0.1）、新功能 = minor（+0.1.0）、breaking change = major（+1.0.0）。commit message 用 `chore(release): bump version to vX.Y.Z`。適用所有 8-外掛/ 下的 WP 外掛。 | WP 外掛 push 前 |
| L061 | **Vite/Next.js dev 模式遇到含中文/非 ASCII 字元的專案路徑會卡死**：症狀為 admin SPA 開啟後白畫面、`<div id="medusa">` 永遠空、無 console error、`@fs/...路徑` 中的中文字元被 URL-encode（如 `2-顧問` → `2-%E9%A1%A7%E5%95%8F`）後 fetch 該檔超時。**L039 提到的 symlink 救不了** — Node 會 resolve symlink 到真實路徑，Vite 拿到真實路徑後仍輸出含中文的 `@fs` URL。**真正解法：把整個專案實體搬家到 ASCII 路徑**（mv，不是 ln -s）。已踩坑：anismile 顧問案在 `/Users/fishtv/Development/2-顧問/anismile/`，Medusa.js 後台白畫面，搬到 `/Users/fishtv/Development/clients/anismile/` 後立刻正常。**通則：任何用 Vite/Next.js/Webpack dev server 的專案，路徑必須全 ASCII**。新顧問案不放 `2-顧問/` 而放 `clients/`。 | 中文路徑 + 前端 dev server |
| L062 | **Electron + Next.js 在 GitHub Actions CI 用 `npm ci --ignore-scripts` 會殺掉 native 模組編譯**。`--ignore-scripts` 同時擋 puppeteer chromium 下載和 better-sqlite3 prebuild postinstall，導致 build 階段 `Could not locate the bindings file`。**正解**：移除 `--ignore-scripts`，改用環境變數 `PUPPETEER_SKIP_DOWNLOAD=true` + `PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true` 精準擋掉 chromium 下載即可。讓 better-sqlite3 自己跑 prebuild 抓 native binding。已踩坑：three-ai v0.1.1 build 第二次失敗。 | Electron CI install |
| L063 | **`next build` 在 standalone 模式會把部分 npm 套件做成 symlink 放到 `.next/standalone/.next/node_modules/`**（如 pdfjs-dist），electron-builder packaging 階段對 symlink stat 會 ENOENT 失敗。**正解**：next build 之後、electron-builder 之前，跑 `node scripts/materialize-standalone-symlinks.js` 把 symlink 攤平成實體檔案。本專案已有此 script，只是 CI workflow 沒接進去。已踩坑：three-ai v0.1.1 build 第三次失敗。 | Electron + Next.js standalone packaging |
| L064 | **electron-builder Mac 同時 build arm64 + x64 時，artifactName 沒設 `${arch}` → 兩個 dmg 同名 → 後 build 的 x64 覆蓋掉 arm64**。GitHub Releases log 看到 `overwrite published file ... reason=already exists` 就是這個。**正解**：`mac.artifactName: "${name}-${version}-${arch}.${ext}"`。這條對 win 也適用（雖然 Windows runner 通常單 arch）。已踩坑：three-ai v0.1.1 release 表面成功但只有 x64 dmg、arm64 被覆蓋，從 release 看不出來。 | electron-builder 多 arch dmg |
| L065 | **electron-updater 的 `provider: 'generic'` + 自訂 license-server URL 會綁死部署位址**。改 GitHub Releases 後若 updater code 沒同步改成 `provider: 'github'`，舊版客戶會永遠檢查不到新版。**正解**：electron-builder.json 的 publish 跟 electron/updater.ts 的 setFeedURL 必須同時改、同一個 commit 改，避免 release pipeline 改完忘記改 updater。 | electron-updater + publish provider |
| L066 | **Spectra skill 一律用 dash 格式 `spectra-propose`，禁止用 colon 格式 `spectra:propose`**。Skills 列表同時有兩組（dash = 實體 skill 檔案，colon = plugin namespace 自動註冊），colon 版會報 Unknown skill 錯誤。已踩坑兩次，每次浪費一輪 token。 | Spectra skill 呼叫 |
| L067 | **Spectra 工作流開始前 MUST 先檢查 `openspec/config.yaml` 是否有 `context:` + `rules:` 且內容非空**。空模板（只有註解）= 不合格。缺任一 → 先讀專案 CLAUDE.md / package.json / README 取得產品定位和 Tech Stack，rules 段落以 22-AIRE 為範本再依專案特性調整。補齊後才進 Spectra 流程。目的：(1) analyze 四維檢查（Coverage/Consistency/Ambiguity/Gaps）需要 rules 才能精準抓問題 (2) 避免 artifacts 格式不一致事後反覆修正。範本位置：`/Users/fishtv/Development/22-AIRE/openspec/config.yaml`。 | Spectra 工作流前置 |
