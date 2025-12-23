#!/usr/bin/env python3
"""
📊 Generador de Reportes de Agentes
Convierte resultados JSON en reportes Markdown legibles
"""

import json
import argparse
from datetime import datetime
from pathlib import Path


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
- **Success Rate:** {(results.get('completed_tasks', 0) / max(results.get('total_tasks', 1), 1) * 100):.1f}%

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
            result_str = json.dumps(task_result['result'], indent=2)
            if len(result_str) > 500:
                result_str = result_str[:500] + "..."
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
    
    # Load results
    with open(args.input, 'r') as f:
        results = json.load(f)
    
    # Generate report
    report = generate_markdown_report(results)
    
    # Save report
    with open(args.output, 'w') as f:
        f.write(report)
    
    print(f"✅ Report generated: {args.output}")


if __name__ == "__main__":
    main()
