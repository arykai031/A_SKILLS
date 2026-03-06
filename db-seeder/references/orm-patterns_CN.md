# ORM 数据填充模式

使用各种 ORM（对象关系映射器）进行数据库填充的模式和最佳实践。

## SQLAlchemy

### 基本设置

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker

# 创建引擎和会话
engine = create_engine('postgresql://user:pass@localhost/db')
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()
```

### 简单填充

```python
from domain.models import User

# 创建单条记录
user = User(
    username=fake.user_name(),
    email=fake.email(),
    first_name=fake.first_name(),
    last_name=fake.last_name()
)
session.add(user)
session.commit()

# 创建多条记录
users = []
for i in range(100):
    user = User(
        username=fake.user_name(),
        email=fake.email(),
        first_name=fake.first_name(),
        last_name=fake.last_name()
    )
    users.append(user)

session.add_all(users)
session.commit()
```

### 批量填充以提升性能

```python
from domain.models import User

# 批量提交的大小
BATCH_SIZE = 1000

users = []
for i in range(10000):
    user = User(
        username=fake.user_name(),
        email=fake.email()
    )
    users.append(user)

    # 分批提交
    if (i + 1) % BATCH_SIZE == 0:
        session.add_all(users)
        session.commit()
        users = []
        print(f"已提交 {i + 1} 个用户")

# 提交剩余记录
if users:
    session.add_all(users)
    session.commit()
```

### 处理关系

```python
from domain.models import User, Post

# 先创建用户
users = []
for i in range(10):
    user = User(username=fake.user_name(), email=fake.email())
    users.append(user)

session.add_all(users)
session.commit()

# 创建带有外键引用的文章
posts = []
for i in range(50):
    post = Post(
        title=fake.sentence(),
        content=fake.paragraph(),
        author_id=fake.random_element([u.id for u in users])
    )
    posts.append(post)

session.add_all(posts)
session.commit()
```

### 多对多关系

```python
from domain.models import User, Skill

# 创建技能
skills = [
    Skill(name='Python'),
    Skill(name='JavaScript'),
    Skill(name='SQL'),
]
session.add_all(skills)
session.commit()

# 创建带有技能的用户（多对多）
for i in range(20):
    user = User(
        username=fake.user_name(),
        email=fake.email()
    )

    # 为用户添加随机技能
    user_skills = fake.random_elements(
        skills,
        length=fake.random_int(min=1, max=len(skills)),
        unique=True
    )
    user.skills.extend(user_skills)

    session.add(user)

session.commit()
```

### 错误处理

```python
from sqlalchemy.exc import IntegrityError

for i in range(100):
    try:
        user = User(
            username=fake.user_name(),
            email=fake.email()
        )
        session.add(user)
        session.commit()
    except IntegrityError as e:
        # 处理重复键冲突
        session.rollback()
        print(f"创建用户 {i} 时出错：{e}")
```

### 使用工厂模式

```python
from faker import Faker
from domain.models import User

class UserFactory:
    def __init__(self, session, faker=None):
        self.session = session
        self.fake = faker or Faker()

    def create(self, **kwargs):
        """创建单个用户"""
        data = {
            'username': self.fake.user_name(),
            'email': self.fake.email(),
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
        }
        data.update(kwargs)

        user = User(**data)
        self.session.add(user)
        self.session.commit()
        return user

    def create_batch(self, count, **kwargs):
        """创建多个用户"""
        users = []
        for _ in range(count):
            data = {
                'username': self.fake.user_name(),
                'email': self.fake.email(),
                'first_name': self.fake.first_name(),
                'last_name': self.fake.last_name(),
            }
            data.update(kwargs)
            users.append(User(**data))

        self.session.add_all(users)
        self.session.commit()
        return users

# 使用示例
factory = UserFactory(session)
user = factory.create(username='john_doe')
users = factory.create_batch(100, is_active=True)
```

## Django ORM

### 基本设置

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from myapp.models import User
from faker import Faker

fake = Faker()
```

### 简单填充

```python
from myapp.models import User

# 创建单条记录
user = User.objects.create(
    username=fake.user_name(),
    email=fake.email(),
    first_name=fake.first_name(),
    last_name=fake.last_name()
)

# 创建多条记录
users = [
    User(
        username=fake.user_name(),
        email=fake.email(),
        first_name=fake.first_name(),
        last_name=fake.last_name()
    )
    for _ in range(100)
]
User.objects.bulk_create(users)
```

### 批量操作

```python
from myapp.models import User

# 批量创建（对大量记录更高效）
users = [User(username=fake.user_name(), email=fake.email()) for _ in range(1000)]
User.objects.bulk_create(users, batch_size=500)

# 获取已创建的对象及其 ID
users = User.objects.bulk_create(users, batch_size=500)
# 注意：在 Django 4.0+ 中，bulk_create 返回带有 ID 的对象
```

### 关系处理

```python
from myapp.models import User, Post

# 创建用户
user = User.objects.create(username=fake.user_name(), email=fake.email())

# 为该用户创建文章
posts = [
    Post(
        title=fake.sentence(),
        content=fake.paragraph(),
        author=user
    )
    for _ in range(10)
]
Post.objects.bulk_create(posts)
```

### 用于填充的管理命令

```python
# myapp/management/commands/seed_database.py

from django.core.management.base import BaseCommand
from faker import Faker
from myapp.models import User

class Command(BaseCommand):
    help = '使用假数据填充数据库'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=10)

    def handle(self, *args, **options):
        fake = Faker()
        count = options['users']

        self.stdout.write(f'正在创建 {count} 个用户...')

        users = [
            User(
                username=fake.user_name(),
                email=fake.email()
            )
            for _ in range(count)
        ]
        User.objects.bulk_create(users)

        self.stdout.write(self.style.SUCCESS(f'✓ 已创建 {count} 个用户'))

# 使用方式：python manage.py seed_database --users 100
```

## Prisma (TypeScript/JavaScript)

### 基本设置

```typescript
import { PrismaClient } from '@prisma/client';
import { faker } from '@faker-js/faker';

const prisma = new PrismaClient();
```

### 简单填充

```typescript
// 单条记录
const user = await prisma.user.create({
  data: {
    username: faker.internet.userName(),
    email: faker.internet.email(),
    firstName: faker.person.firstName(),
    lastName: faker.person.lastName(),
  },
});

// 多条记录
const users = await Promise.all(
  Array.from({ length: 100 }, () =>
    prisma.user.create({
      data: {
        username: faker.internet.userName(),
        email: faker.internet.email(),
        firstName: faker.person.firstName(),
        lastName: faker.person.lastName(),
      },
    })
  )
);
```

### 批量操作

```typescript
// 批量创建（更高效）
const users = await prisma.user.createMany({
  data: Array.from({ length: 100 }, () => ({
    username: faker.internet.userName(),
    email: faker.internet.email(),
    firstName: faker.person.firstName(),
    lastName: faker.person.lastName(),
  })),
});
```

### 填充脚本

```typescript
// prisma/seed.ts

import { PrismaClient } from '@prisma/client';
import { faker } from '@faker-js/faker';

const prisma = new PrismaClient();

async function main() {
  console.log('正在填充数据库...');

  // 创建用户
  const users = await prisma.user.createMany({
    data: Array.from({ length: 10 }, () => ({
      username: faker.internet.userName(),
      email: faker.internet.email(),
    })),
  });

  console.log(`✓ 已创建 ${users.count} 个用户`);
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });

// 添加到 package.json：
// "prisma": {
//   "seed": "ts-node prisma/seed.ts"
// }
```

## MongoDB (PyMongo)

### 基本设置

```python
from pymongo import MongoClient
from faker import Faker

client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
fake = Faker()
```

### 简单填充

```python
// 单个文档
user = {
    'username': fake.user_name(),
    'email': fake.email(),
    'created_at': fake.date_time()
}
result = db.users.insert_one(user)
print(f"已创建用户，ID：{result.inserted_id}")

// 多个文档
users = [
    {
        'username': fake.user_name(),
        'email': fake.email(),
        'created_at': fake.date_time()
    }
    for _ in range(100)
]
result = db.users.insert_many(users)
print(f"已创建 {len(result.inserted_ids)} 个用户")
```

### 带关系（嵌入文档）

```python
// 带有嵌入文章的用户
user = {
    'username': fake.user_name(),
    'email': fake.email(),
    'posts': [
        {
            'title': fake.sentence(),
            'content': fake.paragraph(),
            'created_at': fake.date_time()
        }
        for _ in range(5)
    ]
}
db.users.insert_one(user)
```

### 带引用

```python
// 先创建用户
users = [
    {'username': fake.user_name(), 'email': fake.email()}
    for _ in range(10)
]
user_ids = db.users.insert_many(users).inserted_ids

// 创建带有用户引用的文章
posts = [
    {
        'title': fake.sentence(),
        'content': fake.paragraph(),
        'author_id': fake.random_element(user_ids)
    }
    for _ in range(50)
]
db.posts.insert_many(posts)
```

## 最佳实践

### 1. 事务安全

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://user:pass@localhost/db')
Session = sessionmaker(bind=engine)

def seed_database():
    session = Session()
    try:
        # 填充操作
        users = [User(username=fake.user_name()) for _ in range(100)]
        session.add_all(users)
        session.commit()
        print("✓ 填充成功")
    except Exception as e:
        session.rollback()
        print(f"✗ 填充失败：{e}")
        raise
    finally:
        session.close()
```

### 2. 幂等填充

```python
def seed_users(session, count=100):
    # 检查是否已填充
    existing_count = session.query(User).count()
    if existing_count >= count:
        print(f"数据库已有 {existing_count} 个用户，跳过...")
        return

    # 填充剩余数量
    remaining = count - existing_count
    users = [User(username=fake.user_name()) for _ in range(remaining)]
    session.add_all(users)
    session.commit()
    print(f"✓ 已创建 {remaining} 个用户（共 {count} 个）")
```

### 3. 填充前清空数据

```python
def clear_and_seed(session):
    # 清空现有数据
    session.query(Post).delete()
    session.query(User).delete()
    session.commit()

    # 填充新数据
    users = [User(username=fake.user_name()) for _ in range(100)]
    session.add_all(users)
    session.commit()
```

### 4. 带约束的填充

```python
def seed_unique_users(session, count=100):
    """确保用户名/邮箱唯一"""
    existing_emails = {u.email for u in session.query(User.email).all()}

    users = []
    attempts = 0
    max_attempts = count * 10

    while len(users) < count and attempts < max_attempts:
        email = fake.email()
        if email not in existing_emails:
            user = User(username=fake.user_name(), email=email)
            users.append(user)
            existing_emails.add(email)
        attempts += 1

    session.add_all(users)
    session.commit()
    return len(users)
```

### 5. 进度报告

```python
def seed_with_progress(session, count=10000):
    """带进度报告的填充"""
    batch_size = 1000

    for i in range(0, count, batch_size):
        batch = [
            User(username=fake.user_name(), email=fake.email())
            for _ in range(min(batch_size, count - i))
        ]
        session.add_all(batch)
        session.commit()

        completed = min(i + batch_size, count)
        progress = (completed / count) * 100
        print(f"进度：{completed}/{count} ({progress:.1f}%)")
```

## 资源

- [SQLAlchemy 文档](https://docs.sqlalchemy.org/)
- [Django ORM 文档](https://docs.djangoproject.com/en/stable/topics/db/)
- [Prisma 文档](https://www.prisma.io/docs/)
- [PyMongo 文档](https://pymongo.readthedocs.io/)
