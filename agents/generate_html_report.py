#!/usr/bin/env python3
"""
Tokyo-IA HTML Report Generator

Converts JSON reports from agent workflows into beautiful HTML reports
with visualizations, charts, and formatted output.

Usage:
    python agents/generate_html_report.py agent_reports_20250129_123456/
    python agents/generate_html_report.py agent_reports_20250129_123456/ --output custom_report.html
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tokyo-IA Agent Report - {timestamp}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header .subtitle {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section h2 {{
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
            font-size: 1.8em;
        }}
        
        .agent-card {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
            transition: transform 0.2s;
        }}
        
        .agent-card:hover {{
            transform: translateX(5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .agent-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .agent-name {{
            font-size: 1.4em;
            font-weight: bold;
            color: #333;
        }}
        
        .agent-status {{
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
        }}
        
        .status-success {{
            background: #d4edda;
            color: #155724;
        }}
        
        .status-error {{
            background: #f8d7da;
            color: #721c24;
        }}
        
        .agent-content {{
            color: #555;
            line-height: 1.6;
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            max-height: 300px;
            overflow-y: auto;
            background: white;
            padding: 15px;
            border-radius: 5px;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            font-size: 1em;
            opacity: 0.9;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #dee2e6;
        }}
        
        .timestamp {{
            font-size: 0.9em;
            color: #888;
            margin-top: 10px;
        }}
        
        .badge {{
            display: inline-block;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: bold;
            margin-left: 10px;
        }}
        
        .badge-free {{
            background: #d4edda;
            color: #155724;
        }}
        
        .badge-paid {{
            background: #fff3cd;
            color: #856404;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🗼 Tokyo-IA Agent Report</h1>
            <div class="subtitle">{report_title}</div>
            <div class="timestamp">Generated: {timestamp}</div>
        </div>
        
        <div class="content">
            {stats_section}
            
            {sections}
        </div>
        
        <div class="footer">
            <p><strong>Tokyo-IA Agent Orchestration System</strong></p>
            <p>Powered by CrewAI • 5 Specialized Agents • Production Ready</p>
        </div>
    </div>
</body>
</html>
"""


def generate_stats_section(data: Dict[str, Any]) -> str:
    """Generate statistics section HTML."""
    stats = []
    
    # Count agent results
    if 'agent_results' in data:
        total_agents = len(data['agent_results'])
        successful = sum(1 for r in data['agent_results'].values() if not str(r).startswith('Error:'))
        stats.append(('Total Agents', str(total_agents)))
        stats.append(('Successful', str(successful)))
        stats.append(('Success Rate', f"{(successful/total_agents*100) if total_agents > 0 else 0:.0f}%"))
    
    # Cleanup tasks
    if 'cleanup_tasks' in data:
        tasks = len(data['cleanup_tasks'])
        stats.append(('Cleanup Tasks', str(tasks)))
    
    # PR number
    if 'pr_number' in data:
        stats.append(('PR Number', f"#{data['pr_number']}"))
    
    if not stats:
        return ""
    
    html = '<div class="stats">'
    for label, value in stats:
        html += f'''
        <div class="stat-card">
            <div class="stat-value">{value}</div>
            <div class="stat-label">{label}</div>
        </div>
        '''
    html += '</div>'
    
    return html


def generate_agent_card(agent_name: str, result: str, is_error: bool = False) -> str:
    """Generate HTML for a single agent result card."""
    status_class = 'status-error' if is_error else 'status-success'
    status_text = 'Error' if is_error else 'Success'
    
    # Truncate long results
    display_result = result if len(result) < 2000 else result[:2000] + "\n\n... (truncated)"
    
    return f'''
    <div class="agent-card">
        <div class="agent-header">
            <div class="agent-name">{agent_name}</div>
            <div class="agent-status {status_class}">{status_text}</div>
        </div>
        <div class="agent-content">{display_result}</div>
    </div>
    '''


def generate_pr_analysis_html(data: Dict[str, Any]) -> str:
    """Generate HTML for PR analysis report."""
    sections = []
    
    if 'agent_results' in data:
        agent_names = {
            'akira': '侍 Akira - Code Review',
            'yuki': '❄️ Yuki - Test Engineering',
            'hiro': '🛡️ Hiro - SRE/DevOps',
            'sakura': '🌸 Sakura - Documentation',
            'kenji': '🏗️ Kenji - Architecture'
        }
        
        content = '<div class="section"><h2>Agent Analysis Results</h2>'
        
        for agent_id, result in data['agent_results'].items():
            agent_name = agent_names.get(agent_id, agent_id.title())
            is_error = str(result).startswith('Error:')
            content += generate_agent_card(agent_name, str(result), is_error)
        
        content += '</div>'
        sections.append(content)
    
    return ''.join(sections)


def generate_cleanup_html(data: Dict[str, Any]) -> str:
    """Generate HTML for cleanup report."""
    sections = []
    
    if 'cleanup_tasks' in data:
        task_names = {
            'branch_cleanup': '🛡️ Hiro - Branch Analysis',
            'pr_categorization': '侍 Akira - PR Categorization',
            'documentation_audit': '🌸 Sakura - Documentation Audit',
            'q1_2026_roadmap': '🏗️ Kenji - Q1 2026 Roadmap'
        }
        
        content = '<div class="section"><h2>Cleanup Tasks</h2>'
        
        for task_id, result in data['cleanup_tasks'].items():
            task_name = task_names.get(task_id, task_id.replace('_', ' ').title())
            is_error = str(result).startswith('Error:')
            content += generate_agent_card(task_name, str(result), is_error)
        
        content += '</div>'
        sections.append(content)
    
    return ''.join(sections)


def generate_documentation_html(data: Dict[str, Any]) -> str:
    """Generate HTML for documentation generation report."""
    sections = []
    
    if 'documentation' in data:
        content = '<div class="section"><h2>Generated Documentation</h2>'
        content += generate_agent_card('🌸 Sakura - Documentation Generation', 
                                       str(data['documentation']), 
                                       is_error=False)
        content += '</div>'
        sections.append(content)
    
    if 'error' in data:
        content = '<div class="section"><h2>Error</h2>'
        content += generate_agent_card('Error', str(data['error']), is_error=True)
        content += '</div>'
        sections.append(content)
    
    return ''.join(sections)


def generate_html_report(report_dir: Path, output_file: str = None) -> str:
    """Generate HTML report from JSON files in report directory."""
    if not report_dir.exists():
        raise FileNotFoundError(f"Report directory not found: {report_dir}")
    
    # Determine report type and load data
    json_files = list(report_dir.glob('*.json'))
    
    if not json_files:
        raise ValueError(f"No JSON files found in {report_dir}")
    
    # Load all JSON files
    all_data = {}
    report_type = "General Report"
    
    for json_file in json_files:
        with open(json_file, 'r') as f:
            data = json.load(f)
            
            if 'pr_number' in data:
                report_type = f"PR #{data['pr_number']} Analysis"
                all_data.update(data)
            elif 'cleanup_tasks' in data:
                report_type = "Repository Cleanup Plan"
                all_data.update(data)
            elif 'documentation' in data:
                report_type = "Documentation Generation"
                all_data.update(data)
    
    # Generate sections based on report type
    stats_html = generate_stats_section(all_data)
    
    if 'pr_number' in all_data:
        sections_html = generate_pr_analysis_html(all_data)
    elif 'cleanup_tasks' in all_data:
        sections_html = generate_cleanup_html(all_data)
    elif 'documentation' in all_data:
        sections_html = generate_documentation_html(all_data)
    else:
        sections_html = '<div class="section"><h2>Report Data</h2><pre>' + json.dumps(all_data, indent=2) + '</pre></div>'
    
    # Generate final HTML
    html = HTML_TEMPLATE.format(
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        report_title=report_type,
        stats_section=stats_html,
        sections=sections_html
    )
    
    # Write to file
    if not output_file:
        output_file = report_dir / 'report.html'
    else:
        output_file = Path(output_file)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return str(output_file)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Generate HTML reports from Tokyo-IA agent JSON outputs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s agent_reports_20250129_123456/
  %(prog)s agent_reports_20250129_123456/ --output custom.html
  %(prog)s agent_reports_20250129_123456/ -o /tmp/report.html
        '''
    )
    
    parser.add_argument(
        'report_dir',
        type=str,
        help='Directory containing agent report JSON files'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Output HTML file path (default: report_dir/report.html)'
    )
    
    args = parser.parse_args()
    
    try:
        report_dir = Path(args.report_dir)
        output_file = generate_html_report(report_dir, args.output)
        
        print(f"✅ HTML report generated successfully!")
        print(f"📁 Location: {output_file}")
        print(f"🌐 Open in browser: file://{Path(output_file).absolute()}")
        
        return 0
    
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
