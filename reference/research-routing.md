# 研究路由詳細規則

> 從 Development/CLAUDE.md 抽出，研究任務觸發時再載入。

## 關鍵字觸發（對話中出現以下詞語）
- 「查一下」、「查查」、「幫我查」
- 「研究」、「研究一下」
- 「搜尋」、「找一下」
- 「比較」、「哪個比較好」、「差異」
- 「最新」、「現在」、「目前」
- 「文件」、「怎麼用」、「API 怎麼」

## 任務類型觸發（任一符合）
- 第三方平台 API 查詢（LINE Pay、綠界、藍新、Stripe、Meta、TapPay...）
- 技術方案比較（A vs B、哪個適合）
- 法規 / 政策查詢（電子發票、個資法、金流規範...）
- 競品 / 市場調查
- 錯誤訊息查詢（搜尋社群解法）
- 套件 / 外掛最新版本或 changelog
- 問題答案可能在過去 1 年內有變動

## Gemini CLI 呼叫方式
`PATH="$HOME/.nvm/versions/node/v22.19.0/bin:/opt/homebrew/bin:$PATH" gemini -p "prompt"`

## 不適合 Gemini 的任務（改用其他模型）
- 寫程式碼、修 bug → Sonnet
- 分析本地 codebase → Kimi
- 規劃 / 架構決策 → Opus（主對話）

## Gemini Batch API（大量批量處理）
觸發條件：任務筆數 > 100 且非即時需求（可等 4-24 小時）
- 比同步 API **便宜 50%**
- 工具：`python tools/gemini-batch/batch_runner.py --input requests.jsonl`
- Dry run 測試：`python tools/gemini-batch/batch_runner.py --dry-run`
- 適用：Migration 批量生成、大量文件分類、批量翻譯

## Gemini CLI 重複執行模式
觸發條件：重複性高、機械性、腳本可循環的工作
- 走免費 dev 配額（Google 帳號登入），0 額外成本
- 呼叫：`gemini -p "..." --yolo`（搭配 shell 腳本循環）
- 適用：Playwright 爬取批跑、重複生成腳本、大量格式轉換
