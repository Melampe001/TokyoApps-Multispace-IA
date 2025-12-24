#!/usr/bin/env python3
"""
SYNEMU Agents and Bots Package
===============================

Python package containing all SYNEMU Suite specialized agents.

Part of: Tokyo-IA SYNEMU Suite (TokyoApps® / TokRaggcorp®)
"""

__version__ = "1.0.0"
__author__ = "TokyoApps® / TokRaggcorp®"

# Import all agents for easy access
from .synemu_integrations import SynemuIntegrations, get_integrations
from .synemu_orchestrator import SynemuOrchestrator, TaskType, TaskStatus
from .synemu_supreme_orchestrator import (
    SynemuSupremeOrchestrator,
    AnalysisMode,
    AgentStatus,
    QualityLevel
)
from .synemu_compliance_validator import (
    SynemuComplianceValidator,
    ComplianceStandard,
    ComplianceLevel
)
from .synemu_agent2d_flare import Synemu2DFlareAgent
from .synemu_agent3d_unity import Synemu3DUnityAgent, PrimitiveType
from .synemu_agent_video_viz import SynemuVideoVizAgent, VideoFormat, RenderQuality
from .synemu_qa_owl import SynemuQAOwlAgent, TestType, TestStatus
from .synemu_docu_libra import SynemuDocuLibraAgent, DocType, DocFormat
from .synemu_asset_atlas import SynemuAssetAtlasAgent, AssetType, StorageLocation

__all__ = [
    # Core
    "SynemuIntegrations",
    "get_integrations",
    
    # Orchestrators
    "SynemuOrchestrator",
    "TaskType",
    "TaskStatus",
    "SynemuSupremeOrchestrator",
    "AnalysisMode",
    "AgentStatus",
    "QualityLevel",
    
    # Enterprise
    "SynemuComplianceValidator",
    "ComplianceStandard",
    "ComplianceLevel",
    
    # Agents
    "Synemu2DFlareAgent",
    "Synemu3DUnityAgent",
    "SynemuVideoVizAgent",
    "SynemuQAOwlAgent",
    "SynemuDocuLibraAgent",
    "SynemuAssetAtlasAgent",
    
    # Enums
    "PrimitiveType",
    "VideoFormat",
    "RenderQuality",
    "TestType",
    "TestStatus",
    "DocType",
    "DocFormat",
    "AssetType",
    "StorageLocation",
]
