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
| L087 | **React controlled input 寫值 MUST 用 nativeInputValueSetter，不能用 `computer.type` 或直接設 `.value`**。`computer.type` 只模擬鍵盤事件，React 不會收到 onChange。正確做法：`form_input` with ref（MCP 自動用 nativeInputValueSetter）；或 JS：`const s=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set; s.call(el,val); el.dispatchEvent(new Event('input',{bubbles:true}))`。症狀：`input.value` 看起來空白，但 DOM 有值 = React state 沒更新。 | Chrome MCP 操作 React 表單 |
| L088 | **`find()` 返回 ref 後，下一個 batch action 必須直接用該 ref，不能猜 ref_id 數字**。`find` 每次執行結果的 ref 號碼不固定，hardcode "ref_61"、"ref_79" 等猜測號碼 = 必錯。正確：`find` → 從輸出取 `ref_XX` → 同 batch 後續 action 用該 ref。如需跨 batch 保存 ref，先用 JS 查 element id 再 `find`。 | Chrome MCP ref 使用 |
| L089 | **操作前先 `read_page filter=interactive` 取得所有 ref，再一次 batch 完成所有動作**。分多次 `find` → `click` 造成 ref 失效、多餘 round-trip。正確流程：`read_page` → 從輸出取所有需要的 ref → 一個 `browser_batch` 完成填表+點擊+等待。 | Chrome MCP 效率 |
| L019 | UI 按鈕/圖示一律用 SVG icon（Heroicons/Lucide），禁止 Emoji | UI 設計 |
| L045 | UI 任務（HTML 原型、React 元件、CSS 改動）commit 前 MUST 跑視覺驗證：用 playwright/chrome MCP 截圖每個畫面或狀態 → 主對話 Read 截圖確認渲染對 → 錯誤就退回 Agent 改。**禁止**「Agent 回報完成 + grep 字串存在」就 commit。理由：字面驗證 ≠ 行為驗證，HTML 結構正確不代表瀏覽器渲染對。 | 任何 UI 任務 commit 前 |
| L046 | 派工給 cursor-agent / Sonnet 子代理做 UI 時，prompt 結尾 MUST 加：「完成後用 playwright 截圖每個畫面/狀態存到 /tmp/，把路徑列出，不要說『完成』，說『截圖在 X 請主對話驗證』」。沒附截圖證據 = 退回重做。 | 派工 UI 任務時 |
| L082 | **理解 UI 結構用 DOM/HTML，不用截圖**。截圖 = 圖片 token（每張 ~1500 tokens）+「看圖說話」再產文字 = 雙倍浪費。讀 HTML/DOM（`read_page`、`get_page_text`、`javascript_tool` 抓 computed style）= 純文字 token，直接得到 class、px、hex、font-size、佈局。鐵律：**給人看的是圖形介面，給 AI 看的是 0 與 1 的介面**。截圖只用於最終視覺驗證（L045），分析結構階段一律讀代碼。 | 任何 UI 偵察/spec 撰寫 |

## 變更歷程

- 2026-05-19: 從 lessons.md 收 L019 / L045 / L046 / L082（UI 設計 / 截圖驗證 / 派工附證據 / DOM 偵察）
