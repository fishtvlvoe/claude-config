# lessons.md — 被糾正的規則

> 每次被 Fish 糾正 → 當場更新這裡。
> session 開始時讀這個，避免重複犯同樣的錯。

## 規則速查表

| # | 規則 | 觸發情境 |
|---|------|---------|
| L001 | 遇到 A 不通，先讀 .env 找 B/C 替代，不說「沒辦法」 | 工具/API 不可用 |
| L002 | Phase 完成後直接說結果（通過/失敗/commit hash），不等問 | 任務完成 |
| L003 | 收到任務先問「這在整個計畫的哪裡？」，主動展開全貌 | 新任務開始 |
| L004 | 中文/特殊字元路徑 → 先建 symlink 再跑指令 | macOS 路徑問題 |
| L005 | session 開始先確認全貌（CLAUDE.md/memory/context） | session 啟動 |
| L006 | 功能完成後：單元測試 ✅ + e2e 測試 ✅，分開回報 | 測試驗收 |
| L007 | next_auth schema 欄位是 camelCase，PostgREST 查詢要加雙引號 | Supabase next_auth |
| L008 | 新欄位先用 REST API OpenAPI 確認存在，再寫程式碼 | DB schema 變更 |
| L009 | normalizeHeader 必須做 `replace(/\r\n/g,'\n').replace(/\r/g,'\n')` | XLSX.js 解析 |
| L010 | Gmail API 使用前確認 Google Cloud Console 已啟用 | Gmail API |
| L011 | next-auth middleware 保護路由時 session strategy 必須是 jwt | NextAuth 設定 |
| L012 | 新供應商首次處理前，必須先在 supplier_schemas 建立對應 row | parseExcel |
| L013 | 每個 Phase：討論確認→spec→TDD 紅燈→實作→CR→Coverage，不允許跳過 | Phase 開始 |
| L014 | 每個任務強制三步：討論對齊→寫入記錄→才開始執行 | 任務開始 |
| L015 | 任何任務（含 bug fix）都要走 Copilot 測試→代碼→Kimi CR→回報，唯一例外：1 行 hotfix | 開發流程 |
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
