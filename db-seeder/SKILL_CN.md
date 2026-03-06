---
name: db-seeder
description: 此技能应用于在开发、测试或预发布环境中使用逼真的虚拟数据填充数据库。支持 PostgreSQL、MySQL、SQLite、MongoDB，基于 ORM 的种子数据生成（SQLAlchemy、Django、Prisma）和 Faker 库生成逼真的测试数据。当用户需要使用示例数据填充数据库、创建测试夹具或为开发/预发布环境设置逼真数据时使用此技能。
---

# Database Seeder Skill（数据库种子数据生成技能）

使用 ORM 模式和 Faker 库为任何数据库填充逼真的虚拟数据。此技能提供脚本、参考和模板，用于高效地为开发、测试和预发布环境的数据库填充测试数据。

## 何时使用此技能

适用于以下场景：
- 为本地开发数据库设置示例数据
- 为自动化测试创建测试夹具
- 为预发布环境填充逼真的类生产数据
- 为演示或用户入职生成演示数据
- 需要快速创建大量逼真的测试数据
- 在数据库系统之间迁移时需要填充新数据库

## 支持的数据库

- **PostgreSQL** - 关系型数据库（生产环境默认）
- **MySQL / MariaDB** - 关系型数据库
- **SQLite** - 基于文件的数据库（测试、开发）
- **MongoDB** - NoSQL 文档数据库
- **任何 ORM 支持的数据库** - 通过 SQLAlchemy、Django ORM、Prisma 等

此技能会自动从以下位置检测数据库配置：
- 环境变量（`DATABASE_URL`、`DB_TYPE` 等）
- 配置文件（`.env`、`settings.py`、`config.yaml`）
- Alembic 迁移文件（`alembic.ini`）
- Docker Compose 文件

## 技能工作流程

### 步骤 1：检测数据库配置

在种子数据生成之前，自动检测数据库配置：

```bash
python scripts/detect_db_config.py
```

检测脚本将：
1. 检查环境变量（`DATABASE_URL`、`DB_TYPE` 等）
2. 搜索配置文件（`.env`、`settings.py`、`alembic.ini`）
3. 分析项目结构（SQLite 文件、Docker Compose）
4. 输出连接详情和立即可用的种子数据生成命令

### 步骤 1.5：检查数据库模式（可选但推荐）

**新增**：自动检查数据库模式以生成工厂函数和夹具：

```bash
# 检查模式并打印摘要
python scripts/inspect_schema.py \
  --db postgresql \
  --connection "postgresql://user:pass@localhost/mydb"

# 为所有表生成工厂函数
python scripts/inspect_schema.py \
  --db postgresql \
  --connection "postgresql://user:pass@localhost/mydb" \
  --generate-factories

# 生成 JSON 夹具模板
python scripts/inspect_schema.py \
  --db postgresql \
  --connection "postgresql://user:pass@localhost/mydb" \
  --generate-fixtures \
  --fixture-count 5

# 两者都生成
python scripts/inspect_schema.py \
  --db postgresql \
  --connection "postgresql://user:pass@localhost/mydb" \
  --generate-factories \
  --generate-fixtures
```

**功能说明：**
- ✅ **检测所有表/集合** 在你的数据库中
- ✅ **分析列类型**（VARCHAR、INTEGER、DATE 等）
- ✅ **识别外键关系**
- ✅ **为每个字段生成合适的 Faker 方法**
- ✅ **创建立即可用的工厂函数**（`generated_factories.py`）
- ✅ **创建 JSON 夹具模板**（`generated_fixtures.json`）

**适用于任何模式** - 没有硬编码的假设！

**手动配置：**
如果自动检测失败，手动指定数据库详细信息：

```bash
# PostgreSQL
python scripts/seed_database.py \
  --db postgresql \
  --connection "postgresql://user:pass@localhost:5432/mydb" \
  --count 100

# SQLite
python scripts/seed_database.py \
  --db sqlite \
  --connection "sqlite:///./test.db" \
  --count 50

# MongoDB
python scripts/seed_database.py \
  --db mongodb \
  --connection "mongodb://admin:pass@localhost:27017/mydb" \
  --count 100
```

**配置文件参考：**
有关数据库连接模式和配置示例的详细信息，请参考：
`references/database-configs.md`

### 步骤 2：选择种子数据生成方法

提供三种主要方法：

#### 方法 A：优先生成 JSON 夹具（推荐用于可重用性）

生成可版本控制和共享的可重用 JSON 夹具：

```bash
# 使用预定义模板生成
python scripts/generate_fixtures.py \
  --template elios-interview \
  --output fixtures/elios_data.json \
  --pretty

# 生成特定模型
python scripts/generate_fixtures.py \
  --models User:100,Post:500,Candidate:50 \
  --output fixtures/test_data.json \
  --pretty

# 从夹具种子数据库
python scripts/seed_database.py \
  --fixtures fixtures/test_data.json \
  --db postgresql \
  --connection "postgresql://user:pass@localhost/db"
```

**优势：**
- 夹具可以进行版本控制
- 可在不同环境间重用
- 测试数据一致
- 易于与团队共享

#### 方法 B：使用自定义工厂直接种子数据库

创建 Python 工厂函数并直接种子：

```python
# 创建种子脚本：scripts/seed_elios.py

from seed_database import DatabaseSeeder, create_seeder

def candidate_factory(fake, index):
    return {
        'full_name': fake.name(),
        'email': fake.email(),
        'years_of_experience': fake.random_int(min=0, max=15),
        'skills': fake.random_elements(
            ['Python', 'JavaScript', 'SQL', 'React'],
            length=fake.random_int(min=2, max=6),
            unique=True
        ),
        'status': fake.random_element(['pending', 'interviewed', 'hired']),
    }

# 运行种子生成
seeder = create_seeder('postgresql', 'postgresql://user:pass@localhost/db')
seeder.seed_model(Candidate, count=50, factory_func=candidate_factory)
```

**优势：**
- 完全控制数据生成
- 可以使用复杂的业务逻辑
- 直接插入数据库（更快）

#### 方法 C：基于配置的种子数据生成

使用 YAML 配置文件进行声明式种子生成：

```bash
# 复制模板
cp assets/seed-config-template.yaml seed-config.yaml

# 编辑 seed-config.yaml 定义模型和工厂

# 运行种子生成
python scripts/seed_database.py --config seed-config.yaml
```

**优势：**
- 声明式配置
- 无需编码
- 易于修改数量和设置

### 步骤 3：执行种子数据生成

根据选择的方法：

**对于夹具：**
```bash
python scripts/seed_database.py \
  --fixtures fixtures/test_data.json \
  --db postgresql \
  --connection "postgresql://user:pass@localhost/db"
```

**对于自定义工厂：**
```bash
python scripts/seed_elios.py
```

**对于配置：**
```bash
python scripts/seed_database.py --config seed-config.yaml
```

### 步骤 4：验证种子数据

种子生成完成后，验证数据：

```bash
# 对于 PostgreSQL/MySQL
psql -d mydb -c "SELECT COUNT(*) FROM users;"
psql -d mydb -c "SELECT COUNT(*) FROM candidates;"

# 对于 SQLite
sqlite3 mydb.db "SELECT COUNT(*) FROM users;"

# 对于 MongoDB
mongosh mydb --eval "db.users.countDocuments()"
```

## 捆绑资源

### 脚本（`scripts/`）

#### `seed_database.py`
主种子编排器，集成 Faker。

**功能：**
- 从连接字符串自动检测数据库类型
- 支持基于 SQLAlchemy 的数据库（PostgreSQL、MySQL、SQLite）
- 支持使用 PyMongo 的 MongoDB
- 批量插入以提高性能
- 进度报告
- 错误处理和回滚

**用法：**
```bash
# 从夹具种子
python scripts/seed_database.py \
  --fixtures data.json \
  --db postgresql \
  --connection "postgresql://user:pass@localhost/db"

# 从配置种子
python scripts/seed_database.py --config seed-config.yaml

# 使用自定义语言环境生成国际数据
python scripts/seed_database.py \
  --fixtures data.json \
  --db sqlite \
  --connection "sqlite:///test.db" \
  --locale fr_FR
```

#### `detect_db_config.py`
自动从项目中检测数据库配置。

**功能：**
- 扫描环境变量
- 解析配置文件（`.env`、`settings.py`、`config.yaml`）
- 检测 Alembic 迁移配置
- 查找 SQLite 数据库文件
- 输出带密码掩码的连接字符串

**用法：**
```bash
# 自动检测
python scripts/detect_db_config.py

# 指定配置文件
python scripts/detect_db_config.py --config-path src/infrastructure/config/settings.py

# 指定 .env 文件
python scripts/detect_db_config.py --env-file .env.local

# 指定项目根目录
python scripts/detect_db_config.py --project-root /path/to/project
```

#### `generate_fixtures.py`
使用逼真的虚拟数据生成 JSON 夹具。

**功能：**
- 预定义模板（Elios 面试系统、博客、电子商务）
- 自定义模型生成
- 可配置的记录数量
- 多种 Faker 语言环境
- 美化 JSON 输出

**用法：**
```bash
# 从模板生成
python scripts/generate_fixtures.py \
  --template elios-interview \
  --output fixtures.json \
  --pretty

# 生成特定模型
python scripts/generate_fixtures.py \
  --models User:100,Post:500 \
  --output test_data.json

# 使用不同的语言环境（越南语）
python scripts/generate_fixtures.py \
  --template elios-interview \
  --locale vi_VN \
  --output vietnamese_data.json \
  --pretty

# 日语语言环境
python scripts/generate_fixtures.py \
  --template blog \
  --locale ja_JP \
  --output japanese_blog_data.json
```

**可用模板：**
- `elios-interview` - 候选人、问题、面试会话（Elios 专用）
- `blog` - 用户、文章
- 更多模板可以添加到脚本中

**支持的语言环境：**
- `en_US` - 英语（美国）- 默认
- `vi_VN` - 越南语（越南）- **包含越南大学、学位、专业**
- `ja_JP` - 日语（日本）
- `fr_FR` - 法语（法国）
- `en_GB` - 英语（英国）
- 以及 Faker 支持的 50 多种语言环境

#### `inspect_schema.py` ⭐ 新增
**自动检查数据库模式并生成种子辅助工具。**

**功能：**
- 自动发现所有表/集合
- 分析列类型（VARCHAR、INTEGER、DATE、JSONB 等）
- 识别外键关系
- 为每个字段类型生成合适的 Faker 方法
- 创建立即可用的工厂函数
- 创建带有示例数据的 JSON 夹具模板
- **适用于任何数据库模式** - 没有硬编码的假设！

**用法：**
```bash
# 打印模式摘要
python scripts/inspect_schema.py \
  --db postgresql \
  --connection "postgresql://user:pass@localhost/mydb"

# 为所有表生成工厂函数
python scripts/inspect_schema.py \
  --db postgresql \
  --connection "postgresql://user:pass@localhost/mydb" \
  --generate-factories
# 输出：generated_factories.py

# 生成 JSON 夹具模板
python scripts/inspect_schema.py \
  --db postgresql \
  --connection "postgresql://user:pass@localhost/mydb" \
  --generate-fixtures \
  --fixture-count 5
# 输出：generated_fixtures.json

# 两者都生成
python scripts/inspect_schema.py \
  --db sqlite \
  --connection "sqlite:///./test.db" \
  --generate-factories \
  --generate-fixtures

# 将模式信息保存为 JSON
python scripts/inspect_schema.py \
  --db postgresql \
  --connection "postgresql://user:pass@localhost/mydb" \
  --output schema_info.json
```

**智能字段检测：**
脚本智能检测字段类型并生成合适的 Faker 方法：
- `email` 字段 → `fake.email()`
- `phone` 字段 → `fake.phone_number()`
- `address` 字段 → `fake.address()`
- `first_name` 字段 → `fake.first_name()`
- `description` 字段 → `fake.paragraph()`
- `created_at`（TIMESTAMP）→ `fake.date_time_between()`
- 整数类型 → `fake.random_int()`
- 布尔类型 → `fake.boolean()`
- 以及更多模式...

**示例输出：**
```python
# generated_factories.py（自动生成）

def candidate_factory(fake, index):
    """candidate 模型的工厂函数"""
    return {
        'full_name': fake.name(),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'years_of_experience': fake.random_int(min=1, max=1000),
        'skills': {},  # JSON 字段
        'created_at': fake.date_time_between(start_date='-1y', end_date='now'),
        'status': fake.word(),
    }
```

### 参考资料（`references/`）

#### `database-configs.md`
全面的数据库连接模式和配置示例。

**内容：**
- 所有支持数据库的连接字符串格式
- 环境变量模式
- 配置文件示例（`.env`、`settings.py`、`config.yaml`）
- Docker Compose 配置
- 安全最佳实践
- 常见问题和解决方案

**使用时机：**
- 设置数据库连接时
- 排查连接错误时
- 配置不同环境（开发、预发布、生产）时

#### `faker-recipes.md`
使用 Faker 生成逼真虚拟数据的常用模式和示例。

**内容：**
- 个人信息（姓名、电子邮件、地址）
- 业务数据（公司、职位）
- 技术数据（URL、IP、UUID）
- 日期和时间
- 文本生成
- 数字和序列
- 本地化
- 自定义提供者
- 特定于数据库的工厂模式

**使用时机：**
- 创建自定义工厂函数时
- 需要数据生成灵感时
- 了解 Faker 功能时
- 创建项目特定的数据生成器时

#### `orm-patterns.md`
使用各种 ORM 种子数据库的模式和最佳实践。

**内容：**
- **SQLAlchemy** - 设置、批量操作、关系、错误处理、工厂
- **Django ORM** - 模型、批量操作、管理命令
- **Prisma**（TypeScript）- 种子脚本、关系
- **MongoDB**（PyMongo）- 文档插入、嵌入文档、引用
- 最佳实践（事务、幂等性、约束、进度报告）

**使用时机：**
- 实现特定于 ORM 的种子生成时
- 需要 ORM 示例时
- 了解关系种子生成（一对多、多对多）时
- 创建生产级种子脚本时

### 资源文件（`assets/`）

#### `seed-config-template.yaml`
基于 YAML 的种子数据生成配置模板。

**功能：**
- 数据库连接配置
- Faker 设置（语言环境、用于可重复性的种子）
- 带有工厂函数的模型定义
- 种子选项（批量大小、清除现有数据、幂等性）
- 种子后钩子

**用法：**
```bash
# 复制模板
cp assets/seed-config-template.yaml seed-config.yaml

# 编辑配置
# ... 自定义模型、数量、工厂 ...

# 运行种子生成
python scripts/seed_database.py --config seed-config.yaml
```

#### `fixture-template.json`
JSON 测试夹具模板。

**功能：**
- 常见模型的示例结构（User、Post）
- Elios 专用模型（Candidate、Question、InterviewSession）
- 带有关系的正确 JSON 格式
- 嵌套数据示例（嵌入文档、外键）

**用法：**
```bash
# 复制并自定义
cp assets/fixture-template.json fixtures/my_data.json

# 用你的数据编辑 JSON 文件
# ...

# 种子数据库
python scripts/seed_database.py \
  --fixtures fixtures/my_data.json \
  --db postgresql \
  --connection "postgresql://user:pass@localhost/db"
```

## 常用工作流程

### 工作流程 1：快速开发设置

为即时开发用示例数据种子本地数据库：

```bash
# 1. 自动检测数据库
python scripts/detect_db_config.py

# 2. 生成夹具
python scripts/generate_fixtures.py \
  --template elios-interview \
  --output fixtures/dev_data.json

# 3. 种子数据库
python scripts/seed_database.py \
  --fixtures fixtures/dev_data.json \
  --db postgresql \
  --connection "postgresql://postgres:password@localhost/elios_dev"

# 验证
psql -d elios_dev -c "SELECT COUNT(*) FROM candidates;"
```

### 工作流程 2：创建测试夹具

为自动化测试创建夹具：

```bash
# 生成小型、聚焦的测试夹具
python scripts/generate_fixtures.py \
  --models Candidate:10,Question:20,InterviewSession:5 \
  --output tests/fixtures/test_data.json \
  --pretty

# 在测试中使用：
# - 版本控制 fixtures/test_data.json
# - 在测试设置中加载
# - 在 CI/CD 中保持一致的测试数据
```

### 工作流程 3：预发布环境填充

用类生产数据填充预发布环境：

```bash
# 1. 生成大型数据集
python scripts/generate_fixtures.py \
  --template elios-interview \
  --output fixtures/staging_data.json

# 如有需要，手动增加夹具文件中的数量

# 2. 检测预发布数据库
python scripts/detect_db_config.py --env-file .env.staging

# 3. 种子预发布环境
python scripts/seed_database.py \
  --fixtures fixtures/staging_data.json \
  --db postgresql \
  --connection "$STAGING_DATABASE_URL"
```

### 工作流程 4：数据库迁移测试

用种子数据测试迁移：

```bash
# 1. 种子旧模式
python scripts/seed_database.py --fixtures fixtures/old_schema.json

# 2. 运行迁移
alembic upgrade head

# 3. 验证数据完整性
python scripts/verify_migration.py

# 4. 种子新字段（如需要）
python scripts/seed_database.py --fixtures fixtures/new_fields.json
```

## 最佳实践

### 1. 版本控制夹具

将夹具存储在版本控制中以保持一致性：

```bash
# 创建夹具目录
mkdir -p fixtures/{development,testing,staging}

# 生成并提交
python scripts/generate_fixtures.py \
  --template elios-interview \
  --output fixtures/development/base_data.json \
  --pretty

git add fixtures/
git commit -m "添加基础开发夹具"
```

### 2. 使用可重复的种子

为了保持一致的测试数据，使用 Faker 种子：

```python
from faker import Faker

# 设置种子以保证可重复性
Faker.seed(12345)
fake = Faker()

# 始终生成相同的数据
fake.name()  # 始终为 "John Smith"（示例）
```

### 3. 按环境分离种子脚本

```
scripts/
├── seed_development.py    # 用于本地开发的小型数据集
├── seed_testing.py         # 用于测试的受控夹具
├── seed_staging.py         # 大型类生产数据集
└── seed_demo.py            # 精选的演示数据
```

### 4. 幂等种子生成

确保种子生成可以安全地多次运行：

```python
def seed_users(session, count=100):
    # 检查是否已种子
    existing_count = session.query(User).count()
    if existing_count >= count:
        print(f"已种子 {existing_count} 个用户，跳过...")
        return

    # 种子剩余部分
    remaining = count - existing_count
    # ... 创建用户 ...
```

### 5. 大型数据集的进度报告

```python
# 批量插入并报告进度
batch_size = 1000
for i in range(0, count, batch_size):
    # ... 创建批次 ...
    print(f"进度：{i}/{count} ({(i/count)*100:.1f}%)")
```

## 依赖项

### 必需
- **Python 3.8+**
- **Faker**（`pip install faker`）

### 可选（基于数据库）
- **SQLAlchemy**（`pip install sqlalchemy`）- 用于 PostgreSQL、MySQL、SQLite
- **psycopg2**（`pip install psycopg2-binary`）- PostgreSQL 驱动
- **pymysql**（`pip install pymysql`）- MySQL 驱动
- **pymongo**（`pip install pymongo`）- MongoDB 驱动
- **PyYAML**（`pip install pyyaml`）- 用于 YAML 配置支持

### 安装

```bash
# 安装核心依赖
pip install faker pyyaml

# 安装数据库驱动（根据你的数据库选择）
pip install sqlalchemy psycopg2-binary  # PostgreSQL
pip install sqlalchemy pymysql          # MySQL
pip install pymongo                     # MongoDB
```

## 故障排除

### 问题："Faker 未安装"
```
Error: Faker library not installed
```
**解决方案：**
```bash
pip install faker
```

### 问题：数据库连接被拒绝
```
Error: connection refused
```
**解决方案：**
1. 检查数据库是否正在运行
2. 验证连接字符串（主机、端口、凭据）
3. 检查防火墙设置
4. 参考 `references/database-configs.md` 获取详细故障排除信息

### 问题：唯一约束冲突
```
Error: duplicate key value violates unique constraint
```
**解决方案：**
1. 种子前清空数据库：`session.query(Model).delete()`
2. 使用幂等种子生成（检查现有记录）
3. 使用 Faker 生成唯一值

### 问题：外键约束冲突
```
Error: foreign key constraint fails
```
**解决方案：**
1. 按正确的顺序种子（父模型先于子模型）
2. 使用实际存在的外键 ID
3. 存储创建的记录以供引用：`created_users = [...]; post.author_id = random.choice([u.id for u in created_users])`

### 问题：大型数据集内存不足
```
Error: MemoryError
```
**解决方案：**
1. 使用批量插入并提交：每 N 条记录 `session.flush()`
2. 减小批量大小
3. 流式传输数据而不是全部加载到内存中

## 高级用法

### 自定义 Faker 提供者

创建特定领域的提供者：

```python
from faker import Faker
from faker.providers import BaseProvider

class InterviewProvider(BaseProvider):
    def interview_status(self):
        return self.random_element(['pending', 'scheduled', 'completed', 'cancelled'])

    def skill_level(self):
        return self.random_element(['beginner', 'intermediate', 'advanced', 'expert'])

    def programming_language(self):
        return self.random_element(['Python', 'JavaScript', 'Java', 'C++', 'Go'])

fake = Faker()
fake.add_provider(InterviewProvider)

# 使用自定义方法
candidate = {
    'skill_level': fake.skill_level(),
    'primary_language': fake.programming_language(),
}
```

### 多语言环境数据生成

生成国际化测试数据：

```python
from faker import Faker

# 创建多个语言环境
fake_us = Faker('en_US')
fake_jp = Faker('ja_JP')
fake_fr = Faker('fr_FR')

users = [
    {'name': fake_us.name(), 'address': fake_us.address()},
    {'name': fake_jp.name(), 'address': fake_jp.address()},
    {'name': fake_fr.name(), 'address': fake_fr.address()},
]
```

### 种子生成处理关系

处理复杂的关系：

```python
# 一对多
author = User(username=fake.user_name())
session.add(author)
session.flush()  # 获取 author.id

posts = [
    Post(title=fake.sentence(), author_id=author.id)
    for _ in range(10)
]
session.add_all(posts)

# 多对多
skills = [Skill(name=name) for name in ['Python', 'JavaScript', 'SQL']]
session.add_all(skills)
session.flush()

candidate = Candidate(full_name=fake.name())
candidate.skills.extend(random.sample(skills, k=2))
session.add(candidate)

session.commit()
```

## 示例

### 示例 1：种子 Elios 面试系统

```bash
# 生成 Elios 专用夹具
python scripts/generate_fixtures.py \
  --template elios-interview \
  --output fixtures/elios_dev.json \
  --pretty

# 种子数据库
python scripts/seed_database.py \
  --fixtures fixtures/elios_dev.json \
  --db postgresql \
  --connection "postgresql://postgres:password@localhost/elios_dev"

# 验证
psql -d elios_dev -c "SELECT COUNT(*) FROM candidates;"
psql -d elios_dev -c "SELECT COUNT(*) FROM questions;"
psql -d elios_dev -c "SELECT COUNT(*) FROM interview_sessions;"
```

### 示例 2：为 CI/CD 创建测试夹具

```bash
# 生成小型、受控的夹具
python scripts/generate_fixtures.py \
  --models Candidate:5,Question:10 \
  --output tests/fixtures/ci_test_data.json \
  --pretty

# 在 CI 流水线中：
python scripts/seed_database.py \
  --fixtures tests/fixtures/ci_test_data.json \
  --db sqlite \
  --connection "sqlite:///:memory:"

# 使用种子数据运行测试
pytest tests/
```

### 示例 3：生成越南语测试数据

```bash
# 为 Elios 生成越南语夹具
python scripts/generate_fixtures.py \
  --template elios-interview \
  --locale vi_VN \
  --output fixtures/elios_vietnamese.json \
  --pretty

# 种子数据库
python scripts/seed_database.py \
  --fixtures fixtures/elios_vietnamese.json \
  --db postgresql \
  --connection "postgresql://postgres:password@localhost/elios_dev"

# 验证越南语数据
psql -d elios_dev -c "SELECT full_name, education->>'university' as university FROM candidates LIMIT 5;"
```

**预期输出：**
```
        full_name        |          university
-------------------------+-------------------------------
 Nguyễn Văn Minh         | Đại học Bách Khoa Hà Nội
 Trần Thị Hương          | Đại học FPT
 Lê Minh Tuấn            | Đại học Quốc gia Hà Nội
 Phạm Thị Lan            | Đại học Công nghệ
 Hoàng Văn Nam           | Đại học Bách Khoa TP.HCM
```

### 示例 4：自定义工厂脚本

```python
# scripts/seed_custom.py

from seed_database import create_seeder
from faker import Faker

fake = Faker()

def advanced_candidate_factory(fake, index):
    """生成逼真的面试候选人"""
    skills_by_role = {
        'frontend': ['JavaScript', 'React', 'CSS', 'HTML', 'Vue'],
        'backend': ['Python', 'Django', 'FastAPI', 'SQL', 'Docker'],
        'fullstack': ['JavaScript', 'React', 'Python', 'SQL', 'AWS'],
        'data': ['Python', 'Pandas', 'SQL', 'Machine Learning', 'Statistics'],
    }

    role = fake.random_element(list(skills_by_role.keys()))
    skills = fake.random_elements(
        skills_by_role[role],
        length=fake.random_int(min=3, max=5),
        unique=True
    )

    return {
        'full_name': fake.name(),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'years_of_experience': fake.random_int(min=0, max=15),
        'skills': list(skills),
        'desired_role': role,
        'expected_salary': fake.random_int(min=50000, max=200000),
        'created_at': fake.date_time_between(start_date='-6m', end_date='now'),
    }

# 运行种子生成
seeder = create_seeder('postgresql', 'postgresql://user:pass@localhost/db')
candidates = seeder.seed_model(Candidate, count=100, factory_func=advanced_candidate_factory)
print(f"✓ 创建了 {len(candidates)} 个候选人")
```

## 与开发工作流集成

### Docker Compose 集成

将种子生成添加到 Docker Compose 设置：

```yaml
# docker-compose.yml

version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: elios_dev
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"

  seeder:
    build: .
    depends_on:
      - postgres
    environment:
      DATABASE_URL: postgresql://postgres:password@postgres:5432/elios_dev
    command: >
      sh -c "
        sleep 5 &&
        python scripts/generate_fixtures.py --template elios-interview --output /tmp/fixtures.json &&
        python scripts/seed_database.py --fixtures /tmp/fixtures.json --db postgresql --connection $$DATABASE_URL
      "
```

### Makefile 集成

```makefile
# Makefile

.PHONY: seed seed-dev seed-test

seed-dev:
	python scripts/generate_fixtures.py --template elios-interview --output fixtures/dev.json
	python scripts/seed_database.py --fixtures fixtures/dev.json --db postgresql --connection $(DATABASE_URL)

seed-test:
	python scripts/generate_fixtures.py --models Candidate:10,Question:20 --output tests/fixtures/test.json
	python scripts/seed_database.py --fixtures tests/fixtures/test.json --db sqlite --connection "sqlite:///:memory:"

seed-staging:
	python scripts/detect_db_config.py --env-file .env.staging
	python scripts/seed_database.py --fixtures fixtures/staging.json --db postgresql --connection $(STAGING_DATABASE_URL)
```

用法：
```bash
make seed-dev
make seed-test
make seed-staging
```

## 总结

此技能提供完整的数据库种子数据生成解决方案：

1. **自动检测** - 自动查找数据库配置
2. **多种方法** - 夹具、工厂或基于配置
3. **全面的参考资料** - 数据库配置、Faker 配方、ORM 模式
4. **立即可用的模板** - JSON 夹具和 YAML 配置
5. **生产就绪的脚本** - 批量操作、错误处理、进度报告

只要你需要高效地用逼真的测试数据填充数据库，就可以使用此技能。
