# 钉钉 AI 表格 MCP API 参考（2026-03-10 新版）

> 以 MCP server 实际 schema 为准，不再使用旧版 `dentryUuid / sheetIdOrName / fieldIdOrName` 体系。
> 新版核心 ID 体系：`baseId` / `tableId` / `fieldId` / `recordId`。

推荐使用 `mcporter 0.8.1` 及以上版本。

输出模式兼容说明：
- `mcporter 0.8.1+` 可直接调用
- 更低版本需要显式加 `--output text`
- AI 表格 MCP 无论使用哪种模式，返回体本身都是标准 JSON；差异主要在 `mcporter` 的输出处理方式

## 1. 能力总览

当前 MCP tools 共 20 个：

### Base 管理
- `list_bases`：列出我可访问的 Base
- `search_bases`：按名称搜索 Base
- `get_base`：获取 Base 目录级信息（tables / dashboards 摘要）
- `create_base`：创建 Base
- `update_base`：更新 Base 名称 / 描述
- `delete_base`：删除 Base
- `search_templates`：搜索可用于创建 Base 的模板

### Table 管理
- `get_tables`：批量获取指定 tables 的结构摘要
- `create_table`：创建 table，并可初始化最多 15 个字段
- `update_table`：重命名 table
- `delete_table`：删除 table

### Field 管理
- `get_fields`：获取字段详细配置
- `create_fields`：批量新增字段
- `update_field`：更新字段名称或配置
- `delete_field`：删除字段

### Record 管理
- `query_records`：按条件 / 关键词 / ID 查询记录
- `create_records`：批量新增记录
- `update_records`：批量更新记录
- `delete_records`：批量删除记录

### 附件管理
- `prepare_attachment_upload`：为 attachment 字段申请 OSS 直传地址

---

## 2. 推荐工作流

### 2.1 查找 Base

```bash
mcporter call '<mcp-url>' .list_bases limit=10
mcporter call '<mcp-url>' .search_bases query='销售'
```

先拿到 `baseId`，后续所有操作都从它出发。

### 2.2 进入 Base 看目录

```bash
mcporter call '<mcp-url>' .get_base baseId='base_xxx'
```

从返回结果里先拿 `tableId`；如果只是想知道有哪些表，这一步就够了。

### 2.3 看表结构

```bash
mcporter call '<mcp-url>' .get_tables \
  --args '{"baseId":"base_xxx","tableIds":["tbl_xxx"]}'
```

这一步会返回：
- `tableId`
- `tableName`
- `fields`（仅摘要）
- `views`

### 2.4 看字段完整配置

```bash
mcporter call '<mcp-url>' .get_fields \
  --args '{"baseId":"base_xxx","tableId":"tbl_xxx","fieldIds":["fld_xxx"]}'
```

当字段是单选、多选、日期、进度、关联字段时，**要用这一步读完整 config**，不要只看 `get_tables` 摘要。

### 2.5 查记录

```bash
mcporter call '<mcp-url>' .query_records \
  --args '{"baseId":"base_xxx","tableId":"tbl_xxx","limit":100}'
```

按 recordId 精准取：

```bash
mcporter call '<mcp-url>' .query_records \
  --args '{"baseId":"base_xxx","tableId":"tbl_xxx","recordIds":["rec_xxx"]}'
```

---

## 3. 关键工具详解

## 3.1 list_bases

列出当前用户可访问的 Base。

参数：
- `limit`：每页数量，默认 10，最大 30
- `cursor`：分页游标

## 3.2 search_bases

按名称搜索 Base。

参数：
- `query`：关键词，必填
- `cursor`：分页游标

## 3.3 get_base

获取 Base 目录信息。

参数：
- `baseId`：必填

适用场景：
- 先拿 table 列表
- 后续配合 `get_tables` / `get_fields`

## 3.4 create_base

创建新的 AI 表格 Base。

参数：
- `baseName`：必填
- `templateId`：可选，可通过 `search_templates` 获取

示例：

```bash
mcporter call '<mcp-url>' .create_base baseName='销售日报'
```

## 3.5 update_base

更新 Base 名称或备注。

参数：
- `baseId`
- `newBaseName`
- `description`（可选）

## 3.6 delete_base

删除整个 Base，高风险、不可逆。

参数：
- `baseId`
- `reason`（建议填写）

## 3.7 search_templates

搜索模板，用于 `create_base.templateId`。

参数：
- `query`
- `limit`
- `cursor`

## 3.8 get_tables

批量获取表级信息。

参数：
- `baseId`
- `tableIds`：数组，单次最多 10 个

适用场景：
- 从 `get_base` 拿到 tableId 后展开字段目录
- 获取 fieldId / view 信息

## 3.9 create_table

创建 table，可附带初始字段。

参数：
- `baseId`
- `tableName`
- `fields`：至少 1 个，最多 15 个

字段对象结构：

```json
{
  "fieldName": "优先级",
  "type": "singleSelect",
  "config": {
    "options": [
      {"name": "高"},
      {"name": "中"},
      {"name": "低"}
    ]
  }
}
```

## 3.10 update_table

重命名 table。

参数：
- `baseId`
- `tableId`
- `newTableName`

## 3.11 delete_table

删除 table。若它是 Base 里最后一张表，会失败。

参数：
- `baseId`
- `tableId`
- `reason`（建议填写）

## 3.12 get_fields

获取字段完整配置。

参数：
- `baseId`
- `tableId`
- `fieldIds`：单次最多 10 个

关键用途：
- 读取单选 / 多选字段 option id
- 读取日期 / 进度 / 评分等 config
- 读取关联字段 linkedSheetId

## 3.13 create_fields

批量新增字段。

参数：
- `baseId`
- `tableId`
- `fields`：1~15 个

适用场景：
- 建表后补字段
- 添加复杂字段（关联 / 进度 / 评分等）

## 3.14 update_field

更新字段名称或 config；**不能改字段类型**。

参数：
- `baseId`
- `tableId`
- `fieldId`
- `newFieldName`（可选）
- `config`（可选）

注意：
- `newFieldName` 与 `config` 至少传一个
- 更新单选 / 多选时，`options` 要传**完整列表**，不是追加
- 已有选项应尽量保留原 `id`

## 3.15 delete_field

删除字段，不可逆。

参数：
- `baseId`
- `tableId`
- `fieldId`

限制：
- 不能删主字段
- 不能删最后一个字段

## 3.16 query_records

查询记录，支持：
- `recordIds` 精准查
- `filters` 条件查
- `keyword` 全文查
- `sort` 排序
- `cursor` 分页
- `fieldIds` 限定返回字段

参数：
- `baseId`
- `tableId`
- `recordIds`（可选）
- `filters`（可选）
- `keyword`（可选）
- `sort`（可选）
- `fieldIds`（可选）
- `limit`（默认 100，最大 100）
- `cursor`（可选）

### filters 说明

结构：

```json
{
  "operator": "and",
  "operands": [
    {
      "operator": "eq",
      "operands": ["fld_status", "进行中"]
    }
  ]
}
```

注意：
- `singleSelect / multipleSelect` 做过滤时，**必须传 option id，不是 option name**
- option id 需先通过 `get_fields` 获取

## 3.17 create_records

批量新增记录。

参数：
- `baseId`
- `tableId`
- `records`：单次最多 100 条

记录结构：

```json
{
  "cells": {
    "fld_text": "文本",
    "fld_num": 123,
    "fld_select": "进行中"
  }
}
```

注意：
- key 是 **fieldId**，不是字段名
- `singleSelect / multipleSelect` 写入时可以传 option name
- `url` 必须传对象：`{"text":"官网","link":"https://..."}`
- `richText` 必须传对象：`{"markdown":"**加粗**"}`
- `group` 字段 key 是 `cid`，不是 `openConversationId`
- `attachment` 支持三种写法：
  - `[{"fileToken":"ft_xxx"}]`：通过 `prepare_attachment_upload` 上传后填入（推荐）
  - `[{"url":"https://..."}]`：外链 URL，服务端异步转存，best-effort
  - `[{"filename":"a.xlsx","size":92250,"type":"xls"|"image","resourceId":"<id>","resourceUrl":"<resourceUrl>"}]`：从 `query_records` 读出的原始对象原样回传，用于保留已有附件；`type` 为文件类别枚举（`"xls"`、`"image"` 等）；追加新附件时与 `fileToken` 对象合并为数组

## 3.18 update_records

批量更新记录。

参数：
- `baseId`
- `tableId`
- `records`

结构：

```json
{
  "recordId": "rec_xxx",
  "cells": {
    "fld_status": "已完成"
  }
}
```

注意：
- 只传要更新的字段即可
- 未传字段保持原值
- `attachment` 字段传入后**整体覆盖**（三种写法均支持：`fileToken`、`url`、完整对象数组）；需保留已有附件时，先从 `query_records` 读出原始对象再原样合并回传

## 3.19 delete_records

批量删除记录。

参数：
- `baseId`
- `tableId`
- `recordIds`：最多 100 个

## 3.20 prepare_attachment_upload

为 attachment 字段申请带容量校验的 OSS 直传地址。**仅用于 attachment 字段写入链路，不是通用文件上传入口。**

参数：
- `baseId`：必填
- `fileName`：必填，必须包含扩展名（如 `report.xlsx`、`photo.png`）
- `size`：必填，文件字节数，必须大于 0
- `mimeType`：可选，如 `application/pdf`、`image/png`；不传时服务端按扩展名推断

返回字段（关键）：
- `uploadUrl`：PUT 上传地址
- `fileToken`：写入 attachment 字段用的 token

完整上传流程：

```bash
# 1. 申请上传地址
mcporter call dingtalk-ai-table prepare_attachment_upload \
  --args '{"baseId":"base_xxx","fileName":"report.pdf","size":102400,"mimeType":"application/pdf"}'

# 2. PUT 文件到 uploadUrl（Content-Type 必须与 mimeType 完全一致）
curl -X PUT "<uploadUrl>" \
  -H "Content-Type: application/pdf" \
  --data-binary @report.pdf

# 3. 写入记录
mcporter call dingtalk-ai-table create_records \
  --args '{"baseId":"base_xxx","tableId":"tbl_xxx","records":[{"cells":{"fld_attach":[{"fileToken":"ft_xxx"}]}}]}'
```

注意：
- PUT 请求必须携带 `Content-Type` header，值必须与 `mimeType` 完全一致
- `prepare_attachment_upload` 不接收文件二进制，实际上传在 MCP 外由客户端完成
- 此工具不适用于导入类任务的文件上传

---

## 4. 字段类型速查

支持的主要字段类型：

- `text`
- `number`
- `singleSelect`
- `multipleSelect`
- `date`
- `currency`
- `user`
- `department`
- `group`
- `progress`
- `rating`
- `checkbox`
- `attachment`
- `url`
- `richText`
- `telephone`
- `email`
- `idCard`
- `barcode`
- `geolocation`
- `primaryDoc`
- `formula`
- `unidirectionalLink`
- `bidirectionalLink`
- `creator`
- `lastModifier`
- `createdTime`
- `lastModifiedTime`

---

## 5. 已知边界

- `create_table` / `create_fields` 单次最多 **15 个字段**
- `get_tables` / `get_fields` 单次最多 **10 个对象**
- `create_records` / `update_records` / `delete_records` / `query_records.recordIds` 单次最多 **100 条**
- `formula` 字段当前服务实例可能返回 `not supported yet`
- 关联字段即使传了 `linkedSheetId`，也可能因底层主键约束失败
- 删除最后一张表会失败：`cannot delete the last sheet`

---

## 6. 参数命名规则

通过 `mcporter call ... key=value` 传参时，参数名必须用 **camelCase**：

- `baseId`
- `tableId`
- `fieldId`
- `recordIds`
- `newTableName`

不要写成 kebab-case，例如：
- `base-id`
- `table-id`
- `field-id`

CLI 帮助里会显示 `cliName`，但你在 `mcporter call` 命令里最稳的方式仍然是：
- 简单参数 → `key=value`
- 复杂参数 → `--args '<json>'`

复杂 payload 一律优先 `--args`。
