#!/usr/bin/env python3
"""
安全功能测试用例

测试脚本的安全加固功能：
1. 路径安全限制 (resolve_safe_path)
2. UUID 格式验证
3. 文件扩展名验证
4. 文件大小限制
5. JSON/CSV 安全加载
6. 字段配置验证
"""

import sys
import os
import json
import tempfile
import unittest
from pathlib import Path

# 添加 scripts 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

# 导入被测试模块
import bulk_add_fields
import import_records


class TestResolveSafePath(unittest.TestCase):
    """测试路径安全限制功能"""
    
    def setUp(self):
        """设置测试环境"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.allowed_file = self.test_dir / "allowed.json"
        self.allowed_file.write_text('[]')
        
        # 创建子目录和文件
        self.sub_dir = self.test_dir / "subdir"
        self.sub_dir.mkdir()
        self.sub_file = self.sub_dir / "data.csv"
        self.sub_file.write_text('a,b\n1,2')
    
    def tearDown(self):
        """清理测试文件"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_relative_path_within_root(self):
        """测试：相对路径在允许范围内 - 应成功"""
        original_cwd = os.getcwd()
        try:
            os.chdir(self.test_dir)
            # 设置允许根目录为当前测试目录
            result = bulk_add_fields.resolve_safe_path("allowed.json", str(self.test_dir))
            self.assertEqual(result, self.allowed_file.resolve())
        finally:
            os.chdir(original_cwd)
    
    def test_subdirectory_path(self):
        """测试：子目录路径在允许范围内 - 应成功"""
        original_cwd = os.getcwd()
        try:
            os.chdir(self.test_dir)
            result = bulk_add_fields.resolve_safe_path("subdir/data.csv", str(self.test_dir))
            self.assertEqual(result, self.sub_file.resolve())
        finally:
            os.chdir(original_cwd)
    
    def test_absolute_path_within_root(self):
        """测试：绝对路径在允许范围内 - 应成功"""
        result = bulk_add_fields.resolve_safe_path(str(self.allowed_file), str(self.test_dir))
        self.assertEqual(result, self.allowed_file.resolve())
    
    def test_path_traversal_attack(self):
        """测试：目录遍历攻击 - 应拒绝"""
        with self.assertRaises(ValueError) as context:
            bulk_add_fields.resolve_safe_path("../etc/passwd", str(self.test_dir))
        self.assertIn("路径超出允许范围", str(context.exception))
    
    def test_path_traversal_with_dots(self):
        """测试：多层目录遍历攻击 - 应拒绝"""
        with self.assertRaises(ValueError) as context:
            bulk_add_fields.resolve_safe_path("../../etc/passwd", str(self.test_dir))
        self.assertIn("路径超出允许范围", str(context.exception))
    
    def test_absolute_path_outside_root(self):
        """测试：绝对路径超出允许范围 - 应拒绝"""
        with self.assertRaises(ValueError) as context:
            bulk_add_fields.resolve_safe_path("/etc/passwd", str(self.test_dir))
        self.assertIn("路径超出允许范围", str(context.exception))
    
    def test_default_allowed_root(self):
        """测试：未指定允许根目录时使用环境变量或当前目录"""
        # 保存原环境变量
        original_env = os.environ.get('OPENCLAW_WORKSPACE')
        original_cwd = os.getcwd()
        
        try:
            # 清除环境变量
            if 'OPENCLAW_WORKSPACE' in os.environ:
                del os.environ['OPENCLAW_WORKSPACE']
            
            os.chdir(self.test_dir)
            # 应该使用当前目录作为允许根目录
            result = bulk_add_fields.resolve_safe_path("allowed.json")
            self.assertEqual(result, self.allowed_file.resolve())
        finally:
            # 恢复环境变量
            if original_env:
                os.environ['OPENCLAW_WORKSPACE'] = original_env
            os.chdir(original_cwd)


class TestUUIDValidation(unittest.TestCase):
    """测试 UUID 格式验证功能"""
    
    def test_valid_uuid(self):
        """测试：有效的 UUID"""
        valid_uuids = [
            "123e4567-e89b-12d3-a456-426614174000",
            "123E4567-E89B-12D3-A456-426614174000",  # 大写
            "123e4567-e89b-12d3-a456-426614174000\n",  # 带换行
        ]
        for uuid in valid_uuids:
            with self.subTest(uuid=uuid):
                self.assertTrue(bulk_add_fields.validate_uuid(uuid))
    
    def test_invalid_uuid(self):
        """测试：无效的 UUID"""
        invalid_uuids = [
            "",
            "not-a-uuid",
            "123e4567-e89b-12d3-a456",  # 太短
            "123e4567e89b12d3a456426614174000",  # 无连字符
            "123e4567-e89b-12d3-a456-426614174000-extra",  # 太长
            "123e4567-e89b-12d3-a456-42661417400g",  # 无效字符
        ]
        for uuid in invalid_uuids:
            with self.subTest(uuid=uuid):
                self.assertFalse(bulk_add_fields.validate_uuid(uuid))


class TestFileExtensionValidation(unittest.TestCase):
    """测试文件扩展名验证功能"""
    
    def test_allowed_extensions(self):
        """测试：允许的扩展名"""
        self.assertTrue(bulk_add_fields.validate_file_extension("test.json", ['.json']))
        self.assertTrue(bulk_add_fields.validate_file_extension("test.JSON", ['.json']))  # 大写
        self.assertTrue(import_records.validate_file_extension("test.csv", ['.csv']))
        self.assertTrue(import_records.validate_file_extension("test.CSV", ['.csv']))
    
    def test_disallowed_extensions(self):
        """测试：不允许的扩展名"""
        self.assertFalse(bulk_add_fields.validate_file_extension("test.txt", ['.json']))
        self.assertFalse(bulk_add_fields.validate_file_extension("test.csv", ['.json']))
        self.assertFalse(bulk_add_fields.validate_file_extension("test.json.exe", ['.json']))
        self.assertFalse(bulk_add_fields.validate_file_extension("test", ['.json']))  # 无扩展名


class TestSafeJsonLoad(unittest.TestCase):
    """测试 JSON 安全加载功能"""
    
    def setUp(self):
        """设置测试文件"""
        self.test_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """清理测试文件"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_valid_json(self):
        """测试：有效的 JSON 文件"""
        test_file = self.test_dir / "valid.json"
        test_data = [{"name": "test", "type": "text"}]
        test_file.write_text(json.dumps(test_data))
        
        result = bulk_add_fields.safe_json_load(test_file)
        self.assertEqual(result, test_data)
    
    def test_file_size_limit(self):
        """测试：文件大小限制"""
        test_file = self.test_dir / "large.json"
        # 创建一个超过限制的文件
        large_data = "x" * (bulk_add_fields.MAX_FILE_SIZE + 1)
        test_file.write_text(large_data)
        
        with self.assertRaises(ValueError) as context:
            bulk_add_fields.safe_json_load(test_file)
        self.assertIn("文件过大", str(context.exception))
    
    def test_invalid_json(self):
        """测试：无效的 JSON 格式"""
        test_file = self.test_dir / "invalid.json"
        test_file.write_text('{invalid json}')
        
        with self.assertRaises(json.JSONDecodeError):
            bulk_add_fields.safe_json_load(test_file)


class TestFieldConfigValidation(unittest.TestCase):
    """测试字段配置验证功能"""
    
    def test_valid_field_configs(self):
        """测试：有效的字段配置"""
        valid_configs = [
            {"name": "姓名", "type": "text"},
            {"name": "数量", "type": "number"},
            {"name": "状态", "type": "singleSelect"},
            {"name": "标签", "type": "multipleSelect"},
            {"name": "日期", "type": "date"},
            {"name": "负责人", "type": "user"},
            {"name": "文件", "type": "attachment"},
            {"name": "复选", "type": "checkbox"},
            {"name": "电话", "type": "phone"},
            {"name": "邮箱", "type": "email"},
            {"name": "网址", "type": "url"},
            {"name": "默认类型"},  # 无 type，应使用默认值 text
        ]
        for config in valid_configs:
            with self.subTest(config=config):
                valid, error = bulk_add_fields.validate_field_config(config)
                self.assertTrue(valid, f"配置 {config} 应有效：{error}")
    
    def test_invalid_field_configs(self):
        """测试：无效的字段配置"""
        invalid_configs = [
            ({"type": "text"}, "缺少 name"),  # 缺少 name
            ({"name": ""}, "空 name"),  # 空 name
            ({"name": "   "}, "空白 name"),  # 空白 name
            ({"name": "test", "type": "invalid_type"}, "无效类型"),
            ("not a dict", "不是对象"),  # 不是字典
            ([], "是数组"),  # 是数组
        ]
        for config, description in invalid_configs:
            with self.subTest(description=description):
                valid, error = bulk_add_fields.validate_field_config(config)
                self.assertFalse(valid, f"配置 {config} ({description}) 应无效")


class TestRecordValidation(unittest.TestCase):
    """测试记录验证功能（import_records）"""
    
    def test_valid_record(self):
        """测试：有效的记录"""
        record = {"fields": {"姓名": "张三", "年龄": 25}}
        valid, error = import_records.validate_record(record, [])
        self.assertTrue(valid, f"记录应有效：{error}")
    
    def test_invalid_record(self):
        """测试：无效的记录"""
        invalid_records = [
            ("not a dict", "不是对象"),
            ({}, "缺少 fields"),
            ({"fields": "not a dict"}, "fields 不是对象"),
            ({"fields": {}}, "fields 为空"),
        ]
        for record, description in invalid_records:
            with self.subTest(description=description):
                valid, error = import_records.validate_record(record, [])
                self.assertFalse(valid, f"记录 {record} ({description}) 应无效")


class TestSanitizeRecordValue(unittest.TestCase):
    """测试记录值清理功能"""
    
    def test_string_value(self):
        """测试：字符串值保持不变"""
        self.assertEqual(import_records.sanitize_record_value("hello"), "hello")
    
    def test_integer_value(self):
        """测试：整数字符串转换为整数"""
        self.assertEqual(import_records.sanitize_record_value("123"), 123)
        self.assertEqual(import_records.sanitize_record_value("-456"), -456)
    
    def test_float_value(self):
        """测试：浮点数字符串转换为浮点数"""
        self.assertEqual(import_records.sanitize_record_value("123.45"), 123.45)
        self.assertEqual(import_records.sanitize_record_value("-3.14"), -3.14)
    
    def test_empty_value(self):
        """测试：空值返回 None"""
        self.assertIsNone(import_records.sanitize_record_value(""))
        self.assertIsNone(import_records.sanitize_record_value("   "))
        self.assertIsNone(import_records.sanitize_record_value(None))
    
    def test_whitespace_trimming(self):
        """测试：自动去除首尾空白"""
        self.assertEqual(import_records.sanitize_record_value("  hello  "), "hello")


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.test_dir = Path(tempfile.mkdtemp())
        os.environ['OPENCLAW_WORKSPACE'] = str(self.test_dir)
    
    def tearDown(self):
        """清理测试文件"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
        # 恢复环境变量
        if 'OPENCLAW_WORKSPACE' in os.environ:
            del os.environ['OPENCLAW_WORKSPACE']
    
    def test_bulk_add_fields_workflow(self):
        """测试：bulk_add_fields 完整工作流程"""
        # 创建测试文件
        fields_file = self.test_dir / "fields.json"
        fields_data = [
            {"name": "字段 1", "type": "text"},
            {"name": "字段 2", "type": "number"},
        ]
        fields_file.write_text(json.dumps(fields_data))
        
        # 验证路径解析
        safe_path = bulk_add_fields.resolve_safe_path(str(fields_file))
        self.assertEqual(safe_path, fields_file.resolve())
        
        # 验证 UUID
        self.assertTrue(bulk_add_fields.validate_uuid("123e4567-e89b-12d3-a456-426614174000"))
        
        # 验证文件扩展名
        self.assertTrue(bulk_add_fields.validate_file_extension(str(fields_file), ['.json']))
        
        # 验证 JSON 加载
        loaded_data = bulk_add_fields.safe_json_load(safe_path)
        self.assertEqual(loaded_data, fields_data)
        
        # 验证字段配置
        for field in loaded_data:
            valid, error = bulk_add_fields.validate_field_config(field)
            self.assertTrue(valid, f"字段配置 {field} 应有效：{error}")
    
    def test_import_records_workflow(self):
        """测试：import_records 完整工作流程"""
        # 创建测试 CSV 文件（使用英文表头避免编码问题）
        csv_file = self.test_dir / "data.csv"
        csv_content = "name,age,email\nzhangsan,25,zhangsan@example.com\nlisi,30,lisi@example.com"
        csv_file.write_text(csv_content, encoding='utf-8')
        
        # 验证路径解析
        safe_path = import_records.resolve_safe_path(str(csv_file))
        self.assertEqual(safe_path, csv_file.resolve())
        
        # 验证文件扩展名
        self.assertTrue(import_records.validate_file_extension(str(csv_file), ['.csv']))
        
        # 验证 CSV 加载
        records = import_records.safe_csv_load(safe_path)
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]['name'], 'zhangsan')
        self.assertEqual(records[1]['age'], '30')
        
        # 验证记录清理
        for record in records:
            for key, value in record.items():
                sanitized = import_records.sanitize_record_value(value)
                self.assertIsNotNone(sanitized)


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestResolveSafePath))
    suite.addTests(loader.loadTestsFromTestCase(TestUUIDValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestFileExtensionValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestSafeJsonLoad))
    suite.addTests(loader.loadTestsFromTestCase(TestFieldConfigValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestRecordValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestSanitizeRecordValue))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回结果
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
