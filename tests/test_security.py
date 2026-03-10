#!/usr/bin/env python3
"""
新 MCP schema 下的安全与构造测试
"""

import sys
import os
import json
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

import bulk_add_fields
import import_records


class TestResolveSafePath(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.allowed_file = self.test_dir / 'allowed.json'
        self.allowed_file.write_text('[]')
        self.sub_dir = self.test_dir / 'subdir'
        self.sub_dir.mkdir()
        self.sub_file = self.sub_dir / 'data.csv'
        self.sub_file.write_text('a,b\n1,2')

    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_relative_path_within_root(self):
        original_cwd = os.getcwd()
        try:
            os.chdir(self.test_dir)
            result = bulk_add_fields.resolve_safe_path('allowed.json', str(self.test_dir))
            self.assertEqual(result, self.allowed_file.resolve())
        finally:
            os.chdir(original_cwd)

    def test_subdirectory_path(self):
        original_cwd = os.getcwd()
        try:
            os.chdir(self.test_dir)
            result = bulk_add_fields.resolve_safe_path('subdir/data.csv', str(self.test_dir))
            self.assertEqual(result, self.sub_file.resolve())
        finally:
            os.chdir(original_cwd)

    def test_absolute_path_within_root(self):
        result = bulk_add_fields.resolve_safe_path(str(self.allowed_file), str(self.test_dir))
        self.assertEqual(result, self.allowed_file.resolve())

    def test_path_traversal_attack(self):
        with self.assertRaises(ValueError):
            bulk_add_fields.resolve_safe_path('../etc/passwd', str(self.test_dir))

    def test_absolute_path_outside_root(self):
        with self.assertRaises(ValueError):
            bulk_add_fields.resolve_safe_path('/etc/passwd', str(self.test_dir))


class TestResourceIdValidation(unittest.TestCase):
    def test_valid_resource_id(self):
        valid_ids = [
            '123e4567-e89b-12d3-a456-426614174000',
            'base_example_id_12345678',
            'tblABC123_-xyz789',
            'fld_example_12345678\n',
        ]
        for resource_id in valid_ids:
            with self.subTest(resource_id=resource_id):
                self.assertTrue(bulk_add_fields.validate_resource_id(resource_id))
                self.assertTrue(import_records.validate_resource_id(resource_id))

    def test_invalid_resource_id(self):
        invalid_ids = ['', 'short', '含中文', 'has space', 'bad/char', 'a' * 129]
        for resource_id in invalid_ids:
            with self.subTest(resource_id=resource_id):
                self.assertFalse(bulk_add_fields.validate_resource_id(resource_id))
                self.assertFalse(import_records.validate_resource_id(resource_id))


class TestFileExtensionValidation(unittest.TestCase):
    def test_allowed_extensions(self):
        self.assertTrue(bulk_add_fields.validate_file_extension('test.json', ['.json']))
        self.assertTrue(import_records.validate_file_extension('test.csv', ['.csv']))
        self.assertTrue(import_records.validate_file_extension('test.JSON', ['.json']))

    def test_disallowed_extensions(self):
        self.assertFalse(bulk_add_fields.validate_file_extension('test.txt', ['.json']))
        self.assertFalse(import_records.validate_file_extension('test.exe', ['.csv']))


class TestSafeJsonLoad(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_valid_json(self):
        test_file = self.test_dir / 'valid.json'
        data = [{'fieldName': 'test', 'type': 'text'}]
        test_file.write_text(json.dumps(data))
        self.assertEqual(bulk_add_fields.safe_json_load(test_file), data)

    def test_invalid_json(self):
        test_file = self.test_dir / 'invalid.json'
        test_file.write_text('{invalid json}')
        with self.assertRaises(json.JSONDecodeError):
            bulk_add_fields.safe_json_load(test_file)


class TestFieldConfigValidation(unittest.TestCase):
    def test_valid_field_configs(self):
        valid_configs = [
            {'fieldName': '姓名', 'type': 'text'},
            {'name': '数量', 'type': 'number'},
            {'fieldName': '状态', 'type': 'singleSelect', 'config': {'options': [{'name': '高'}]}},
            {'fieldName': '电话', 'type': 'phone'},
            {'fieldName': '负责人', 'type': 'user', 'config': {'multiple': False}},
        ]
        for config in valid_configs:
            valid, error = bulk_add_fields.validate_field_config(config)
            self.assertTrue(valid, f'{config} should be valid: {error}')

    def test_invalid_field_configs(self):
        invalid_configs = [
            {'type': 'text'},
            {'fieldName': ''},
            {'fieldName': '状态', 'type': 'singleSelect'},
            {'fieldName': '关联', 'type': 'bidirectionalLink', 'config': {}},
            {'fieldName': 'X', 'type': 'invalid_type'},
        ]
        for config in invalid_configs:
            valid, _ = bulk_add_fields.validate_field_config(config)
            self.assertFalse(valid)


class TestRecordValidation(unittest.TestCase):
    def test_valid_record(self):
        self.assertTrue(import_records.validate_record({'cells': {'fldName': '张三'}}, [])[0])
        self.assertTrue(import_records.validate_record({'fldName': '张三'}, [])[0])

    def test_invalid_record(self):
        self.assertFalse(import_records.validate_record({}, [])[0])
        self.assertFalse(import_records.validate_record({'cells': {}}, [])[0])
        self.assertFalse(import_records.validate_record('bad', [])[0])


class TestSanitizeRecordValue(unittest.TestCase):
    def test_string_and_number(self):
        self.assertEqual(import_records.sanitize_record_value('hello'), 'hello')
        self.assertEqual(import_records.sanitize_record_value('123'), 123)
        self.assertEqual(import_records.sanitize_record_value('123.45'), 123.45)

    def test_bool_and_empty(self):
        self.assertIs(import_records.sanitize_record_value('true'), True)
        self.assertIs(import_records.sanitize_record_value('false'), False)
        self.assertIsNone(import_records.sanitize_record_value('   '))
        self.assertIsNone(import_records.sanitize_record_value(None))


class TestPayloadBuilders(unittest.TestCase):
    def test_build_create_fields_payload(self):
        payload = bulk_add_fields.build_create_fields_payload('base12345', 'table12345', [
            {'name': '电话', 'type': 'phone'},
            {'fieldName': '状态', 'type': 'singleSelect', 'config': {'options': [{'name': '高'}]}}
        ])
        self.assertEqual(payload['baseId'], 'base12345')
        self.assertEqual(payload['tableId'], 'table12345')
        self.assertEqual(payload['fields'][0]['fieldName'], '电话')
        self.assertEqual(payload['fields'][0]['type'], 'telephone')

    def test_build_create_records_payload(self):
        payload = import_records.build_create_records_payload('base12345', 'table12345', [
            {'cells': {'fldName': '张三', 'fldAge': '25'}},
            {'fldName': '李四', 'fldActive': 'true'}
        ])
        self.assertEqual(payload['baseId'], 'base12345')
        self.assertEqual(payload['tableId'], 'table12345')
        self.assertEqual(payload['records'][0]['cells']['fldAge'], 25)
        self.assertEqual(payload['records'][1]['cells']['fldActive'], True)


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        os.environ['OPENCLAW_WORKSPACE'] = str(self.test_dir)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
        os.environ.pop('OPENCLAW_WORKSPACE', None)

    def test_bulk_add_fields_workflow(self):
        fields_file = self.test_dir / 'fields.json'
        fields = [
            {'fieldName': '任务名', 'type': 'text'},
            {'fieldName': '优先级', 'type': 'singleSelect', 'config': {'options': [{'name': '高'}]}},
        ]
        fields_file.write_text(json.dumps(fields), encoding='utf-8')
        loaded = bulk_add_fields.safe_json_load(fields_file)
        payload = bulk_add_fields.build_create_fields_payload('base12345', 'table12345', loaded)
        self.assertEqual(len(payload['fields']), 2)

    def test_import_records_workflow(self):
        csv_file = self.test_dir / 'data.csv'
        csv_file.write_text('fldName,fldAge\nzhangsan,25\nlisi,30', encoding='utf-8')
        rows = import_records.safe_csv_load(csv_file)
        payload = import_records.build_create_records_payload('base12345', 'table12345', rows)
        self.assertEqual(len(payload['records']), 2)
        self.assertEqual(payload['records'][0]['cells']['fldAge'], 25)


if __name__ == '__main__':
    unittest.main(verbosity=2)
