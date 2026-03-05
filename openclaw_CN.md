# OpenClaw 用户使用手册

> 版本：2026.2.26  
> 适用对象：OpenClaw 初学者和进阶用户  
> 用途：完整的安装、配置、使用指南与常见问题速查

---

## 目录

1. [简介](#1-简介)
2. [安装与配置](#2-安装与配置)
3. [快速入门](#3-快速入门)
4. [通道配置](#4-通道配置)
5. [代理系统](#5-代理系统)
6. [工具使用](#6-工具使用)
7. [技能系统](#7-技能系统)
8. [安全配置](#8-安全配置)
9. [高级功能](#9-高级功能)
10. [故障排除](#10-故障排除)
11. [最佳实践](#11-最佳实践)
12. [附录](#12-附录)

---

## 1. 简介

### 1.1 OpenClaw 是什么？

**OpenClaw** 是一个跨平台的消息网关，用于连接 AI 代理与各种消息服务。它提供了一个统一的接口来处理来自不同渠道的消息，并将其路由到 AI 代理进行处理。

**核心特性**：
- ✅ 支持多平台消息服务（WhatsApp、Telegram、Discord、飞书、钉钉、iMessage 等）
- ✅ AI 代理集成（内置智能代理系统）
- ✅ 消息会话管理
- ✅ 安全访问控制
- ✅ 可扩展的工具和技能系统
- ✅ 本地部署，保护隐私

### 1.2 使用场景

| 场景 | 功能描述 |
|------|---------|
| **智能客服** | 自动回复 WhatsApp/Telegram 消息 |
| **办公自动化** | 飞书/钉钉机器人，处理工作流 |
| **社交媒体管理** | 自动发布、回复评论 |
| **个人助理** | 定时任务、日程管理、提醒服务 |
| **数据监控** | 监控股价、网站变化、API 状态 |
| **内容创作** | 自动生成文章、多平台分发 |

---

## 2. 安装与配置

### 2.1 系统要求

| 配置项 | 最低要求 | 推荐配置 |
|--------|---------|---------|
| **操作系统** | macOS / Linux / Windows (WSL) | macOS 或 Ubuntu |
| **内存** | 4GB | 8GB+ |
| **Node.js** | v22+ | v24 LTS |
| **磁盘空间** | 1GB | 5GB+ |
| **网络** | 能访问互联网 | 稳定的网络连接 |

### 2.2 安装步骤

#### 方式一：使用安装脚本（推荐）

**Windows (PowerShell)**：
```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

**macOS / Linux (Bash)**：
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

#### 方式二：使用 npm
```bash
npm install -g openclaw@latest
```

#### 方式三：使用 pnpm（推荐用于源码构建）
```bash
pnpm add -g openclaw@latest
```

#### 验证安装
```bash
openclaw --version
openclaw doctor
```

### 2.3 初始化配置

运行初始化向导：
```bash
openclaw onboard --install-daemon
```

此命令将引导您完成：
- ✅ 模型/认证配置（推荐 OAuth）
- ✅ 网关设置
- ✅ 通道配置（WhatsApp/Telegram/飞书/钉钉等）
- ✅ 配对接入默认设置（安全 DM）
- ✅ 工作区引导 + 技能可选
- ✅ 后台服务安装（可选）

### 2.4 启动网关服务

如果在向导中安装了服务，网关应该已经在运行：
```bash
openclaw gateway status
```

手动启动网关：
```bash
openclaw gateway --port 18789 --verbose
```

### 2.5 验证安装

```bash
# 查看状态
openclaw status

# 健康检查
openclaw health

# 安全审计
openclaw security audit --deep
```

---

## 3. 快速入门

### 3.1 第一次运行

**打开控制面板**（最快聊天方式，无需通道设置）：
```bash
openclaw dashboard
```

或者直接访问：http://127.0.0.1:18789/

### 3.2 配置通道

**使用 CLI 登录 WhatsApp**：
```bash
openclaw channels login
```

然后扫描 WhatsApp → 设置 → 已连接的设备 中显示的二维码。

### 3.3 测试连接

发送测试消息：
```bash
openclaw message send --target +15555550123 --message "Hello from OpenClaw"
```

### 3.4 基本命令速查

```bash
# 查看状态
openclaw status

# 查看健康状况
openclaw health

# 查看当前配置
openclaw config get

# 查看日志
openclaw logs --follow

# 重启网关
openclaw gateway restart

# 停止网关
openclaw gateway stop
```

---

## 4. 通道配置

### 4.1 WhatsApp 配置

#### 基本配置
```json
{
  "channels": {
    "whatsapp": {
      "dmPolicy": "pairing",
      "allowFrom": ["+15555550123"],
      "groups": {
        "*": { "requireMention": true }
      },
      "sendReadReceipts": true
    }
  }
}
```

#### 多账号配置
```json
{
  "channels": {
    "whatsapp": {
      "accounts": {
        "default": {},
        "personal": {},
        "business": {}
      }
    }
  }
}
```

#### 配对接入管理

未知发件人会收到配对代码。

查看待处理请求：
```bash
openclaw pairing list whatsapp
```

批准配对：
```bash
openclaw pairing approve whatsapp <code>
```

### 4.2 Telegram 配置

#### 基本配置
```json
{
  "channels": {
    "telegram": {
      "botToken": "your-telegram-bot-token",
      "dmPolicy": "pairing",
      "allowFrom": ["tg:123456789"],
      "groups": {
        "*": { "requireMention": true }
      }
    }
  }
}
```

#### 高级配置
```json
{
  "channels": {
    "telegram": {
      "customCommands": [
        { "command": "backup", "description": "Git backup" },
        { "command": "generate", "description": "Create an image" }
      ],
      "historyLimit": 50,
      "streamMode": "partial"
    }
  }
}
```

### 4.3 Discord 配置

#### 基本配置
```json
{
  "channels": {
    "discord": {
      "token": "your-discord-bot-token",
      "dm": {
        "enabled": true,
        "policy": "pairing",
        "allowFrom": ["1234567890"]
      },
      "guilds": {
        "123456789012345678": {
          "slug": "friends-of-openclaw",
          "requireMention": false,
          "channels": {
            "general": { "allow": true },
            "help": {
              "allow": true,
              "requireMention": true
            }
          }
        }
      }
    }
  }
}
```

### 4.4 钉钉配置

#### 基本配置
```json
{
  "channels": {
    "dingtalk": {
      "enabled": true,
      "clientId": "dingxxxxxxxxxx",
      "clientSecret": "your-app-secret",
      "robotCode": "dingxxxxxxxxxx",
      "corpId": "dingxxxxxxxxxx",
      "agentId": "123456789",
      "dmPolicy": "open",
      "groupPolicy": "open",
      "messageType": "markdown"
    }
  }
}
```

### 4.5 飞书配置

#### 基本配置
```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_xxxxxxxx",
      "appSecret": "your-app-secret",
      "dmPolicy": "pairing",
      "groups": {
        "*": { "requireMention": true }
      }
    }
  }
}
```

### 4.6 iMessage 配置（仅 macOS）

```json
{
  "channels": {
    "imessage": {
      "enabled": true,
      "dmPolicy": "pairing",
      "allowFrom": ["+15555550123", "user@example.com"]
    }
  }
}
```

---

## 5. 代理系统

### 5.1 默认代理配置

```json
{
  "agents": {
    "defaults": {
      "workspace": "~/.openclaw/workspace",
      "model": {
        "primary": "anthropic/claude-opus-4-5",
        "fallbacks": ["openai/gpt-4o"]
      },
      "sandbox": {
        "mode": "non-main",
        "scope": "session",
        "workspaceAccess": "none"
      }
    }
  }
}
```

### 5.2 多代理配置

```json
{
  "agents": {
    "list": [
      {
        "id": "personal",
        "workspace": "~/.openclaw/workspace-personal",
        "sandbox": { "mode": "off" }
      },
      {
        "id": "work",
        "workspace": "~/.openclaw/workspace-work",
        "sandbox": {
          "mode": "all",
          "scope": "agent",
          "workspaceAccess": "ro"
        },
        "tools": {
          "allow": ["read", "sessions_list", "sessions_history"],
          "deny": ["write", "exec", "browser"]
        }
      }
    ]
  },
  "bindings": [
    {
      "agentId": "personal",
      "match": {
        "channel": "whatsapp",
        "accountId": "personal"
      }
    },
    {
      "agentId": "work",
      "match": {
        "channel": "whatsapp",
        "accountId": "business"
      }
    }
  ]
}
```

### 5.3 代理身份配置

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "identity": {
          "name": "Samantha",
          "theme": "helpful sloth",
          "emoji": "🦥",
          "avatar": "avatars/samantha.png"
        }
      }
    ]
  }
}
```

---

## 6. 工具使用

### 6.1 核心工具介绍

#### 1. exec - 执行命令

在工作区执行命令：
```bash
openclaw exec --command "ls -la"
```

**参数说明**：
- `command` (必需) - 要执行的命令
- `yieldMs` - 自动后台运行超时时间
- `background` - 立即后台运行
- `timeout` - 超时时间（秒）
- `host` - 运行主机（sandbox | gateway | node）

#### 2. web_search - 网络搜索

搜索网络：
```bash
openclaw web_search --query "OpenClaw 架构"
```

需要配置 Brave API 密钥：
```bash
openclaw configure --section web
```

#### 3. web_fetch - 获取网页内容

获取网页内容：
```bash
openclaw web_fetch --url "https://docs.openclaw.ai/"
```

#### 4. browser - 浏览器控制

启动浏览器：
```bash
openclaw browser start --profile chrome
```

截图：
```bash
openclaw browser screenshot --target https://example.com
```

获取页面快照：
```bash
openclaw browser snapshot --target https://example.com
```

#### 5. message - 发送消息

发送消息：
```bash
openclaw message send --target +15555550123 --message "Hello"
```

### 6.2 工具策略配置

```json
{
  "tools": {
    "profile": "coding",
    "allow": ["read", "write", "exec", "web_search"],
    "deny": ["gateway", "process"],
    "byProvider": {
      "openai/gpt-4o": {
        "allow": ["read", "write", "web_search"]
      }
    }
  }
}
```

---

## 7. 技能系统

### 7.1 技能结构

技能存储在 `SKILL.md` 文件中，包含 YAML 前置元数据：

```yaml
---
name: skill-name
description: Skill description
metadata:
  openclaw:
    requires:
      bins: ["binary"]
      env: ["ENV_VAR"]
      config: ["browser.enabled"]
    primaryEnv: "ENV_VAR"
    os: ["darwin", "linux", "win32"]
    emoji: "🦞"
    homepage: "https://example.com"
---
# 技能说明和指令
```

### 7.2 技能位置

| 类型 | 路径 | 优先级 |
|------|------|--------|
| **工作区技能** | `<workspace>/skills` | 最高 |
| **管理/本地技能** | `~/.openclaw/skills` | 中等 |
| **捆绑技能** | 随安装包分发 | 最低 |

### 7.3 安装第三方技能

从 ClawHub 安装技能：
```bash
clawhub install skill-name

# 更新所有技能
clawhub update --all
```

### 7.4 技能配置

```json
{
  "skills": {
    "entries": {
      "skill-name": {
        "enabled": true,
        "apiKey": "API_KEY_HERE",
        "env": {
          "ENV_VAR": "VALUE"
        },
        "config": {
          "custom_option": "value"
        }
      }
    }
  }
}
```

---

## 8. 安全配置

### 8.1 网关安全

```json
{
  "gateway": {
    "bind": "loopback",
    "port": 18789,
    "auth": {
      "mode": "token",
      "token": "your-long-random-token"
    }
  }
}
```

### 8.2 访问控制策略

```json
{
  "channels": {
    "whatsapp": {
      "dmPolicy": "pairing",
      "allowFrom": ["+15555550123"],
      "groups": {
        "*": { "requireMention": true }
      }
    }
  }
}
```

### 8.3 安全审计

定期运行安全审计：
```bash
# 基本审计
openclaw security audit

# 深度审计
openclaw security audit --deep

# 自动修复
openclaw security audit --fix
```

### 8.4 沙箱配置

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main",
        "scope": "session",
        "workspaceAccess": "none"
      }
    }
  }
}
```

---

## 9. 高级功能

### 9.1 定时任务（Cron）

添加定时任务：
```bash
openclaw cron add --job '{
  "name": "daily-report",
  "schedule": {
    "kind": "every",
    "everyMs": 86400000
  },
  "payload": {
    "kind": "systemEvent",
    "text": "Daily report"
  },
  "sessionTarget": "main"
}'
```

### 9.2 节点管理

```bash
# 查看节点状态
openclaw nodes status

# 描述节点
openclaw nodes describe --node node-id

# 在节点上运行命令
openclaw nodes run --node node-id -- echo "Hello"
```

### 9.3 会话管理

```bash
# 列出会话
openclaw sessions_list

# 查看会话历史
openclaw sessions_history --sessionKey session-key

# 向会话发送消息
openclaw sessions_send --sessionKey session-key --message "Hello"
```

### 9.4 子代理

启动子代理：
```bash
openclaw sessions_spawn --task "Perform analysis" --label "analysis-task"
```

---

## 10. 故障排除

### 10.1 常见问题

#### 问题 1：网关无法启动

**检查配置文件格式**：
```bash
openclaw doctor
```

#### 问题 2：通道连接失败

- 验证凭据是否正确
- 检查网络连接
- 查看日志：
```bash
openclaw logs --follow
```

#### 问题 3：工具调用失败

- 检查工具策略配置
- 确认工具是否被允许
- 查看安全审计结果

#### 问题 4：消息无法发送

- 验证目标地址格式
- 检查通道配置
- 确认授权状态

### 10.2 诊断命令

```bash
# 全面状态报告
openclaw status --all

# 健康检查
openclaw health

# 安全审计
openclaw security audit --deep

# 日志查看
openclaw logs --follow

# 配置验证
openclaw doctor
```

### 10.3 重启服务

```bash
# 停止网关
openclaw gateway stop

# 重启网关
openclaw gateway restart

# 检查服务状态
openclaw gateway status
```

---

## 11. 最佳实践

### 11.1 安全最佳实践

- ✅ 保持直接消息锁定（配对/允许列表）
- ✅ 在群组中优先使用提及门控
- ✅ 将敏感工具限制为可信代理
- ✅ 定期运行安全审计
- ✅ 使用强 token 和密码

### 11.2 性能最佳实践

- ✅ 合理配置沙箱设置
- ✅ 设置适当的会话历史限制
- ✅ 使用缓存和重试策略
- ✅ 监控资源使用情况
- ✅ 定期清理日志和临时文件

### 11.3 维护最佳实践

- ✅ 定期备份配置文件
- ✅ 使用版本控制系统管理配置
- ✅ 设置适当的日志保留策略
- ✅ 定期更新到最新版本
- ✅ 监控系统资源使用

---

## 12. 附录

### 12.1 完整的安全基线配置

```json
{
  "gateway": {
    "mode": "local",
    "bind": "loopback",
    "port": 18789,
    "auth": {
      "mode": "token",
      "token": "your-long-random-token"
    }
  },
  "channels": {
    "whatsapp": {
      "dmPolicy": "pairing",
      "groups": {
        "*": { "requireMention": true }
      }
    }
  },
  "agents": {
    "defaults": {
      "workspace": "~/.openclaw/workspace",
      "sandbox": {
        "mode": "non-main",
        "scope": "session",
        "workspaceAccess": "none"
      }
    }
  }
}
```

### 12.2 命令速查表

| 命令 | 功能描述 |
|------|---------|
| `openclaw status` | 查看系统状态 |
| `openclaw health` | 健康检查 |
| `openclaw logs --follow` | 查看实时日志 |
| `openclaw config get` | 获取配置 |
| `openclaw security audit` | 安全审计 |
| `openclaw gateway status` | 网关状态 |
| `openclaw pairing list <channel>` | 查看配对请求 |
| `openclaw pairing approve <channel> <code>` | 批准配对 |
| `openclaw sessions_list` | 列出会话 |
| `openclaw sessions_history` | 查看会话历史 |
| `openclaw cron add` | 添加定时任务 |
| `openclaw browser start` | 启动浏览器 |
| `openclaw web_search` | 网络搜索 |
| `openclaw exec` | 执行命令 |

### 12.3 配置文件路径

| 配置文件 | 路径 |
|---------|------|
| **主配置文件** | `~/.openclaw/openclaw.json` |
| **工作区** | `~/.openclaw/workspace` |
| **技能目录** | `~/.openclaw/skills` |
| **日志文件** | `~/.openclaw/logs/` |
| **会话数据** | `~/.openclaw/agents/<agent-id>/sessions/` |

### 12.4 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `OPENCLAW_HOME` | OpenClaw 主目录 | `~/.openclaw` |
| `OPENCLAW_GATEWAY_PORT` | 网关端口 | `18789` |
| `OPENCLAW_WORKSPACE` | 工作区路径 | `~/.openclaw/workspace` |
| `OPENCLAW_LOG_LEVEL` | 日志级别 | `info` |

### 12.5 相关资源

- 📚 **官方文档**：https://docs.openclaw.ai/
- 💬 **社区论坛**：https://community.openclaw.ai/
- 🐛 **问题反馈**：https://github.com/openclaw/openclaw/issues
- 🎓 **教程集合**：https://docs.openclaw.ai/tutorials/
- 🔧 **技能市场**：https://clawhub.ai/

---

## 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| 2026.2.26 | 2026-02-28 | 初始版本，基于 OpenClaw 官方文档整理 |

---

**最后更新**：2026-02-28  
**维护者**：OpenClaw 中文社区  
**许可证**：CC BY-SA 4.0
