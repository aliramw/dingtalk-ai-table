# 钉钉 AI 表格 MCP 常见错误与排查

> 以下内容针对 2026-03-10 后的新 schema：`baseId / tableId / fieldId / recordId`。

## 1. 常见错误模式

### 参数体系写错

**现象**
- 还在用旧参数：`dentryUuid` / `sheetIdOrName`
- 接口直接报参数缺失 / 无效请求

**原因**
- MCP server 已升级到新 schema，但本地脚本或技能文档没跟上

**解决**
- Base 级：用 `baseId`
- Table 级：用 `tableId`
- Field 级：用 `fieldId`
- Record 级：用 `recordId` / `recordIds`

---

### 参数名大小写或命名风格错误

**现象**
- 参数看起来传了，但服务端像没收到
- 报字段缺失 / 资源不存在

**原因**
- `mcporter call key=value` 方式下参数名必须是 **camelCase**

**正确示例**
```bash
mcporter call server.get_base baseId='base_xxx'
mcporter call server.update_table baseId='base_xxx' tableId='tbl_xxx' newTableName='新表名'
```

**错误示例**
```bash
mcporter call server.get_base base-id='base_xxx'
mcporter call server.update_table table-id='tbl_xxx'
```

**建议**
- 简单参数用 `key=value`
- 复杂对象、数组一律用 `--args '<json>'`

---

### 查询记录时单选 / 多选过滤无结果

**现象**
- 明明记录存在，但 `query_records.filters` 查不出来

**原因**
- 对 `singleSelect / multipleSelect` 字段做过滤时，必须传 **option id**，不能传 option name

**解决**
1. 先 `get_fields` 读取字段完整配置
2. 找到 options 里的 id
3. 在 filters 里传 id

---

### create_records / update_records 写入失败

**常见原因**
- `cells` 的 key 用了字段名，不是 `fieldId`
- `url` 字段直接传字符串
- `richText` 字段直接传字符串
- `group` 字段写成 `openConversationId`
- 单次超过 100 条

**解决**
- 先用 `get_tables` 拿字段目录，必要时 `get_fields`
- `url` 用：
  ```json
  {"text":"官网","link":"https://..."}
  ```
- `richText` 用：
  ```json
  {"markdown":"**加粗**"}
  ```
- `group` 用：
  ```json
  [{"cid":"74577067501"}]
  ```

---

### update_field 更新单选 / 多选后历史数据异常

**现象**
- 更新选项后，已有单元格显示错乱或丢值

**原因**
- 更新 `options` 时没有传完整列表
- 已有 option 没保留原 `id`

**解决**
- 先 `get_fields` 取完整配置
- 更新时传完整 options 列表
- 已有项尽量保留原 `id`
- 新增项可不传 `id`

---

### delete_table 失败：cannot delete the last sheet

**原因**
- 该表是 Base 中最后一张表

**解决**
- 先新建一张表，再删旧表
- 或者如果目标就是整个 Base 都不要了，改用 `delete_base`

---

### create_fields / create_table 某些字段类型失败

**已知边界**
- `formula` 当前实例可能 `not supported yet`
- 关联字段可能因为下游主键约束失败，即使已传 `linkedSheetId`

**建议**
- 复杂字段拆开单独创建
- 先建立基础结构，再逐项补复杂字段
- 遇到关联字段失败，优先检查被关联表的主字段 / 主键约束

---

## 2. 推荐排查顺序

### 先确认 ID 链路

1. `list_bases` / `search_bases` → 拿 `baseId`
2. `get_base` → 拿 `tableId`
3. `get_tables` → 拿 `fieldId`
4. `query_records` / 结果对象 → 拿 `recordId`

别跳步，别猜 ID。

### 再确认 payload 结构

- 新增 / 更新记录：看 `cells`
- 新增字段：看 `fields[]`
- 更新字段：看 `config`
- 查询过滤：看 `filters`

### 最后确认批量上限

- 字段批量：15
- table / field 详情批量：10
- record 批量：100

---

## 3. 调试命令模板

### 看 Base

```bash
mcporter call '<mcp-url>' .list_bases limit=10 --output json
mcporter call '<mcp-url>' .get_base baseId='base_xxx' --output json
```

### 看 Table / Field

```bash
mcporter call '<mcp-url>' .get_tables \
  --args '{"baseId":"base_xxx","tableIds":["tbl_xxx"]}' \
  --output json

mcporter call '<mcp-url>' .get_fields \
  --args '{"baseId":"base_xxx","tableId":"tbl_xxx","fieldIds":["fld_xxx"]}' \
  --output json
```

### 查记录

```bash
mcporter call '<mcp-url>' .query_records \
  --args '{"baseId":"base_xxx","tableId":"tbl_xxx","limit":10}' \
  --output json
```

### 新增记录

```bash
mcporter call '<mcp-url>' .create_records \
  --args '{"baseId":"base_xxx","tableId":"tbl_xxx","records":[{"cells":{"fld_name":"张三"}}]}' \
  --output json
```

---

## 4. 一句话原则

- **别再用旧 schema。**
- **别猜 ID。**
- **复杂参数一律 `--args`。**
- **先读结构，再写数据。**
