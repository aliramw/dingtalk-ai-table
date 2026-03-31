# 示例数据文件

## fields.json - 批量新增字段示例

```json
[
  {
    "fieldName": "任务名",
    "type": "text"
  },
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
  },
  {
    "fieldName": "截止日期",
    "type": "date"
  },
  {
    "fieldName": "负责人",
    "type": "user",
    "config": {
      "multiple": false
    }
  },
  {
    "fieldName": "进度",
    "type": "progress"
  }
]
```

## data.csv - 批量导入记录示例

```csv
fld_name,fld_age,fld_status,fld_salary
张三,25,进行中,15000
李四,30,已完成,18000
王五,28,进行中,16000
```

## data.json - JSON 格式导入示例

```json
[
  {
    "cells": {
      "fld_name": "张三",
      "fld_age": 25,
      "fld_status": "进行中",
      "fld_salary": 15000
    }
  },
  {
    "cells": {
      "fld_name": "李四",
      "fld_age": 30,
      "fld_status": "已完成",
      "fld_salary": 18000
    }
  }
]
```

## 字段类型参考

| 类型 | 说明 | 示例 |
|------|------|------|
| `text` | 文本 | `"张三"` |
| `number` | 数字 | `25` |
| `singleSelect` | 单选 | `{"name":"高"}` |
| `multipleSelect` | 多选 | `[{"name":"高"},{"name":"紧急"}]` |
| `date` | 日期 | `"2026-03-31"` |
| `user` | 用户 | `{"id":"user_xxx"}` |
| `checkbox` | 复选框 | `true` |
| `attachment` | 附件 | `[{"fileId":"file_xxx"}]` |
| `url` | 链接 | `{"text":"官网","link":"https://..."}` |
| `richText` | 富文本 | `{"markdown":"**加粗**"}` |
