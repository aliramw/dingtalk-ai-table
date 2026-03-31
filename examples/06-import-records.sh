#!/bin/bash
# 示例 6：批量导入记录

MCP_URL="${DINGTALK_MCP_URL}"
BASE_ID="${1}"
TABLE_ID="${2}"
CSV_FILE="${3}"

if [ -z "$MCP_URL" ]; then
  echo "❌ 错误：未设置 DINGTALK_MCP_URL"
  exit 1
fi

if [ -z "$BASE_ID" ] || [ -z "$TABLE_ID" ] || [ -z "$CSV_FILE" ]; then
  echo "❌ 用法：$0 <baseId> <tableId> <csv_file>"
  exit 1
fi

echo "📥 批量导入记录..."
python3 scripts/import_records.py "$BASE_ID" "$TABLE_ID" "$CSV_FILE"
