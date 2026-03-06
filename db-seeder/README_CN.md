# Database Seeder Skill

一个用于使用逼真的假数据填充数据库的综合 Claude Code 技能。

## 安装

### 选项 1：解压归档文件

```bash
# 解压技能归档文件
tar -xzf db-seeder.tar.gz -C .claude/skills/

# 安装依赖
pip install faker pyyaml sqlalchemy psycopg2-binary

# uv 安装依赖
uv pip install faker pyyaml sqlalchemy psycopg2-binary
```

### 选项 2：手动复制

将 `db-seeder` 目录复制到项目的 `.claude/skills/` 文件夹中。

## 快速开始

### 1. 检测数据库配置

```bash
python .claude/skills/db-seeder/scripts/detect_db_config.py
```

### 2. 生成测试夹具

```bash
# 用于 Elios 项目
python .claude/skills/db-seeder/scripts/generate_fixtures.py \
  --template elios-interview \
  --output fixtures/elios_data.json \
  --pretty

# 用于自定义模型
python .claude/skills/db-seeder/scripts/generate_fixtures.py \
  --models User:100,Post:500 \
  --output fixtures/test_data.json
```

### 3. 填充数据库

```bash
python .claude/skills/db-seeder/scripts/seed_database.py \
  --fixtures fixtures/elios_data.json \
  --db postgresql \
  --connection "postgresql://user:pass@localhost/mydb"
```

## 功能特性

- **自动检测**：自动从环境变量、配置文件和项目结构中检测数据库配置
- **多数据库支持**：PostgreSQL、MySQL、SQLite、MongoDB 支持
- **ORM 集成**：适用于 SQLAlchemy、Django ORM、Prisma
- **Faker 集成**：使用 100+ 数据类型生成逼真的假数据
- **灵活的方法**：JSON 夹具、Python 工厂或 YAML 配置
- **生产就绪**：批量操作、错误处理、进度报告

## 技能内容

### 脚本

- `seed_database.py` - 主填充协调器
- `detect_db_config.py` - 自动检测数据库配置
- `generate_fixtures.py` - 使用 Faker 生成 JSON 夹具

### 参考资料

- `database-configs.md` - 数据库连接模式和故障排除
- `faker-recipes.md` - 常见 Faker 模式和示例
- `orm-patterns.md` - ORM 特定的填充模式

### 资源

- `seed-config-template.yaml` - 配置模板
- `fixture-template.json` - JSON 夹具模板

## 使用场景

1. **开发环境设置** - 使用示例数据填充本地数据库
2. **测试** - 为 CI/CD 创建一致的测试夹具
3. **预发布环境** - 使用逼真的数据填充预发布环境
4. **演示** - 为演示生成演示数据

## 示例：填充 Elios 面试系统

```bash
# 生成 Elios 专用夹具
python .claude/skills/db-seeder/scripts/generate_fixtures.py \
  --template elios-interview \
  --output fixtures/elios_dev.json \
  --pretty

# 填充数据库
python .claude/skills/db-seeder/scripts/seed_database.py \
  --fixtures fixtures/elios_dev.json \
  --db postgresql \
  --connection "postgresql://postgres:password@localhost/elios_dev"

# 验证
psql -d elios_dev -c "SELECT COUNT(*) FROM candidates;"
psql -d elios_dev -c "SELECT COUNT(*) FROM questions;"
psql -d elios_dev -c "SELECT COUNT(*) FROM interview_sessions;"
```

## 文档

请参阅 `SKILL.md` 获取完整文档，包括：

- 详细工作流程
- 高级用法
- 最佳实践
- 故障排除指南
- 集成示例

## 依赖

### 必需的

- Python 3.8+
- Faker (`pip install faker`)

### 可选的（基于数据库）

- SQLAlchemy + psycopg2-binary (PostgreSQL)
- SQLAlchemy + pymysql (MySQL)
- pymongo (MongoDB)
- PyYAML (YAML 配置支持)

## 快速参考

### 常用命令

```bash
# 自动检测数据库
python scripts/detect_db_config.py

# 生成夹具
python scripts/generate_fixtures.py --template elios-interview --output fixtures.json

# 填充数据库
python scripts/seed_database.py --fixtures fixtures.json --db postgresql --connection "DB_URL"

# 自定义区域设置
python scripts/generate_fixtures.py --template blog --locale ja_JP --output japanese_data.json
```

### 支持的数据库

| 数据库     | 连接字符串示例                        |
| ---------- | ------------------------------------- |
| PostgreSQL | `postgresql://user:pass@host:5432/db` |
| MySQL      | `mysql://user:pass@host:3306/db`      |
| SQLite     | `sqlite:///path/to/db.db`             |
| MongoDB    | `mongodb://user:pass@host:27017/db`   |

## 支持

如有问题或疑问：

1. 查看 `SKILL.md` 获取详细文档
2. 查看 `references/` 获取特定主题
3. 查看 `assets/` 获取模板

## 许可证

为 Elios AI 面试服务项目创建。
