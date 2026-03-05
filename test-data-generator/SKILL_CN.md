---
name: test-data-generator
description: 为单元测试和集成测试创建测试夹具、模拟数据和测试场景。用于设置测试数据、创建模拟对象或生成测试夹具。
---

# 测试数据生成器

生成测试数据、夹具和模拟对象用于测试。

## 快速开始

创建简单的夹具：
```javascript
const mockUser = {
  id: 1,
  name: '测试用户',
  email: 'test@example.com'
}
```

## 使用说明

### 工厂函数

创建可复用的数据生成器：

```javascript
function createUser(overrides = {}) {
  return {
    id: Math.floor(Math.random() * 1000),
    name: '测试用户',
    email: 'test@example.com',
    role: 'user',
    createdAt: new Date().toISOString(),
    ...overrides
  }
}

// 使用示例
const admin = createUser({ role: 'admin', name: '管理员用户' })
const regularUser = createUser()
```

```python
def create_user(**kwargs):
    defaults = {
        'id': random.randint(1, 1000),
        'name': '测试用户',
        'email': 'test@example.com',
        'role': 'user',
        'created_at': datetime.now()
    }
    return {**defaults, **kwargs}

# 使用示例
admin = create_user(role='admin', name='管理员用户')
```

### 构建器模式

用于复杂对象：

```javascript
class UserBuilder {
  constructor() {
    this.user = {
      id: 1,
      name: '测试用户',
      email: 'test@example.com',
      role: 'user',
      preferences: {}
    }
  }
  
  withId(id) {
    this.user.id = id
    return this
  }
  
  withName(name) {
    this.user.name = name
    return this
  }
  
  withRole(role) {
    this.user.role = role
    return this
  }
  
  withPreferences(preferences) {
    this.user.preferences = preferences
    return this
  }
  
  build() {
    return this.user
  }
}

// 使用示例
const user = new UserBuilder()
  .withId(123)
  .withName('张三')
  .withRole('admin')
  .withPreferences({ theme: 'dark' })
  .build()
```

### 测试夹具

**JavaScript/TypeScript**:
```javascript
// fixtures/users.js
export const users = {
  admin: {
    id: 1,
    name: '管理员用户',
    email: 'admin@example.com',
    role: 'admin'
  },
  regular: {
    id: 2,
    name: '普通用户',
    email: 'user@example.com',
    role: 'user'
  }
}

// 在测试中使用
import { users } from './fixtures/users'

test('管理员可以删除帖子', () => {
  expect(canDelete(users.admin)).toBe(true)
})
```

**Python (pytest)**:
```python
# conftest.py
import pytest

@pytest.fixture
def sample_user():
    return {
        'id': 1,
        'name': '测试用户',
        'email': 'test@example.com',
        'role': 'user'
    }

@pytest.fixture
def admin_user():
    return {
        'id': 2,
        'name': '管理员用户',
        'email': 'admin@example.com',
        'role': 'admin'
    }

# 在测试中使用
def test_user_permissions(sample_user, admin_user):
    assert can_delete(admin_user)
    assert not can_delete(sample_user)
```

### 模拟数据

**API 响应**:
```javascript
const mockApiResponse = {
  data: {
    users: [
      { id: 1, name: 'Alice' },
      { id: 2, name: 'Bob' }
    ]
  },
  status: 200,
  statusText: 'OK'
}

// 模拟 fetch
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve(mockApiResponse.data)
  })
)
```

**数据库记录**:
```python
mock_db_records = [
    {'id': 1, 'name': '产品 A', 'price': 10.99},
    {'id': 2, 'name': '产品 B', 'price': 20.99},
    {'id': 3, 'name': '产品 C', 'price': 15.99}
]

@patch('app.database.query')
def test_get_products(mock_query):
    mock_query.return_value = mock_db_records
    products = get_products()
    assert len(products) == 3
```

### 随机数据生成

**使用 faker (JavaScript)**:
```javascript
import { faker } from '@faker-js/faker'

function generateUser() {
  return {
    id: faker.string.uuid(),
    name: faker.person.fullName(),
    email: faker.internet.email(),
    avatar: faker.image.avatar(),
    address: {
      street: faker.location.streetAddress(),
      city: faker.location.city(),
      country: faker.location.country()
    }
  }
}

// 生成多个用户
const users = Array.from({ length: 10 }, generateUser)
```

**使用 Faker (Python)**:
```python
from faker import Faker

fake = Faker()

def generate_user():
    return {
        'id': fake.uuid4(),
        'name': fake.name(),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'address': {
            'street': fake.street_address(),
            'city': fake.city(),
            'country': fake.country()
        }
    }

# 生成多个用户
users = [generate_user() for _ in range(10)]
```

### 种子随机数据

用于可重复的测试：

```javascript
import { faker } from '@faker-js/faker'

test('使用种子生成一致的数据', () => {
  faker.seed(123)
  const user1 = generateUser()
  
  faker.seed(123)
  const user2 = generateUser()
  
  expect(user1).toEqual(user2)
})
```

```python
from faker import Faker

def test_consistent_data():
    fake = Faker()
    Faker.seed(123)
    user1 = generate_user(fake)
    
    Faker.seed(123)
    user2 = generate_user(fake)
    
    assert user1 == user2
```

### 模拟函数

**Jest**:
```javascript
const mockCallback = jest.fn(x => x * 2)

test('为每个项目调用回调', () => {
  const items = [1, 2, 3]
  items.forEach(mockCallback)
  
  expect(mockCallback).toHaveBeenCalledTimes(3)
  expect(mockCallback).toHaveBeenCalledWith(1)
  expect(mockCallback).toHaveBeenCalledWith(2)
  expect(mockCallback).toHaveBeenCalledWith(3)
})
```

**Python (unittest.mock)**:
```python
from unittest.mock import Mock

def test_callback():
    mock_callback = Mock(return_value=42)
    
    result = process_data([1, 2, 3], mock_callback)
    
    assert mock_callback.call_count == 3
    mock_callback.assert_called_with(3)
```

### 基于时间的数据

**冻结时间**:
```javascript
import { jest } from '@jest/globals'

test('创建时间戳', () => {
  const mockDate = new Date('2024-01-01T00:00:00Z')
  jest.useFakeTimers()
  jest.setSystemTime(mockDate)
  
  const record = createRecord()
  expect(record.createdAt).toBe('2024-01-01T00:00:00.000Z')
  
  jest.useRealTimers()
})
```

```python
from freezegun import freeze_time

@freeze_time("2024-01-01 00:00:00")
def test_timestamp():
    record = create_record()
    assert record['created_at'] == datetime(2024, 1, 1, 0, 0, 0)
```

## 常见模式

**模式：测试用例数组**:
```javascript
const testCases = [
  { input: 'hello', expected: 'HELLO' },
  { input: 'world', expected: 'WORLD' },
  { input: '', expected: '' }
]

testCases.forEach(({ input, expected }) => {
  test(`将 "${input}" 转换为 "${expected}"`, () => {
    expect(toUpperCase(input)).toBe(expected)
  })
})
```

**模式：共享设置**:
```javascript
describe('UserService', () => {
  let service
  let mockDb
  
  beforeEach(() => {
    mockDb = {
      query: jest.fn(),
      insert: jest.fn()
    }
    service = new UserService(mockDb)
  })
  
  test('获取用户列表', async () => {
    mockDb.query.mockResolvedValue([{ id: 1 }])
    const users = await service.getUsers()
    expect(users).toHaveLength(1)
  })
})
```

**模式：测试数据文件**:
```javascript
// testData/users.json
[
  {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
  },
  {
    "id": 2,
    "name": "Bob",
    "email": "bob@example.com"
  }
]

// 在测试中
import users from './testData/users.json'

test('处理用户数据', () => {
  const result = processUsers(users)
  expect(result).toHaveLength(2)
})
```

## 高级用法

用于复杂场景：
- 使用工厂库（factory-bot、fishery、rosie）
- 生成 GraphQL 模拟数据
- 创建数据库种子程序
- 构建测试数据管道
