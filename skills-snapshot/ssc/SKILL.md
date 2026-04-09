---
name: ssc
description: "建立或升級 Skill / Agent / Hook 時使用。走世代 3 完整流程：GATE 確認方向 → 分類 → 訪談 → 產出結構 → 品質檢查。用戶說「建 Skill」、「做 Agent」、「加 Hook」、「升級這個 Skill」等都應觸發。"
user-invocable: true
---

# SSC — Super Skills Creator

## GATE：強制對焦（不可跳過）

收到任務後，第一步必須：
1. 一句話複述「我理解你要 ___」
2. 判斷模式：
   - **新建**：從零打造
   - **轉換**：把別人的 Skill 改造成我們的結構
   - **升級**：把現有世代 1/2 升級到世代 3
3. 問「方向對嗎？」→ 用戶說 OK 才往下

> **強制委派規則（不可跳過）：**
> - 需要讀取參考檔、現有 Skill、範本 → 用 `cursor-agent -f --print` 收集，主對話只看摘要
> - 需要讀取 3+ 個檔案 → 用 Kimi 或 Haiku 子代理，禁止主對話逐檔 Read
> - 建立/寫入檔案 → Haiku 子代理執行，主對話確認結構後下指令
> - 主對話只做：確認方向、決定結構、核查輸出

---

## 步驟 1：分類（Skill / Agent / Hook）

Read knowledge/classification.md 依決策樹判斷類型。

判斷完成後，向用戶報告：
- 「這個適合做 **[Skill / Agent / Hook]**，因為 ___」
- 如果是灰色地帶（混合型），說明拆法

> **強制停止點：用戶確認分類結果才往下。**

---

## 步驟 2：訪談收集資訊

依分類類型，問不同的問題：

**Skill（互動式工作流）：**
1. 這個 Skill 要完成什麼任務？
2. 需要用戶確認哪些關鍵決策？（→ 停止點）
3. 品質怎麼判斷？（→ 品質檢查類型）
4. 有沒有固定的輸出格式？（→ TEMPLATES.md）
5. 有哪些參考資料需要按需載入？（→ knowledge/）

**Agent（獨立執行）：**
1. 這個 Agent 的專業領域是什麼？
2. 輸入什麼、輸出什麼？
3. 有沒有 Checklist 需要逐項檢查？
4. 嚴重程度怎麼分級？

**Hook（事件觸發）：**
1. 什麼事件觸發？（SessionStart / Stop / PreToolUse 等）
2. 要執行什麼 Shell 指令？
3. timeout 多少？

---

## 步驟 3：產出結構

Read knowledge/templates.md 取得對應模板，生成完整檔案。

**Skill → 世代 3 結構：**
- 建立 `~/.claude/skills/<name>/SKILL.md`（含 GATE + 流程 + 品質檢查 + 完成條件）
- 建立 `knowledge/` 資料夾（如有參考資料）
- 建立 `TEMPLATES.md`（如有固定輸出格式）

**Agent → agents/*.md：**
- 建立 `~/.claude/agents/<name>.md`

**Hook → settings.json：**
- 輸出 hook 設定片段，由用戶確認後寫入

> **強制停止點：產出後展示給用戶，確認才寫入檔案。**

---

## 步驟 4：品質檢查

Read knowledge/quality-check.md 執行品質驗證。

驗證項目依類型不同：
- Skill → 世代 3 完整性檢查（5 項必備元件）
- Agent → 結構完整性 + 職責單一性
- Hook → 指令可執行性 + 事件正確性

---

## 完成條件（全部達到才算完成）

- [ ] GATE 已通過
- [ ] 分類已確認（Skill / Agent / Hook）
- [ ] 結構已產出且用戶已確認
- [ ] 品質檢查全部通過
- [ ] 檔案已寫入正確位置
