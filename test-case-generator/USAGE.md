# test-case-generator 使用指南

## 快速开始

### 方式一：单个文件生成测试用例

适用于单个需求文档生成测试用例:

```bash
# 使用 AI 技能直接生成
请帮我为 SRS/1_唯一码收货.md 生成测试用例
```

### 方式二：批量生成测试用例 (推荐)

适用于多个需求文档，自动去重和优化:

```bash
# 1. 进入项目根目录
cd e:\WY\110_Ongoing_Projects\01_Code_Box\Private\markdownToCase

# 2. 运行批量生成脚本
python .trae/skills/test-case-generator/scripts/generate_test_cases_enhanced.py
```

## 完整工作流程

### 步骤 1: 功能点去重分析

```bash
python .trae/skills/test-case-generator/scripts/feature_deduplication.py
```

**输出**:
- `config/feature_groups.json` - 功能点分组配置
- `reports/feature_analysis.md` - 功能点分析报告

**作用**:
- 遍历所有 SRS 文档，提取功能点
- 计算功能点相似度，识别重复功能点
- 将功能点分为"通用"和"特有"两类

### 步骤 2: 生成测试用例

```bash
python .trae/skills/test-case-generator/scripts/generate_test_cases_enhanced.py
```

**输出**:
- `case_MD/0_用例复用.md` - 通用测试用例 (跨模块复用)
- `case_MD/<模块名>_测试用例.md` - 模块特有测试用例
- `reports/test_cases_statistics.md` - 统计报告

**作用**:
- 根据功能点分组生成测试用例
- 通用用例写入 `0_用例复用.md`
- 特有用例写入各模块文件
- 自动建立引用关系

### 步骤 3: 转换为 Excel(可选)

```bash
# 转换通用用例
python .trae/skills/test-case-generator/scripts/md_to_excel.py case_MD/0_用例复用.md

# 转换模块用例
python .trae/skills/test-case-generator/scripts/md_to_excel.py case_MD/1_唯一码收货_测试用例.md
```

**输出**:
- `case_excel/0_用例复用.xlsx`
- `case_excel/<模块名>_测试用例.xlsx`

### 步骤 4: 思维导图可视化 (可选)

```bash
# 安装 markmap
npm install -g markmap-cli

# 生成思维导图
markmap case_MD/0_用例复用.md
markmap case_MD/1_唯一码收货_测试用例.md
```

**输出**:
- `case_MD/0_用例复用.html`
- `case_MD/1_唯一码收货_测试用例.html`

## 输出文件说明

### 1. 功能点分组配置 (config/feature_groups.json)

```json
{
  "version": "1.0",
  "generated_at": "2026-02-28 10:30:00",
  "summary": {
    "total_features": 45,
    "common_features_count": 12,
    "unique_features_count": 33
  },
  "feature_groups": [
    {
      "group_id": "FG001",
      "type": "common",
      "feature_name": "唯一码验证",
      "modules": ["唯一码收货", "唯一码组盘"],
      "test_case_file": "0_用例复用.md",
      "aspects": {
        "common": ["空唯一码", "格式错误"],
        "specific": {
          "唯一码收货": ["状态为初始化"],
          "唯一码组盘": ["容器未锁定"]
        }
      }
    }
  ]
}
```

### 2. 通用测试用例 (case_MD/0_用例复用.md)

```markdown
# 通用测试用例

> 本文件包含跨模块复用的通用测试用例

## 唯一码验证 (跨模块复用)

**适用模块**: 唯一码收货、唯一码组盘

### 空唯一码校验

- [P1] 用户已登录 PDA 系统;已进入对应模块页面 | 输入空唯一码 | 系统提示"唯一码不能为空"
```

### 3. 模块特有测试用例 (case_MD/1_唯一码收货_测试用例.md)

```markdown
# 唯一码收货

> **注意**: 本模块复用了以下通用测试用例，请参考 `0_用例复用.md`
> - 唯一码验证 (空唯一码、格式错误、特殊字符)

## 收货处理 - 容器绑定

### 收货完成绑定容器

- [P0] 用户已提交收货;所有唯一码收货成功 | 绑定容器 | 唯一码绑定到容器;库存更新
```

## 配置说明

### 调整相似度阈值

编辑 `config/feature_groups.json`:

```json
{
  "settings": {
    "similarity_threshold": 0.7,  // 调高更严格，调低更宽松
    "min_common_modules": 2,      // 至少几个模块共用才算通用功能点
    "keyword_weight": 0.4,        // 关键词权重
    "semantic_weight": 0.6        // 语义权重
  }
}
```

**建议**:
- 发现过多重复用例 → 调低 `similarity_threshold` 到 0.6
- 发现过少通用用例 → 调高 `similarity_threshold` 到 0.8
- 默认值 0.7 适用于大多数场景

### 人工调整分组

在 `config/feature_groups.json` 中添加:

```json
{
  "manual_adjustments": [
    {
      "group_id": "FG001",
      "force_type": "common",
      "reason": "人工确认跨模块复用"
    }
  ]
}
```

## 常见问题

### Q1: 如何查看功能点分组是否准确？

**A**: 查看 `reports/feature_analysis.md` 报告，重点关注:
- 通用功能点是否确实跨多个模块
- 特有功能点是否确实为单模块独有
- 可疑重复功能点是否需要合并

### Q2: 生成的测试用例太简单怎么办？

**A**: 当前脚本生成的是示例用例，详细用例需要:
1. 使用 AI 技能补充详细测试步骤
2. 或手动编辑测试用例文件
3. 或调整脚本中的用例生成逻辑

### Q3: 如何添加新的测试场景？

**A**: 有两种方式:
1. **直接编辑**: 打开 `case_MD/XX_测试用例.md` 手动添加
2. **重新生成**: 修改 SRS 文档，重新运行生成脚本

### Q4: 如何合并重复的测试用例？

**A**: 
1. 查看 `reports/test_cases_statistics.md` 中的重复用例检测
2. 手动合并重复用例
3. 保留到 `0_用例复用.md`，从模块文件删除

### Q5: 如何更新已有的测试用例？

**A**:
1. 修改 SRS 文档中的功能点
2. 重新运行 `feature_deduplication.py`
3. 重新运行 `generate_test_cases_enhanced.py`
4. 对比新旧测试用例，手动合并差异

## 最佳实践

### 1. 首次生成

```bash
# 完整流程
python feature_deduplication.py
python generate_test_cases_enhanced.py

# 查看报告
cat reports/feature_analysis.md
cat reports/test_cases_statistics.md
```

### 2. 审核调整

1. 打开功能点分析报告
2. 确认通用/特有功能点分类
3. 如需调整，编辑 `config/feature_groups.json`
4. 重新生成测试用例

### 3. 日常维护

- **新增需求**: 放入 SRS/目录，重新运行生成脚本
- **修改需求**: 修改 SRS 文件，重新运行生成脚本
- **删除需求**: 从 SRS/删除文件，重新运行生成脚本

### 4. 用例优化

- **补充细节**: 手动编辑测试用例，添加详细步骤
- **调整优先级**: 根据业务重要性调整 P0/P1/P2/P3
- **添加标签**: 可自定义标签如 `@smoke`, `@regression`

## 依赖安装

### 必需依赖

```bash
# 安装 Python 依赖
pip install scikit-learn
```

### 可选依赖

```bash
# Excel 转换
pip install openpyxl

# 思维导图
npm install -g markmap-cli
```

## 脚本说明

### feature_deduplication.py

**功能**: 功能点去重分析

**输入**: SRS/目录下所有需求文档

**输出**:
- `config/feature_groups.json`
- `reports/feature_analysis.md`

**参数**:
- `similarity_threshold`: 相似度阈值 (默认 0.7)
- `min_common_modules`: 最小通用模块数 (默认 2)

### generate_test_cases_enhanced.py

**功能**: 批量生成测试用例

**输入**: `config/feature_groups.json`

**输出**:
- `case_MD/0_用例复用.md`
- `case_MD/<模块名>_测试用例.md`
- `reports/test_cases_statistics.md`

**特点**:
- 自动调用 `feature_deduplication.py`
- 根据分组结果生成用例
- 自动建立引用关系

### md_to_excel.py

**功能**: Markdown 转 Excel

**输入**: Markdown 测试用例文件

**输出**: Excel 测试用例文件

**参数**:
- `input`: 输入文件路径
- `output`: 输出文件路径 (可选)
- `--prefix`: 用例编号前缀 (默认 DH)

## 版本历史

### v2.0 (当前版本) - 增强版

- ✅ 新增功能点智能去重机制
- ✅ 新增通用/特有用例分离
- ✅ 新增批量生成优化
- ✅ 新增重复用例检测
- ✅ 新增配置化管理

### v1.0 - 基础版

- 基础测试用例生成功能
- 支持 Excel 转换
- 支持思维导图可视化

## 技术支持

如有问题，请查看:
- `SKILL.md` - 技能详细说明
- `references/` - 参考模板
- `reports/` - 生成的报告
