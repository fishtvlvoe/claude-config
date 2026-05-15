# lessons-web-deploy.md — Web 部署 / CSS / Vercel / Supabase / rsync / Postgres

> 載入時機：碰到 CSS 改動、Vercel env、Supabase migration、rsync 部署、Postgres schema 演進、403/500 debug。
> 核心通則見 `~/.claude/lessons.md`。

| # | 規則 | 觸發情境 |
|---|------|---------|
| L017 | Supabase migration 直接用 CLI + DB URL，不叫用戶貼 SQL | DB migration |
| L022 | Gmail 專案：Vercel + Supabase 已授權，.env 改了就自己去同步，不叫用戶手動改 | 環境變數同步 |
| L024 | Vercel 操作一律用 CLI（vercel env / vercel deploy），不開瀏覽器 | Vercel 操作 |
| L025 | Supabase 操作一律用 CLI（supabase db / supabase secrets），不開瀏覽器 | Supabase 操作 |
| L029 | CSS/HTML 改完 MUST 用 curl/fetch 抓線上頁面驗證，不能只看原始碼就說「修好了」 | CSS 驗收 |
| L030 | 覆蓋按鈕或有漸層的元素，MUST 同時設定 background-color + background-image: none + box-shadow: none，只改 background-color 不夠 | CSS gradient 覆蓋 |
| L033 | CSS 改兩次沒修好 → STOP，curl 抓 theme CSS，列出影響目標元素的所有 rule 再診斷，不要繼續疊 patch | CSS 根因診斷 |
| L038 | rsync 部署後 MUST 執行 `find <plugin_dir> -type d -exec chmod 755 {} \; && find <plugin_dir> -type f -exec chmod 644 {} \;` 修正權限，否則靜態資源（CSS/JS）會回 403 | rsync 部署後 |
| L042 | sshpass + rsync 部署 SOP：(1) `SSHPASS='<pw>' sshpass -e ssh -o StrictHostKeyChecking=no -p <port> user@host` 測連線，(2) rsync 時用 `-e "sshpass -e ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p <port>"`，(3) 部署後 MUST 跑 `find <dir> -type d -exec chmod 755 {} \; && find <dir> -type f -exec chmod 644 {} \;`。常見坑：source 端目錄是 700（macOS 預設），rsync 會原樣帶過去，導致 WordPress/Apache 讀不到檔案回 403。每次 rsync 部署後不管 source 權限長怎樣，都強制重設權限。 | sshpass + rsync 部署 |
| L043 | 用戶貼 DevTools console 的 403/500 錯誤來 debug 前，MUST 先 SSH 去看 server access log（`~/web/<site>/logs/<site>.log`）的時間戳與 HTTP 狀態分布（`awk '{print $9}' \| sort \| uniq -c`），確認錯誤是否是「當下正在發生」還是「DevTools 保留的歷史紀錄」。判斷方式：比對 access log 最後一筆 200/500 的時間 vs 部署完成時間。部署後若 log 全是 200，就叫用戶 Cmd+Shift+R 強制刷新，不要憑 console 舊紀錄動手改代碼。 | Debug 403/500 前必做 |
| L051 | **`vercel env add` 絕對不可用 `echo "value" \| vercel env add X production`** — `echo` 會帶一個 `\n` 進去，Vercel 存成字面值。後果：email env 變成 `fish@aiver.me\n`，toSend 回 4xx → 被 `.catch()` 吞掉。正確：`printf "value" > /tmp/v && vercel env add X production < /tmp/v`。每次加完 MUST `vercel env pull /tmp/.env.prod --environment=production && grep "^X=" /tmp/.env.prod` 驗證值結尾。 | Vercel env add |
| L052 | Postgres `CREATE TABLE IF NOT EXISTS` 不會升級既有表，schema 演進必須用 `ALTER TABLE ... ADD COLUMN IF NOT EXISTS`。同理 CHECK 約束擴展要 `DO $$ ... DROP CONSTRAINT ... ADD CONSTRAINT $$`。Debug 假設前先查 production 真實 schema（`psql ... -c "\d <table>"`），不要憑 migration 檔案推論——CREATE TABLE IF NOT EXISTS 在已存在的表上是 no-op。 | Postgres schema 演進 |
