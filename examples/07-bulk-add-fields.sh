#!/bin/bash
# 示例 7：批量新增字段

MCP_URL="${DINGTALK_MCP_URL}"
BASE_ID="${1}"
TABLE_ID="${2}"
FIELDS_FILE="${3}"

if [ -z "$MCP_URL" ]; then
  echo "❌ 错误：未设置 DINGTALK_MCP_URL"
  exit 1
fi

if [ -z "$BASE_ID" ] || [ -z "$TABLE_ID" ] || [ -z "$FIELDS_FILE" ]; then
  echo "❌ 用法：$0 <baseId> <tableId> <fields_file>"
  exit 1
fi

echo "🆕 批量新增字段..."
python3 scripts/bulk_add_fields.py "$BASE_ID" "$TABLE_ID" "$FIELDS_FILE"
