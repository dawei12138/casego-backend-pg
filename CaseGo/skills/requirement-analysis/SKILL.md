---
name: requirement-analysis
description: 对需求进行结构化分析与评审，输出标准化需求分析报告，作为测试用例生成的输入。测试用例生成链第一环。
---

# Requirement Analysis — 产品需求分析与评审

## 触发条件

当用户消息包含以下关键词时**必须**激活：
`需求分析`、`分析需求`、`评审需求`、`requirement analysis`、`analyze requirement`

触发后确认："已激活 **Requirement Analysis** 技能，将对需求进行结构化分析与评审。"

## 技能定位

```
[需求分析评审] ★ → [测试用例生成] → [测试用例评审]
```

核心职责：将自然语言需求转化为结构化、可测试的需求分析文档。

## 输入

用户提供以下任一形式（可组合）：
- 功能描述 / 需求文档(PRD/用户故事) / 业务场景 — **至少一种**
- 原型图/截图、接口文档 — 可选辅助

## 输出

标准化 JSON 需求分析报告，作为 `testcase-generator` 技能的直接输入。

---

## 执行流程

**开始前**先读取 `protocol.md` 了解文件管理协议并初始化 `_progress.json`，然后按顺序执行每步。

**执行每步时，读取对应 `steps/stepN.md` 获取详细指令。**

| 步骤 | 名称 | 指令文件 | 输出文件 | 标记 |
|------|------|---------|---------|------|
| 初始化 | 创建进度索引 | `protocol.md` | /`_progress.json` | - |
| Step 1 | 需求收集与澄清 | `steps/step1.md` | `ra_step1_input_summary.md` | `[RA-STEP-1-DONE]` |
| Step 2 | 功能模块拆解 | `steps/step2.md` | `ra_step2_module_breakdown.md` | `[RA-STEP-2-DONE]` |
| Step 3 | 业务规则提取 | `steps/step3.md` | `ra_step3_business_rules.md` | `[RA-STEP-3-DONE]` |
| Step 4 | 用户操作流程梳理 | `steps/step4.md` | `ra_step4_user_flows.md` | `[RA-STEP-4-DONE]` |
| Step 5 | 测试关注点与风险 | `steps/step5.md` | `ra_step5_risk_analysis.md` | `[RA-STEP-5-DONE]` |
| Step 6 | 需求评审与问题清单 | `steps/step6.md` | `ra_step6_review_issues.md` | `[RA-STEP-6-DONE]` |
| Step 7 | 生成分析报告 | `steps/step7.md` | `requirement_analysis_{名称}_{时间戳}.json` | `[RA-STEP-7-DONE]` |
| Step 8 | 输出分析摘要 | `steps/step8.md` | `ra_step8_summary.md` | `[RA-STEP-8-DONE]` |

---

## 关键约束

1. **顺序执行**：Step 1→8 不得跳步或合并，每步完成后输出标记
2. **文件驱动**：每步开始前读取前置输出文件，完成后写入产出文件，禁止仅依赖对话记忆
3. **进度同步**：每步开始/完成时更新 `_progress.json`
4. **P0 阻塞**：Step 1 中 P0 级澄清问题必须多轮调用ask_user_question，来和用户进行交互，确保拿到足够多的信息后结束交互并且进入下一步
5. **隐式标注**：推导出的业务规则必须标注为隐式
6. **分支必需**：每个操作流程必须识别至少 1 个分支流程
7. **链式对齐**：输出格式必须与 `testcase-generator` 输入格式对齐
8. **评审客观**：不遗漏问题，不过度解读，严重程度评估合理
