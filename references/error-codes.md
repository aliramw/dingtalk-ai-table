# 错误码说明

## 常见错误码

### 5000001 - fail to get document info
**原因**: 常见于 `dentryUuid` 参数不正确、文档不存在，或在 `mcporter call key:value` 方式下误用了 kebab-case 参数名（如 `dentry-uuid`）导致参数未被正确识别。  
**解决**: 
- 确认使用 API 返回的正确 dentryUuid（如 create_base_app 返回的 `info.uuid` 或根节点 `rootDentryUuid`），不要自行构造，也不要假设它必须是 UUID v4
- 检查文档权限
- 在 `key:value` 调用方式下，使用 camelCase 参数名：`dentryUuid`、`sheetIdOrName`、`recordIds`
- 对复杂参数优先使用 `--args` JSON，避免参数名被误写

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
**A**: 先检查参数命名，再检查 ID：
- 如果你用的是 `mcporter call key:value`，参数名必须是 camelCase：`dentryUuid`，不要写成 `dentry-uuid`
- 推荐直接用 `--args '{"dentryUuid":"xxx"}'`
- 然后再确认是否使用了正确的 ID：
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
