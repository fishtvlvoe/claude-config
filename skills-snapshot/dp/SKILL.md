---
name: design-philosophy
description: "設計哲學核對、思維模型討論、設計洞察捕獲"
disable-model-invocation: true
user-invocable: true
---

# 設計哲學 — Fish 的底層邏輯核對與討論工具

## GATE：強制對焦（不可跳過）

收到任務後，第一步必須：
1. 一句話複述「我理解你要 ___」
2. 判斷模式：
   - **核對**（預設）：拿設計哲學核對當前設計/功能/方向
   - **討論**：用思維模型探討想法、對焦思維
   - **capture**：捕獲這次對話的設計洞察到 inbox
   - **review**：清理 inbox，分類歸位到原始檔案
3. 問「方向對嗎？」→ 用戶說 OK 才往下

---

## 模式 A：核對

### 步驟 1：判斷情境，載入對應模組

| 情境 | 載入 |
|------|------|
| 產品設計 / 功能決策 | engines.md + 對應產品核心 |
| UI/UX 設計 | engines.md（外化元框架、血清素設計相關段落） |
| 新產品 / 新外掛啟動 | engines.md + philosophy.md |
| 大範圍推導 | engines.md + emergence.md |

Read knowledge/engines.md 取得 12 引擎指針，按需 Read 原始檔對應段落。
如為 BuyGo 產品線 → 額外 Read knowledge/buygo-core.md。

### 步驟 2：逐項核對

用 TEMPLATES.md 的「表格 A」格式，逐引擎核對當前設計。

> **強制停止點：核對結果展示給用戶，確認後才結束。**

---

## 模式 B：討論

### 步驟 1：Read knowledge/models/_index.md

從情境標籤匹配當前討論主題，找出相關模型。

### 步驟 2：載入相關模型模組

根據 _index.md 的指針，Read 對應的模型分類檔（如 models/cognition.md）。
分類檔再指向原始檔案的具體段落 → 按需 Read 原始檔。

### 步驟 3：同時載入哲學層

Read knowledge/philosophy.md → 按需 Read 原始檔案對應段落。
確保正向（Why→What→How）和逆向（How→What→Why）推理鏈完整。

### 步驟 4：展開討論

用模型 + 哲學層 + 引擎交叉分析，與用戶深度對話。

> **原則：不給答案，當鏡子。反映盲點，不替用戶下結論。**

---

## 模式 C：capture

### 步驟 1：回顧當前對話

識別：引擎邊界被挑戰、新模型被應用、違反直覺但有道理的設計決策。

### 步驟 2：一句話摘要 + 寫入 inbox

追加到 `Development/1-設計哲學/inbox.md`，格式見 TEMPLATES.md。

---

## 模式 D：review

### 步驟 1：Read `Development/1-設計哲學/inbox.md`

### 步驟 2：逐項分類

| 判斷 | 動作 |
|------|------|
| 強化現有引擎 | 指出該更新哪個引擎的哪個段落 |
| 新的邊界發現 | 指出該補充到哪個引擎的「適用邊界」 |
| 全新洞察 | 暫存，累積 3+ 筆再提煉 |
| 不重要 | 建議刪除，說明理由 |

> **強制停止點：分類結果展示給用戶，確認後才執行寫入。**

---

## 完成條件

- [ ] GATE 已通過（模式已確認）
- [ ] 對應模組已載入（不多載、不少載）
- [ ] 核對/討論/捕獲/整理已完成
- [ ] 用戶已確認結果
