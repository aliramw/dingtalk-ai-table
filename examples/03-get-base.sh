#!/bin/bash
# 示例 3：查看 Base 内的表

MCP_URL="${DINGTALK_MCP_URL}"
BASE_ID="${1}"

if [ -z "$MCP_URL" ]; then
  echo "❌ 错误：未设置 DINGTALK_MCP_URL"
  exit 1
fi

if [ -z "$BASE_ID" ]; then
  echo "❌ 用法：$0 <baseId>"
  exit 1
fi

echo "📊 查看 Base 内的表..."
mcporter call "$MCP_URL" .get_base baseId="$BASE_ID"
