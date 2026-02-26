#!/usr/bin/env python3
"""
从 CSV 批量导入记录到钉钉 AI 表格

用法:
    python import_records.py <dentryUuid> <sheetName> data.csv

CSV 格式:
    标题，商品编号，数量，单价，分类
    MacBook Pro,MBP14-001,15,14999，电子产品
    无线鼠标，MX-003,200,699，电子配件
"""

import sys
import csv
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

def import_records(dentry_uuid, sheet_name, csv_file, batch_size=50):
    """从 CSV 批量导入记录"""
    # 读取 CSV
    records = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        for row in reader:
            records.append(row)
    
    print(f"将从 CSV 导入 {len(records)} 条记录...")
    print(f"字段：{', '.join(headers)}")
    
    success_count = 0
    fail_count = 0
    
    # 分批导入
    for i in range(0, len(records), batch_size):
        batch = records[i:i+batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (len(records) + batch_size - 1) // batch_size
        
        # 构建记录数据
        record_data = []
        for row in batch:
            fields = {}
            for key, value in row.items():
                if value.strip():  # 跳过空值
                    # 尝试转换数字
                    try:
                        if '.' in value:
                            fields[key] = float(value)
                        else:
                            fields[key] = int(value)
                    except ValueError:
                        fields[key] = value
            
            if fields:  # 只添加有字段的记录
                record_data.append({"fields": fields})
        
        if not record_data:
            continue
        
        args = json.dumps({
            "dentryUuid": dentry_uuid,
            "sheetIdOrName": sheet_name,
            "records": record_data
        }, ensure_ascii=False)
        
        result = run_mcporter([
            "add_base_record",
            "--args", args,
            "--output", "json"
        ])
        
        if result and result.get('success'):
            added = len(result.get('result', []))
            success_count += added
            print(f"✓ 批次 {batch_num}/{total_batches}: 添加 {added} 条记录")
        else:
            fail_count += len(batch)
            print(f"✗ 批次 {batch_num}/{total_batches}: 导入失败")
            if result:
                print(f"  错误：{result.get('errorMsg', '未知错误')}")
    
    print(f"\n完成：成功 {success_count} 条，失败 {fail_count} 条")
    return fail_count == 0

def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    
    dentry_uuid = sys.argv[1]
    sheet_name = sys.argv[2]
    csv_file = sys.argv[3]
    
    success = import_records(dentry_uuid, sheet_name, csv_file)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
