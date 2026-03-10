## [0.5.2] - 2026-03-11

### 技能流程优化

- ✅ 新增“版本守门规则”：若 `mcporter` 注册的 `dingtalk-ai-table` 仍返回旧版 schema，必须先提示用户去新版 MCP 页面获取新的 Server 地址，再替换本地注册配置
- ✅ 修正新版 MCP 获取页面链接为 `https://mcp.dingtalk.com/#/detail?mcpId=9555&detailType=marketMcpDetail`
- ✅ 将守门逻辑优化为“同一个 MCP Server 地址只强制检查一次”，避免每次运行重复做迁移检查
- ✅ 移除带真实业务场景的示例内容，保留通用、可复用的技能规则

## [0.5.1] - 2026-03-11

### 元数据修复

- ✅ 补回 `SKILL.md` frontmatter 中的 `version` 与 `metadata.openclaw.requires` 声明
- ✅ 明确声明必需环境变量：`DINGTALK_MCP_URL`、`OPENCLAW_WORKSPACE`
- ✅ 明确声明必需二进制：`mcporter`、`python3`
- ✅ `package.json` 同步补充 `requiredEnv` / `requiresBinaries` / credentials 信息，修复 ClawHub 审核指出的 metadata mismatch
- ✅ README 同步补充依赖与环境声明

## [0.5.0] - 2026-03-11

### 重大升级

**全面切换到钉钉 AI 表格新版 MCP schema：**
- ✅ 从旧参数体系 `dentryUuid / sheetIdOrName / fieldIdOrName` 全面切换到新体系 `baseId / tableId / fieldId / recordId`
- ✅ 以 2026-03-10 发布的新 MCP server 实际 methods 为准，重建技能文档与脚本
- ✅ 覆盖新版全部 19 个 tools：Base / Table / Field / Record 全链路能力

### 脚本重写

**`scripts/bulk_add_fields.py`：**
- ✅ 改为调用 `create_fields`
- ✅ 输入参数改为 `<baseId> <tableId> fields.json`
- ✅ 支持 `name -> fieldName` 自动兼容
- ✅ 支持 `phone -> telephone` 自动兼容
- ✅ 增加新字段类型与关联字段 config 校验

**`scripts/import_records.py`：**
- ✅ 改为调用 `create_records`
- ✅ 输入参数改为 `<baseId> <tableId> data.(csv|json)`
- ✅ 记录结构改为 `cells`
- ✅ CSV 表头按 `fieldId` 解释
- ✅ JSON 同时支持裸对象和 `{"cells": ...}` 两种格式
- ✅ 支持布尔值 / 数字自动清洗

### 文档重写

- ✅ `SKILL.md` 按新版 schema 重写
- ✅ `references/api-reference.md` 按真实 MCP schema 重写
- ✅ `references/error-codes.md` 按新版排障逻辑重写
- ✅ `README.md` 更新为新版说明
- ✅ `package.json` 描述同步更新，版本提升到 `0.5.0`

### 测试

- ✅ `tests/test_security.py` 重写为新版 schema 测试
- ✅ 自动化测试 **21 / 21 全通过**
- ✅ Python 语法编译通过：`bulk_add_fields.py`、`import_records.py`、`test_security.py`

## [0.4.1] - 2026-03-10

### 文档更新

**README / SKILL 同步补充：**
- ✅ README 增加说明：本技能会随着钉钉 AI 表格 MCP 能力更新持续同步更新
- ✅ SKILL 新增“能力更新”章节，明确当 MCP Server 方法与技能说明不一致时，应优先升级技能
- ✅ SKILL 补充最新技能获取入口：ClawHub 页面与 GitHub 仓库链接

**变更说明：**
- 此版本仅文档更新，无脚本逻辑变更
- 目标是降低因 MCP 能力演进导致的使用偏差

## [0.4.0] - 2026-03-07

### 修复

**ClawHub 审核问题修复：**
- ✅ 将根节点缓存文件路径从工作区外的 `~/workspace/TABLE.md` 改为工作区内的 `$OPENCLAW_WORKSPACE/TABLE.md`
- ✅ 文档明确要求根节点缓存文件必须位于工作区内，避免 instruction scope 与脚本安全边界冲突
- ✅ 脚本中的 `dentryUuid` 校验从“仅允许 UUID v4”放宽为“兼容平台返回的合法 dentryUuid”
- ✅ README / SKILL / references 同步说明：`dentryUuid` 以 API 实际返回为准，不要求必须是 UUID v4
- ✅ 安全测试用例同步更新，覆盖 `dtcn_...` 风格 ID

## [0.3.9] - 2026-03-07

### 文档修正

**参数命名说明修复：**
- ✅ 修正 `SKILL.md` 中 `list_base_tables` 示例参数名：`dentry-uuid` → `dentryUuid`
- ✅ 在 `README.md` 故障排查中补充说明：`mcporter call ... key:value` 方式必须使用 camelCase 参数名
- ✅ 在 `references/error-codes.md` 中补充 `5000001` 的常见诱因：误用 kebab-case 参数名
- ✅ 在 `references/error-codes.md` 的 FAQ 中增加明确排查顺序：先查参数命名，再查 ID / 权限

**变更说明：**
- 此版本仅文档修正，无功能变更
- 修复 issue #1 中提到的调用误导问题

## [0.3.8] - 2026-03-05

### 文档更新

**SKILL.md 更新：**
- ✅ 新增"根节点配置"章节：根节点 UUID 保存在 `TABLE.md`，无需每次调 API 查询
- ✅ 提供从 `TABLE.md` 读取根节点并创建表格的示例命令

## [0.3.7] - 2026-03-02

### 文档修正

**SKILL.md 更新：**
- ✅ 修正 MCP 配置按钮名称："获取 MCP 凭证配置" → "获取 MCP Server 配置"

**变更说明：**
- 此版本仅文档修正，无功能变更
- 确保文档与钉钉 MCP 广场实际 UI 保持一致

# Changelog
## [0.3.6] - 2026-03-02

### 文档修正

**SKILL.md 更新：**
- ✅ 修正 MCP 配置按钮名称："获取 MCP 凭证配置" → "获取 MCP Server 配置"

**变更说明：**
- 此版本仅文档修正，无功能变更
- 确保文档与钉钉 MCP 广场实际 UI 保持一致


# Changelog
## [0.3.5] - 2025-12-21

### 文档完善

**SKILL.md 更新：**
- ✅ 补充 `add_base_table` 创建数据表的示例代码（之前缺失）
- ✅ 数据表操作部分现在包含完整的 CRUD 示例（创建/列出/重命名/删除）
- ✅ 确保所有 14 个 API 方法在文档中都有覆盖

**验证结果：**
- 14/14 API 方法全部覆盖 ✅
- SKILL.md 和 api-reference.md 保持一致 ✅

**变更说明：**
- 此版本仅文档更新，无功能变更
- 修复了用户反馈的"数据表操作缺少创建方法说明"问题


## [0.3.4] - 2025-02-27

### 🔒 安全加固（重大更新）

**新增安全功能：**
- ✅ **路径沙箱** - 新增 `resolve_safe_path()` 函数，防止目录遍历攻击（如 `../etc/passwd`）
- ✅ **dentryUuid 合法性验证** - 所有 dentryUuid 参数都会校验为 API 返回的合法 ID 形态，避免空值和明显异常输入
- ✅ **文件扩展名白名单** - 仅允许 `.json` 和 `.csv` 文件
- ✅ **文件大小限制** - JSON 最大 10MB，CSV 最大 50MB，防止 DoS 攻击
- ✅ **字段类型白名单** - 仅允许预定义的 11 种字段类型
- ✅ **命令超时保护** - mcporter 命令超时限制（60-120 秒）
- ✅ **输入清理** - 自动去除空白、验证空值、数字类型自动转换

**脚本重构：**
- `scripts/bulk_add_fields.py` - 全面安全加固，Python 3.9 兼容
- `scripts/import_records.py` - 全面安全加固，新增 JSON 导入支持

**测试覆盖：**
- 新增 `tests/test_security.py` - 25 项自动化安全测试，全部通过 ✅
- 新增 `tests/TEST_REPORT.md` - 完整测试报告和安全对比分析

**文档更新：**
- SKILL.md 新增"安全加固措施"章节，透明说明所有保护机制
- 添加配置建议：`OPENCLAW_WORKSPACE` 环境变量

**对比改进：**
- 安全维度对齐 ontology (Benign) 标准
- 除 mcporter 外部依赖外，其他风险已降至最低

---

## [0.3.3] - 2026-02-27

### 安全与元数据
- 在 SKILL.md frontmatter 中添加 `metadata.openclaw.requires` 声明
- 明确声明需要的环境变量：`DINGTALK_MCP_URL`
- 明确声明需要的二进制文件：`mcporter`
- 添加 `primaryEnv: DINGTALK_MCP_URL` 指定主要凭证
- 添加 `homepage` 字段指向 GitHub 仓库
- 修复 ClawHub 审核指出的元数据不一致问题


## [0.3.2] - 2026-02-27

### 文档
- 更新获取 Streamable HTTP URL 的说明，添加"点击'获取 MCP 凭证配置'按钮"步骤
- README.md 和 SKILL.md 同步更新

## [0.3.1] - 2026-02-27

### 修复
- 修复 credentials 存储方式说明不一致的问题
- package.json 移除 `requiredEnv`，添加 `storageMethod` 说明
- SKILL.md 补充两种凭证配置方式：`mcporter config`（推荐）和环境变量

## [0.3.0] - 2026-02-27

### 修复
- 调整 registry metadata 格式，使用 `requiredEnv` 和 `credentials` 字段
- SKILL.md description 中明确提及需要 DINGTALK_MCP_URL 凭证
- 移除 frontmatter 中的非标准字段（仅保留 name 和 description）

## [0.2.9] - 2026-02-27

### 修复
- 调整 registry metadata 格式，使用 `requiredEnv` 和 `credentials` 字段
- SKILL.md description 中明确提及需要 DINGTALK_MCP_URL 凭证
- 移除 frontmatter 中的非标准字段（仅保留 name 和 description）

## [0.2.8] - 2026-02-27

### 修复
- 修复 registry metadata 未正确声明 required credentials 的问题
- SKILL.md frontmatter 添加 `requiresCredentials` 和 `requiresBinaries` 声明
- package.json 改用 `peerDependencies` 声明 mcporter 依赖
- 明确凭证名称 `DINGTALK_MCP_URL` 和获取方式

## [0.2.7] - 2026-02-27

### 安全
- 新增"安全须知"章节，明确安装前注意事项
- 添加 mcporter 官方来源说明和验证提示
- 增加 Streamable HTTP URL 凭证安全警告
- 补充脚本使用安全说明（源码审查、测试环境优先）

## [0.2.6] - 2026-02-27

### 修复
- 添加 ClawHub 元数据声明，明确标注所需二进制文件和认证要求
- 修复安全警告中提到的 metadata omissions 问题

## [0.2.5] - 2026-02-27

### 改进
- 大幅完善 README.md，增加详细使用指南
- 新增"常用命令速查"表格，方便快速参考
- 新增"支持的字段类型"说明表
- 新增"故障排查"章节（认证失败、权限错误、字段类型不匹配等）
- 补充批量操作脚本使用说明
- 添加钉钉讨论群链接

### 文档
- README.md 从 526 字节扩展至完整使用指南

## [0.2.4] - 2026-02-26

### 更新
- 更新 MCP 广场 URL 地址为市场详情页 (mcpId=1060)

---

# Changelog

## [0.2.3] - 2026-02-26

### 新增
- 在 package.json 中添加了 GitHub 仓库链接

## [0.2.2] - 2026-02-26

### 新增
- 在 package.json 中添加了包依赖说明
- 添加了 Changelog

---

## [0.2.1] - 2026-02-26

### 新增
- 完善 CHANGELOG.md 和 package.json 文件
- 添加完整的版本管理和发布文档

### 修复
- 修正技能元数据信息

---

## [0.2.0] - 2026-02-25

### 新增
- 支持批量操作（最多 1000 条记录）
- 添加 `update_records` 方法用于批量更新记录
- 添加字段类型说明文档

### 改进
- 优化错误处理和错误码说明
- 完善 API 参考文档

---

## [0.1.0] - 2026-02-24

### 新增
- 钉钉 AI 表格（多维表）操作支持
- 表格创建、数据表管理、字段操作、记录增删改查
- 支持 7 种字段类型：text, number, singleSelect, multipleSelect, date, user, attachment

### 功能详情
- `get_root_node_of_my_document` - 获取文档根节点
- `create_base_app` - 创建 AI 表格
- `search_accessible_ai_tables` - 搜索可访问的表格
- `list_base_tables` - 列出数据表
- `update_base_tables` - 重命名数据表
- `delete_base_table` - 删除数据表
- `list_base_field` - 查看字段列表
- `add_base_field` - 添加字段
- `delete_base_field` - 删除字段
- `search_base_record` - 查询记录
- `add_base_record` - 添加记录
- `delete_base_record` - 删除记录

### 文档
- API 参考文档 (references/api-reference.md)
- 错误码说明 (references/error-codes.md)
- 示例脚本 (scripts/)

### 依赖
- mcporter CLI (v0.7.0+)
- 钉钉 MCP Server 配置
