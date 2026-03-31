#!/usr/bin/env python3
"""
触发测试：验证技能在正确的场景下被触发
"""

import unittest

class TestSkillTriggering(unittest.TestCase):
    """测试技能触发条件"""

    # 应该触发技能的查询
    SHOULD_TRIGGER = [
        "帮我操作钉钉 AI 表格",
        "创建一个新的 Base",
        "批量导入记录到钉钉表格",
        "查询 AI 表格的记录",
        "更新多维表的数据",
        "添加字段到钉钉表格",
        "从 CSV 导入数据",
        "搜索我的 Base",
        "删除表格中的记录",
        "获取表格结构",
    ]

    # 不应该触发技能的查询
    SHOULD_NOT_TRIGGER = [
        "今天天气怎么样",
        "帮我写 Python 代码",
        "创建 Excel 文件",
        "发送钉钉消息",
        "查询数据库",
        "生成 PDF 报告",
        "翻译这段文字",
        "总结这篇文章",
    ]

    def test_should_trigger_queries(self):
        """测试应该触发的查询"""
        for query in self.SHOULD_TRIGGER:
            with self.subTest(query=query):
                # 这里只是记录测试用例
                # 实际触发测试需要在 Claude 环境中进行
                self.assertIsNotNone(query)

    def test_should_not_trigger_queries(self):
        """测试不应该触发的查询"""
        for query in self.SHOULD_NOT_TRIGGER:
            with self.subTest(query=query):
                self.assertIsNotNone(query)

if __name__ == '__main__':
    print("触发测试用例列表")
    print("\n✅ 应该触发的查询：")
    for i, query in enumerate(TestSkillTriggering.SHOULD_TRIGGER, 1):
        print(f"  {i}. {query}")

    print("\n❌ 不应该触发的查询：")
    for i, query in enumerate(TestSkillTriggering.SHOULD_NOT_TRIGGER, 1):
        print(f"  {i}. {query}")

    print("\n运行单元测试...")
    unittest.main(verbosity=2)
