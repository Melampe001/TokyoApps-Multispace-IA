#!/usr/bin/env python3
"""
📊 Generador de Reportes de Agentes
Convierte resultados JSON en reportes Markdown legibles
"""

import json
import argparse
from datetime import datetime
from pathlib import Path

# Constants
MAX_RESULT_LENGTH = 500  # Maximum length for result preview in report


def generate_markdown_report(results: dict) -> str:
    """Genera reporte en Markdown"""
    
    report = f"""# 🤖 Tokyo-IA Agent Automation Report

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Workflow:** {results.get('workflow_name', 'Unknown')}
**Status:** {results.get('status', 'unknown').upper()}

---

## 📊 Summary

- **Total Tasks:** {results.get('total_tasks', 0)}
- **Completed:** {results.get('completed_tasks', 0)} ✅
- **Failed:** {results.get('failed_tasks', 0)} ❌
- **Success Rate:** {(results.get('completed_tasks', 0) / results.get('total_tasks', 1) * 100) if results.get('total_tasks', 0) > 0 else 0.0:.1f}%

---

## 🔍 Task Details

"""
    
    for i, task_result in enumerate(results.get('results', []), 1):
        agent_name = task_result.get('agent_name', 'Unknown')
        success = task_result.get('success', False)
        duration = task_result.get('duration_ms', 0)
        
        status_icon = "✅" if success else "❌"
        
        report += f"""### {status_icon} Task {i}: {agent_name}

**Duration:** {duration}ms
**Status:** {'SUCCESS' if success else 'FAILED'}

"""
        
        if success and 'result' in task_result:
            try:
                result_str = json.dumps(task_result['result'], indent=2)
                if len(result_str) > MAX_RESULT_LENGTH:
                    result_str = result_str[:MAX_RESULT_LENGTH] + "..."
            except (TypeError, ValueError) as e:
                result_str = f"Error serializing result: {str(e)}"
            report += f"""**Result:**
```
{result_str}
```

"""
        elif not success and 'error' in task_result:
            report += f"""**Error:**
```
{task_result['error']}
```

"""
    
    report += """---

## 🎯 Next Steps

"""
    
    if results.get('failed_tasks', 0) > 0:
        report += """- ⚠️ Review failed tasks and fix issues
- 🔄 Re-run automation after fixes
"""
    else:
        report += """- ✅ All tasks completed successfully!
- 🚀 Ready for next phase
"""
    
    return report


def main():
    parser = argparse.ArgumentParser(description='Generate agent automation report')
    parser.add_argument('--input', required=True, help='Input JSON file')
    parser.add_argument('--output', required=True, help='Output Markdown file')
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not Path(args.input).exists():
        print(f"⚠️ Warning: Input file '{args.input}' not found. Generating default report.")
        results = {
            'workflow_name': 'Agent Automation',
            'status': 'failed',
            'total_tasks': 0,
            'completed_tasks': 0,
            'failed_tasks': 1,
            'results': [{
                'agent_name': 'Automation',
                'success': False,
                'duration_ms': 0,
                'error': f'Input file {args.input} was not generated. Check previous steps for failures.'
            }]
        }
    else:
        # Load results
        try:
            with open(args.input, 'r') as f:
                results = json.load(f)
        except json.JSONDecodeError as e:
            print(f"⚠️ Error: Invalid JSON in '{args.input}': {e}")
            results = {
                'workflow_name': 'Agent Automation',
                'status': 'failed',
                'total_tasks': 0,
                'completed_tasks': 0,
                'failed_tasks': 1,
                'results': [{
                    'agent_name': 'JSON Parser',
                    'success': False,
                    'duration_ms': 0,
                    'error': f'Invalid JSON in {args.input}: {str(e)}'
                }]
            }
        except Exception as e:
            print(f"⚠️ Error reading file '{args.input}': {e}")
            results = {
                'workflow_name': 'Agent Automation',
                'status': 'failed',
                'total_tasks': 0,
                'completed_tasks': 0,
                'failed_tasks': 1,
                'results': [{
                    'agent_name': 'File Reader',
                    'success': False,
                    'duration_ms': 0,
                    'error': f'Error reading {args.input}: {str(e)}'
                }]
            }
    
    # Generate report
    report = generate_markdown_report(results)
    
    # Save report
    try:
        # Ensure output directory exists
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(args.output, 'w') as f:
            f.write(report)
        
        print(f"✅ Report generated: {args.output}")
    except Exception as e:
        print(f"❌ Error writing report to '{args.output}': {e}")
        # Try to write to a fallback location
        fallback = Path("agent_report_fallback.md")
        try:
            with open(fallback, 'w') as f:
                f.write(report)
            print(f"✅ Report saved to fallback location: {fallback}")
        except Exception as fallback_error:
            print(f"❌ Failed to write to fallback location: {fallback_error}")
            print("Report content:")
            print(report)


if __name__ == "__main__":
    main()
