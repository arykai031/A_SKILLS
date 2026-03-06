# Faker 用法和模式

使用 Faker 库生成逼真的虚拟数据的常用模式和示例。

## 基本用法

```python
from faker import Faker

fake = Faker()

# 生成单个值
name = fake.name()
email = fake.email()

# 生成多个值
names = [fake.name() for _ in range(10)]
```

## 个人信息

### 姓名

```python
fake.name()                    # "John Smith"
fake.first_name()              # "John"
fake.last_name()               # "Smith"
fake.name_male()               # "Michael Johnson"
fake.name_female()             # "Sarah Williams"
fake.prefix()                  # "Dr."
fake.suffix()                  # "Jr."
```

### 联系信息

```python
fake.email()                   # "john.smith@example.com"
fake.safe_email()              # "john.smith@example.org" (安全域名)
fake.company_email()           # "john.smith@company.com"
fake.phone_number()            # "+1-555-123-4567"
fake.address()                 # "123 Main St, Springfield, IL 62701"
fake.street_address()          # "123 Main St"
fake.city()                    # "Springfield"
fake.state()                   # "Illinois"
fake.zipcode()                 # "62701"
fake.country()                 # "United States"
```

## 商业数据

### 公司信息

```python
fake.company()                 # "Tech Corp Inc."
fake.company_suffix()          # "Inc."
fake.job()                     # "Software Engineer"
fake.bs()                      # "synergize innovative solutions" (商业术语)
fake.catch_phrase()            # "Innovative solutions for tomorrow"
```

## 技术数据

### 互联网和 URLs

```python
fake.url()                     # "https://example.com"
fake.uri()                     # "/path/to/resource"
fake.domain_name()             # "example.com"
fake.ipv4()                    # "192.168.1.1"
fake.ipv6()                    # "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
fake.mac_address()             # "00:1B:44:11:3A:B7"
fake.user_agent()              # "Mozilla/5.0 ..."
fake.slug()                    # "this-is-a-slug"
```

### 文件和存储

```python
fake.file_name()               # "document.pdf"
fake.file_extension()          # "pdf"
fake.mime_type()               # "application/pdf"
fake.file_path()               # "/home/user/document.pdf"
fake.uuid4()                   # "550e8400-e29b-41d4-a716-446655440000"
```

### 颜色和图像

```python
fake.color_name()              # "Red"
fake.hex_color()               # "#FF5733"
fake.rgb_color()               # "rgb(255, 87, 51)"
fake.image_url()               # "https://picsum.photos/640/480"
```

## 日期和时间

```python
from datetime import datetime, timedelta

# 随机日期
fake.date()                                    # "2023-05-15"
fake.date_of_birth(minimum_age=18, maximum_age=70)  # 日期对象
fake.date_time()                               # datetime 对象
fake.date_between(start_date='-1y', end_date='today')  # 最近一年内
fake.date_time_between(start_date='-30d', end_date='now')  # 最近 30 天

# 特定格式
fake.date_time_this_month()
fake.date_time_this_year()
fake.future_date()             # 未来日期
fake.past_date()               # 过去日期

# 时间组件
fake.time()                    # "14:30:45"
fake.timezone()                # "America/New_York"
```

## 文本生成

```python
# 单词和句子
fake.word()                    # "example"
fake.words(nb=5)               # ["word1", "word2", ...]
fake.sentence()                # "This is a sentence."
fake.sentence(nb_words=10)     # 包含 10 个单词的句子
fake.sentences(nb=3)           # 3 个句子的列表

# 段落
fake.paragraph()               # 单个段落
fake.paragraph(nb_sentences=5) # 包含 5 个句子的段落
fake.paragraphs(nb=3)          # 3 个段落的列表
fake.text(max_nb_chars=200)    # 最多 200 个字符的文本

# Lorem ipsum
fake.text()                    # Lorem ipsum 文本
```

## 数字和数据

```python
# 随机数字
fake.random_int(min=0, max=100)          # 0-100 之间的整数
fake.random_number(digits=5)             # 5 位数
fake.random_digit()                      # 0-9
fake.pyfloat(left_digits=3, right_digits=2)  # 123.45

# 布尔值
fake.boolean()                           # True 或 False
fake.boolean(chance_of_getting_true=75)  # 75% 的概率为 True

# 序列
fake.random_element(['A', 'B', 'C'])     # 选择一个
fake.random_elements(['A', 'B', 'C'], length=2, unique=True)  # 选择 2 个不重复的

# 信用卡
fake.credit_card_number()
fake.credit_card_expire()
fake.credit_card_provider()
```

## 本地化

```python
# 创建带有特定语言环境的 Faker
fake_us = Faker('en_US')
fake_uk = Faker('en_GB')
fake_fr = Faker('fr_FR')
fake_ja = Faker('ja_JP')
fake_vi = Faker('vi_VN')       # 越南语

# 示例
fake_us.phone_number()         # 美国格式：+1-555-123-4567
fake_uk.phone_number()         # 英国格式：01234 567890
fake_fr.name()                 # 法国姓名：Jean Dupont
fake_ja.address()              # 日本地址：東京都...
fake_vi.name()                 # 越南姓名：Nguyễn Văn An
fake_vi.phone_number()         # 越南格式：+84 912 345 678
fake_vi.address()              # 越南地址：123 Nguyễn Huệ, Hà Nội

# 多语言环境
fake = Faker(['en_US', 'en_GB', 'fr_FR'])  # 从所有语言环境中随机选择
```

### 越南语语言环境 (vi_VN)

Faker 支持越南语数据生成，用于创建本地化的测试数据：

```python
from faker import Faker

fake_vi = Faker('vi_VN')

# 个人信息
fake_vi.name()                 # "Nguyễn Văn An", "Trần Thị Bình"
fake_vi.first_name()           # "Văn", "Thị"
fake_vi.last_name()            # "Nguyễn", "Trần", "Lê"
fake_vi.phone_number()         # "+84 912 345 678", "0987654321"

# 地址
fake_vi.address()              # "123 Nguyễn Huệ, Quận 1, Hồ Chí Minh"
fake_vi.city()                 # "Hà Nội", "Hồ Chí Minh", "Đà Nẵng"
fake_vi.street_address()       # "456 Lê Lợi"

# 公司名称（越南风格）
fake_vi.company()              # "Công ty TNHH ABC"
```

**Elios 的越南语特定自定义：**

```python
from faker import Faker

fake_vi = Faker('vi_VN')

# 越南大学
vietnamese_universities = [
    'Đại học Bách Khoa Hà Nội',
    'Đại học Quốc gia Hà Nội',
    'Đại học FPT',
    'Đại học Công nghệ',
    'Đại học Kinh tế Quốc dân',
    'Đại học Ngoại thương',
    'Đại học Bách Khoa TP.HCM',
    'Đại học Quốc gia TP.HCM',
    'Đại học Khoa học Tự nhiên',
    'Đại học Sư phạm Hà Nội',
]

# 越南学位
vietnamese_degrees = ['Cử nhân', 'Thạc sĩ', 'Tiến sĩ']

# 越南专业
vietnamese_majors = [
    'Khoa học Máy tính',
    'Kỹ thuật Phần mềm',
    'Công nghệ Thông tin',
    'Khoa học Dữ liệu',
    'An toàn Thông tin',
    'Trí tuệ Nhân tạo',
]

# 越南语面试状态
vietnamese_statuses = ['đang chờ', 'đã phỏng vấn', 'đã tuyển', 'đã từ chối']

# 生成越南候选人
def vietnamese_candidate_factory(fake, index):
    return {
        'full_name': fake.name(),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'years_of_experience': fake.random_int(min=0, max=15),
        'skills': fake.random_elements(
            ['Python', 'JavaScript', 'SQL', 'React', 'Docker'],
            length=fake.random_int(min=2, max=5),
            unique=True
        ),
        'education': {
            'degree': fake.random_element(vietnamese_degrees),
            'major': fake.random_element(vietnamese_majors),
            'university': fake.random_element(vietnamese_universities),
            'graduation_year': fake.random_int(min=2015, max=2024),
        },
        'address': fake.address(),
        'city': fake.city(),
        'status': fake.random_element(vietnamese_statuses),
        'created_at': fake.date_time_between(start_date='-1y', end_date='now'),
    }
```

## 自定义 Provider

```python
from faker import Faker
from faker.providers import BaseProvider

class TechSkillProvider(BaseProvider):
    def programming_language(self):
        languages = ['Python', 'JavaScript', 'Java', 'C++', 'Go', 'Rust']
        return self.random_element(languages)

    def framework(self):
        frameworks = ['React', 'Vue', 'Angular', 'Django', 'FastAPI', 'Flask']
        return self.random_element(frameworks)

fake = Faker()
fake.add_provider(TechSkillProvider)

fake.programming_language()    # "Python"
fake.framework()               # "React"
```

## 数据库填充模式

### 用户工厂

```python
def user_factory(fake, index):
    return {
        'id': index + 1,
        'username': fake.user_name(),
        'email': fake.email(),
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'password_hash': fake.sha256(),
        'created_at': fake.date_time_between(start_date='-2y', end_date='now'),
        'is_active': fake.boolean(chance_of_getting_true=80),
        'last_login': fake.date_time_between(start_date='-30d', end_date='now'),
    }
```

### 产品工厂

```python
def product_factory(fake, index):
    return {
        'id': index + 1,
        'name': ' '.join(fake.words(nb=3)).title(),
        'slug': fake.slug(),
        'description': fake.paragraph(nb_sentences=5),
        'price': fake.pyfloat(left_digits=3, right_digits=2, min_value=10, max_value=1000),
        'stock': fake.random_int(min=0, max=500),
        'sku': fake.bothify(text='???-####', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
        'category': fake.random_element(['Electronics', 'Clothing', 'Books', 'Home']),
        'created_at': fake.date_time_between(start_date='-1y', end_date='now'),
    }
```

### 面试候选人工厂（Elios 专用）

```python
def candidate_factory(fake, index):
    skills_pool = [
        'Python', 'JavaScript', 'React', 'Node.js', 'SQL', 'MongoDB',
        'Docker', 'Kubernetes', 'AWS', 'Git', 'REST APIs', 'GraphQL',
    ]

    return {
        'id': index + 1,
        'full_name': fake.name(),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'years_of_experience': fake.random_int(min=0, max=15),
        'skills': fake.random_elements(skills_pool, length=fake.random_int(min=2, max=6), unique=True),
        'education_degree': fake.random_element(['Bachelor', 'Master', 'PhD']),
        'education_major': 'Computer Science',
        'university': fake.company() + ' University',
        'graduation_year': fake.random_int(min=2010, max=2024),
        'cv_url': f"s3://bucket/cvs/candidate_{index+1}.pdf",
        'linkedin_url': f"https://linkedin.com/in/{fake.user_name()}",
        'created_at': fake.date_time_between(start_date='-6m', end_date='now'),
        'status': fake.random_element(['pending', 'interviewed', 'hired', 'rejected']),
    }
```

### 问题工厂（Elios 专用）

```python
def question_factory(fake, index):
    categories = ['technical', 'behavioral', 'system-design', 'coding']
    difficulties = ['easy', 'medium', 'hard']

    return {
        'id': index + 1,
        'text': fake.sentence(nb_words=10) + '?',
        'category': fake.random_element(categories),
        'difficulty': fake.random_element(difficulties),
        'related_skill': fake.random_element(['Python', 'JavaScript', 'SQL', 'System Design']),
        'expected_keywords': [fake.word() for _ in range(fake.random_int(min=3, max=8))],
        'model_answer': fake.paragraph(nb_sentences=5),
        'time_limit_minutes': fake.random_element([5, 10, 15, 30]),
        'created_at': fake.date_time_between(start_date='-1y', end_date='now'),
    }
```

## 性能提示

### 批量生成

```python
# 高效：一次性生成所有数据
fake = Faker()
names = [fake.name() for _ in range(1000)]

# 低效：多个 Faker 实例
names = [Faker().name() for _ in range(1000)]
```

### 设置种子以确保可重现性

```python
from faker import Faker

# 设置种子以获得可重现的数据
Faker.seed(12345)
fake = Faker()

# 始终生成相同的值
fake.name()  # 始终为 "John Smith"（示例）
```

### 缓存常用值

```python
# 缓存常用值
fake = Faker()
user_ids = list(range(1, 101))  # 100 个用户 ID
cities = [fake.city() for _ in range(20)]  # 20 个城市

# 重用缓存的值
post = {
    'author_id': fake.random_element(user_ids),
    'city': fake.random_element(cities),
}
```

## 常见陷阱

### 1. 唯一约束冲突

```python
# 问题：可能生成重复的电子邮件
users = [{'email': fake.email()} for _ in range(100)]

# 解决方案：确保唯一性
emails = set()
users = []
while len(users) < 100:
    email = fake.email()
    if email not in emails:
        emails.add(email)
        users.append({'email': email})
```

### 2. 外键引用

```python
# 问题：随机外键可能不存在
post = {
    'author_id': fake.random_int(min=1, max=1000),  # 用户可能不存在
}

# 解决方案：使用实际存在的 ID
existing_user_ids = [1, 2, 3, 4, 5]  # 从已创建的用户中获取
post = {
    'author_id': fake.random_element(existing_user_ids),
}
```

### 3. 数据类型不匹配

```python
# 问题：在需要整数的地方使用了字符串
user = {
    'age': fake.random_int(min=18, max=80),  # ✓ 正确
    'age': str(fake.random_int(min=18, max=80)),  # ✗ 错误，如果数据库期望整数
}
```

## 资源

- [Faker 文档](https://faker.readthedocs.io/)
- [可用的语言环境](https://faker.readthedocs.io/en/master/locales.html)
- [标准 Provider](https://faker.readthedocs.io/en/master/providers.html)
