---
name: debug-buygo
description: "BuyGo 五階段自動化 debug"
disable-model-invocation: true
---

# BuyGo+1 Debug 閉環流程

五階段自動化 debug，全程只在兩個點暫停等用戶確認。

## GATE — 開始前對焦

複述理解：「你遇到了 _[bug 描述]_，表現是 _[什麼現象]_，對嗎？」

確認：
- Bug 描述（症狀）
- 有沒有截圖或錯誤訊息

> **等用戶確認後才開始分析，不要猜測。**

---

## 環境（不問用戶，直接用）

| 環境 | 網址 |
|------|------|
| 本機 | https://test.buygo.me |
| 雲端 | https://buygo.me |
| 備用 | https://one.buygo.me |

- 開發目錄：`/Users/fishtv/Development/wp-plugins/buygo-plus-one/`
- 測試指令：`composer test`（在 buygo-plus-one 目錄執行）

---

## 執行流程

**Phase 1：分析**（Kimi 分析相關代碼 → 確認根因 + 受影響檔案）

**Phase 2：TDD 修復**（寫測試紅燈 → 寫修復代碼 → 測試綠燈 → 瀏覽器自動驗證截圖）

**Phase 3：閉環**（Code Review via Kimi → Commit + Push + PR → 版本號遞增 → Release）

---

## Phase 1：分析

### 模型路由
- **主分析**：用 Kimi MCP（`kimi_analyze`）掃描相關檔案，確認根因與受影響範圍
- **交叉檢查**：用 Agent model="haiku" 快速確認 Kimi 結果有沒有遺漏的相關檔案（搜尋同模組、同功能的其他檔案）
- **讀取個別檔案**：直接 Bash `cat`（零 token）或 Read 工具

### 熵減審核
- [ ] **完整性**：Kimi 分析結果涵蓋所有相關檔案？Haiku 交叉檢查無遺漏？
- [ ] **根因確認**：找到的是根因（Why），不只是現象（What）？
- [ ] **熵減**：根因理解夠深，能讓修復方向最小化改動範圍？
- [ ] **有主見**：根因已確認，不是「可能是 A 或 B 或 C」的猜測清單

---

## Phase 2：TDD 修復

### 模型路由
- **寫紅燈測試**：用 Agent model="sonnet"（寫碼主力）
- **跑測試**（`composer test`）：直接 Bash（零 token）
- **修復代碼讓測試通過**：用 Agent model="sonnet"
- **跑瀏覽器驗證**：直接 Bash（零 token）

### 熵減審核
- [ ] **熵減**：修復有沒有讓代碼變得更簡單？還是只是打補丁？
- [ ] **三問**：修完之後，下次遇到類似 bug 會更容易找嗎？
- [ ] **量化**：修改的行數 ≤ 原始問題範圍？沒有擴散到不相關的檔案？
- [ ] **有主見**：只改該改的，不順手重構周邊代碼

---

## Phase 3：閉環

### 模型路由
- **Code Review**：用 Bash 呼叫 `kimi --yolo --print "review 以下 diff：$(git diff HEAD~1)"` （免費）
- **Commit message 撰寫**：用 Agent model="haiku"（瑣事）
- **PR 建立**：直接 Bash `gh pr create`（零 token）
- **版本號遞增**：直接 Bash（zero token）
- **Release 建立**：直接 Bash `gh release create`（零 token）

### 熵減審核
- [ ] **熵減**：PR 描述是否說明「為什麼這樣修」，不只是「改了什麼」？
- [ ] **三問**：Release notes 能讓下一個接手的人秒懂問題脈絡？
- [ ] **量化**：Commit 範圍精準，無多餘的格式調整或無關改動混入？
- [ ] **有主見**：Review 發現問題就修，不「留到下次」

---

## Phase 4：截圖確認 ← 第一個暫停點

呈現給用戶：修了什麼、測試結果、版本號、PR 連結、Release 連結。

> **等用戶確認 OK 才繼續。**

---

## Phase 5：部署雲端 ← 第二個暫停點

> **等用戶明確說「OK 推雲端」「部署」「上線」才執行 `/deploy`。**

部署後：瀏覽器自動驗證截圖 → 回報狀態。

---

## 品質檢查（開發類 — 測試驅動）

Phase 2 完成後逐項確認：

| 檢查項 | 標準 | 狀態 |
|--------|------|------|
| 測試從紅燈開始 | 修復前測試必須 FAIL，確認測試有效性 | ✅/❌ |
| 測試綠燈 | 修復後全部測試通過，含 regression | ✅/❌ |
| Code Review 通過 | Kimi 掃描無 CRITICAL（SQL Injection / XSS / Nonce / 權限） | ✅/❌ |
| PR 結構完整 | PR 含：bug 描述、根因、修復方式、測試截圖 | ✅/❌ |
| 版本號正確 | semver 規則：fix=patch / feat=minor / breaking=major | ✅/❌ |

## 品質驗證（Phase 3 必做）

- [ ] Code Review：無 CRITICAL 問題（SQL Injection / XSS / 硬編碼 key / Nonce / 權限）
- [ ] PR 已建立（含描述、測試結果、Review 摘要）
- [ ] 版本號已遞增（semver：fix=patch, feat=minor, breaking=major）
- [ ] Release 已建立（繁體中文 release notes）

---

## 完成條件

- [ ] GATE 已確認 bug 描述
- [ ] 根因已確認（不是猜測）
- [ ] 測試通過（綠燈）
- [ ] 閉環完成（Review + PR + Release）
- [ ] 用戶已確認截圖（Phase 4）
- [ ] 雲端部署（如需，Phase 5）
