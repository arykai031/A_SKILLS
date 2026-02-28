"""
功能点去重工具

功能:
1. 遍历所有 SRS 文档，提取功能点
2. 计算功能点相似度
3. 生成功能点分组配置
4. 生成测试用例去重报告

用法:
    python feature_deduplication.py

输出:
    - config/feature_groups.json: 功能点分组配置
    - reports/feature_analysis.md: 功能点分析报告
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from collections import defaultdict

# 尝试导入 sklearn 用于相似度计算
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("警告：sklearn 库未安装，将使用简化的相似度计算方法")
    print("请运行：pip install scikit-learn")


@dataclass
class Feature:
    """功能点数据类"""
    name: str
    description: str
    module: str
    file_path: str
    keywords: List[str]
    similarity_score: float = 0.0


@dataclass
class FeatureGroup:
    """功能点分组数据类"""
    group_id: str
    type: str  # "common" or "unique"
    feature_name: str
    modules: List[str]
    test_case_file: str
    aspects: Dict[str, Any]
    similarity_score: float = 0.0


class FeatureExtractor:
    """功能点提取器"""

    def __init__(self, srs_dir: str = "SRS"):
        self.srs_dir = srs_dir
        self.features: List[Feature] = []

    def extract_all_features(self) -> List[Feature]:
        """从所有 SRS 文档中提取功能点"""
        print(f"📖 正在遍历 SRS 目录：{self.srs_dir}")

        srs_files = list(Path(self.srs_dir).glob("*.md"))
        print(f"📁 找到 {len(srs_files)} 个需求文档")

        for file_path in srs_files:
            module_name = self._extract_module_name(file_path.name)
            features = self._extract_features_from_file(str(file_path), module_name)
            self.features.extend(features)

        print(f"✅ 共提取 {len(self.features)} 个功能点")
        return self.features

    def _extract_module_name(self, file_name: str) -> str:
        """从文件名提取模块名称"""
        # 移除数字前缀和扩展名
        name = re.sub(r'^\d+[_\.]?', '', file_name)
        name = re.sub(r'\.md$', '', name)
        return name.strip()

    def _extract_features_from_file(self, file_path: str, module_name: str) -> List[Feature]:
        """从单个文件中提取功能点"""
        features = []

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 查找功能点分析部分
        feature_pattern = r'### 功能点\d+: (.+?)\n(.*?)(?=### 功能点\d+:|$)'
        matches = re.findall(feature_pattern, content, re.DOTALL)

        for match in matches:
            feature_name = match[0].strip()
            feature_content = match[1].strip()

            # 提取功能描述
            description = self._extract_description(feature_content)

            # 提取关键词
            keywords = self._extract_keywords(feature_name, description)

            features.append(Feature(
                name=feature_name,
                description=description,
                module=module_name,
                file_path=file_path,
                keywords=keywords
            ))

        return features

    def _extract_description(self, content: str) -> str:
        """从功能点内容中提取描述"""
        # 查找"**功能描述**:"后的内容
        match = re.search(r'\*\*功能描述\*\*:(.+?)(?=\n\*\*|\Z)', content, re.DOTALL)
        if match:
            return match.group(1).strip()
        return content.split('\n')[0].strip()

    def _extract_keywords(self, name: str, description: str) -> List[str]:
        """提取关键词"""
        # 简单的关键词提取：分词 + 去除停用词
        text = name + " " + description

        # 常见停用词
        stop_words = {
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人',
            '都', '一', '一个', '中', '来', '上', '没有', '可以', '这个',
            '进行', '一个', '以及', '等', '相关', '包括', '通过', '进行'
        }

        # 简单的中文分词 (按标点和空格分割)
        words = re.split(r'[\s,;.，。；：]+', text)

        # 过滤停用词和短词
        keywords = [
            word for word in words
            if len(word) > 1 and word not in stop_words
        ]

        return keywords[:10]  # 限制最多 10 个关键词


class SimilarityCalculator:
    """相似度计算器"""

    def __init__(self, keyword_weight: float = 0.4, semantic_weight: float = 0.6):
        self.keyword_weight = keyword_weight
        self.semantic_weight = semantic_weight

    def calculate_similarity(self, feature1: Feature, feature2: Feature) -> float:
        """计算两个功能点的综合相似度"""
        # 1. 关键词相似度 (Jaccard)
        keyword_sim = self._jaccard_similarity(
            set(feature1.keywords),
            set(feature2.keywords)
        )

        # 2. 语义相似度 (TF-IDF + 余弦相似度)
        semantic_sim = self._cosine_similarity(
            feature1.description,
            feature2.description
        )

        # 3. 综合相似度
        similarity = (
            self.keyword_weight * keyword_sim +
            self.semantic_weight * semantic_sim
        )

        return round(similarity, 3)

    def _jaccard_similarity(self, set1: set, set2: set) -> float:
        """计算 Jaccard 相似度"""
        if not set1 and not set2:
            return 0.0
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union > 0 else 0.0

    def _cosine_similarity(self, text1: str, text2: str) -> float:
        """计算余弦相似度"""
        if not SKLEARN_AVAILABLE:
            # 简化版本：使用词频向量
            return self._simple_cosine_similarity(text1, text2)

        vectorizer = TfidfVectorizer()
        try:
            tfidf = vectorizer.fit_transform([text1, text2])
            sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
            return round(sim, 3)
        except Exception:
            return 0.0

    def _simple_cosine_similarity(self, text1: str, text2: str) -> float:
        """简化的余弦相似度计算 (不使用 sklearn)"""
        # 分词
        words1 = set(text1.split())
        words2 = set(text2.split())

        # 计算交集和并集
        intersection = len(words1 & words2)
        union = len(words1 | words2)

        return round(intersection / union if union > 0 else 0.0, 3)


class FeatureGrouper:
    """功能点分组器"""

    def __init__(self, similarity_threshold: float = 0.7, min_common_modules: int = 2):
        self.similarity_threshold = similarity_threshold
        self.min_common_modules = min_common_modules
        self.calculator = SimilarityCalculator()
        self.groups: List[FeatureGroup] = []

    def group_features(self, features: List[Feature]) -> List[FeatureGroup]:
        """对功能点进行分组"""
        print(f"🔍 开始功能点分组...")
        print(f"   相似度阈值：{self.similarity_threshold}")
        print(f"   最小通用模块数：{self.min_common_modules}")

        used = set()
        group_counter = 0

        for i, f1 in enumerate(features):
            if i in used:
                continue

            # 创建新组
            group_counter += 1
            group_features = [f1]
            used.add(i)

            # 查找相似功能点
            for j, f2 in enumerate(features[i + 1:], i + 1):
                if j in used:
                    continue

                similarity = self.calculator.calculate_similarity(f1, f2)

                if similarity >= self.similarity_threshold:
                    group_features.append(f2)
                    used.add(j)

            # 确定组类型
            modules = list(set(f.module for f in group_features))
            group_type = "common" if len(modules) >= self.min_common_modules else "unique"

            # 创建分组
            group = self._create_group(
                group_id=f"FG{group_counter:03d}",
                features=group_features,
                group_type=group_type
            )

            self.groups.append(group)

        common_count = sum(1 for g in self.groups if g.type == "common")
        unique_count = sum(1 for g in self.groups if g.type == "unique")

        print(f"✅ 分组完成:")
        print(f"   总组数：{len(self.groups)}")
        print(f"   通用功能点：{common_count} 组")
        print(f"   特有功能点：{unique_count} 组")

        return self.groups

    def _create_group(self, group_id: str, features: List[Feature], group_type: str) -> FeatureGroup:
        """创建功能点分组"""
        modules = list(set(f.module for f in features))

        # 提取共性场景
        common_aspects = self._extract_common_aspects(features)

        # 提取模块特定场景
        specific_aspects = self._extract_specific_aspects(features)

        # 确定测试用例文件
        test_case_file = "0_用例复用.md" if group_type == "common" else f"{modules[0]}_测试用例.md"

        # 计算平均相似度
        avg_similarity = sum(f.similarity_score for f in features) / len(features) if features else 0.0

        return FeatureGroup(
            group_id=group_id,
            type=group_type,
            feature_name=features[0].name.split('(')[0].strip(),  # 移除括号内容
            modules=modules,
            test_case_file=test_case_file,
            aspects={
                "common": common_aspects,
                "specific": specific_aspects
            },
            similarity_score=round(avg_similarity, 3)
        )

    def _extract_common_aspects(self, features: List[Feature]) -> List[str]:
        """提取共性场景"""
        # 简化实现：返回所有功能点的共同关键词
        all_keywords = [set(f.keywords) for f in features]
        if not all_keywords:
            return []

        common_keywords = set.intersection(*all_keywords)
        return list(common_keywords)[:5]

    def _extract_specific_aspects(self, features: List[Feature]) -> Dict[str, List[str]]:
        """提取模块特定场景"""
        specific = {}
        for feature in features:
            if feature.module not in specific:
                specific[feature.module] = []
            # 提取该模块特有的关键词
            specific[feature.module].append(
                f"{feature.name}: {feature.description[:50]}..."
            )
        return specific


class ConfigGenerator:
    """配置文件生成器"""

    def __init__(self, output_dir: str = "config"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_config(self, groups: List[FeatureGroup], features: List[Feature]) -> str:
        """生成配置文件"""
        config = {
            "version": "1.0",
            "generated_at": self._get_current_time(),
            "settings": {
                "similarity_threshold": 0.7,
                "min_common_modules": 2,
                "keyword_weight": 0.4,
                "semantic_weight": 0.6
            },
            "summary": {
                "total_features": len(features),
                "common_features_count": sum(1 for g in groups if g.type == "common"),
                "unique_features_count": sum(1 for g in groups if g.type == "unique"),
                "modules_analyzed": list(set(f.module for f in features))
            },
            "manual_adjustments": [],
            "feature_groups": [asdict(g) for g in groups]
        }

        output_path = os.path.join(self.output_dir, "feature_groups.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

        print(f"✅ 配置文件已生成：{output_path}")
        return output_path

    def _get_current_time(self) -> str:
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class ReportGenerator:
    """报告生成器"""

    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_analysis_report(self, groups: List[FeatureGroup], features: List[Feature]) -> str:
        """生成分析报告"""
        report = []

        # 标题
        report.append("# 功能点分析报告\n")
        report.append(f"**生成时间**: {self._get_current_time()}\n")
        report.append(f"**分析范围**: SRS/ 目录下所有需求文档\n")
        report.append("---\n\n")

        # 总体统计
        report.append("## 总体统计\n\n")
        report.append(f"- **总功能点数**: {len(features)}\n")
        common_count = sum(1 for g in groups if g.type == "common")
        unique_count = sum(1 for g in groups if g.type == "unique")
        report.append(f"- **通用功能点**: {common_count} ({common_count*100//len(groups) if groups else 0}%)\n")
        report.append(f"- **特有功能点**: {unique_count} ({unique_count*100//len(groups) if groups else 0}%)\n")
        report.append(f"- **涉及模块数**: {len(set(f.module for f in features))}\n\n")
        report.append("---\n\n")

        # 通用功能点
        report.append("## 通用功能点 (跨 2 个及以上模块)\n\n")
        for group in [g for g in groups if g.type == "common"]:
            report.append(f"### {group.group_id}: {group.feature_name}\n\n")
            report.append(f"**涉及模块**: {'、'.join(group.modules)}\n\n")
            report.append(f"**共性场景**:\n")
            for aspect in group.aspects.get("common", [])[:3]:
                report.append(f"- {aspect}\n")
            report.append(f"\n**相似度评分**: {group.similarity_score}\n\n")
            report.append(f"**建议**: 生成通用测试用例到 `0_用例复用.md`\n\n")
            report.append("---\n\n")

        # 特有功能点
        report.append("## 特有功能点 (仅单模块存在)\n\n")
        for group in [g for g in groups if g.type == "unique"]:
            report.append(f"### {group.group_id}: {group.feature_name}\n\n")
            report.append(f"**涉及模块**: {group.modules[0]}\n\n")
            report.append(f"**建议**: 生成特有测试用例到 `{group.test_case_file}`\n\n")
            report.append("---\n\n")

        # 下一步行动
        report.append("## 下一步行动\n\n")
        report.append("1. [ ] 审核可疑重复功能点\n")
        report.append("2. [ ] 确认通用功能点的共性场景提取\n")
        report.append("3. [ ] 确认特有功能点的分类\n")
        report.append("4. [ ] 生成通用测试用例\n")
        report.append("5. [ ] 生成模块特有测试用例\n")

        output_path = os.path.join(self.output_dir, "feature_analysis.md")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(report)

        print(f"✅ 分析报告已生成：{output_path}")
        return output_path

    def _get_current_time(self) -> str:
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    """主函数"""
    print("=" * 80)
    print("功能点去重工具 v2.0")
    print("=" * 80)
    print()

    # 1. 提取功能点
    extractor = FeatureExtractor()
    features = extractor.extract_all_features()

    if not features:
        print("❌ 未找到任何功能点，请检查 SRS 目录")
        return

    print()

    # 2. 功能点分组
    grouper = FeatureGrouper(
        similarity_threshold=0.7,
        min_common_modules=2
    )
    groups = grouper.group_features(features)

    print()

    # 3. 生成配置文件
    config_gen = ConfigGenerator()
    config_path = config_gen.generate_config(groups, features)

    print()

    # 4. 生成分析报告
    report_gen = ReportGenerator()
    report_path = report_gen.generate_analysis_report(groups, features)

    print()
    print("=" * 80)
    print("✅ 功能点去重完成!")
    print("=" * 80)
    print()
    print("输出文件:")
    print(f"  - 配置文件：{config_path}")
    print(f"  - 分析报告：{report_path}")
    print()
    print("下一步:")
    print("  1. 查看分析报告，确认功能点分组")
    print("  2. 根据需要调整配置文件")
    print("  3. 使用 test-case-generator 生成测试用例")


if __name__ == "__main__":
    main()
