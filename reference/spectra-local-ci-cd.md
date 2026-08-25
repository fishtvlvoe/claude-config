# Spectra Local CI / Cloud CD Delivery Contract

這是所有 Spectra SR／SDD change 的預設交付契約。`propose`、`discuss`、`ingest` 與 `apply` 都必須依本檔執行，不等待使用者再次提醒。

## 1. 每個 SR 都要先盤點

在建立或更新 artifacts 前，確認目標 repo 的：

- repo root、branch、package manager、實際測試入口。
- 本地 hooks：`.husky/`、`.githooks/`、`lefthook`、`pre-commit` 或 package scripts。
- 本地 CI：syntax/type-check、lint、format check、focused unit/integration test、behavior validation。
- Cloud CI/CD：`.github/workflows/` 或等價設定、整合測試、deploy target、觸發條件、Secrets／環境變數來源。

盤點結果必須寫進 `design.md` 的 `## Local CI / Cloud CD`，不可只留在對話裡。

## 2. SR artifacts 必須留下的內容

### proposal.md

在 Impact 補上受影響的 local CI、cloud CI/CD、hooks、deploy target；沒有受影響的面向也要明寫 `N/A` 與原因。

### design.md

加入 `## Local CI / Cloud CD`，至少包含：

```markdown
## Local CI / Cloud CD

### Local CI
- Hooks: [present / missing / N/A] — <path or reason>
- Syntax/type-check: `<command>`
- Lint/format: `<command>`
- Focused tests: `<command>`
- Behavior validation: `<command or bounded procedure>`

### Cloud CI/CD
- Workflow: [present / missing / N/A] — <path or reason>
- Integration checks: `<command or workflow job>`
- Deploy target and trigger: `<target>`, `<event>`
- Secrets boundary: `<GitHub/Vercel/Cloudflare secret or env source>`; no hardcoded secret

### Boundary
- Local scripts never deploy.
- Cloud workflow owns integration checks and deployment.
- Missing hooks or cloud gates become explicit tasks, unless this change is truly out of scope with a reason.
```

### tasks.md

每個會改程式碼的 change 都要有可執行的驗證 task，並且只能在實際證據存在後勾選：

1. Red test：先寫能重現需求或失敗路徑的測試。
2. Local gate：跑 syntax/type-check、lint/format、focused tests。
3. Behavior gate：用 fixture、curl/fetch、CLI 或 browser smoke 產出實際結果。
4. Cloud gate：若 change 影響 CI/CD 或上線，驗證 workflow、Secrets 邊界與 deploy target；若不影響，寫明 N/A 原因。

## 3. 自動停損規則

- 發現本地腳本含部署指令：停止，移到 cloud workflow 或提出修正 task。
- 發現 CI/CD YAML 硬編碼 API key、token、密碼：停止，改用 Secrets／環境變數。
- 缺少 hooks、測試入口或 cloud gate：在 tasks.md 補明確 task；不能用「之後補」代替。
- build 通過不等於完成；沒有行為驗證證據不得勾選 task。
- 部署完成不等於線上完成；涉及部署時還要回讀 live URL／API。
