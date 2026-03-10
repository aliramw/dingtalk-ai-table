---
name: dingtalk-ai-table
description: 钉钉 AI 表格（多维表）操作技能。使用 mcporter CLI 连接钉钉官方新版 AI 表格 MCP server，基于 baseId / tableId / fieldId / recordId 体系执行 Base、Table、Field、Record 的查询与增删改。适用于创建 AI 表格、搜索表格、读取表结构、批量增删改记录、批量建字段、更新字段配置、按模板建表等场景。需要配置 DINGTALK_MCP_URL 或直接使用 Streamable HTTP URL。
version: 0.5.2
metadata:
  openclaw:
    requires:
      env:
        - DINGTALK_MCP_URL
        - OPENCLAW_WORKSPACE
      bins:
        - mcporter
        - python3
    primaryEnv: DINGTALK_MCP_URL
    homepage: https://github.com/aliramw/dingtalk-ai-table
---

# 钉钉 AI 表格操作（新版 MCP）

按 **新版 MCP schema** 工作：
- Base：`baseId`
- Table：`tableId`
- Field：`fieldId`
- Record：`recordId`

不要再用旧版 `dentryUuid / sheetIdOrName / fieldIdOrName`。

## 版本守门规则（每个 MCP Server 地址只强制检查一次）

在真正开始任何 AI 表格操作前，必须先检查当前 `mcporter` 注册的 `dingtalk-ai-table` MCP server 实际返回的 tools schema。**但这个检查不该每次都重复做；同一个 MCP Server 地址只需要强制检查一次。**

### 一次性检查策略

1. 先读取当前 `mcporter` 里 `dingtalk-ai-table` 对应的 MCP Server 地址。
2. 用这个地址生成一个本地检查标记（例如基于完整 URL 或其 hash）。
3. 在工作区保存检查结果，例如放到：

```text
~/.openclaw/workspace/.cache/dingtalk-ai-table/
```

建议文件名模式：

```text
schema-check-<url-hash>.json
```

4. 如果当前地址对应的检查标记已经存在，并且结果是“已确认新版 schema”，则**跳过重复检查**，直接继续后续 AI 表格操作。
5. 只有在以下情况才重新强制检查：
   - 第一次运行，没有检查标记
   - `mcporter` 里的 MCP Server 地址变了
   - 之前检查结果是旧版 schema / 检查失败
   - 用户明确要求重新验证

### 强制检查时执行

```bash
mcporter list dingtalk-ai-table --schema
```

### 判断标准

如果返回的 tools 仍然是旧版这一套，例如出现：
- `get_root_node_of_my_document`
- `create_base_app`
- `list_base_tables`
- `add_base_record`
- `search_base_record`
- `list_base_field`

或者整体仍然基于：
- `dentryUuid`
- `sheetIdOrName`
- `fieldIdOrName`

那么说明：**虽然 skill 文件已经是新版，但 mcporter 里注册的 MCP server 地址还是旧的，不能继续操作。**

### 遇到旧版 schema 时的强制提示

此时必须明确提示用户：

1. 打开这个页面：
   `https://mcp.dingtalk.com/#/detail?mcpId=9555&detailType=marketMcpDetail`
2. 点击右侧 **「获取 MCP Server 配置」** 按钮
3. 复制新的 MCP Server 地址
4. 用新的地址替换 `mcporter` 里已经注册的 `dingtalk-ai-table` 地址
5. 替换完成后，再重新执行：

```bash
mcporter list dingtalk-ai-table --schema
```

只有当返回的 tools 已经变成新版 schema，例如出现：
- `list_bases`
- `get_base`
- `get_tables`
- `get_fields`
- `query_records`
- `create_records`
- `update_records`
- `delete_records`

才允许继续真正的 AI 表格操作。

### 通过检查后的处理

一旦确认当前 MCP Server 地址返回的是新版 schema，就把结果写入本地检查标记。后续只要 `mcporter` 里的 `dingtalk-ai-table` 地址没变，就不要再重复做这一步守门检查。

### 用户提示文案（可直接复用）

```text
当前 mcporter 里注册的 dingtalk-ai-table 还是旧版 MCP schema，暂时不能按新版技能操作。
请打开 https://mcp.dingtalk.com/#/detail?mcpId=9555&detailType=marketMcpDetail ，点击右侧“获取 MCP Server 配置”按钮，复制新的 MCP Server 地址，并替换 mcporter 里已注册的 dingtalk-ai-table 地址。替换后重新检查 schema，确认出现 list_bases / get_base / create_records 等新版 tools 后，再继续操作 AI 表格。
```

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

在钉钉 MCP 广场 https://mcp.dingtalk.com/#/detail?mcpId=9555&detailType=marketMcpDetail 获取新版钉钉 AI 表格 MCP 的 `Streamable HTTP URL`。

方式一：直接配置到 mcporter

```bash
mcporter config add dingtalk-ai-table --url "<Streamable_HTTP_URL>"
```

方式二：使用环境变量

```bash
export DINGTALK_MCP_URL="<Streamable_HTTP_URL>"
```

> 这个 URL 带访问令牌，等同密码，不要泄露。

### 工作区沙箱

脚本读取本地文件时，会优先使用 `OPENCLAW_WORKSPACE` 作为允许根目录：

```bash
export OPENCLAW_WORKSPACE="$HOME/.openclaw/workspace"
```

未设置时默认使用当前工作目录。

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
python3 scripts/bulk_add_fields.py <baseId> <tableId> fields.json
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
python3 scripts/import_records.py <baseId> <tableId> data.csv
python3 scripts/import_records.py <baseId> <tableId> data.json 50
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
