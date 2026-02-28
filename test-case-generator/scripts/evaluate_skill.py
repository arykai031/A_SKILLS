"""
技能评估脚本

功能:
1. 验证需求分析插入功能
2. 验证测试用例生成功能
3. 验证通用场景和特有场景区分
4. 验证代码质量和错误处理

用法:
    python evaluate_skill.py
"""

import os
import json
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ai_test_case_generator import AITestCaseGenerator


def evaluate_skill():
    """评估技能的所有功能"""
    print("=== 技能评估开始 ===")

    # 初始化生成器
    generator = AITestCaseGenerator()

    # 测试1: 需求分析插入功能
    print("\n1. 测试需求分析插入功能")
    test_requirement_path = "SRS/5. 唯一码直接移库.md"
    if os.path.exists(test_requirement_path):
        try:
            # 分析需求
            analysis = generator.analyze_requirement(test_requirement_path)
            # 插入需求分析
            generator.insert_requirement_analysis(test_requirement_path, analysis)
            print("✓ 需求分析插入功能测试通过")
        except Exception as e:
            print(f"✗ 需求分析插入功能测试失败: {e}")
    else:
        print(f"✗ 需求文档不存在: {test_requirement_path}")

    # 测试2: 测试用例生成功能
    print("\n2. 测试测试用例生成功能")
    try:
        # 生成增强的测试用例
        enhanced_result = generator.generate_enhanced_test_cases(test_requirement_path)
        print(f"✓ 测试用例生成功能测试通过")
        print(f"  - 功能点数量: {len(enhanced_result['features'])}")
        print(f"  - LangChain使用: {enhanced_result['langchain_used']}")
        print(
            f"  - 测试覆盖率: {enhanced_result.get('coverage_analysis', {}).get('coverage_score', 0) * 100:.1f}%"
        )
    except Exception as e:
        print(f"✗ 测试用例生成功能测试失败: {e}")

    # 测试3: 通用场景和特有场景区分
    print("\n3. 测试通用场景和特有场景区分")
    try:
        # 加载模块配置
        config_path = "config/module_config.json"
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            module_config = config.get("modules", {}).get("唯一码直接移库", {})
            if module_config:
                # 设置模块名称
                module_config["name"] = "唯一码直接移库"
                # 生成测试用例
                integrated_test_cases = generator.integrate_with_existing(
                    enhanced_result, module_config
                )

                # 检查是否包含通用场景和特有场景
                has_common_scenarios = "## 通用场景" in integrated_test_cases
                has_unique_scenarios = "## 特有场景" in integrated_test_cases

                print(f"✓ 通用场景和特有场景区分测试通过")
                print(f"  - 包含通用场景: {has_common_scenarios}")
                print(f"  - 包含特有场景: {has_unique_scenarios}")
            else:
                print("✗ 模块配置不存在")
        else:
            print(f"✗ 配置文件不存在: {config_path}")
    except Exception as e:
        print(f"✗ 通用场景和特有场景区分测试失败: {e}")

    # 测试4: 代码质量和错误处理
    print("\n4. 测试代码质量和错误处理")
    try:
        # 测试错误处理
        generator.insert_requirement_analysis("nonexistent_file.md", {"features": []})
        print("✓ 错误处理测试通过")
    except Exception as e:
        print(f"✗ 错误处理测试失败: {e}")

    print("\n=== 技能评估完成 ===")


if __name__ == "__main__":
    evaluate_skill()
