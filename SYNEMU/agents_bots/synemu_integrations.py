#!/usr/bin/env python3
"""
SYNEMU Integrations Module
===========================

Handles all external API integrations and credentials for the SYNEMU Suite.
All API keys and secrets are managed through environment variables.

Part of: Tokyo-IA SYNEMU Suite (TokyoApps® / TokRaggcorp®)
Security: All credentials via environment variables only - NO hardcoded secrets
"""

import os
from typing import Dict, Optional, Any
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SynemuCredentials:
    """Container for SYNEMU Suite credentials"""
    
    # LLM Provider API Keys
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    
    # Simulation & Emulation APIs
    unity_api_key: Optional[str] = None
    flare_api_key: Optional[str] = None
    
    # Video & Visualization
    video_api_key: Optional[str] = None
    rendering_api_key: Optional[str] = None
    
    # Asset Management
    asset_storage_key: Optional[str] = None
    cdn_api_key: Optional[str] = None
    
    # Database & Storage
    database_url: Optional[str] = None
    redis_url: Optional[str] = None
    
    # Cloud Services
    aws_access_key: Optional[str] = None
    aws_secret_key: Optional[str] = None
    gcp_credentials: Optional[str] = None
    
    # Monitoring & Logging
    datadog_api_key: Optional[str] = None
    sentry_dsn: Optional[str] = None


class SynemuIntegrations:
    """
    SYNEMU Integrations Manager
    
    Centralized management of all external API integrations for the SYNEMU Suite.
    Ensures secure credential handling through environment variables only.
    """
    
    def __init__(self):
        """Initialize integrations manager and load credentials from environment"""
        self.credentials = self._load_credentials()
        self._validate_required_credentials()
        logger.info("SYNEMU Integrations initialized successfully")
    
    def _load_credentials(self) -> SynemuCredentials:
        """
        Load all credentials from environment variables.
        
        Returns:
            SynemuCredentials object with all available credentials
        """
        return SynemuCredentials(
            # LLM Providers
            anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY"),
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
            groq_api_key=os.environ.get("GROQ_API_KEY"),
            google_api_key=os.environ.get("GOOGLE_API_KEY"),
            
            # Simulation & Emulation
            unity_api_key=os.environ.get("SYNEMU_UNITY_API_KEY"),
            flare_api_key=os.environ.get("SYNEMU_FLARE_API_KEY"),
            
            # Video & Visualization
            video_api_key=os.environ.get("SYNEMU_VIDEO_API_KEY"),
            rendering_api_key=os.environ.get("SYNEMU_RENDERING_API_KEY"),
            
            # Asset Management
            asset_storage_key=os.environ.get("SYNEMU_ASSET_STORAGE_KEY"),
            cdn_api_key=os.environ.get("SYNEMU_CDN_API_KEY"),
            
            # Database & Storage
            database_url=os.environ.get("DATABASE_URL"),
            redis_url=os.environ.get("REDIS_URL"),
            
            # Cloud Services
            aws_access_key=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            gcp_credentials=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
            
            # Monitoring & Logging
            datadog_api_key=os.environ.get("DATADOG_API_KEY"),
            sentry_dsn=os.environ.get("SENTRY_DSN"),
        )
    
    def _validate_required_credentials(self) -> None:
        """
        Validate that required credentials are present.
        Logs warnings for missing optional credentials.
        """
        # Check for at least one LLM provider
        llm_providers = [
            self.credentials.anthropic_api_key,
            self.credentials.openai_api_key,
            self.credentials.groq_api_key,
            self.credentials.google_api_key,
        ]
        
        if not any(llm_providers):
            logger.warning(
                "No LLM provider API keys found. "
                "Set at least one: ANTHROPIC_API_KEY, OPENAI_API_KEY, GROQ_API_KEY, or GOOGLE_API_KEY"
            )
    
    def get_llm_config(self, provider: str = "openai") -> Dict[str, Any]:
        """
        Get LLM configuration for specified provider.
        
        Args:
            provider: LLM provider name (openai, anthropic, groq, google)
            
        Returns:
            Configuration dictionary for the LLM provider
            
        Raises:
            ValueError: If provider is not supported or API key is missing
        """
        provider = provider.lower()
        
        config_map = {
            "openai": {
                "api_key": self.credentials.openai_api_key,
                "model": "gpt-4o",
                "temperature": 0.7,
            },
            "anthropic": {
                "api_key": self.credentials.anthropic_api_key,
                "model": "claude-opus-4.1",
                "temperature": 0.7,
            },
            "groq": {
                "api_key": self.credentials.groq_api_key,
                "model": "llama-4-405b",
                "temperature": 0.7,
            },
            "google": {
                "api_key": self.credentials.google_api_key,
                "model": "gemini-3.0-ultra",
                "temperature": 0.7,
            },
        }
        
        if provider not in config_map:
            raise ValueError(f"Unsupported LLM provider: {provider}")
        
        config = config_map[provider]
        if not config["api_key"]:
            raise ValueError(f"API key not found for provider: {provider}")
        
        return config
    
    def get_simulation_config(self, sim_type: str = "2d") -> Dict[str, Any]:
        """
        Get simulation/emulation configuration.
        
        Args:
            sim_type: Type of simulation (2d, 3d, unity)
            
        Returns:
            Configuration dictionary for the simulation system
        """
        if sim_type == "2d":
            return {
                "api_key": self.credentials.flare_api_key,
                "engine": "flare",
                "max_instances": 10,
            }
        elif sim_type in ["3d", "unity"]:
            return {
                "api_key": self.credentials.unity_api_key,
                "engine": "unity",
                "max_instances": 5,
            }
        else:
            raise ValueError(f"Unsupported simulation type: {sim_type}")
    
    def get_asset_config(self) -> Dict[str, Any]:
        """
        Get asset management configuration.
        
        Returns:
            Configuration dictionary for asset management
        """
        return {
            "storage_key": self.credentials.asset_storage_key,
            "cdn_key": self.credentials.cdn_api_key,
            "max_file_size_mb": 500,
            "supported_formats": ["png", "jpg", "svg", "fbx", "obj", "gltf", "mp4", "webm"],
        }
    
    def get_database_url(self) -> str:
        """
        Get database connection URL.
        
        Returns:
            Database URL string
            
        Raises:
            ValueError: If DATABASE_URL is not set
        """
        if not self.credentials.database_url:
            raise ValueError("DATABASE_URL environment variable not set")
        return self.credentials.database_url
    
    def is_feature_enabled(self, feature: str) -> bool:
        """
        Check if a specific feature is enabled based on available credentials.
        
        Args:
            feature: Feature name to check
            
        Returns:
            True if feature credentials are available, False otherwise
        """
        feature_map = {
            "llm": any([
                self.credentials.anthropic_api_key,
                self.credentials.openai_api_key,
                self.credentials.groq_api_key,
                self.credentials.google_api_key,
            ]),
            "2d_simulation": bool(self.credentials.flare_api_key),
            "3d_simulation": bool(self.credentials.unity_api_key),
            "video": bool(self.credentials.video_api_key),
            "asset_management": bool(self.credentials.asset_storage_key),
            "monitoring": bool(self.credentials.datadog_api_key),
        }
        
        return feature_map.get(feature, False)
    
    def get_monitoring_config(self) -> Dict[str, Any]:
        """
        Get monitoring and logging configuration.
        
        Returns:
            Configuration dictionary for monitoring services
        """
        return {
            "datadog_enabled": bool(self.credentials.datadog_api_key),
            "sentry_enabled": bool(self.credentials.sentry_dsn),
            "datadog_api_key": self.credentials.datadog_api_key,
            "sentry_dsn": self.credentials.sentry_dsn,
        }


# Global integrations instance
_integrations_instance: Optional[SynemuIntegrations] = None


def get_integrations() -> SynemuIntegrations:
    """
    Get or create the global SYNEMU integrations instance.
    
    Returns:
        Global SynemuIntegrations instance
    """
    global _integrations_instance
    if _integrations_instance is None:
        _integrations_instance = SynemuIntegrations()
    return _integrations_instance


if __name__ == "__main__":
    # Example usage and validation
    print("SYNEMU Integrations Module - Validation")
    print("=" * 50)
    
    integrations = get_integrations()
    
    print("\n✓ Integrations module loaded successfully")
    print(f"✓ LLM enabled: {integrations.is_feature_enabled('llm')}")
    print(f"✓ 2D Simulation enabled: {integrations.is_feature_enabled('2d_simulation')}")
    print(f"✓ 3D Simulation enabled: {integrations.is_feature_enabled('3d_simulation')}")
    print(f"✓ Video enabled: {integrations.is_feature_enabled('video')}")
    print(f"✓ Asset Management enabled: {integrations.is_feature_enabled('asset_management')}")
    print(f"✓ Monitoring enabled: {integrations.is_feature_enabled('monitoring')}")
    
    print("\n" + "=" * 50)
    print("Configuration loaded from environment variables only.")
    print("No hardcoded secrets present. ✓")
