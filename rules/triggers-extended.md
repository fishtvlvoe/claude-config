<!-- on-demand: 不自動載入，需要時 Read 此檔 -->

# 自動觸發規則（低頻）

## claude-mem 空殼清理
policy: claude-mem 會在子目錄自動建只有 `<claude-mem-context>` 標籤的空殼 CLAUDE.md，無法關閉
trigger: session 開始時如果發現 wp-plugins 子目錄有只含 claude-mem 標籤的 CLAUDE.md（無 gates/rules/policy/trigger）
action: 直接刪除（trash），這些空殼浪費 context 且無實際規則
policy: 每個外掛只保留根目錄一個 CLAUDE.md，子目錄不需要

## 設計洞察捕獲
trigger: 對話中引擎邊界被挑戰 | 新思維模型被實際應用 | 違反直覺但有道理的設計決策
action: 主動問用戶「💡 這個設計洞察值得捕獲嗎？（[一句話描述]）」
action: 用戶說好 → 追加到 Development/1-設計哲學/inbox.md
format: - **日期** | 類型（引擎邊界/新模型應用/違反直覺決策） | 一句話摘要 | 來源
policy: 只在上述三種情境觸發，日常開發不問
policy: 定期用 `/design-philosophy review` 清理 inbox

## ACT 判斷案例（灰色地帶學習）
trigger: 用戶糾正我的做法 | 我做了非顯而易見的判斷（對了或錯了）| 灰色地帶遇到新情境
action: 寫 draft 對比案例 → 問用戶確認 → 存進 judgment-cases.md
action: 同類案例累積 3+ 筆 → 提煉通則 → 穩定後升級到 CLAUDE.md rules
ref: ~/.claude/projects/-Users-fishtv-Development/memory/judgment-cases.md
format: 情境 → 選項A（差）→ 選項B（好）→ 為什麼B好 → 通則

## L1 焦點新鮮度提醒
trigger: session 開始時，讀取 MEMORY.md L0 的「焦點」行，檢查括號內的日期
action: 如果日期距今超過 7 天 → 提醒用戶「L0 焦點已 N 天未更新（{舊焦點}），目前最重要的事是什麼？」
action: 用戶回答後 → 直接更新 MEMORY.md L0 焦點行
policy: 只提醒一次，不重複；若焦點行無日期則跳過

## 交接檔過期提醒
trigger: session 開始時，看到 MEMORY.md L2「交接（活躍）」區有 handoff- 檔案
action: 若同一 handoff 檔案連續 14 天沒有被更新或提及 → 問用戶「handoff-{X} 還有效嗎？可以歸檔了嗎？」
policy: 一次只問一個，不要一次列出所有過期的
policy: 用戶說「歸檔」→ trash 該檔案並從 MEMORY.md 移除；用戶說「還有效」→ 在檔案頭更新日期

## TwinMind 討論記錄
trigger: 用戶說「開啟討論模式」| 「記一下」| 「寫在記憶中」| 「存起來」| 「筆記一下」
action: 將當前討論的關鍵決策、結論、待辦寫成知識卡片 → 存入 TwinMind/vault/Cards/
path: ~/Library/Mobile Documents/iCloud~md~obsidian/Documents/筆記/TwinMind/vault/Cards/
format: frontmatter（title, created, type: card, tags, status） + 結構化內容
policy: 「開啟討論模式」→ 整段討論結束時自動產出一張總結卡片
policy: 「記一下」→ 立即針對當下這段內容產出卡片
policy: 不是每句話都記，只記決策、結論、待辦、重要發現
policy: 檔名格式：{主題}-{YYYY-MM-DD}.md

## 判斷校準（AI Judge）— 低頻高質
optional-trigger: 高風險或出乎意料的方向選擇（選框架、推回指令、預測趨勢）
action: 靜默記錄至 ~/.claude/projects/-Users-fishtv-Development/memory/judgment_log.json
not-triggered: 純事實回答 | 簡單操作 | 日常路由決策 | 用戶明確指定做法的執行
format: 精簡 5 欄：id, date, context, judgment, outcome
