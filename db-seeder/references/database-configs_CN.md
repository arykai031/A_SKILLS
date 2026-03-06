# 数据库配置参考

本参考文档提供了各种数据库系统的数据库连接模式和配置示例。

## PostgreSQL

### 连接字符串格式

```
postgresql://username:password@host:port/database
```

### 环境变量

```bash
DATABASE_URL=postgresql://postgres:password@localhost:5432/elios_dev
# 或者单独的组件
DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_NAME=elios_dev
DB_USER=postgres
DB_PASSWORD=password
```

### SQLAlchemy 配置

```python
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:password@localhost:5432/elios_dev')
```

### 默认端口

`5432`

## MySQL / MariaDB

### 连接字符串格式

```
mysql://username:password@host:port/database
```

### 环境变量

```bash
DATABASE_URL=mysql://root:password@localhost:3306/elios_dev
# 或者单独的组件
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=elios_dev
DB_USER=root
DB_PASSWORD=password
```

### SQLAlchemy 配置

```python
from sqlalchemy import create_engine

engine = create_engine('mysql://root:password@localhost:3306/elios_dev')
```

### 默认端口

`3306`

## SQLite

### 连接字符串格式

```
sqlite:///path/to/database.db
# 或者内存数据库
sqlite:///:memory:
```

### 环境变量

```bash
DATABASE_URL=sqlite:///./elios_dev.db
# 或者
DB_TYPE=sqlite
DB_PATH=./elios_dev.db
```

### SQLAlchemy 配置

```python
from sqlalchemy import create_engine

# 基于文件
engine = create_engine('sqlite:///./elios_dev.db')

# 内存中
engine = create_engine('sqlite:///:memory:')
```

### 默认端口

N/A（基于文件的数据库）

## MongoDB

### 连接字符串格式

```
mongodb://username:password@host:port/database
# 带认证数据库
mongodb://username:password@host:port/database?authSource=admin
```

### 环境变量

```bash
MONGODB_URI=mongodb://admin:password@localhost:27017/elios_dev
# 或者单独的组件
DB_TYPE=mongodb
DB_HOST=localhost
DB_PORT=27017
DB_NAME=elios_dev
DB_USER=admin
DB_PASSWORD=password
```

### PyMongo 配置

```python
from pymongo import MongoClient

client = MongoClient('mongodb://admin:password@localhost:27017/')
db = client['elios_dev']
```

### 默认端口

`27017`

## 配置文件模式

### .env 文件

```bash
# PostgreSQL
DATABASE_URL=postgresql://postgres:password@localhost:5432/elios_dev

# MySQL
DATABASE_URL=mysql://root:password@localhost:3306/elios_dev

# SQLite
DATABASE_URL=sqlite:///./elios_dev.db

# MongoDB
MONGODB_URI=mongodb://admin:password@localhost:27017/elios_dev
```

### settings.py (Pydantic)

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    db_type: str = "postgresql"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "elios_dev"
    db_user: str = "postgres"
    db_password: str = ""

    class Config:
        env_file = ".env"
```

### config.yaml

```yaml
database:
  type: postgresql
  host: localhost
  port: 5432
  name: elios_dev
  user: postgres
  password: password
```

### alembic.ini (SQLAlchemy 迁移)

```ini
[alembic]
sqlalchemy.url = postgresql://postgres:password@localhost:5432/elios_dev
```

## Docker Compose 配置

### PostgreSQL

```yaml
version: "3.8"
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: elios_dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

连接字符串：`postgresql://postgres:password@localhost:5432/elios_dev`

### MySQL

```yaml
version: "3.8"
services:
  mysql:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: elios_dev
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

连接字符串：`mysql://root:password@localhost:3306/elios_dev`

### MongoDB

```yaml
version: "3.8"
services:
  mongodb:
    image: mongo:6
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password
      MONGO_INITDB_DATABASE: elios_dev
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
```

连接字符串：`mongodb://admin:password@localhost:27017/elios_dev`

## 连接字符串安全

### 最佳实践

1. **切勿将包含凭据的连接字符串提交到版本控制**
   - 使用 `.env` 文件（添加到 `.gitignore`）
   - 使用环境变量
   - 使用密钥管理系统（AWS Secrets Manager、HashiCorp Vault）

2. **对特殊字符使用连接字符串编码**

   ```python
   from urllib.parse import quote_plus

   password = "p@ssw0rd!"
   encoded = quote_plus(password)  # "p%40ssw0rd%21"
   connection = f"postgresql://user:{encoded}@localhost/db"
   ```

3. **对远程连接使用 SSL/TLS**

   ```
   # 带 SSL 的 PostgreSQL
   postgresql://user:pass@host/db?sslmode=require

   # 带 SSL 的 MySQL
   mysql://user:pass@host/db?ssl-mode=REQUIRED

   # 带 SSL 的 MongoDB
   mongodb://user:pass@host/db?ssl=true
   ```

4. **定期轮换凭据**

5. **使用最小权限的数据库用户**
   - 为种子数据和生产环境创建单独的用户
   - 仅限制所需的权限

## 常见问题和解决方案

### PostgreSQL 连接被拒绝

```
Error: connection refused
```

**解决方案：**

- 检查 PostgreSQL 是否正在运行：`pg_isready`
- 验证端口：`5432`（默认）
- 检查 `pg_hba.conf` 中的连接权限
- 确保防火墙允许连接

### MySQL 访问被拒绝

```
Error: Access denied for user 'root'@'localhost'
```

**解决方案：**

- 验证用户名/密码
- 检查 MySQL 用户权限：`SHOW GRANTS FOR 'root'@'localhost';`
- 如有需要重置密码

### SQLite 数据库被锁定

```
Error: database is locked
```

**解决方案：**

- 关闭其他到数据库的连接
- 使用 `sqlite3` CLI 检查：`.databases`
- 重启应用程序

### MongoDB 认证失败

```
Error: Authentication failed
```

**解决方案：**

- 验证 `authSource` 参数（通常是 `admin`）
- 在 mongo shell 中检查用户是否存在：`db.getUsers()`
- 确保连接字符串中的数据库正确

## 检测脚本使用

`detect_db_config.py` 脚本可自动检测数据库配置：

```bash
# 从环境和配置文件中自动检测
python scripts/detect_db_config.py

# 指定配置文件
python scripts/detect_db_config.py --config-path src/infrastructure/config/settings.py

# 指定 .env 文件
python scripts/detect_db_config.py --env-file .env

# 指定项目根目录
python scripts/detect_db_config.py --project-root /path/to/project
```

脚本将输出：

- 检测到的数据库类型
- 连接详情（密码已掩码）
- 可直接使用的 `seed_database.py` 命令
