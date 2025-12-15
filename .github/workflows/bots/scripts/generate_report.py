#!/usr/bin/env python3
"""
Bot Report Generator
Aggregates metrics from all bot runs and generates a summary report.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Dict, List


class BotReportGenerator:
    def __init__(self):
        self.reports = {
            "backend_quality": None,
            "backend_performance": None,
            "frontend_ux": None,
            "frontend_build": None
        }
        self.summary = {
            "total_prs_analyzed": 0,
            "total_issues_found": 0,
            "total_optimizations": 0,
            "estimated_time_saved_hours": 0
        }

    def load_report(self, bot_name: str, filepath: str) -> None:
        """Load a bot report from JSON file."""
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                self.reports[bot_name] = json.load(f)

    def aggregate_metrics(self) -> Dict:
        """Aggregate metrics from all bot reports."""
        aggregate = {
            "backend_quality": {"analyzed": 0, "issues": 0, "time_saved": 0},
            "backend_performance": {"analyzed": 0, "issues": 0, "time_saved": 0},
            "frontend_ux": {"analyzed": 0, "issues": 0, "time_saved": 0},
            "frontend_build": {"analyzed": 0, "optimizations": 0, "time_saved": 0}
        }

        # Backend Quality
        if self.reports["backend_quality"]:
            report = self.reports["backend_quality"]
            aggregate["backend_quality"]["analyzed"] = 1
            aggregate["backend_quality"]["issues"] = report.get("summary", {}).get("total_issues", 0)
            aggregate["backend_quality"]["time_saved"] = 0.5  # 30 min per PR review

        # Backend Performance
        if self.reports["backend_performance"]:
            report = self.reports["backend_performance"]
            aggregate["backend_performance"]["analyzed"] = 1
            aggregate["backend_performance"]["issues"] = len(report.get("issues", []))
            aggregate["backend_performance"]["time_saved"] = 0.3  # 20 min per performance check

        # Frontend UX
        if self.reports["frontend_ux"]:
            report = self.reports["frontend_ux"]
            aggregate["frontend_ux"]["analyzed"] = 1
            aggregate["frontend_ux"]["issues"] = report.get("summary", {}).get("total_issues", 0)
            aggregate["frontend_ux"]["time_saved"] = 0.4  # 25 min per UI review

        # Frontend Build
        if self.reports["frontend_build"]:
            report = self.reports["frontend_build"]
            aggregate["frontend_build"]["analyzed"] = 1
            aggregate["frontend_build"]["optimizations"] = report.get("optimizations_applied", 0)
            aggregate["frontend_build"]["time_saved"] = 0.2  # 15 min per asset optimization

        # Calculate totals
        self.summary["total_prs_analyzed"] = sum(
            bot["analyzed"] for bot in aggregate.values()
        )
        self.summary["total_issues_found"] = sum(
            bot.get("issues", 0) for bot in aggregate.values()
        )
        self.summary["total_optimizations"] = aggregate["frontend_build"]["optimizations"]
        self.summary["estimated_time_saved_hours"] = sum(
            bot["time_saved"] for bot in aggregate.values()
        )

        return aggregate

    def generate_markdown_report(self, aggregate: Dict) -> str:
        """Generate a markdown report."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""# 🤖 Bot Coordinator Report
Generated: {now}

## 📊 Summary

- **Total PRs Analyzed**: {self.summary['total_prs_analyzed']}
- **Total Issues Detected**: {self.summary['total_issues_found']}
- **Total Optimizations Applied**: {self.summary['total_optimizations']}
- **⏱️ Estimated Time Saved**: {self.summary['estimated_time_saved_hours']:.1f} hours

---

## 🔧 Backend Quality Guardian

"""
        
        bq = aggregate["backend_quality"]
        report += f"""- PRs Analyzed: {bq['analyzed']}
- Issues Found: {bq['issues']}
- Time Saved: ~{bq['time_saved']*60:.0f} minutes

"""

        report += """## 🚀 Backend Performance Monitor

"""
        bp = aggregate["backend_performance"]
        report += f"""- PRs Analyzed: {bp['analyzed']}
- Performance Issues: {bp['issues']}
- Time Saved: ~{bp['time_saved']*60:.0f} minutes

"""

        report += """## 🎨 Frontend UI/UX Compliance

"""
        fu = aggregate["frontend_ux"]
        report += f"""- PRs Analyzed: {fu['analyzed']}
- UI/UX Issues: {fu['issues']}
- Time Saved: ~{fu['time_saved']*60:.0f} minutes

"""

        report += """## 🖼️ Frontend Build & Asset Optimizer

"""
        fb = aggregate["frontend_build"]
        report += f"""- PRs Analyzed: {fb['analyzed']}
- Assets Optimized: {fb['optimizations']}
- Time Saved: ~{fb['time_saved']*60:.0f} minutes

"""

        report += f"""---

## 🎯 Impact

This week, our automated bots saved the team approximately **{self.summary['estimated_time_saved_hours']:.1f} hours** 
of manual code review and optimization work, allowing developers to focus on building features.

### Key Achievements

- ✅ Automated quality checks on {self.summary['total_prs_analyzed']} PRs
- ✅ Identified {self.summary['total_issues_found']} potential issues early
- ✅ Applied {self.summary['total_optimizations']} optimizations automatically

---

*This report is automatically generated by the Bot Coordinator*
"""
        
        return report

    def save_report(self, output_path: str) -> None:
        """Save aggregated report to file."""
        aggregate = self.aggregate_metrics()
        
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": self.summary,
            "details": aggregate,
            "markdown": self.generate_markdown_report(aggregate)
        }
        
        with open(output_path, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        # Also save markdown version
        md_path = output_path.replace('.json', '.md')
        with open(md_path, 'w') as f:
            f.write(report_data["markdown"])
        
        print(f"Report saved to: {output_path}")
        print(f"Markdown report saved to: {md_path}")


def main():
    parser = argparse.ArgumentParser(description='Generate bot coordinator report')
    parser.add_argument('--backend-quality', type=str, help='Backend quality report JSON')
    parser.add_argument('--backend-performance', type=str, help='Backend performance report JSON')
    parser.add_argument('--frontend-ux', type=str, help='Frontend UX report JSON')
    parser.add_argument('--frontend-build', type=str, help='Frontend build report JSON')
    parser.add_argument('--output', type=str, default='bot-coordinator-report.json', help='Output file')
    
    args = parser.parse_args()
    
    generator = BotReportGenerator()
    
    # Load available reports
    if args.backend_quality:
        generator.load_report("backend_quality", args.backend_quality)
    if args.backend_performance:
        generator.load_report("backend_performance", args.backend_performance)
    if args.frontend_ux:
        generator.load_report("frontend_ux", args.frontend_ux)
    if args.frontend_build:
        generator.load_report("frontend_build", args.frontend_build)
    
    # Generate and save report
    generator.save_report(args.output)
    
    # Print summary
    print("\n" + "="*50)
    print(generator.generate_markdown_report(generator.aggregate_metrics()))
    print("="*50)


if __name__ == '__main__':
    main()
