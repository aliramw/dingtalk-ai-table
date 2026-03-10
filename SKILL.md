---
name: dingtalk-ai-table
description: 钉钉 AI 表格（多维表）操作技能。使用 mcporter CLI 连接钉钉官方新版 AI 表格 MCP server，基于 baseId / tableId / fieldId / recordId 体系执行 Base、Table、Field、Record 的查询与增删改。适用于创建 AI 表格、搜索表格、读取表结构、批量增删改记录、批量建字段、更新字段配置、按模板建表等场景。需要配置 DINGTALK_MCP_URL 或直接使用 Streamable HTTP URL。
---

# 钉钉 AI 表格操作（新版 MCP）

按 **新版 MCP schema** 工作：
- Base：`baseId`
- Table：`tableId`
- Field：`fieldId`
- Record：`recordId`

不要再用旧版 `dentryUuid / sheetIdOrName / fieldIdOrName`。

## 前置要求

### 安装 mcporter CLI

```bash
npm install -g mcporter
# 或
bun install -g mcporter
```

验证：

```bash
mcporter --version
```

### 配置 MCP Server

在钉钉 MCP 广场获取新版钉钉 AI 表格 MCP 的 `Streamable HTTP URL`。

方式一：直接配置到 mcporter

```bash
mcporter config add dingtalk-ai-table --url "<Streamable_HTTP_URL>"
```

方式二：使用环境变量

```bash
export DINGTALK_MCP_URL="<Streamable_HTTP_URL>"
```

> 这个 URL 带访问令牌，等同密码，不要泄露。

## 核心工具集

### Base 层
- `list_bases`
- `search_bases`
- `get_base`
- `create_base`
- `update_base`
- `delete_base`
- `search_templates`

### Table 层
- `get_tables`
- `create_table`
- `update_table`
- `delete_table`

### Field 层
- `get_fields`
- `create_fields`
- `update_field`
- `delete_field`

### Record 层
- `query_records`
- `create_records`
- `update_records`
- `delete_records`

## 推荐工作流

### 1. 先找 Base

```bash
mcporter call dingtalk-ai-table list_bases limit=10 --output json
mcporter call dingtalk-ai-table search_bases query="销售" --output json
```

### 2. 再拿 Table 目录

```bash
mcporter call dingtalk-ai-table get_base baseId="base_xxx" --output json
```

### 3. 再展开表结构

```bash
mcporter call dingtalk-ai-table get_tables \
  --args '{"baseId":"base_xxx","tableIds":["tbl_xxx"]}' \
  --output json
```

### 4. 字段复杂时读完整配置

```bash
mcporter call dingtalk-ai-table get_fields \
  --args '{"baseId":"base_xxx","tableId":"tbl_xxx","fieldIds":["fld_xxx"]}' \
  --output json
```

### 5. 再查 / 写记录

```bash
mcporter call dingtalk-ai-table query_records \
  --args '{"baseId":"base_xxx","tableId":"tbl_xxx","limit":20}' \
  --output json

mcporter call dingtalk-ai-table create_records \
  --args '{"baseId":"base_xxx","tableId":"tbl_xxx","records":[{"cells":{"fld_name":"张三"}}]}' \
  --output json
```

## 脚本

### 批量新增字段

```bash
python scripts/bulk_add_fields.py <baseId> <tableId> fields.json
```

`fields.json` 示例：

```json
[
  {"fieldName":"任务名","type":"text"},
  {"fieldName":"优先级","type":"singleSelect","config":{"options":[{"name":"高"},{"name":"中"},{"name":"低"}]}}
]
```

兼容项：
- `name` 会自动映射为 `fieldName`
- `phone` 会自动映射为 `telephone`

### 批量导入记录

```bash
python scripts/import_records.py <baseId> <tableId> data.csv
python scripts/import_records.py <baseId> <tableId> data.json 50
```

说明：
- CSV 表头默认按 `fieldId` 解释
- JSON 支持：
  - `[{"cells": {...}}]`
  - `[{"fld_xxx": "value"}]`

## 安全规则

- 文件路径受 `OPENCLAW_WORKSPACE` 沙箱限制
- 仅允许读取工作区内 `.json` / `.csv` 文件
- Base / Table / Field / Record ID 都做格式校验
- 批量上限按 MCP server 实际限制控制：
  - `create_fields`：最多 15
  - `get_tables / get_fields`：最多 10
  - `create_records / update_records / delete_records`：最多 100

## 调试原则

- 先 `get_base`，再 `get_tables`，必要时 `get_fields`
- 不要猜 `fieldId`
- 复杂参数一律用 `--args` JSON
- `singleSelect / multipleSelect` 过滤时必须传 option ID，不是 option name

## 参考

- API 参考：`references/api-reference.md`
- 错误排查：`references/error-codes.md`
