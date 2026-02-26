# 错误码说明

## 常见错误码

### 5000001 - fail to get document info
**原因**: dentryUuid 参数不正确或文档不存在  
**解决**: 
- 确认使用正确的 UUID（来自 create_base_app 返回的 `info.uuid`）
- 检查文档权限

### 500 - 通用服务器错误
**原因**: 参数格式错误或服务器内部问题  
**解决**:
- 检查 JSON 参数格式
- 确认必填字段完整

### 600 - 参数验证错误
**原因**: 参数值为空或格式不匹配  
**解决**:
- 检查 `addField` 等对象参数不为 null
- 使用 `--args` 传递复杂 JSON

### InvalidRequest.ResourceNotFound
**原因**: 指定的资源（表、字段、记录）不存在  
**解决**:
- 使用 `list_base_tables` 确认表名
- 使用 `list_base_field` 确认字段名
- 检查表名是否为中文（默认"数据表"）

## 调试技巧

### 1. 启用详细输出
```bash
mcporter call dingtalk-ai-table <tool> --args '<json>' --output json
```

### 2. 验证连接
```bash
mcporter call dingtalk-ai-table get_root_node_of_my_document --output json
mcporter call dingtalk-ai-table search_accessible_ai_tables --output json
```

### 3. 检查配置
```bash
mcporter config list --output json
```

### 4. 重新认证
```bash
mcporter auth dingtalk-ai-table --reset
```

## 常见问题

### Q: list_base_tables 返回 "fail to get document info"
**A**: 尝试使用不同的 ID：
- `uuid` 字段（推荐）
- `dentryId` 字段
- `docId` 字段

### Q: add_base_field 返回 "may not be null"
**A**: 使用 `--args` 传递 JSON：
```bash
mcporter call dingtalk-ai-table add_base_field \
  --args '{"dentryUuid":"xxx","sheetIdOrName":"表名","addField":{"name":"字段","type":"text"}}'
```

### Q: 记录添加成功但字段值为空
**A**: 检查字段名是否完全匹配（包括大小写和空格）

### Q: 单选字段如何设置值
**A**: 直接传选项名称，系统自动创建：
```json
{"fields": {"分类": "电子产品"}}
```
