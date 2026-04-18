# 三道 Gate — Constitution Check

計畫（Plan）必須通過以下三道 Gate，任一失敗需修正後重新檢查。

## Gate 1: Simplicity Gate

**問題：** 這個計畫是不是最簡單的可行方案？

檢查項：
- [ ] 沒有「以防萬一」的功能（YAGNI）
- [ ] 沒有過度設計的架構（如：單一功能卻用微服務）
- [ ] 依賴數量是否最少化
- [ ] 能用現有工具/函式庫的，沒有重造輪子
- [ ] 每個元件都有明確的存在理由

**失敗信號：** 「未來可能需要」、「為了彈性」、「預留擴展」

## Gate 2: Anti-Abstraction Gate

**問題：** 有沒有不必要的抽象層？

檢查項：
- [ ] 沒有只被一處使用的介面/抽象類
- [ ] 沒有「策略模式」只有一個策略
- [ ] 沒有 wrapper 只是轉發呼叫
- [ ] 資料夾層級 ≤ 3 層（除非有明確理由）
- [ ] 三行重複程式碼優於一個過早抽象

**失敗信號：** `AbstractFactory`、`BaseManager`、`IService` 只有一個實作

## Gate 3: Integration-First Gate

**問題：** 是不是從整合點開始設計？

檢查項：
- [ ] 先定義外部介面（API contract / CLI schema / UI wireframe）
- [ ] 資料流從使用者操作到儲存都有描述
- [ ] 第三方整合的 happy path + error path 都考慮了
- [ ] 先有 end-to-end 骨架，再填充內部邏輯
- [ ] 測試策略從整合測試開始，不是從單元測試開始

**失敗信號：** 先寫內部 utility，最後才想怎麼串起來

---

## 評估格式

```markdown
### Constitution Check

| Gate | 結果 | 說明 |
|------|------|------|
| Simplicity | PASS/FAIL | [具體說明] |
| Anti-Abstraction | PASS/FAIL | [具體說明] |
| Integration-First | PASS/FAIL | [具體說明] |

**整體判定：** PASS / 需修正（列出具體修改項）
```

## 違規追蹤（僅在 Gate 有正當違規時填寫）

| 違規項 | 為什麼需要 | 更簡單的替代方案為什麼不行 |
|--------|-----------|------------------------|
| [具體違規] | [當前需求] | [為什麼簡單方案不夠] |
