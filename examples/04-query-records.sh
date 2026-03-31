#!/bin/bash
# 示例 4：查询记录

MCP_URL="${DINGTALK_MCP_URL}"
BASE_ID="${1}"
TABLE_ID="${2}"

if [ -z "$MCP_URL" ]; then
  echo "❌ 错误：未设置 DINGTALK_MCP_URL"
  exit 1
fi

if [ -z "$BASE_ID" ] || [ -z "$TABLE_ID" ]; then
  echo "❌ 用法：$0 <baseId> <tableId>"
  exit 1
fi

echo "🔍 查询记录..."
mcporter call "$MCP_URL" .query_records \
  --args "{\"baseId\":\"$BASE_ID\",\"tableId\":\"$TABLE_ID\",\"limit\":10}"
