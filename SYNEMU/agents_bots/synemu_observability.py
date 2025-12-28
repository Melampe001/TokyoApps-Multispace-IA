#!/usr/bin/env python3
"""
SYNEMU Observability Module
============================

Advanced observability, tracing, and monitoring for SYNEMU agents.
Integrates with LangSmith, Prometheus, and custom telemetry.

Part of: Tokyo-IA SYNEMU Suite (TokyoApps® / TokRaggcorp®)
"""

import logging
import os
import time
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime
from contextlib import contextmanager
from dataclasses import dataclass, field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Optional LangSmith integration
try:
    from langsmith import Client
    from langsmith.run_helpers import traceable
    LANGSMITH_AVAILABLE = True
except ImportError:
    LANGSMITH_AVAILABLE = False
    logger.warning("LangSmith not available. Install with: pip install langsmith")


@dataclass
class TraceSpan:
    """Represents a trace span for agent execution"""
    span_id: str
    agent_id: str
    agent_name: str
    start_time: float
    end_time: Optional[float] = None
    status: str = "running"
    metadata: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, float] = field(default_factory=dict)
    error: Optional[str] = None


class SynemuObservability:
    """
    Advanced observability for SYNEMU agents
    
    Features:
    - Distributed tracing with LangSmith
    - Performance metrics collection
    - Error tracking and alerting
    - Custom telemetry
    """
    
    def __init__(self):
        """Initialize observability system"""
        self.langsmith_client = None
        self.langsmith_enabled = False
        self.active_spans: Dict[str, TraceSpan] = {}
        self.completed_spans: List[TraceSpan] = []
        
        # Initialize LangSmith if available
        if LANGSMITH_AVAILABLE and os.environ.get("LANGSMITH_API_KEY"):
            try:
                self.langsmith_client = Client()
                self.langsmith_enabled = True
                logger.info("✅ LangSmith observability enabled")
            except Exception as e:
                logger.warning(f"LangSmith initialization failed: {e}")
        else:
            logger.info("ℹ️  LangSmith observability disabled (set LANGSMITH_API_KEY to enable)")
    
    @contextmanager
    def trace_agent_execution(
        self,
        agent_id: str,
        agent_name: str,
        project_path: str,
        standards: List[str],
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Context manager for tracing agent execution
        
        Usage:
            with observability.trace_agent_execution(...) as trace:
                result = execute_agent()
                trace.log_metrics({"score": result.score})
        """
        span_id = f"{agent_id}_{int(time.time() * 1000)}"
        start_time = time.time()
        
        # Create span
        span = TraceSpan(
            span_id=span_id,
            agent_id=agent_id,
            agent_name=agent_name,
            start_time=start_time,
            metadata={
                "project_path": project_path,
                "standards": standards,
                **(metadata or {})
            }
        )
        
        self.active_spans[span_id] = span
        
        # LangSmith tracing
        langsmith_trace = None
        if self.langsmith_enabled:
            try:
                langsmith_trace = self.langsmith_client.create_run(
                    name=f"{agent_name} Analysis",
                    run_type="agent",
                    inputs={
                        "project_path": project_path,
                        "standards": standards
                    },
                    extra={
                        "agent_id": agent_id,
                        "metadata": metadata or {}
                    }
                )
            except Exception as e:
                logger.warning(f"LangSmith trace creation failed: {e}")
        
        try:
            # Provide trace object for logging
            yield span
            
            # Mark as completed
            span.status = "completed"
            span.end_time = time.time()
            
            # Update LangSmith
            if langsmith_trace and self.langsmith_enabled:
                try:
                    self.langsmith_client.update_run(
                        run_id=langsmith_trace.id,
                        outputs=span.metrics,
                        end_time=datetime.now(),
                        extra={"metrics": span.metrics}
                    )
                except Exception as e:
                    logger.warning(f"LangSmith trace update failed: {e}")
        
        except Exception as e:
            # Mark as failed
            span.status = "failed"
            span.end_time = time.time()
            span.error = str(e)
            
            # Update LangSmith with error
            if langsmith_trace and self.langsmith_enabled:
                try:
                    self.langsmith_client.update_run(
                        run_id=langsmith_trace.id,
                        error=str(e),
                        end_time=datetime.now()
                    )
                except Exception as ex:
                    logger.warning(f"LangSmith error update failed: {ex}")
            
            raise
        
        finally:
            # Move to completed
            if span_id in self.active_spans:
                del self.active_spans[span_id]
            self.completed_spans.append(span)
            
            # Log completion
            duration = span.end_time - span.start_time if span.end_time else 0
            logger.info(
                f"🔍 Trace completed: {agent_name} | "
                f"Status: {span.status} | "
                f"Duration: {duration:.2f}s"
            )
    
    def log_metrics(self, span: TraceSpan, metrics: Dict[str, float]):
        """Log metrics for a trace span"""
        span.metrics.update(metrics)
        logger.debug(f"📊 Metrics logged for {span.agent_name}: {metrics}")
    
    def get_trace_summary(self) -> Dict[str, Any]:
        """Get summary of all traces"""
        total_spans = len(self.completed_spans)
        successful = sum(1 for s in self.completed_spans if s.status == "completed")
        failed = sum(1 for s in self.completed_spans if s.status == "failed")
        
        if total_spans > 0:
            avg_duration = sum(
                (s.end_time - s.start_time) for s in self.completed_spans if s.end_time
            ) / total_spans
        else:
            avg_duration = 0
        
        return {
            "total_traces": total_spans,
            "successful": successful,
            "failed": failed,
            "success_rate": (successful / total_spans * 100) if total_spans > 0 else 0,
            "avg_duration_seconds": avg_duration,
            "active_traces": len(self.active_spans)
        }
    
    def export_traces(self, output_path: str):
        """Export traces to JSON file"""
        import json
        
        traces_data = {
            "summary": self.get_trace_summary(),
            "traces": [
                {
                    "span_id": span.span_id,
                    "agent_id": span.agent_id,
                    "agent_name": span.agent_name,
                    "start_time": span.start_time,
                    "end_time": span.end_time,
                    "duration": (span.end_time - span.start_time) if span.end_time else None,
                    "status": span.status,
                    "metadata": span.metadata,
                    "metrics": span.metrics,
                    "error": span.error
                }
                for span in self.completed_spans
            ]
        }
        
        with open(output_path, 'w') as f:
            json.dump(traces_data, f, indent=2)
        
        logger.info(f"📁 Traces exported to: {output_path}")


# Global observability instance
_observability_instance: Optional[SynemuObservability] = None


def get_observability() -> SynemuObservability:
    """Get or create global observability instance"""
    global _observability_instance
    if _observability_instance is None:
        _observability_instance = SynemuObservability()
    return _observability_instance


def main():
    """Test observability system"""
    print("=" * 70)
    print("🔍 SYNEMU Observability System Test")
    print("=" * 70)
    print()
    
    obs = get_observability()
    
    # Simulate agent execution
    with obs.trace_agent_execution(
        agent_id="test_agent",
        agent_name="Test Agent",
        project_path="./test",
        standards=["ISO27001", "GDPR"]
    ) as trace:
        # Simulate work
        time.sleep(0.5)
        
        # Log metrics
        obs.log_metrics(trace, {
            "score": 95.5,
            "findings_count": 3,
            "execution_time": 0.5
        })
    
    # Get summary
    summary = obs.get_trace_summary()
    print(f"Trace Summary:")
    print(f"  Total traces: {summary['total_traces']}")
    print(f"  Success rate: {summary['success_rate']:.1f}%")
    print(f"  Avg duration: {summary['avg_duration_seconds']:.2f}s")
    
    # Export traces
    obs.export_traces("traces_export.json")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
