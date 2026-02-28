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
import os
import re
from pathlib import Path
from typing import Union, List, Dict, Any, Optional, Tuple

# 类型别名（Python 3.9 兼容）
JsonData = Union[List[Any], Dict[str, Any]]
RecordDict = Dict[str, str]

# ============== 安全常量 ==============
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB 文件限制（CSV 可能较大）
ALLOWED_CSV_EXTENSIONS = ['.csv']
ALLOWED_JSON_EXTENSIONS = ['.json']
UUID_PATTERN = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)
MAX_RECORDS_PER_BATCH = 100  # 单次批量操作最大记录数（API 限制）
DEFAULT_BATCH_SIZE = 50

# ============== 安全函数 ==============

def resolve_safe_path(path: str, allowed_root: Optional[str] = None) -> Path:
    """
    解析路径并限制在允许的工作目录内，防止目录遍历攻击
    
    Args:
        path: 用户提供的路径
        allowed_root: 允许的根目录，默认为 OPENCLAW_WORKSPACE 环境变量或当前目录
    
    Returns:
        解析后的安全路径
    
    Raises:
        ValueError: 当路径超出允许范围时
    """
    if allowed_root is None:
        allowed_root = os.environ.get('OPENCLAW_WORKSPACE', os.getcwd())
    
    allowed_root = Path(allowed_root).resolve()
    
    # 解析目标路径（处理相对路径）
    if Path(path).is_absolute():
        target_path = Path(path).resolve()
    else:
        target_path = (Path.cwd() / path).resolve()
    
    # 验证路径在允许范围内
    try:
        target_path.relative_to(allowed_root)
        return target_path
    except ValueError:
        raise ValueError(
            f"路径超出允许范围：{path}\n"
            f"目标路径：{target_path}\n"
            f"允许根目录：{allowed_root}\n"
            f"提示：设置 OPENCLAW_WORKSPACE 环境变量或确保文件在工作目录内"
        )

def validate_uuid(uuid: str) -> bool:
    """验证 UUID 格式"""
    return bool(UUID_PATTERN.match(uuid.strip()))

def validate_file_extension(filename: str, allowed_extensions: list) -> bool:
    """验证文件扩展名"""
    return any(filename.lower().endswith(ext) for ext in allowed_extensions)

def safe_csv_load(file_path: Path, max_size: int = MAX_FILE_SIZE) -> List[RecordDict]:
    """
    安全加载 CSV 文件（带大小限制）
    
    Args:
        file_path: 文件路径
        max_size: 最大文件大小（字节）
    
    Returns:
        解析后的记录列表
    
    Raises:
        ValueError: 当文件过大时
    """
    file_size = file_path.stat().st_size
    if file_size > max_size:
        raise ValueError(f"文件过大：{file_size:,} 字节 (限制：{max_size:,} 字节)")
    
    records = []
    with open(file_path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
    
    return records

def safe_json_load(file_path: Path, max_size: int = MAX_FILE_SIZE) -> JsonData:
    """
    安全加载 JSON 文件（带大小限制）
    
    Args:
        file_path: 文件路径
        max_size: 最大文件大小（字节）
    
    Returns:
        解析后的 JSON 数据
    
    Raises:
        ValueError: 当文件过大时
    """
    file_size = file_path.stat().st_size
    if file_size > max_size:
        raise ValueError(f"文件过大：{file_size:,} 字节 (限制：{max_size:,} 字节)")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def sanitize_record_value(value: str) -> Optional[Union[str, int, float]]:
    """
    清理和转换记录字段值
    
    Args:
        value: 原始字符串值
    
    Returns:
        转换后的值（字符串、数字或 None）
    """
    if not value or not value.strip():
        return None
    
    value = value.strip()
    
    # 尝试转换为数字
    try:
        if '.' in value:
            return float(value)
        else:
            return int(value)
    except ValueError:
        return value

def validate_record(record: Dict[str, Any], headers: List[str]) -> Tuple[bool, str]:
    """
    验证记录数据
    
    Returns:
        (是否有效，错误信息)
    """
    if not isinstance(record, dict):
        return False, "记录必须是对象"
    
    # 检查是否有有效字段
    fields = record.get('fields', {})
    if not fields or not isinstance(fields, dict):
        return False, "记录必须包含 fields 对象"
    
    return True, ""

# ============== 核心功能 ==============

def run_mcporter(args: List[str]) -> Optional[Dict[str, Any]]:
    """
    执行 mcporter 命令（带基础验证）
    
    Args:
        args: 命令参数列表
    
    Returns:
        解析后的 JSON 响应，失败返回 None
    """
    if not args:
        print("错误：空命令")
        return None
    
    cmd = ["mcporter", "call", "dingtalk-ai-table"] + args
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            print(f"错误：{result.stderr.strip()}")
            return None
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError as e:
            print(f"无法解析响应：{result.stdout[:200]}...")
            print(f"JSON 解析错误：{e}")
            return None
    except subprocess.TimeoutExpired:
        print("错误：命令执行超时（120 秒）")
        return None
    except FileNotFoundError:
        print("错误：未找到 mcporter 命令，请确认已安装")
        return None

def import_from_csv(dentry_uuid: str, sheet_name: str, csv_file: str, batch_size: int = DEFAULT_BATCH_SIZE) -> bool:
    """
    从 CSV 批量导入记录
    
    Args:
        dentry_uuid: 表格 UUID
        sheet_name: 数据表名称
        csv_file: CSV 文件路径
        batch_size: 每批次记录数
    
    Returns:
        是否全部成功
    """
    # 解析并验证文件路径
    try:
        safe_path = resolve_safe_path(csv_file)
    except ValueError as e:
        print(f"路径验证失败：{e}")
        return False
    
    # 验证文件扩展名
    if not validate_file_extension(csv_file, ALLOWED_CSV_EXTENSIONS):
        print(f"错误：只允许 {', '.join(ALLOWED_CSV_EXTENSIONS)} 文件")
        return False
    
    # 检查文件是否存在
    if not safe_path.exists():
        print(f"错误：文件不存在：{safe_path}")
        return False
    
    # 安全加载 CSV
    try:
        records = safe_csv_load(safe_path)
    except ValueError as e:
        print(f"错误：{e}")
        return False
    except csv.Error as e:
        print(f"错误：CSV 格式无效：{e}")
        return False
    
    if not records:
        print("错误：CSV 文件为空或没有有效数据行")
        return False
    
    # 获取表头
    headers = list(records[0].keys()) if records else []
    
    print(f"将从 CSV 导入 {len(records)} 条记录...")
    print(f"字段：{', '.join(headers)}")
    print(f"批次大小：{batch_size} 条/批\n")
    
    success_count = 0
    fail_count = 0
    skip_count = 0
    
    # 分批导入
    total_batches = (len(records) + batch_size - 1) // batch_size
    
    for i in range(0, len(records), batch_size):
        batch = records[i:i+batch_size]
        batch_num = (i // batch_size) + 1
        
        # 构建记录数据
        record_data = []
        for row in batch:
            fields = {}
            for key, value in row.items():
                sanitized = sanitize_record_value(value)
                if sanitized is not None:
                    fields[key] = sanitized
            
            if fields:
                record_data.append({"fields": fields})
            else:
                skip_count += 1
        
        if not record_data:
            print(f"[{batch_num}/{total_batches}] 跳过：该批次无有效数据")
            continue
        
        # 限制单次批量大小
        if len(record_data) > MAX_RECORDS_PER_BATCH:
            print(f"警告：单批次记录数超过 API 限制 ({MAX_RECORDS_PER_BATCH})，已自动截断")
            record_data = record_data[:MAX_RECORDS_PER_BATCH]
        
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
            print(f"[{batch_num}/{total_batches}] ✓ 添加 {added} 条记录")
        else:
            fail_count += len(batch)
            print(f"[{batch_num}/{total_batches}] ✗ 导入失败")
            if result:
                print(f"  错误：{result.get('errorMsg', '未知错误')}")
    
    print(f"\n{'='*50}")
    print(f"完成：成功 {success_count} 条，失败 {fail_count} 条，跳过 {skip_count} 条")
    return fail_count == 0

def import_from_json(dentry_uuid: str, sheet_name: str, json_file: str, batch_size: int = DEFAULT_BATCH_SIZE) -> bool:
    """
    从 JSON 批量导入记录
    
    Args:
        dentry_uuid: 表格 UUID
        sheet_name: 数据表名称
        json_file: JSON 文件路径（格式：[{"fields": {...}}, ...]）
        batch_size: 每批次记录数
    
    Returns:
        是否全部成功
    """
    # 解析并验证文件路径
    try:
        safe_path = resolve_safe_path(json_file)
    except ValueError as e:
        print(f"路径验证失败：{e}")
        return False
    
    # 验证文件扩展名
    if not validate_file_extension(json_file, ALLOWED_JSON_EXTENSIONS):
        print(f"错误：只允许 {', '.join(ALLOWED_JSON_EXTENSIONS)} 文件")
        return False
    
    # 检查文件是否存在
    if not safe_path.exists():
        print(f"错误：文件不存在：{safe_path}")
        return False
    
    # 安全加载 JSON
    try:
        records = safe_json_load(safe_path)
    except ValueError as e:
        print(f"错误：{e}")
        return False
    except json.JSONDecodeError as e:
        print(f"错误：JSON 格式无效：{e}")
        return False
    
    if not isinstance(records, list):
        print("错误：JSON 文件必须是数组格式")
        return False
    
    if not records:
        print("错误：JSON 文件为空")
        return False
    
    print(f"将从 JSON 导入 {len(records)} 条记录...")
    print(f"批次大小：{batch_size} 条/批\n")
    
    success_count = 0
    fail_count = 0
    
    # 验证所有记录
    print("正在验证记录格式...")
    for i, record in enumerate(records):
        valid, error = validate_record(record, [])
        if not valid:
            print(f"错误：记录 #{i+1} 格式无效：{error}")
            return False
    print("记录格式验证通过，开始导入...\n")
    
    # 分批导入
    total_batches = (len(records) + batch_size - 1) // batch_size
    
    for i in range(0, len(records), batch_size):
        batch = records[i:i+batch_size]
        batch_num = (i // batch_size) + 1
        
        # 限制单次批量大小
        if len(batch) > MAX_RECORDS_PER_BATCH:
            print(f"警告：单批次记录数超过 API 限制 ({MAX_RECORDS_PER_BATCH})，已自动截断")
            batch = batch[:MAX_RECORDS_PER_BATCH]
        
        args = json.dumps({
            "dentryUuid": dentry_uuid,
            "sheetIdOrName": sheet_name,
            "records": batch
        }, ensure_ascii=False)
        
        result = run_mcporter([
            "add_base_record",
            "--args", args,
            "--output", "json"
        ])
        
        if result and result.get('success'):
            added = len(result.get('result', []))
            success_count += added
            print(f"[{batch_num}/{total_batches}] ✓ 添加 {added} 条记录")
        else:
            fail_count += len(batch)
            print(f"[{batch_num}/{total_batches}] ✗ 导入失败")
            if result:
                print(f"  错误：{result.get('errorMsg', '未知错误')}")
    
    print(f"\n{'='*50}")
    print(f"完成：成功 {success_count} 条，失败 {fail_count} 条")
    return fail_count == 0

def main():
    """主函数"""
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print(__doc__)
        print("\n用法示例:")
        print('  python import_records.py 123e4567-e89b-12d3-a456-426614174000 "数据表" data.csv')
        print('  python import_records.py 123e4567-e89b-12d3-a456-426614174000 "数据表" data.json')
        print('  python import_records.py 123e4567-e89b-12d3-a456-426614174000 "数据表" data.csv 100')
        sys.exit(1)
    
    dentry_uuid = sys.argv[1]
    sheet_name = sys.argv[2]
    data_file = sys.argv[3]
    batch_size = int(sys.argv[4]) if len(sys.argv) == 5 else DEFAULT_BATCH_SIZE
    
    # 验证 UUID 格式
    if not validate_uuid(dentry_uuid):
        print("错误：无效的 dentryUuid 格式")
        print("期望格式：xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx (UUID v4)")
        sys.exit(1)
    
    # 验证 sheet_name 非空
    if not sheet_name.strip():
        print("错误：数据表名称不能为空")
        sys.exit(1)
    
    # 验证 batch_size
    if batch_size < 1 or batch_size > MAX_RECORDS_PER_BATCH:
        print(f"错误：批次大小必须在 1-{MAX_RECORDS_PER_BATCH} 之间")
        sys.exit(1)
    
    # 根据文件扩展名选择导入方式
    if data_file.lower().endswith('.csv'):
        success = import_from_csv(dentry_uuid, sheet_name, data_file, batch_size)
    elif data_file.lower().endswith('.json'):
        success = import_from_json(dentry_uuid, sheet_name, data_file, batch_size)
    else:
        print(f"错误：不支持的文件格式：{data_file}")
        print(f"支持的格式：{', '.join(ALLOWED_CSV_EXTENSIONS + ALLOWED_JSON_EXTENSIONS)}")
        sys.exit(1)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
