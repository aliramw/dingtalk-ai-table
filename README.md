# dingtalk-ai-table

钉钉 AI 表格技能，已适配 **2026-03-10 发布的新版 MCP tools**。

## 依赖与环境声明

- 必需二进制：`mcporter`、`python3`
- 必需环境变量：`DINGTALK_MCP_URL`
- 推荐环境变量：`OPENCLAW_WORKSPACE`（脚本本地文件沙箱根目录）


## 本次升级重点

- 全面切换到新 schema：`baseId / tableId / fieldId / recordId`
- 覆盖 19 个 MCP tools
- 重写批量字段脚本
- 重写批量导入脚本
- 重写测试，当前 `21 / 21` 通过

## 目录

- `SKILL.md`：技能说明
- `references/api-reference.md`：新版 API 参考
- `references/error-codes.md`：错误排查
- `scripts/bulk_add_fields.py`：批量新增字段
- `scripts/import_records.py`：批量导入记录
- `tests/test_security.py`：安全与构造测试

## 测试

```bash
cd /Users/marila/Skills/dingtalk-ai-table
python3 tests/test_security.py
```

## 注意

旧版脚本依赖 `dentryUuid / sheetIdOrName`，现在已经废弃。后续调用必须使用新版 ID 体系。
