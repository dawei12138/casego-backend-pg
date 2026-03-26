---
name: api-testcase-generator
description: 用户提到接口测试时触发
---

# TestCase Generator — 接口测试用例生成

当用户消息中包含以下任一关键词时，**必须**激活此技能：
- `生成接口用例`
- `创建接口测试用例`
- `创建接口用例`
- `generate api test`
- `api test case`

触发后，向用户确认："已激活 **api-testcase-generator** 技能"

使用步骤：
* 所有内置工具操作都基于 / 虚拟根目录
* 先确定工作目录，使用内置工具 ls / ，检查项目目录是否已初始化。
* 如果已经有"data,common等文件夹"的目录结构，则跳过初始化，如果目录为空可以直接使用casego init 进行项目目录的初始化
* 接口测试的核心是在于编写测试用例，
* 编写规则，用例编写必须在data目录下，一个模块建立一个文件夹下，例如/data/user或者/data/system分开
* yaml测试用例编写请参考文件/skills/api-testcase-generator/references/yaml-examples.md
* 需要登录的接口统一到conftest.py文件当中进行配置，seesion级别的前置钩子，/skills/api-testcase-generator/references/conftest-auth-examples.zh-CN.md
* conftest.py文件禁止使用缓存CacheHandler来获取基础信息语法或者{}，因为该文件的优先级较高使用缓存{}或者获取配置会导致找不到值
* 编写完成后，参考文档进行语法检查
* 最后用例跑起来，使用casego gen，生成测试代码，在使用casego run，运行测试，也可以合并进行casego all
* 最终结果汇报给用户