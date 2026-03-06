# 钉钉 AI 表格 Skill

OpenClaw 技能，用于操作钉钉 AI 表格（多维表）。通过 MCP 协议连接钉钉官方 API，实现表格创建、数据管理、自动化 workflows。

## 功能特性

- ✅ 创建/删除 AI 表格
- ✅ 管理数据表（重命名、删除）
- ✅ 字段操作（添加/删除，支持 7 种字段类型）
- ✅ 记录增删改查（支持批量操作）
- ✅ 批量导入导出（CSV/JSON）

## 前置要求

### 1. 安装 mcporter CLI

本技能依赖 `mcporter` 工具，用于连接钉钉 MCP 服务器。

```bash
# 使用 npm 安装
npm install -g mcporter

# 或使用 bun 安装
bun install -g mcporter
```

验证安装：
```bash
mcporter --version
```

### 2. 获取钉钉 MCP Server URL

1. 访问钉钉 MCP 广场 - AI 表格页面：
   https://mcp.dingtalk.com/#/detail?mcpId=1060&detailType=marketMcpDetail
2. 在页面**右侧**点击“获取 MCP Server 配置”按钮，然后找到 `Streamable HTTP URL`
3. 点击复制该 URL（完整地址，以 http 开头）

### 3. 配置 MCP 服务器

```bash
mcporter config add dingtalk-ai-table --url "<你的 Streamable HTTP URL>"
```

将 `<你的 Streamable HTTP URL>` 替换为步骤 2 中复制的实际 URL。

## 快速开始

### 安装技能

```bash
# 方式 1：使用 clawhub（推荐）
clawhub install dingtalk-ai-table

# 方式 2：直接对 OpenClaw 说
"安装 dingtalk-ai-table 这个 skill"
```

### 验证配置

```bash
mcporter call dingtalk-ai-table get_root_node_of_my_document --output json
```

成功时会返回包含 `rootDentryUuid` 的 JSON，例如：
```json
{
  "rootDentryUuid": "dtcn_example_root_id_12345678"
}
```

> `rootDentryUuid` / `dentryUuid` 以 API 实际返回为准。它可能不是 UUID v4，不要自行套用 UUID v4 格式校验。

### 创建第一个表格

跟你的 Claw 对话让他创建一个AI表格，看看能否创建成功。

## 故障排查

### 认证失败 / 无法连接服务器

1. 检查 `mcporter` 是否正确安装：`mcporter --version`
2. 确认服务器 URL 配置正确：`mcporter config list`
3. 确认 URL 是完整的（以 `http` 或 `https` 开头）
4. 检查网络连接，确保能访问钉钉服务

### 某些表格操作失败

先检查参数命名。

如果你使用的是 `mcporter call ... key:value` 这种调用方式，参数名必须使用 **camelCase**，例如：
- `dentryUuid`
- `sheetIdOrName`
- `recordIds`

不要写成 kebab-case，例如 `dentry-uuid`、`sheet-id-or-name`、`record-ids`。这类写法可能导致接口返回：
- `errorCode: 5000001`
- `errorMsg: fail to get document info`

更稳妥的方式是统一使用 `--args` 传 JSON。

我们仍在不断增强钉钉 AI 表格的 MCP 能力，每天都会有更新，很可能今天无法实现的操作，明天就能让你的 OpenClaw 实现。

也可以加入我们的讨论群，让我们第一时间了解当前最紧迫的功能需求。
[加入钉钉讨论群](https://qr.dingtalk.com/action/joingroup?code=v1,k1,6T6sMqtYnX3JrR03p4y5EeTBHP4T+GLZbmGs3/dDTs29AN2XwsPGIg==&_dt_no_comment=1&origin=11?)

## 相关链接

- 📊 [钉钉 AI 表格官网](https://table.dingtalk.com)
- 🔌 [钉钉 MCP 广场 - AI 表格](https://mcp.dingtalk.com/#/detail?mcpId=1060&detailType=marketMcpDetail)
- 📦 [ClawHub 技能页面](https://clawhub.ai/aliramw/dingtalk-ai-table)
- 🐛 [问题反馈 (GitHub Issues)](https://github.com/aliramw/dingtalk-ai-table/issues)
- 📖 [源代码仓库](https://github.com/aliramw/dingtalk-ai-table)
- 💬 [加入钉钉讨论群](https://qr.dingtalk.com/action/joingroup?code=v1,k1,6T6sMqtYnX3JrR03p4y5EeTBHP4T+GLZbmGs3/dDTs29AN2XwsPGIg==&_dt_no_comment=1&origin=11?)

## 技术支持

如有问题，请在钉钉 AI 表格官方交流群提问，或通过 GitHub Issues 反馈。
