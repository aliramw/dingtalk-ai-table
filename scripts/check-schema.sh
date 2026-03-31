#!/bin/bash
# 自动检查 dingtalk-ai-table MCP schema 版本
# 一次性检查策略：同一 MCP Server 地址只检查一次

set -e

MCP_URL="${DINGTALK_MCP_URL:-}"
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
CACHE_DIR="$WORKSPACE/.cache/dingtalk-ai-table"

if [ -z "$MCP_URL" ]; then
  echo "❌ 错误：未设置 DINGTALK_MCP_URL"
  exit 1
fi

# 生成 URL hash 作为检查标记
URL_HASH=$(echo -n "$MCP_URL" | md5sum | cut -d' ' -f1)
CACHE_FILE="$CACHE_DIR/schema-check-$URL_HASH.json"

# 如果已检查过且结果为新版，直接跳过
if [ -f "$CACHE_FILE" ]; then
  RESULT=$(cat "$CACHE_FILE" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
  if [ "$RESULT" = "new_schema" ]; then
    echo "✅ 已确认新版 schema（缓存）"
    exit 0
  fi
fi

# 执行检查
echo "🔍 检查 MCP schema 版本..."
SCHEMA=$(mcporter list dingtalk-ai-table --schema 2>/dev/null || echo "")

if echo "$SCHEMA" | grep -q "list_bases\|get_base\|create_records"; then
  echo "✅ 确认新版 schema"
  mkdir -p "$CACHE_DIR"
  echo "{\"status\":\"new_schema\",\"checked_at\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" > "$CACHE_FILE"
  exit 0
else
  echo "❌ 检测到旧版 schema"
  echo ""
  echo "请按以下步骤更新："
  echo "1. 打开：https://mcp.dingtalk.com/#/detail?mcpId=9555&detailType=marketMcpDetail"
  echo "2. 点击右侧「获取 MCP Server 配置」"
  echo "3. 复制新的 MCP Server 地址"
  echo "4. 运行：mcporter config update dingtalk-ai-table --url '<新地址>'"
  echo "5. 重新运行此脚本"
  exit 1
fi
