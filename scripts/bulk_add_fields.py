#!/usr/bin/env python3
"""
批量添加字段到钉钉 AI 表格数据表

用法:
    python bulk_add_fields.py <dentryUuid> <sheetName> fields.json

fields.json 格式:
    [
        {"name": "字段 1", "type": "text"},
        {"name": "字段 2", "type": "number"},
        {"name": "字段 3", "type": "singleSelect"}
    ]
"""

import sys
import json
import subprocess

def run_mcporter(args):
    """执行 mcporter 命令"""
    cmd = ["mcporter", "call", "dingtalk-ai-table"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"错误：{result.stderr}")
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"无法解析响应：{result.stdout}")
        return None

def bulk_add_fields(dentry_uuid, sheet_name, fields_file):
    """批量添加字段"""
    # 读取字段配置
    with open(fields_file, 'r', encoding='utf-8') as f:
        fields = json.load(f)
    
    print(f"将为数据表 '{sheet_name}' 添加 {len(fields)} 个字段...")
    
    success_count = 0
    for field in fields:
        name = field.get('name')
        field_type = field.get('type', 'text')
        
        args = json.dumps({
            "dentryUuid": dentry_uuid,
            "sheetIdOrName": sheet_name,
            "addField": {
                "name": name,
                "type": field_type
            }
        })
        
        result = run_mcporter([
            "add_base_field",
            "--args", args,
            "--output", "json"
        ])
        
        if result and result.get('success'):
            field_id = result.get('result', {}).get('id', '未知')
            print(f"✓ 添加字段：{name} ({field_type}) - ID: {field_id}")
            success_count += 1
        else:
            print(f"✗ 添加字段失败：{name}")
            if result:
                print(f"  错误：{result.get('errorMsg', '未知错误')}")
    
    print(f"\n完成：{success_count}/{len(fields)} 个字段添加成功")
    return success_count == len(fields)

def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    
    dentry_uuid = sys.argv[1]
    sheet_name = sys.argv[2]
    fields_file = sys.argv[3]
    
    success = bulk_add_fields(dentry_uuid, sheet_name, fields_file)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
