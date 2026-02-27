# 钉钉 AI 表格 Skill

OpenClaw 技能，用于操作钉钉 AI 表格（多维表）。通过 MCP 协议连接钉钉官方 API，实现表格创建、数据管理、自动化 workflows。

## 功能特性

- ✅ 创建/删除 AI 表格
- ✅ 管理数据表（重命名、删除）
- ✅ 字段操作（添加/删除，支持 7 种字段类型）
- ✅ 记录增删改查（支持批量操作）
- ✅ 批量导入导出（CSV/JSON）

## 前置要求

### 1. 安装 mcporter CLI

本技能依赖 `mcporter` 工具，用于连接钉钉 MCP 服务器。

```bash
# 使用 npm 安装
npm install -g mcporter

# 或使用 bun 安装
bun install -g mcporter
```

验证安装：
```bash
mcporter --version
```

### 2. 获取钉钉 MCP Server URL

1. 访问钉钉 MCP 广场 - AI 表格页面：
   https://mcp.dingtalk.com/#/detail?mcpId=1060&detailType=marketMcpDetail
2. 在页面**右侧**找到 `Streamable HTTP URL`
3. 点击复制该 URL（完整地址，以 http 开头）

### 3. 配置 MCP 服务器

```bash
mcporter config add dingtalk-ai-table --url "<你的 Streamable HTTP URL>"
```

将 `<你的 Streamable HTTP URL>` 替换为步骤 2 中复制的实际 URL。

## 快速开始

### 安装技能

```bash
# 方式 1：使用 clawhub（推荐）
clawhub install dingtalk-ai-table

# 方式 2：直接对 OpenClaw 说
"安装 dingtalk-ai-table 这个 skill"
```

### 验证配置

```bash
mcporter call dingtalk-ai-table get_root_node_of_my_document --output json
```

成功时会返回包含 `rootDentryUuid` 的 JSON，例如：
```json
{
  "rootDentryUuid": "dtcn_xxxxxxxx"
}
```

### 创建第一个表格

```bash
# 使用上一步获取的 rootDentryUuid
mcporter call dingtalk-ai-table create_base_app \
  filename="我的第一个表格" \
  target="dtcn_xxxxxxxx" \
  --output json
```

创建成功后会返回表格的 `uuid`（即 `dentryUuid`），用于后续操作。

## 常用命令速查

| 操作 | 命令 |
|------|------|
| 获取根节点 | `mcporter call dingtalk-ai-table get_root_node_of_my_document --output json` |
| 搜索表格 | `mcporter call dingtalk-ai-table search_accessible_ai_tables keyword="关键词" --output json` |
| 列出数据表 | `mcporter call dingtalk-ai-table list_base_tables dentry-uuid="<UUID>" --output json` |
| 查看字段 | `mcporter call dingtalk-ai-table list_base_field --args '{"dentryUuid":"<UUID>","sheetIdOrName":"数据表"}' --output json` |
| 添加字段 | `mcporter call dingtalk-ai-table add_base_field --args '{"dentryUuid":"<UUID>","sheetIdOrName":"数据表","addField":{"name":"字段名","type":"text"}}' --output json` |
| 添加记录 | `mcporter call dingtalk-ai-table add_base_record --args '{"dentryUuid":"<UUID>","sheetIdOrName":"数据表","records":[{"fields":{"字段 1":"值 1"}}]}' --output json` |
| 查询记录 | `mcporter call dingtalk-ai-table search_base_record --args '{"dentryUuid":"<UUID>","sheetIdOrName":"数据表"}' --output json` |

## 支持的字段类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `text` | 文本 | `{"name":"姓名","type":"text"}` |
| `number` | 数字 | `{"name":"数量","type":"number"}` |
| `singleSelect` | 单选 | `{"name":"状态","type":"singleSelect"}` |
| `multipleSelect` | 多选 | `{"name":"标签","type":"multipleSelect"}` |
| `date` | 日期 | `{"name":"日期","type":"date"}` |
| `user` | 人员 | `{"name":"负责人","type":"user"}` |
| `attachment` | 附件 | `{"name":"文件","type":"attachment"}` |

## 故障排查

### 认证失败 / 无法连接服务器

1. 检查 `mcporter` 是否正确安装：`mcporter --version`
2. 确认服务器 URL 配置正确：`mcporter config list`
3. 确认 URL 是完整的（以 `http` 或 `https` 开头）
4. 检查网络连接，确保能访问钉钉服务

### 找不到表格 / 权限错误

1. 确认使用的是正确的 `dentryUuid`（创建表格后返回的 `uuid` 字段）
2. 确认你有该表格的访问权限
3. 使用 `search_accessible_ai_tables` 搜索你可访问的表格

### 字段类型不匹配

- 单选/多选字段：添加记录时需使用 `{"name":"选项名","id":"选项 ID"}` 格式
- 日期字段：支持 Unix 时间戳（毫秒）或 `YYYY-MM-DD` 格式
- 人员字段：需使用钉钉用户 ID

### 批量操作失败

- 单次添加/删除记录最多 1000 条
- 确保 JSON 格式正确（使用 `--args` 时）
- 检查字段名是否与数据表中完全一致

## 使用脚本

对于批量操作，可使用项目自带的 Python 脚本：

```bash
# 批量添加字段
python scripts/bulk_add_fields.py <dentryUuid> <sheetName> fields.json

# 批量导入记录
python scripts/import_records.py <dentryUuid> <sheetName> data.csv
```

## 相关链接

- 📊 [钉钉 AI 表格官网](https://table.dingtalk.com)
- 🔌 [钉钉 MCP 广场 - AI 表格](https://mcp.dingtalk.com/#/detail?mcpId=1060&detailType=marketMcpDetail)
- 📦 [ClawHub 技能页面](https://clawhub.com/skills/dingtalk-ai-table)
- 🐛 [问题反馈 (GitHub Issues)](https://github.com/aliramw/dingtalk-ai-table/issues)
- 📖 [源代码仓库](https://github.com/aliramw/dingtalk-ai-table)

## 技术支持

如有问题，请在钉钉 AI 表格官方交流群提问，或通过 GitHub Issues 反馈。
