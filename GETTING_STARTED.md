# 快速开始指南

## 前置检查清单

- [ ] 安装 `mcporter >= 0.8.1`：`npm install -g mcporter`
- [ ] 获取钉钉 MCP Server URL（从 https://mcp.dingtalk.com/#/detail?mcpId=9555 获取）
- [ ] 设置环境变量：`export DINGTALK_MCP_URL='<your-url>'`
- [ ] 可选：设置 `OPENCLAW_WORKSPACE` 用于脚本文件沙箱

## 工作流程

### 第 1 步：找到你的表格

```bash
# 列出所有可访问的 Base
mcporter call "$DINGTALK_MCP_URL" .list_bases limit=10

# 或按名称搜索
mcporter call "$DINGTALK_MCP_URL" .search_bases query='销售'
```

从结果中记下 `baseId`。

### 第 2 步：查看表格结构

```bash
# 查看 Base 内的所有表
mcporter call "$DINGTALK_MCP_URL" .get_base baseId='base_xxx'

# 查看表的字段
mcporter call "$DINGTALK_MCP_URL" .get_tables \
  --args '{"baseId":"base_xxx","tableIds":["tbl_xxx"]}'
```

从结果中记下 `tableId` 和 `fieldId`。

### 第 3 步：操作数据

**查询记录**
```bash
mcporter call "$DINGTALK_MCP_URL" .query_records \
  --args '{"baseId":"base_xxx","tableId":"tbl_xxx","limit":100}'
```

**新增记录**
```bash
mcporter call "$DINGTALK_MCP_URL" .create_records \
  --args '{
    "baseId":"base_xxx",
    "tableId":"tbl_xxx",
    "records":[
      {"cells":{"fld_name":"张三","fld_age":25}},
      {"cells":{"fld_name":"李四","fld_age":30}}
    ]
  }'
```

**更新记录**
```bash
mcporter call "$DINGTALK_MCP_URL" .update_records \
  --args '{
    "baseId":"base_xxx",
    "tableId":"tbl_xxx",
    "records":[
      {"recordId":"rec_xxx","cells":{"fld_name":"王五"}}
    ]
  }'
```

**删除记录**
```bash
mcporter call "$DINGTALK_MCP_URL" .delete_records \
  --args '{
    "baseId":"base_xxx",
    "tableId":"tbl_xxx",
    "recordIds":["rec_xxx","rec_yyy"]
  }'
```

### 第 4 步：批量操作（可选）

**批量新增字段**

创建 `fields.json`：
```json
[
  {"fieldName":"任务名","type":"text"},
  {"fieldName":"优先级","type":"singleSelect","config":{"options":[{"name":"高"},{"name":"中"},{"name":"低"}]}}
]
```

运行：
```bash
python3 scripts/bulk_add_fields.py base_xxx tbl_xxx fields.json
```

**批量导入记录**

创建 `data.csv`：
```csv
fld_name,fld_age,fld_status
张三,25,进行中
李四,30,已完成
```

运行：
```bash
python3 scripts/import_records.py base_xxx tbl_xxx data.csv
```

## 常见问题

### Q: 参数怎么传？
**A:** 简单参数用 `key=value`，复杂对象/数组用 `--args '<json>'`。

### Q: 为什么查不到记录？
**A:** 检查 `fieldId` 是否正确。用 `get_tables` 或 `get_fields` 确认。

### Q: 单选/多选字段怎么过滤？
**A:** 必须用 option **id**，不是 name。先 `get_fields` 查完整配置。

### Q: 批量操作有上限吗？
**A:** 有。字段最多 15 个，记录最多 100 条。

## 下一步

- 📖 详细 API 参考：`references/api-reference.md`
- 🐛 错误排查：`references/error-codes.md`
- 🔒 安全规则：`SKILL.md` 的"安全规则"部分
