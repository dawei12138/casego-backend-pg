# Step 5: 测试关注点与风险分析

**标记：`[RA-STEP-5-DONE]`**

## 文件操作

- 读取：`ra_step2_module_breakdown.md`、`ra_step3_business_rules.md`、`ra_step4_user_flows.md`
- 写入：`ra_step5_risk_analysis.md`
- 更新：`_progress.json`（step5 → in_progress → completed）

## 任务

识别高风险区域和需要重点测试的关注点。

## 输出格式

写入 `ra_step5_risk_analysis.md`：

```markdown
# Step 5: 测试关注点与风险分析

## 风险矩阵

| ID | 风险点 | 可能性 | 影响度 | 建议测试策略 |
|----|-------|--------|-------|-------------|
| T1 | 并发注册同一手机号 | 中 | 高 | 多终端同时操作测试 |

## 测试类型覆盖建议
- 功能测试: [覆盖的功能点]
- 边界值测试: [需要边界测试的输入字段]
- 异常流程测试: [异常场景列表]
- UI/交互测试: [是否需要，理由]
- 兼容性测试: [是否需要，理由]
- 易用性测试: [是否需要，理由]
- 安全测试: [是否需要，理由]
```
