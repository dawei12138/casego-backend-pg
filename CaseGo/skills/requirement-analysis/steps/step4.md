# Step 4: 用户操作流程梳理

**标记：`[RA-STEP-4-DONE]`**

## 文件操作

- 读取：`ra_step1_input_summary.md`、`ra_step2_module_breakdown.md`、`ra_step3_business_rules.md`
- 写入：`ra_step4_user_flows.md`
- 更新：`_progress.json`（step4 → in_progress → completed）

## 任务

梳理用户操作路径和交互流程，这是手工测试用例设计的核心依据。

## 输出格式

写入 `ra_step4_user_flows.md`：

```markdown
# Step 4: 用户操作流程梳理

## 流程 P1: [流程名称]
- 参与角色: [普通用户 / 管理员 / ...]
- 入口: [从哪里开始操作]

### 主流程（Happy Path）:
1. 步骤1
2. 步骤2
...

### 分支流程:
- 分支A（步骤X处）: [条件] → [预期行为]
- 分支B（步骤Y处）: [条件] → [预期行为]

### 异常流程:
- 网络中断 → [预期行为]
- 页面超时 → [预期行为]

## 流程 P2: [下一个流程]
...
```

## 关键要求

- 每个流程必须包含**主流程 + 至少1个分支流程**
- 分支流程标注从主流程哪一步分出
- 涉及页面跳转时标明页面名称
