---
paths:
  - "ST/"
  - "products/"
  - "8-外掛/"
---

# opcOS 子服務開發指南

> 適用：任何 opcOS 旗下子服務（BuyGo、AIRE、anismile、FlowGo 等）的 SDD 開發流程。
> 無論在 ST/ 還是 Development/products/<name>/ 工作，這份指引都要遵守。

## 目錄對照（雙資料夾慣例）

| 用途 | 路徑 |
|------|------|
| 程式碼（monorepo） | `ST/apps/<name>/` |
| SDD 專案管理（SR） | `Development/products/<name>/openspec/` |
| 共用套件 | `ST/packages/` |
| 共用文件 | `ST/docs/` |

## 開發前強制 Checklist（supastarter-first，L083/L084）

每次開新功能 / 新子服務 **SDD 提案前**，必須先產出「可用資源清單」給 Fish 確認，才能動手：

1. 查 `ST/supastarter-nextjs/` — 有沒有現成功能可直接用？
2. 查 supastarter.dev 開發文件
3. 查 `ST/packages/` 12 個共用套件
4. grep `ST/apps/` 找既有 pattern；查 archived changes
5. 查 `Development/products/<name>/openspec/changes/` archived changes
6. 產出三分類清單：
   - ✅ 直接用（supastarter 已內建）
   - 🔧 改一點（小幅客製）
   - 🆕 需新寫（真正的新 scope）

沒產出清單 → 禁止進 `/spectra-propose`。

## SDD 入口流程

```
supastarter-first checklist
→ /spectra-discuss（可選，需求不清時）
→ /spectra-propose（產出 spec.md + tasks.md）
→ /spectra-apply（執行，按 Wave SOP）
→ /spectra-archive（完成後封存）
```

## 架構決策

- 子服務部署：子 domain 模式（`<name>.opcos.me`）
- 資料庫：共用 PostgreSQL `opcos`，app 專屬表加前綴（`<name>_*`）
- 統一登入：`opcos.me/login`（better-auth），cookie domain `.opcos.me`
- UI 元件：`@repo/ui`（L1-L3 三層積木），不要自建 button/input
- i18n：每個字串都要加 `apps/<name>/messages/` 翻譯

## 禁止事項

- 禁止自建 auth（用 supastarter auth 模組）
- 禁止繞過 oRPC procedure 直接打 DB
- 禁止只做靜態 UI 不接 API 就標「完成」（L084）
- 禁止新子服務用 Medusa（已封存方案）
