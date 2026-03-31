#!/bin/bash
# 示例 2：创建新 Base

MCP_URL="${DINGTALK_MCP_URL}"

if [ -z "$MCP_URL" ]; then
  echo "❌ 错误：未设置 DINGTALK_MCP_URL"
  exit 1
fi

BASE_NAME="${1:-我的项目}"

echo "🆕 创建 Base: $BASE_NAME"
mcporter call "$MCP_URL" .create_base baseName="$BASE_NAME"
