#!/bin/bash
# 示例 1：列出所有可访问的 Base

MCP_URL="${DINGTALK_MCP_URL}"

if [ -z "$MCP_URL" ]; then
  echo "❌ 错误：未设置 DINGTALK_MCP_URL"
  exit 1
fi

echo "📋 列出所有 Base..."
mcporter call "$MCP_URL" .list_bases limit=10
