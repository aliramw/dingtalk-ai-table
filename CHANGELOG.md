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
- ✅ **UUID 严格验证** - 所有 dentryUuid 参数必须通过 UUID v4 格式校验
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
