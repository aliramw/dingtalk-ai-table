# dingtalk-ai-table（官方维护）

钉钉 AI 表格技能，已适配 **2026-03-10 发布的新版 MCP tools**。

ClawHub 技能地址：https://clawhub.ai/aliramw/dingtalk-ai-table

## 🚀 快速开始

**5 分钟内完成第一个操作：**

```bash
# 1. 列出所有表格
mcporter call "$DINGTALK_MCP_URL" .list_bases limit=5

# 2. 创建新表格
mcporter call "$DINGTALK_MCP_URL" .create_base baseName='我的项目'

# 3. 查询记录
mcporter call "$DINGTALK_MCP_URL" .query_records \
  --args '{"baseId":"base_xxx","tableId":"tbl_xxx","limit":10}'
```

👉 详见 `GETTING_STARTED.md`

## 📚 文档导航

| 文档 | 用途 |
|------|------|
| `GETTING_STARTED.md` | 新手入门（推荐从这里开始） |
| `SKILL.md` | 技能完整说明 |
| `references/api-reference.md` | API 详细参考 |
| `references/error-codes.md` | 常见错误排查 |
| `examples/` | 7 个实战示例脚本 |

## 🛠️ 工具与脚本

- `scripts/check-schema.sh` - 自动检查 MCP schema 版本
- `scripts/bulk_add_fields.py` - 批量新增字段
- `scripts/import_records.py` - 批量导入记录

## ✅ 依赖与环境

- 必需二进制：`mcporter >= 0.8.1`、`python3`
- 必需环境变量：`DINGTALK_MCP_URL`
- 推荐环境变量：`OPENCLAW_WORKSPACE`（脚本文件沙箱）

## 🧪 测试

```bash
python3 tests/test_security.py
```

**测试覆盖**：25 项安全与功能测试，100% 通过

## 📋 核心特性

- ✅ 新版 MCP schema：`baseId / tableId / fieldId / recordId`
- ✅ 覆盖 20 个 MCP tools
- ✅ 批量操作支持（字段、记录）
- ✅ 完整的安全沙箱
- ✅ 自动 schema 版本检查
- ✅ 7 个实战示例
- ✅ 详细的错误排查指南

## ⚠️ 注意

旧版脚本依赖 `dentryUuid / sheetIdOrName`，已废弃。必须使用新版 ID 体系。
