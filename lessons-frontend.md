# lessons-frontend.md — React / Next.js / iOS / Chrome / Vite

> 載入時機：React hook 開發、Next.js 設定、iOS 手機實機測試、Chrome MCP 操作、Vite dev server 問題。
> 核心通則見 `~/.claude/lessons.md`。

| # | 規則 | 觸發情境 |
|---|------|---------|
| L044 | React hook 回傳物件的 callback（如 `useConversation` 的 `onConnect`、`useWebSocket` 的 `onOpen`）內，**禁止**呼叫 hook 本身回傳的方法（`conversation.sendUserMessage` 等）。閉包抓到初始化未完成的舊值 → 靜默失敗無錯誤。改法：callback 只更新 state，後續動作用 `useEffect` 監聽該 state 觸發。症狀：功能不動、Console 無 error、WebSocket frames 看不到對應 message。 | React hook callback 閉包陷阱 |
| L047 | Next.js 16+ 手機/外部 IP 連本機 dev server 時，CSS/JS 被跨來源保護擋住 → React hydrate 失敗 → skeleton 永遠不消失。修法：在 `next.config.ts` 加 `allowedDevOrigins: ['<LAN IP>']` 再重啟 server。症狀：API 正常、HTML 有回、但畫面卡在 loading。 | Next.js 手機實機測試 |
| L048 | iOS Safari 在 `http://` 環境下：(1) `navigator.share()` 拋 NotAllowedError 靜默失敗；(2) `<a download>` 不觸發「儲存到相簿/檔案」彈窗，改在新分頁開圖。兩個行為都需要 HTTPS 才正常。本機測試看到這些現象不是 bug，部署到 Vercel 後自動修復。 | iOS 手機實機測試 |
| L061 | **Vite/Next.js dev 模式遇到含中文/非 ASCII 字元的專案路徑會卡死**：症狀為 admin SPA 開啟後白畫面、無 console error、`@fs/...路徑` 中的中文字元被 URL-encode 後 fetch 超時。**symlink 救不了** — Node 會 resolve symlink 到真實路徑。真正解法：把整個專案實體搬家到 ASCII 路徑（mv，不是 ln -s）。**通則：任何用 Vite/Next.js/Webpack dev server 的專案，路徑必須全 ASCII**。新顧問案不放 `2-顧問/` 而放 `clients/`。 | 中文路徑 + 前端 dev server |
| L068 | 瀏覽器自動化（claude-in-chrome MCP）一律用 Chrome，不用 Brave。Brave 的 extension 安全策略會擋截圖（Cannot access a chrome-extension:// URL of different extension）。已連線的 Chrome profile 名稱是「老魚」。 | 瀏覽器自動化 |
| L072 | localhost dev server 測試前 MUST 清舊 service worker + caches。具體：(1) DevTools → Application → Service Workers → Unregister；(2) Application → Storage → Clear site data；或 (3) console 跑 `(async()=>{const r=await navigator.serviceWorker.getRegistrations();for(const x of r)await x.unregister();const k=await caches.keys();for(const c of k)await caches.delete(c)})()`。症狀：curl 對但瀏覽器錯 = SW 攔截。每次同個 port 換不同專案的 dev server 都要先清。 | localhost dev 換專案 |
| L073 | Chrome MCP 截圖偶發「Cannot access a chrome-extension:// URL of different extension」錯誤：同一 tab 持續操作後可能觸發；換新分頁（`tabs_create_mcp` + 重新 navigate）通常能繞過。遇到直接換 tab，不要 debug。 | Chrome MCP 截圖卡住 |
