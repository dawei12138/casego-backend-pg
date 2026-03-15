# Step 8: 输出分析摘要

**标记：`[RA-STEP-8-DONE]`**

## 文件操作

- 读取：Step 7 生成的 JSON 报告文件
- 写入：`ra_step8_summary.md`
- 更新：`_progress.json`（step8 → completed，顶层 status → completed）

## 任务

读取 Step 7 的 JSON 报告，生成摘要并在对话中展示。

## 输出格式

同时写入 `ra_step8_summary.md` 并在对话中展示：

```markdown
| 指标 | 结果 |
|------|------|
| 原始需求 | [一句话概括] |
| 功能模块 | N 个 |
| 功能点 | N 个（P0: X / P1: Y / P2: Z） |
| 业务规则 | N 个（显式: X / 隐式: Y） |
| 操作流程 | N 个（主流程: X / 分支: Y） |
| 风险点 | N 个（高: X / 中: Y / 低: Z） |
| 评审问题 | N 个（需修复: X / 建议: Y） |
| 完整度 | X% |
| 输出文件 | requirement_analysis_xxx.json |
```

结尾提示：

> **下一步**: 使用 `testcase-generator` 技能生成测试用例，输入文件为上述输出文件路径。
