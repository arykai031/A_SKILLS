"""
批量生成测试用例工具 (增强版)

功能:
1. 先执行功能点去重分析
2. 根据功能点分组结果生成测试用例
3. 通用用例写入 0_用例复用.md
4. 特有用例写入各模块文件

用法:
    python generate_test_cases_enhanced.py

依赖:
    - feature_deduplication.py: 功能点去重工具
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any


class TestCaseGenerator:
    """测试用例生成器"""

    def __init__(self):
        self.config_path = "config/feature_groups.json"
        self.config = None
        self.stats = {
            "total_features": 0,
            "common_features": 0,
            "unique_features": 0,
            "total_test_cases": 0,
            "common_test_cases": 0,
            "unique_test_cases": 0
        }

    def load_config(self) -> bool:
        """加载功能点分组配置"""
        if not os.path.exists(self.config_path):
            print(f"❌ 配置文件不存在：{self.config_path}")
            print("请先运行：python feature_deduplication.py")
            return False

        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        print(f"✅ 已加载配置文件：{self.config_path}")
        return True

    def generate_all_test_cases(self):
        """生成所有测试用例"""
        if not self.load_config():
            return

        print()
        print("=" * 80)
        print("开始生成测试用例")
        print("=" * 80)
        print()

        # 1. 生成通用测试用例
        print("📝 步骤 1: 生成通用测试用例...")
        self._generate_common_test_cases()

        # 2. 生成模块特有测试用例
        print()
        print("📝 步骤 2: 生成模块特有测试用例...")
        self._generate_unique_test_cases()

        # 3. 生成统计报告
        print()
        print("📊 步骤 3: 生成统计报告...")
        self._generate_statistics_report()

        print()
        print("=" * 80)
        print("✅ 测试用例生成完成!")
        print("=" * 80)

    def _generate_common_test_cases(self):
        """生成通用测试用例"""
        common_groups = [
            g for g in self.config['feature_groups']
            if g['type'] == 'common'
        ]

        if not common_groups:
            print("   ⚠️  无通用功能点，跳过通用测试用例生成")
            return

        print(f"   找到 {len(common_groups)} 个通用功能点组")

        # 生成通用测试用例文件
        output_path = "case_MD/0_用例复用.md"
        os.makedirs("case_MD", exist_ok=True)

        content = []
        content.append("# 通用测试用例\n")
        content.append("> 本文件包含跨模块复用的通用测试用例，适用于多个业务模块\n")
        content.append(">\n")
        content.append("> **使用说明**:\n")
        content.append("> - 本文件的测试用例可被多个模块复用\n")
        content.append("> - 模块特有测试用例请参考对应的 `XX_测试用例.md` 文件\n")
        content.append("> - 执行测试时，先执行本文件的通用用例，再执行模块特有用例\n")
        content.append("\n---\n\n")

        for group in common_groups:
            content.append(f"## {group['feature_name']} (跨模块复用)\n\n")
            content.append(f"**适用模块**: {'、'.join(group['modules'])}\n\n")
            content.append(f"**共性场景**:\n")
            for aspect in group['aspects'].get('common', [])[:5]:
                content.append(f"- {aspect}\n")
            content.append("\n")

            # 生成示例测试用例 (这里简化处理，实际需要 AI 生成)
            content.append(f"\n### {group['feature_name']}验证\n\n")
            content.append(f"- [P1] 用户已登录 PDA 系统;已进入对应模块页面 | 执行{group['feature_name']}操作 | 功能正常执行;返回预期结果\n\n")
            content.append(f"- [P2] 用户已登录 PDA 系统;输入异常数据 | 执行{group['feature_name']}操作 | 系统提示错误信息;操作失败\n\n")

            content.append("---\n\n")

            self.stats['common_test_cases'] += 2  # 每个功能点生成 2 个示例用例

        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(content)

        print(f"   ✅ 通用测试用例已生成：{output_path}")
        print(f"      共 {len(common_groups)} 个功能点，约 {self.stats['common_test_cases']} 条测试用例")

    def _generate_unique_test_cases(self):
        """生成模块特有测试用例"""
        unique_groups = [
            g for g in self.config['feature_groups']
            if g['type'] == 'unique'
        ]

        if not unique_groups:
            print("   ⚠️  无特有功能点，跳过模块特有测试用例生成")
            return

        # 按模块分组
        modules_dict: Dict[str, List] = {}
        for group in unique_groups:
            module = group['modules'][0]
            if module not in modules_dict:
                modules_dict[module] = []
            modules_dict[module].append(group)

        print(f"   找到 {len(unique_groups)} 个特有功能点，涉及 {len(modules_dict)} 个模块")

        # 为每个模块生成测试用例文件
        for module, groups in modules_dict.items():
            output_path = f"case_MD/{module}_测试用例.md"
            os.makedirs("case_MD", exist_ok=True)

            content = []
            content.append(f"# {module}\n\n")
            content.append(f"> 本文件包含 {module} 模块的特有测试用例\n")
            content.append(">\n")
            content.append(f"> **注意**: 本模块复用了以下通用测试用例，请在执行测试时参考 `0_用例复用.md`\n")
            content.append(">\n")

            # 列出复用的通用用例
            common_features = [
                g['feature_name'] for g in self.config['feature_groups']
                if g['type'] == 'common' and module in g['modules']
            ]
            if common_features:
                content.append(f"> - 复用通用用例：{', '.join(common_features)}\n")
            content.append("\n---\n\n")

            # 生成特有功能点测试用例
            for group in groups:
                content.append(f"## {group['feature_name']}\n\n")
                content.append(f"**功能描述**: {group['feature_name']}功能\n\n")

                # 生成示例测试用例
                content.append(f"### {group['feature_name']}正常流程\n\n")
                content.append(f"- [P0] 用户已登录 PDA 系统;已进入{module}页面 | 执行{group['feature_name']}正常操作 | 功能正常执行;返回预期结果\n\n")

                content.append(f"### {group['feature_name']}异常流程\n\n")
                content.append(f"- [P1] 用户已登录 PDA 系统;输入异常数据 | 执行{group['feature_name']}操作 | 系统提示错误信息;操作失败\n\n")

                content.append("---\n\n")

                self.stats['unique_test_cases'] += 2  # 每个功能点生成 2 个示例用例

            with open(output_path, 'w', encoding='utf-8') as f:
                f.writelines(content)

            print(f"   ✅ 模块测试用例已生成：{output_path}")
            print(f"      共 {len(groups)} 个功能点，约 {len(groups) * 2} 条测试用例")

    def _generate_statistics_report(self):
        """生成统计报告"""
        self.stats['total_features'] = self.config['summary']['total_features']
        self.stats['common_features'] = self.config['summary']['common_features_count']
        self.stats['unique_features'] = self.config['summary']['unique_features_count']
        self.stats['total_test_cases'] = self.stats['common_test_cases'] + self.stats['unique_test_cases']

        report_path = "reports/test_cases_statistics.md"
        os.makedirs("reports", exist_ok=True)

        content = []
        content.append("# 测试用例生成统计报告\n\n")
        content.append(f"**生成时间**: {self.config['generated_at']}\n\n")
        content.append("---\n\n")

        content.append("## 总体统计\n\n")
        content.append(f"- **总功能点数**: {self.stats['total_features']}\n")
        content.append(f"- **通用功能点**: {self.stats['common_features']} ({self.stats['common_features']*100//max(self.stats['total_features'], 1)}%)\n")
        content.append(f"- **特有功能点**: {self.stats['unique_features']} ({self.stats['unique_features']*100//max(self.stats['total_features'], 1)}%)\n")
        content.append(f"- **总测试用例数**: {self.stats['total_test_cases']}\n\n")

        content.append("## 用例分布\n\n")
        content.append(f"- **通用测试用例** (0_用例复用.md): {self.stats['common_test_cases']} 条 ({self.stats['common_test_cases']*100//max(self.stats['total_test_cases'], 1)}%)\n")
        content.append(f"- **模块特有测试用例**: {self.stats['unique_test_cases']} 条 ({self.stats['unique_test_cases']*100//max(self.stats['total_test_cases'], 1)}%)\n\n")

        content.append("## 去重效果\n\n")
        content.append(f"- **识别重复功能点**: {self.stats['common_features']} 组\n")
        content.append(f"- **避免重复用例**: 约 {self.stats['common_features'] * 3} 条 (估算)\n")
        content.append(f"- **用例精简率**: {self.stats['common_features']*100//max(self.stats['total_features'], 1)}%\n\n")

        content.append("## 模块分布\n\n")
        for module in self.config['summary']['modules_analyzed']:
            module_groups = [
                g for g in self.config['feature_groups']
                if module in g['modules'] and g['type'] == 'unique'
            ]
            content.append(f"- **{module}**: {len(module_groups)} 个特有功能点\n")

        content.append("\n---\n\n")
        content.append("## 下一步行动\n\n")
        content.append("1. [ ] 审核生成的测试用例\n")
        content.append("2. [ ] 补充详细测试步骤和预期结果\n")
        content.append("3. [ ] 转换为 Excel 格式 (可选)\n")
        content.append("4. [ ] 导入测试管理工具\n")

        with open(report_path, 'w', encoding='utf-8') as f:
            f.writelines(content)

        print(f"   ✅ 统计报告已生成：{report_path}")

        # 打印摘要
        print()
        print("📊 统计摘要:")
        print(f"   总功能点：{self.stats['total_features']}")
        print(f"   通用功能点：{self.stats['common_features']} ({self.stats['common_features']*100//max(self.stats['total_features'], 1)}%)")
        print(f"   特有功能点：{self.stats['unique_features']} ({self.stats['unique_features']*100//max(self.stats['total_features'], 1)}%)")
        print(f"   总测试用例：{self.stats['total_test_cases']}")
        print(f"   用例精简率：{self.stats['common_features']*100//max(self.stats['total_features'], 1)}%")


def main():
    """主函数"""
    print("=" * 80)
    print("批量生成测试用例工具 (增强版) v2.0")
    print("=" * 80)
    print()

    # 1. 先执行功能点去重
    print("🔍 步骤 1: 执行功能点去重分析...")
    print()

    dedup_script = Path(__file__).parent / "feature_deduplication.py"
    if dedup_script.exists():
        result = subprocess.run(
            ["python", str(dedup_script)],
            cwd=str(Path(__file__).parent.parent.parent.parent),
            check=False
        )

        if result.returncode != 0:
            print("❌ 功能点去重失败，请检查错误信息")
            return
    else:
        print(f"⚠️  去重脚本不存在：{dedup_script}")
        print("请手动运行：python feature_deduplication.py")
        return

    print()
    print("=" * 80)
    print()

    # 2. 生成测试用例
    print("📝 步骤 2: 生成测试用例...")
    print()

    generator = TestCaseGenerator()
    generator.generate_all_test_cases()


if __name__ == "__main__":
    main()
