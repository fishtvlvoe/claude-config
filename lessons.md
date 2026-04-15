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
