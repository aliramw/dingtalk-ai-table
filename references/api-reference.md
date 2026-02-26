# 钉钉 AI 表格 API 参考

## 工具列表

### 文档管理

| 工具名 | 描述 | 必需参数 |
|--------|------|----------|
| `get_root_node_of_my_document` | 获取我的文档根节点 | 无 |
| `create_base_app` | 创建 AI 表格 | `filename`, `target` |
| `search_accessible_ai_tables` | 搜索有权限的表格 | 无 |

### 数据表管理

| 工具名 | 描述 | 必需参数 |
|--------|------|----------|
| `list_base_tables` | 列出所有数据表 | `dentryUuid` |
| `add_base_table` | 新增数据表 | `dentryUuid`, `name` |
| `update_base_tables` | 更新表名 | `dentryUuid`, `oldSheetIdOrName`, `newName` |
| `delete_base_table` | 删除数据表 | `dentryUuid`, `sheetIdOrName` |

### 字段管理

| 工具名 | 描述 | 必需参数 |
|--------|------|----------|
| `list_base_field` | 获取字段列表 | `dentryUuid`, `sheetIdOrName` |
| `add_base_field` | 添加字段 | `dentryUuid`, `sheetIdOrName` |
| `delete_base_field` | 删除字段 | `dentryUuid`, `sheetIdOrName`, `fieldIdOrName` |

### 记录管理

| 工具名 | 描述 | 必需参数 |
|--------|------|----------|
| `search_base_record` | 查询记录 | `dentryUuid`, `sheetIdOrName` |
| `add_base_record` | 添加记录 | `dentryUuid`, `sheetIdOrName`, `records` |
| `update_records` | 更新记录 | `dentryUuid`, `sheetIdOrName`, `records` |
| `delete_base_record` | 删除记录 | `dentryUuid`, `sheetIdOrName`, `recordIds` |

## 参数详解

### create_base_app

```json
{
  "filename": "表格名称",
  "target": "根节点 dentryUuid（来自 get_root_node_of_my_document）"
}
```

返回示例：
```json
{
  "body": {
    "info": {
      "name": "表格名.able",
      "docKey": "xxx",
      "uuid": "表格 UUID（用作 dentryUuid）",
      "dentryId": "xxx",
      "dentryKey": "xxx",
      "spaceId": "xxx",
      "dentryType": "file",
      "docId": 123456
    }
  }
}
```

### add_base_table

```json
{
  "dentryUuid": "表格 UUID",
  "name": "数据表名称",
  "fields": [
    {"name": "字段 1", "type": "text"},
    {"name": "字段 2", "type": "number"}
  ]
}
```

### add_base_field

```json
{
  "dentryUuid": "表格 UUID",
  "sheetIdOrName": "数据表 ID 或名称",
  "addField": {
    "name": "新字段名",
    "type": "text|number|singleSelect|multipleSelect|date|user|attachment"
  }
}
```

### add_base_record

```json
{
  "dentryUuid": "表格 UUID",
  "sheetIdOrName": "数据表 ID 或名称",
  "records": [
    {
      "fields": {
        "字段 1": "值 1",
        "字段 2": 100,
        "单选字段": "选项名"
      }
    }
  ]
}
```

### update_records

```json
{
  "dentryUuid": "表格 UUID",
  "sheetIdOrName": "数据表 ID 或名称",
  "records": [
    {
      "id": "记录 ID",
      "fields": {
        "字段名": "新值"
      }
    }
  ]
}
```

## 字段类型详情

### text
文本类型，支持单行和多行文本。

### number
数字类型，可配置格式：
- `INT`: 整数
- `DECIMAL`: 小数

### singleSelect
单选类型，首次使用时自动创建选项。

### multipleSelect
多选类型，值为数组。

### date
日期类型，格式 `YYYY-MM-DD`，内部存储为 Unix 时间戳（毫秒）。

### user
人员类型，值为钉钉用户对象。

### attachment
附件类型，支持上传文件。
