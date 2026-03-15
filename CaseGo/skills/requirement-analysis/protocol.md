# 文件上下文管理协议

本技能采用**文件驱动的上下文管理**，所有产出通过文件系统持久化。

## 核心原则

1. **写入优先**：每步完成后立即写入产出文件
2. **写入路径**: 产出物路径/，必须是根目录开头路径，严禁skills目录下写入新路径
3. **索引追踪**：通过 `_progress.json` 追踪执行进度和产出路径
4. **任务分解**: 通过todolist工具来进行任务的分解并且更新任务进度
## 文件清单

| 步骤 | 输出文件                                        | 说明 |
|------|---------------------------------------------|------|
| 初始化 | `_progress.json`                            | 进度索引 |
| Step 1 | `ra_step1_input_summary.md`                 | 需求收集与澄清 |
| Step 2 | `ra_step2_module_breakdown.md`              | 功能模块拆解 |
| Step 3 | `ra_step3_business_rules.md`                | 业务规则提取 |
| Step 4 | `ra_step4_user_flows.md`                    | 用户操作流程 |
| Step 5 | `ra_step5_risk_analysis.md`                 | 测试关注点与风险 |
| Step 6 | `ra_step6_review_issues.md`                 | 需求评审问题清单 |
| Step 7 | `requirement_analysis_{功能名}_{timestamp}.json` | 最终分析报告 |
| Step 8 | `ra_step8_summary.md`                       | 分析摘要 |

## `_progress.json` 初始结构

```json
{
  "skill": "requirement-analysis",
  "started_at": "ISO8601时间",
  "status": "in_progress",
  "steps": {
    "step1": { "status": "not_started", "output_file": null },
    "step2": { "status": "not_started", "output_file": null },
    "step3": { "status": "not_started", "output_file": null },
    "step4": { "status": "not_started", "output_file": null },
    "step5": { "status": "not_started", "output_file": null },
    "step6": { "status": "not_started", "output_file": null },
    "step7": { "status": "not_started", "output_file": null },
    "step8": { "status": "not_started", "output_file": null }
  },
  "deliverables": []
}
```

## 状态管理规则

1. 开始步骤前：对应状态 → `"in_progress"`
2. 完成步骤后：对应状态 → `"completed"`，填入 `output_file` 路径
3. 步骤被阻塞：保持 `"in_progress"`，多轮调用ask_user_question，来和用户进行交互
4. 全部完成：顶层 `status` → `"completed"`，填入 `deliverables`
