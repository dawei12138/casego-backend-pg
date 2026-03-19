# AI 技能管理 - 前端对接文档

> 基础路径: `/skills/skill`
> 字段命名: 请求/响应均使用 **camelCase** 风格

---

## 目录

1. [技能列表（分页）](#1-技能列表分页)
2. [技能列表（全量/下拉）](#2-技能列表全量下拉)
3. [新增技能](#3-新增技能)
4. [修改技能](#4-修改技能)
5. [删除技能（批量）](#5-删除技能批量)
6. [技能详情](#6-技能详情)
7. [上传技能包（ZIP）](#7-上传技能包zip)
8. [URL 导入技能](#8-url-导入技能)
9. [导出技能列表（Excel）](#9-导出技能列表excel)
10. [获取技能文件列表](#10-获取技能文件列表)
11. [获取技能文件内容](#11-获取技能文件内容)
12. [新增技能文件](#12-新增技能文件)
13. [编辑技能文件](#13-编辑技能文件)
14. [删除技能文件](#14-删除技能文件)

---

## 通用响应格式

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": null
}
```

| 字段   | 类型           | 说明                              |
| ------ | -------------- | --------------------------------- |
| `code` | `number`       | 200=成功, 500=失败/错误, 401=未授权 |
| `msg`  | `string`       | 提示信息                          |
| `data` | `object/array` | 业务数据，无数据时为 `null`        |

---

## 1. 技能列表（分页）

获取技能分页列表。

```
GET /skills/skill/list
```

**权限标识**: `skills:skill:list`

### 请求参数（Query）

| 参数        | 类型      | 必填 | 默认值 | 说明              |
| ----------- | --------- | ---- | ------ | ----------------- |
| `pageNum`   | `number`  | 否   | `1`    | 当前页码          |
| `pageSize`  | `number`  | 否   | `10`   | 每页记录数        |
| `skillName` | `string`  | 否   | -      | 技能名称（模糊搜索） |
| `enabled`   | `boolean` | 否   | -      | 是否启用          |

### 响应示例

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "rows": [
      {
        "skillId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "skillName": "playwright-cli",
        "displayName": "Playwright CLI 测试工具",
        "description": "基于 Playwright 的浏览器自动化测试技能",
        "enabled": true,
        "sourceType": "upload",
        "sourceUrl": null,
        "allowedTools": "Bash,Read,Write",
        "licenseInfo": "MIT",
        "createBy": "admin",
        "createTime": "2026-03-15 10:30:00",
        "updateBy": "admin",
        "updateTime": "2026-03-15 10:30:00",
        "remark": null,
        "sortNo": 1.0
      }
    ],
    "pageNum": 1,
    "pageSize": 10,
    "total": 1
  }
}
```

---

## 2. 技能列表（全量/下拉）

获取所有技能，适用于下拉选择框。

```
GET /skills/skill/all
```

**权限标识**: `skills:skill:list`

### 请求参数（Query）

| 参数        | 类型      | 必填 | 说明              |
| ----------- | --------- | ---- | ----------------- |
| `skillName` | `string`  | 否   | 技能名称（模糊搜索） |
| `enabled`   | `boolean` | 否   | 是否启用          |

### 响应示例

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": [
    {
      "skillId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "skillName": "playwright-cli",
      "displayName": "Playwright CLI 测试工具",
      "enabled": true
    },
    {
      "skillId": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
      "skillName": "frontend-design",
      "displayName": "前端设计",
      "enabled": true
    }
  ]
}
```

---

## 3. 新增技能

手动创建一个新技能。

```
POST /skills/skill
```

**权限标识**: `skills:skill:add`

### 请求体（JSON）

| 字段           | 类型      | 必填 | 说明                                           |
| -------------- | --------- | ---- | ---------------------------------------------- |
| `skillName`    | `string`  | **是** | 技能目录名，只允许小写字母、数字、连字符，如 `my-skill` |
| `displayName`  | `string`  | 否   | 显示名称                                       |
| `description`  | `string`  | 否   | 技能描述                                       |
| `enabled`      | `boolean` | 否   | 是否启用，默认 `true`                           |
| `allowedTools` | `string`  | 否   | 允许的工具列表，如 `"Bash,Read,Write"`          |
| `licenseInfo`  | `string`  | 否   | 许可证信息                                     |
| `remark`       | `string`  | 否   | 备注                                           |
| `sortNo`       | `number`  | 否   | 排序号                                         |

### 请求示例

```json
{
  "skillName": "my-custom-skill",
  "displayName": "我的自定义技能",
  "description": "一个自定义的 AI 技能",
  "enabled": true,
  "allowedTools": "Bash,Read,Write"
}
```

### 响应示例

```json
{
  "code": 200,
  "msg": "新增成功",
  "data": null
}
```

### 校验规则

- `skillName` 不能为空
- `skillName` 格式: `^[a-z0-9][a-z0-9-]*[a-z0-9]$`（或单个字母/数字），最大 128 字符
- `skillName` 不可与已有技能重复

---

## 4. 修改技能

更新已有技能信息。

```
PUT /skills/skill
```

**权限标识**: `skills:skill:edit`

### 请求体（JSON）

| 字段           | 类型      | 必填 | 说明                |
| -------------- | --------- | ---- | ------------------- |
| `skillId`      | `string`  | **是** | 技能 UUID           |
| `skillName`    | `string`  | **是** | 技能目录名          |
| `displayName`  | `string`  | 否   | 显示名称            |
| `description`  | `string`  | 否   | 技能描述            |
| `enabled`      | `boolean` | 否   | 是否启用            |
| `allowedTools` | `string`  | 否   | 允许的工具列表      |
| `licenseInfo`  | `string`  | 否   | 许可证信息          |
| `remark`       | `string`  | 否   | 备注                |
| `sortNo`       | `number`  | 否   | 排序号              |

### 请求示例

```json
{
  "skillId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "skillName": "playwright-cli",
  "displayName": "Playwright CLI（已更新）",
  "enabled": false
}
```

### 响应示例

```json
{
  "code": 200,
  "msg": "修改成功",
  "data": null
}
```

---

## 5. 删除技能（批量）

批量删除技能，同时删除关联的文件记录和文件系统目录。

```
DELETE /skills/skill/{skillIds}
```

**权限标识**: `skills:skill:remove`

### 路径参数

| 参数       | 类型     | 说明                           |
| ---------- | -------- | ------------------------------ |
| `skillIds` | `string` | 技能 ID，多个以逗号分隔         |

### 请求示例

```
DELETE /skills/skill/a1b2c3d4-e5f6-7890-abcd-ef1234567890,b2c3d4e5-f6a7-8901-bcde-f12345678901
```

### 响应示例

```json
{
  "code": 200,
  "msg": "删除成功",
  "data": null
}
```

---

## 6. 技能详情

获取技能详细信息，包含文件列表（不含文件内容）。

```
GET /skills/skill/{skillId}
```

**权限标识**: `skills:skill:query`

### 路径参数

| 参数      | 类型     | 说明      |
| --------- | -------- | --------- |
| `skillId` | `string` | 技能 UUID |

### 响应示例

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "skillId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "skillName": "playwright-cli",
    "displayName": "Playwright CLI 测试工具",
    "description": "基于 Playwright 的浏览器自动化测试技能",
    "enabled": true,
    "sourceType": "upload",
    "sourceUrl": null,
    "allowedTools": "Bash,Read,Write",
    "licenseInfo": "MIT",
    "createBy": "admin",
    "createTime": "2026-03-15 10:30:00",
    "updateBy": "admin",
    "updateTime": "2026-03-15 10:30:00",
    "remark": null,
    "sortNo": 1.0,
    "files": [
      {
        "fileId": "f1a2b3c4-d5e6-7890-abcd-ef1234567890",
        "skillId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "filePath": "SKILL.md",
        "isBinary": false,
        "createTime": "2026-03-15 10:30:00",
        "updateTime": "2026-03-15 10:30:00"
      },
      {
        "fileId": "f2b3c4d5-e6f7-8901-bcde-f12345678901",
        "skillId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "filePath": "references/tracing.md",
        "isBinary": false,
        "createTime": "2026-03-15 10:31:00",
        "updateTime": "2026-03-15 10:31:00"
      }
    ]
  }
}
```

> 注意：文件列表中 `content` 字段不会返回，需通过「获取文件内容」接口单独获取。

---

## 7. 上传技能包（ZIP）

上传 ZIP 文件导入技能。ZIP 包内应包含 `SKILL.md` 文件。

```
POST /skills/skill/upload
```

**权限标识**: `skills:skill:add`

### 请求方式

`Content-Type: multipart/form-data`

| 字段   | 类型   | 必填 | 说明          |
| ------ | ------ | ---- | ------------- |
| `file` | `File` | **是** | ZIP 文件      |

### 前端调用示例

```javascript
const formData = new FormData()
formData.append('file', zipFile) // zipFile 为 File 对象

await request.post('/skills/skill/upload', formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
})
```

### 响应示例

```json
{
  "code": 200,
  "msg": "导入成功: 技能 playwright-cli 已创建，共 8 个文件",
  "data": null
}
```

### 错误响应

```json
{
  "code": 500,
  "msg": "ZIP包中未找到 SKILL.md 文件",
  "data": null
}
```

### ZIP 包结构说明

支持两种结构：

```
# 结构一：根目录直接包含 SKILL.md
my-skill.zip
├── SKILL.md
├── references/
│   └── guide.md
└── ...

# 结构二：嵌套一层目录
my-skill.zip
└── my-skill/
    ├── SKILL.md
    ├── references/
    │   └── guide.md
    └── ...
```

系统会自动检测技能根目录位置。

---

## 8. URL 导入技能

从 URL 地址导入技能，支持 SKILL.md 原始链接或 ZIP 文件链接。

```
POST /skills/skill/import-url
```

**权限标识**: `skills:skill:add`

### 请求体（JSON）

| 字段        | 类型     | 必填 | 说明                                       |
| ----------- | -------- | ---- | ------------------------------------------ |
| `url`       | `string` | **是** | 导入 URL（SKILL.md 原始文件链接或 ZIP 链接） |
| `skillName` | `string` | 否   | 技能目录名，不填则从 URL 自动推断           |

### 请求示例

```json
{
  "url": "https://raw.githubusercontent.com/anthropics/claude-code/main/CaseGo/skills/playwright-cli/SKILL.md",
  "skillName": "playwright-cli"
}
```

### 响应示例

```json
{
  "code": 200,
  "msg": "导入成功: 技能 playwright-cli 已创建",
  "data": null
}
```

### 错误响应

```json
{
  "code": 500,
  "msg": "技能名称 playwright-cli 已存在",
  "data": null
}
```

---

## 9. 导出技能列表（Excel）

导出技能列表为 Excel 文件。

```
POST /skills/skill/export
```

**权限标识**: `skills:skill:export`

### 请求方式

`Content-Type: application/x-www-form-urlencoded`

| 参数        | 类型      | 必填 | 说明              |
| ----------- | --------- | ---- | ----------------- |
| `skillName` | `string`  | 否   | 技能名称（筛选）  |
| `enabled`   | `boolean` | 否   | 是否启用（筛选）  |

### 响应

返回二进制流文件（Excel .xlsx），前端需要做文件下载处理。

### 前端调用示例

```javascript
const response = await request.post('/skills/skill/export', data, {
  responseType: 'blob'
})
const url = window.URL.createObjectURL(new Blob([response.data]))
const link = document.createElement('a')
link.href = url
link.setAttribute('download', 'skills.xlsx')
document.body.appendChild(link)
link.click()
link.remove()
```

---

## 10. 获取技能文件列表

获取指定技能下的所有文件列表（不含文件内容）。

```
GET /skills/skill/{skillId}/files
```

**权限标识**: `skills:skill:query`

### 路径参数

| 参数      | 类型     | 说明      |
| --------- | -------- | --------- |
| `skillId` | `string` | 技能 UUID |

### 响应示例

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": [
    {
      "fileId": "f1a2b3c4-d5e6-7890-abcd-ef1234567890",
      "skillId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "filePath": "SKILL.md",
      "isBinary": false,
      "createTime": "2026-03-15 10:30:00",
      "updateTime": "2026-03-15 10:30:00"
    },
    {
      "fileId": "f2b3c4d5-e6f7-8901-bcde-f12345678901",
      "skillId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "filePath": "references/running-code.md",
      "isBinary": false,
      "createTime": "2026-03-15 10:31:00",
      "updateTime": "2026-03-15 10:31:00"
    },
    {
      "fileId": "f3c4d5e6-f7a8-9012-cdef-123456789012",
      "skillId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "filePath": "references/tracing.md",
      "isBinary": false,
      "createTime": "2026-03-15 10:31:00",
      "updateTime": "2026-03-15 10:31:00"
    }
  ]
}
```

---

## 11. 获取技能文件内容

根据文件相对路径获取文件的完整内容。

```
GET /skills/skill/{skillId}/file
```

**权限标识**: `skills:skill:query`

### 路径参数

| 参数      | 类型     | 说明      |
| --------- | -------- | --------- |
| `skillId` | `string` | 技能 UUID |

### 查询参数

| 参数       | 类型     | 必填 | 说明                          |
| ---------- | -------- | ---- | ----------------------------- |
| `filePath` | `string` | **是** | 文件相对路径，如 `SKILL.md`   |

### 请求示例

```
GET /skills/skill/a1b2c3d4-e5f6-7890-abcd-ef1234567890/file?filePath=SKILL.md
```

### 响应示例

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "fileId": "f1a2b3c4-d5e6-7890-abcd-ef1234567890",
    "skillId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "filePath": "SKILL.md",
    "content": "---\nname: playwright-cli\ndescription: Playwright CLI 测试工具\nallowed_tools:\n  - Bash\n  - Read\n---\n\n# Playwright CLI\n\n这是一个用于浏览器自动化测试的技能...",
    "isBinary": false,
    "createTime": "2026-03-15 10:30:00",
    "updateTime": "2026-03-15 10:30:00"
  }
}
```

---

## 12. 新增技能文件

向指定技能目录中添加新文件。

```
POST /skills/skill/{skillId}/file
```

**权限标识**: `skills:skill:add`

### 路径参数

| 参数      | 类型     | 说明      |
| --------- | -------- | --------- |
| `skillId` | `string` | 技能 UUID |

### 请求体（JSON）

| 字段       | 类型      | 必填 | 说明                                      |
| ---------- | --------- | ---- | ----------------------------------------- |
| `filePath` | `string`  | **是** | 文件相对路径，如 `references/new-guide.md` |
| `content`  | `string`  | 否   | 文件文本内容                              |
| `isBinary` | `boolean` | 否   | 是否二进制文件，默认 `false`              |

### 请求示例

```json
{
  "filePath": "references/new-guide.md",
  "content": "# 新指南\n\n这是一个新添加的参考文档。"
}
```

### 响应示例

```json
{
  "code": 200,
  "msg": "新增成功",
  "data": null
}
```

### 校验规则

- `filePath` 不能与该技能下已有文件重复

---

## 13. 编辑技能文件

更新指定技能文件的内容。

```
PUT /skills/skill/{skillId}/file
```

**权限标识**: `skills:skill:edit`

### 路径参数

| 参数      | 类型     | 说明      |
| --------- | -------- | --------- |
| `skillId` | `string` | 技能 UUID |

### 请求体（JSON）

| 字段       | 类型      | 必填 | 说明                |
| ---------- | --------- | ---- | ------------------- |
| `fileId`   | `string`  | **是** | 文件 UUID           |
| `filePath` | `string`  | 否   | 文件相对路径        |
| `content`  | `string`  | 否   | 更新后的文件内容    |
| `isBinary` | `boolean` | 否   | 是否二进制文件      |

### 请求示例

```json
{
  "fileId": "f1a2b3c4-d5e6-7890-abcd-ef1234567890",
  "content": "# 更新后的内容\n\n文档已被修改。"
}
```

### 响应示例

```json
{
  "code": 200,
  "msg": "修改成功",
  "data": null
}
```

---

## 14. 删除技能文件

从技能目录中删除指定文件。

```
DELETE /skills/skill/{skillId}/file/{fileId}
```

**权限标识**: `skills:skill:remove`

### 路径参数

| 参数      | 类型     | 说明      |
| --------- | -------- | --------- |
| `skillId` | `string` | 技能 UUID |
| `fileId`  | `string` | 文件 UUID |

### 请求示例

```
DELETE /skills/skill/a1b2c3d4-e5f6-7890-abcd-ef1234567890/file/f1a2b3c4-d5e6-7890-abcd-ef1234567890
```

### 响应示例

```json
{
  "code": 200,
  "msg": "删除成功",
  "data": null
}
```

---

## 数据模型参考

### Skill 字段说明

| 字段           | 类型      | 说明                                   |
| -------------- | --------- | -------------------------------------- |
| `skillId`      | `string`  | UUID，技能唯一标识                     |
| `skillName`    | `string`  | 技能目录名（英文，小写+数字+连字符）    |
| `displayName`  | `string`  | 技能显示名称                           |
| `description`  | `string`  | 技能描述                               |
| `enabled`      | `boolean` | 是否启用                               |
| `sourceType`   | `string`  | 来源类型: `manual` / `upload` / `url`  |
| `sourceUrl`    | `string`  | URL 导入时的源地址                     |
| `allowedTools` | `string`  | 允许的工具列表（逗号分隔）             |
| `licenseInfo`  | `string`  | 许可证信息                             |
| `createBy`     | `string`  | 创建人                                 |
| `createTime`   | `string`  | 创建时间                               |
| `updateBy`     | `string`  | 更新人                                 |
| `updateTime`   | `string`  | 更新时间                               |
| `remark`       | `string`  | 备注                                   |
| `sortNo`       | `number`  | 排序号                                 |

### SkillFile 字段说明

| 字段         | 类型      | 说明                                        |
| ------------ | --------- | ------------------------------------------- |
| `fileId`     | `string`  | UUID，文件唯一标识                          |
| `skillId`    | `string`  | 所属技能 ID                                 |
| `filePath`   | `string`  | 文件相对路径，如 `SKILL.md`、`references/x.md` |
| `content`    | `string`  | 文件文本内容                                |
| `isBinary`   | `boolean` | 是否二进制文件                              |
| `createTime` | `string`  | 创建时间                                    |
| `updateTime` | `string`  | 更新时间                                    |

---

## 权限标识汇总

| 权限标识              | 说明         | 对应接口                                      |
| --------------------- | ------------ | --------------------------------------------- |
| `skills:skill:list`   | 查看列表     | 技能列表（分页）、技能列表（全量）            |
| `skills:skill:query`  | 查看详情     | 技能详情、文件列表、文件内容                  |
| `skills:skill:add`    | 新增         | 新增技能、上传技能包、URL导入、新增文件       |
| `skills:skill:edit`   | 编辑         | 修改技能、编辑文件                            |
| `skills:skill:remove` | 删除         | 删除技能、删除文件                            |
| `skills:skill:export` | 导出         | 导出技能列表                                  |
