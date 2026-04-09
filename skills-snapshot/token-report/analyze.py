#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Token Report 分析工具
統計最近 7 天的 Claude Code token 使用量，按專案、session、模型分拆
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import re

# 費率定義（美元/百萬 token）
PRICING = {
    'opus': {'input': 15, 'output': 75},
    'sonnet': {'input': 3, 'output': 15},
    'haiku': {'input': 0.25, 'output': 1.25},
}

# 模型到簡寫的映射
MODEL_ALIASES = {
    'claude-opus': 'opus',
    'claude-sonnet': 'sonnet',
    'claude-haiku': 'haiku',
}


def get_model_name(model_str):
    """從 model 字串推斷簡寫名稱"""
    if not model_str:
        return 'unknown'

    model_lower = model_str.lower()

    # 直接比對
    for alias, name in MODEL_ALIASES.items():
        if alias in model_lower:
            return name

    # 模糊比對
    if 'opus' in model_lower:
        return 'opus'
    if 'sonnet' in model_lower:
        return 'sonnet'
    if 'haiku' in model_lower:
        return 'haiku'

    # 特殊代理
    if 'cursor' in model_lower or 'browser' in model_lower:
        return 'cursor-agent'
    if 'kimi' in model_lower:
        return 'kimi'
    if 'gemini' in model_lower:
        return 'gemini'
    if 'codex' in model_lower:
        return 'codex'

    return 'unknown'


def load_jsonl_files(days=7):
    """
    掃描 ~/.claude/projects/ 下所有 JSONL 檔案
    只處理最近 N 天內修改的檔案

    返回: (檔案路徑, 檔案內容行數列表)
    """
    projects_dir = Path.home() / '.claude' / 'projects'
    cutoff_time = datetime.now() - timedelta(days=days)

    if not projects_dir.exists():
        return []

    files_data = []

    # 遞迴掃描所有 .jsonl 檔案
    for jsonl_file in projects_dir.rglob('*.jsonl'):
        # 檢查修改時間
        mtime = datetime.fromtimestamp(jsonl_file.stat().st_mtime)
        if mtime < cutoff_time:
            continue

        try:
            with open(jsonl_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            files_data.append((jsonl_file, lines))
        except Exception as e:
            print(f"警告: 無法讀取 {jsonl_file}: {e}")

    return files_data


def parse_json_line(line):
    """安全地解析 JSON 行"""
    try:
        return json.loads(line.strip())
    except (json.JSONDecodeError, ValueError):
        return None


def extract_project_name(file_path):
    """從檔案路徑推斷專案名稱，並清理成可讀格式

    路徑格式：~/.claude/projects/-Users-fishtv-Development-8----paygo/...
    清理規則：取最後一段非空字串（以 - 分割）
    """
    parts = file_path.parts
    try:
        projects_idx = parts.index('projects')
        raw_name = parts[projects_idx + 1]
        # 取最後一段非空字串（專案名稱在最後）
        segments = [s for s in raw_name.split('-') if s]
        return segments[-1] if segments else raw_name
    except (ValueError, IndexError):
        return 'unknown'


def calculate_cost(input_tokens, output_tokens, model_name):
    """計算估計成本（美元）"""
    pricing = PRICING.get(model_name, PRICING['haiku'])
    input_cost = (input_tokens / 1_000_000) * pricing['input']
    output_cost = (output_tokens / 1_000_000) * pricing['output']
    return input_cost + output_cost


def analyze_token_usage():
    """主分析函式"""

    # 加載 JSONL 檔案
    files_data = load_jsonl_files(days=7)

    if not files_data:
        print("未找到最近 7 天的 JSONL 檔案")
        return

    # 統計結構
    project_stats = defaultdict(lambda: {'input': 0, 'output': 0, 'cache_creation': 0, 'cache_read': 0})
    model_stats = defaultdict(lambda: {'input': 0, 'output': 0, 'cache_creation': 0, 'cache_read': 0})
    session_stats = []  # [(session_path, input, output, model)]
    total_input = 0
    total_output = 0
    total_cache_creation = 0
    total_cache_read = 0

    # 處理每個檔案
    for file_path, lines in files_data:
        project_name = extract_project_name(file_path)
        session_input = 0
        session_output = 0
        session_models = set()

        for line in lines:
            obj = parse_json_line(line)
            # 只處理 type == "assistant" 的行，token 資訊在 message.usage 內
            if not obj or obj.get('type') != 'assistant':
                continue

            message = obj.get('message', {})
            usage = message.get('usage', {})
            if not usage:
                continue

            model = message.get('model', 'unknown')
            model_name = get_model_name(model)

            input_tokens = usage.get('input_tokens', 0)
            output_tokens = usage.get('output_tokens', 0)
            cache_creation = usage.get('cache_creation_input_tokens', 0)
            cache_read = usage.get('cache_read_input_tokens', 0)

            # 累計全域統計
            project_stats[project_name]['input'] += input_tokens
            project_stats[project_name]['output'] += output_tokens
            project_stats[project_name]['cache_creation'] += cache_creation
            project_stats[project_name]['cache_read'] += cache_read

            model_stats[model_name]['input'] += input_tokens
            model_stats[model_name]['output'] += output_tokens
            model_stats[model_name]['cache_creation'] += cache_creation
            model_stats[model_name]['cache_read'] += cache_read

            session_input += input_tokens
            session_output += output_tokens
            session_models.add(model_name)

            total_input += input_tokens
            total_output += output_tokens
            total_cache_creation += cache_creation
            total_cache_read += cache_read

        if session_input > 0 or session_output > 0:
            primary_model = list(session_models)[0] if session_models else 'unknown'
            session_stats.append({
                'path': str(file_path),
                'project': project_name,
                'input': session_input,
                'output': session_output,
                'model': primary_model,
            })

    # 排序 session（按成本降序）
    session_stats.sort(key=lambda s: calculate_cost(s['input'], s['output'], s['model']), reverse=True)

    # 生成報告
    now = datetime.now()
    report_content = generate_report(
        now, total_input, total_output, total_cache_creation, total_cache_read,
        project_stats, model_stats, session_stats[:5]
    )

    # 存檔
    reports_dir = Path.home() / '.claude' / 'reports'
    reports_dir.mkdir(parents=True, exist_ok=True)

    report_file = reports_dir / f"token-report-{now.strftime('%Y-%m-%d')}.md"
    report_file.write_text(report_content, encoding='utf-8')

    # 終端輸出
    print(report_content)
    print(f"\n✅ 報告已存檔至: {report_file}")


def generate_report(timestamp, total_input, total_output, total_cache_creation, total_cache_read,
                    project_stats, model_stats, top_sessions):
    """生成 Markdown 報告"""

    lines = []
    lines.append("# Token Report — Claude Code 使用量分析\n")
    lines.append(f"**統計期間**：最近 7 天（至 {timestamp.strftime('%Y-%m-%d %H:%M')}）\n")

    # 總覽
    total_cost = calculate_token_cost(total_input, total_output, model_stats)
    lines.append("## 總覽\n")
    lines.append(f"| 指標 | 數值 |")
    lines.append(f"|------|------|")
    lines.append(f"| 輸入 Tokens | {total_input:,} |")
    lines.append(f"| 輸出 Tokens | {total_output:,} |")
    lines.append(f"| Cache 寫入 | {total_cache_creation:,} |")
    lines.append(f"| Cache 讀取 | {total_cache_read:,} |")
    lines.append(f"| **總成本** | **${total_cost:.2f}** |")
    lines.append("")

    # 按專案統計
    lines.append("## 按專案分拆\n")
    lines.append("| 專案名 | Input | Output | Cache 讀/寫 | 成本 |")
    lines.append("|--------|-------|--------|-----------|------|")

    sorted_projects = sorted(project_stats.items(),
                            key=lambda x: x[1]['input'] + x[1]['output'], reverse=True)

    for project_name, stats in sorted_projects:
        project_cost = calculate_cost(stats['input'], stats['output'], 'sonnet')  # 預設用 Sonnet
        cache_info = f"{stats['cache_read']:,} / {stats['cache_creation']:,}"
        lines.append(f"| {project_name} | {stats['input']:,} | {stats['output']:,} | {cache_info} | ${project_cost:.2f} |")

    lines.append("")

    # 按模型統計
    lines.append("## 按模型分拆\n")
    lines.append("| 模型 | Input | Output | Cache 讀/寫 | 成本 |")
    lines.append("|------|-------|--------|-----------|------|")

    sorted_models = sorted(model_stats.items(),
                          key=lambda x: x[1]['input'] + x[1]['output'], reverse=True)

    for model_name, stats in sorted_models:
        model_cost = calculate_cost(stats['input'], stats['output'], model_name)
        cache_info = f"{stats['cache_read']:,} / {stats['cache_creation']:,}"
        lines.append(f"| {model_name} | {stats['input']:,} | {stats['output']:,} | {cache_info} | ${model_cost:.2f} |")

    lines.append("")

    # Top 5 最昂貴 session
    if top_sessions:
        lines.append("## Top 5 最昂貴 Session\n")
        lines.append("| Session | 專案 | Input | Output | 模型 | 成本 |")
        lines.append("|---------|------|-------|--------|------|------|")

        for i, session in enumerate(top_sessions, 1):
            session_cost = calculate_cost(session['input'], session['output'], session['model'])
            session_name = Path(session['path']).name
            lines.append(f"| {i}. {session_name} | {session['project']} | {session['input']:,} | {session['output']:,} | {session['model']} | ${session_cost:.2f} |")

        lines.append("")

    # ASCII bar chart
    lines.append("## Token 消耗分佈（按專案）\n")
    lines.append("```")

    if sorted_projects:
        max_tokens = max(p[1]['input'] + p[1]['output'] for p in sorted_projects) or 1

        for project_name, stats in sorted_projects:
            total_tokens = stats['input'] + stats['output']
            bar_length = int((total_tokens / max_tokens) * 30) if max_tokens > 0 else 0
            bar = '█' * bar_length
            lines.append(f"{project_name:<15} {bar:<30} {total_tokens:>10,}")

    lines.append("```")
    lines.append("")

    return '\n'.join(lines)


def calculate_token_cost(input_tokens, output_tokens, model_stats):
    """計算全部 token 的總成本"""
    total_cost = 0
    for model, stats in model_stats.items():
        total_cost += calculate_cost(stats['input'], stats['output'], model)
    return total_cost


if __name__ == '__main__':
    analyze_token_usage()
