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
import os
import re
from pathlib import Path
from typing import Union, List, Dict, Any, Optional, Tuple

# 类型别名（Python 3.9 兼容）
JsonData = Union[List[Any], Dict[str, Any]]

# ============== 安全常量 ==============
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB 文件限制
ALLOWED_FILE_EXTENSIONS = ['.json']
ALLOWED_FIELD_TYPES = {
    'text', 'number', 'singleSelect', 'multipleSelect',
    'date', 'user', 'attachment', 'checkbox', 'phone', 'email', 'url'
}
UUID_PATTERN = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)

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

def validate_field_config(field: Dict[str, Any]) -> Tuple[bool, str]:
    """
    验证字段配置
    
    Returns:
        (是否有效，错误信息)
    """
    if not isinstance(field, dict):
        return False, "字段配置必须是对象"
    
    if 'name' not in field:
        return False, "缺少必需字段：name"
    
    if not isinstance(field['name'], str) or not field['name'].strip():
        return False, "name 必须是非空字符串"
    
    field_type = field.get('type', 'text')
    if field_type not in ALLOWED_FIELD_TYPES:
        return False, f"不支持的字段类型：{field_type} (允许：{', '.join(ALLOWED_FIELD_TYPES)})"
    
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
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
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
        print("错误：命令执行超时（60 秒）")
        return None
    except FileNotFoundError:
        print("错误：未找到 mcporter 命令，请确认已安装")
        return None

def bulk_add_fields(dentry_uuid: str, sheet_name: str, fields_file: str) -> bool:
    """
    批量添加字段
    
    Args:
        dentry_uuid: 表格 UUID
        sheet_name: 数据表名称
        fields_file: 字段配置文件路径
    
    Returns:
        是否全部成功
    """
    # 解析并验证文件路径
    try:
        safe_path = resolve_safe_path(fields_file)
    except ValueError as e:
        print(f"路径验证失败：{e}")
        return False
    
    # 验证文件扩展名
    if not validate_file_extension(fields_file, ALLOWED_FILE_EXTENSIONS):
        print(f"错误：只允许 {', '.join(ALLOWED_FILE_EXTENSIONS)} 文件")
        return False
    
    # 检查文件是否存在
    if not safe_path.exists():
        print(f"错误：文件不存在：{safe_path}")
        return False
    
    # 安全加载 JSON
    try:
        fields = safe_json_load(safe_path)
    except ValueError as e:
        print(f"错误：{e}")
        return False
    except json.JSONDecodeError as e:
        print(f"错误：JSON 格式无效：{e}")
        return False
    
    # 验证 fields 是列表
    if not isinstance(fields, list):
        print("错误：fields.json 必须是 JSON 数组")
        return False
    
    # 预验证所有字段配置
    print(f"将为数据表 '{sheet_name}' 添加 {len(fields)} 个字段...")
    print("正在验证字段配置...")
    
    for i, field in enumerate(fields):
        valid, error = validate_field_config(field)
        if not valid:
            print(f"错误：字段 #{i+1} 配置无效：{error}")
            return False
    
    print("字段配置验证通过，开始添加...\n")
    
    success_count = 0
    for i, field in enumerate(fields):
        name = field['name'].strip()
        field_type = field.get('type', 'text')
        
        args = json.dumps({
            "dentryUuid": dentry_uuid,
            "sheetIdOrName": sheet_name,
            "addField": {
                "name": name,
                "type": field_type
            }
        }, ensure_ascii=False)
        
        result = run_mcporter([
            "add_base_field",
            "--args", args,
            "--output", "json"
        ])
        
        if result and result.get('success'):
            field_id = result.get('result', {}).get('id', '未知')
            print(f"[{i+1}/{len(fields)}] ✓ 添加字段：{name} ({field_type}) - ID: {field_id}")
            success_count += 1
        else:
            print(f"[{i+1}/{len(fields)}] ✗ 添加字段失败：{name}")
            if result:
                print(f"  错误：{result.get('errorMsg', '未知错误')}")
    
    print(f"\n{'='*50}")
    print(f"完成：{success_count}/{len(fields)} 个字段添加成功")
    return success_count == len(fields)

def main():
    """主函数"""
    if len(sys.argv) != 4:
        print(__doc__)
        print("用法示例:")
        print('  python bulk_add_fields.py 123e4567-e89b-12d3-a456-426614174000 "数据表" fields.json')
        sys.exit(1)
    
    dentry_uuid = sys.argv[1]
    sheet_name = sys.argv[2]
    fields_file = sys.argv[3]
    
    # 验证 UUID 格式
    if not validate_uuid(dentry_uuid):
        print("错误：无效的 dentryUuid 格式")
        print("期望格式：xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx (UUID v4)")
        sys.exit(1)
    
    # 验证 sheet_name 非空
    if not sheet_name.strip():
        print("错误：数据表名称不能为空")
        sys.exit(1)
    
    success = bulk_add_fields(dentry_uuid, sheet_name, fields_file)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
