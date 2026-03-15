# Step 7: 生成需求分析报告

**标记：`[RA-STEP-7-DONE]`**

## 文件操作

- 读取：step1~step6 所有输出文件
- 写入：`requirement_analysis_{功能名}_{YYYYMMDD_HHMMSS}.json`
- 更新：`_progress.json`（step7 → completed，更新 deliverables）

## 任务

汇总所有分析结果为标准化 JSON，作为 `testcase-generator` 技能的输入。

## JSON 结构

```json
{
  "meta": {
    "generator": "Requirement Analysis Skill",
    "version": "2.0",
    "generated_at": "ISO8601",
    "source_description": "用户原始需求描述",
    "chain_position": "1/3",
    "next_skill": "testcase-generator"
  },
  "summary": {
    "total_modules": 0,
    "total_features": 0,
    "total_rules": 0,
    "total_flows": 0,
    "total_risk_points": 0,
    "completeness_score": 0,
    "review_issues_count": 0
  },
  "modules": [{
    "id": "M1", "name": "", "features": [{
      "id": "F1", "name": "", "priority": "P0-核心",
      "description": "", "testability": "高", "depends_on": []
    }]
  }],
  "business_rules": [{
    "id": "R1", "name": "", "type": "数据校验",
    "description": "", "is_implicit": false, "related_features": ["F1"]
  }],
  "user_flows": [{
    "id": "P1", "name": "", "actor": "", "entry_point": "",
    "main_steps": [],
    "branches": [{ "branch_point": "", "condition": "", "expected_behavior": "" }],
    "exception_flows": [{ "condition": "", "expected_behavior": "" }]
  }],
  "test_focus": {
    "risk_matrix": [{
      "id": "T1", "risk": "", "likelihood": "", "impact": "", "test_strategy": ""
    }],
    "recommended_test_types": []
  },
  "review_issues": [{
    "type": "", "description": "", "severity": "", "suggestion": ""
  }],
  "assumptions": []
}
```
