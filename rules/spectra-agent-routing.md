# Spectra Apply SDD 專用規則

> 代理速查表、禁用清單、分類規則 → `~/.claude/rules/routing.md`（SSOT）
> 詳細案例、SOP → `~/.claude/reference/spectra-agent-routing-full.md`

## SDD 模型選擇（成本優化，2026-05-19）

**原則**：Phase 分層模型 —— Opus 做決策層，Sonnet/CLI 做執行層

| Phase | 用途 | 模型 | 成本 | 
|-------|------|------|------|
| 1（規劃） | Discuss / Propose | **Opus** | $60-80 |
| 2（TDD） | 紅燈測試 | Sonnet 子代理 | $15-20 |
| 3（實作） | 代碼撰寫 | Copilot/Kimi CLI | $10-20 |
| 4（Review） | CR 驗證 | Kimi CLI | $5-10 |
| 5（驗收） | E2E 測試 + 部署 | Sonnet 子代理 | $10-15 |
| **合計** | **整個 phase** | **混合** | **$150-200**（vs. 全 Opus $400+） |

**SDD Apply 預設**：用 **Sonnet 子代理**（複雜度足，成本 1/4）

**升 Opus 的條件**（任一符合）：
- 架構決策題（上 /spectra-discuss → Opus）
- 跨棧重構（3+ 層改動）
- 文件變更 > 10 個
- 模型主觀判斷：「這很複雜，需要深思」

## 工作包合併原則

**不要拆太碎**（例如「修 API / 寫測試 / 再修 API」分三份）
**應該合併**（例如「TDD：寫測試 → 修 API → 跑驗證」給 Sonnet 子代理一包，或拆「Copilot 寫 API + Sonnet 寫測試」兩包並行）

## Wave SOP（強制）

### Wave 前
1. 前一 Wave 所有任務 `[x]`
2. `git status` 乾淨
3. `npm run build` 通過

### Wave 執行
```
同 Wave 任務 → 同一訊息多 tool call 並行派出
→ 等回傳
→ Kimi MCP CR（diff > 10 行）
→ build + test
→ git add + commit（conventional）
→ 下一 Wave
```

## 用量不足自動切換（不等 Fish 確認）

| 主力 | 備用 1 | 備用 2 | 備用 3 |
|------|-------|-------|-------|
| Copilot CLI | Kimi CLI | Sonnet 子代理 | — |
| Kimi CLI | Copilot CLI | Sonnet 子代理 | — |
| Sonnet 子代理 | Copilot CLI | Kimi CLI | 主對話直接做 |

切換時主動告知 Fish：「⚠️ [Agent X] 用量不足，切換至 [Y] 繼續」

## Wave 完成驗收（缺一不過）

- `npm run build` 0 錯誤
- Kimi MCP CR 無 Critical
- git commit 存在
- tasks.md `[x]` 已更新

---

> 失敗分類處置、完整 Gmail 專案路徑、Token 預算、並行策略細節
> → `Read ~/.claude/reference/spectra-agent-routing-full.md`
