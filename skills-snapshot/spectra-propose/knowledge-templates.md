# Spectra 規格模板參考

> 在 Spectra 工作流中建立 artifacts 時依據這些結構填寫，不要照抄 placeholder。

---

## Proposal 模板（spectra-propose 第 5 步產出）

### Feature Type

```markdown
## Why

<!-- Why this functionality is needed -->

## What Changes

<!-- What will be different -->

## Non-Goals (optional)

<!-- Scope exclusions and rejected approaches. Required when design.md is skipped. -->

## Capabilities

### New Capabilities

- `<capability-name>`: <brief description>

### Modified Capabilities

(none)

## Impact

- Affected specs: <new or modified capabilities>
- Affected code: <list of affected files>
```

### Bug Fix Type

```markdown
## Problem

<!-- Current broken behavior -->

## Root Cause

<!-- Why it happens -->

## Proposed Solution

<!-- How to fix -->

## Non-Goals (optional)

<!-- Scope exclusions and rejected approaches. Required when design.md is skipped. -->

## Success Criteria

<!-- Expected behavior after fix, verifiable conditions -->

## Impact

- Affected code: <list of affected files>
```

### Refactor / Enhancement Type

```markdown
## Summary

<!-- One sentence description -->

## Motivation

<!-- Why this is needed -->

## Proposed Solution

<!-- How to do it -->

## Non-Goals (optional)

<!-- Scope exclusions and rejected approaches. Required when design.md is skipped. -->

## Alternatives Considered (optional)

<!-- Other approaches considered and why not -->

## Impact

- Affected specs: <affected capabilities>
- Affected code: <list of affected files>
```

---

## Design 模板

### User Scenarios & Testing

每個 User Story 必須可獨立測試、獨立部署、獨立交付價值

```markdown
### User Story 1 - [標題] (Priority: P1)

[用白話描述這個使用者旅程]

**Why this priority**: [為什麼是這個優先級]
**Independent Test**: [如何獨立測試這個 Story]

**Acceptance Scenarios**:
1. **Given** [初始狀態], **When** [動作], **Then** [預期結果]
```

### Functional Requirements

```markdown
### Functional Requirements

- **FR-001**: System MUST [具體能力]
- **FR-002**: System MUST [具體能力]
- 不確定的標記：[NEEDS CLARIFICATION: 具體問題]（最多 3 個）
```

### Key Entities

```markdown
### Key Entities

- **[Entity]**: [代表什麼、關鍵屬性、與其他 Entity 的關係]
```

### Success Criteria

```markdown
### Success Criteria

- **SC-001**: [可量測指標，技術無關]
- **SC-002**: [可量測指標]
```

---

## Tasks 模板

```markdown
# Tasks: [功能名稱]

**Prerequisites**: proposal.md（必要）, design.md（如有）

## 格式：`- [ ] [ID] [P?] [Story?] 描述 + 檔案路徑`

- **[P]**: 可平行執行（不同檔案、無依賴）
- **[US1]**: 所屬 User Story

## Phase 1: Setup
- [ ] T001 建立專案結構
- [ ] T002 初始化依賴

## Phase 2: Foundational（阻塞性前置）
⚠️ 所有 User Story 必須等此階段完成
- [ ] T003 [具體基礎建設 + 檔案路徑]

**Checkpoint**: 基礎就緒，User Story 可開始

## Phase 3: User Story 1 - [標題] (P1) MVP
**Goal**: [此 Story 交付什麼]
**Independent Test**: [獨立測試方法]

- [ ] T010 [P] [US1] [具體任務 + 檔案路徑]
- [ ] T011 [US1] [具體任務 + 檔案路徑]

**Checkpoint**: US1 可獨立運作和測試

## Phase 4: User Story 2 - [標題] (P2)
（同上結構）

## Phase N: Polish
- [ ] TXXX [P] 文件更新
- [ ] TXXX 效能優化
- [ ] TXXX 安全加固

## Dependencies
- Setup → Foundational → User Stories（可平行）→ Polish
- 各 User Story 間盡量獨立

## Implementation Strategy
- **MVP First**: 只做 US1 → 驗證 → 部署
- **Incremental**: US1 → US2 → US3，每個都是可交付增量
- **Parallel**: 多人同時做不同 User Story
```

---

## 品質檢查清單

```markdown
# Specification Quality Checklist: [功能名稱]

**Purpose**: 驗證規格完整性
**Created**: [日期]

## Content Quality
- [ ] 無實作細節（語言、框架、API）
- [ ] 聚焦使用者價值和商業需求
- [ ] 非技術人員可理解

## Requirement Completeness
- [ ] 無未解決的 [NEEDS CLARIFICATION]
- [ ] 每條需求可測試且不模糊
- [ ] Success Criteria 可量測且技術無關
- [ ] Edge Cases 已識別

## Feature Readiness
- [ ] 每條 FR 有明確的 Acceptance Criteria
- [ ] User Scenarios 涵蓋主要流程
- [ ] 無實作細節滲入規格
```
