"""
Shared utilities for GitHub Actions integrations.
"""
import time
import json
import logging
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def retry_with_backoff(max_retries: int = 3, initial_delay: float = 1.0):
    """
    Decorator for retrying functions with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds (doubles with each retry)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}. "
                            f"Retrying in {delay}s..."
                        )
                        time.sleep(delay)
                        delay *= 2
                    else:
                        logger.error(f"All {max_retries} retry attempts failed")
            
            raise last_exception
        
        return wrapper
    return decorator


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from JSON file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in configuration file: {e}")
        raise


def safe_get(data: Dict, *keys, default=None) -> Any:
    """
    Safely get nested dictionary values.
    
    Args:
        data: Dictionary to query
        *keys: Sequence of keys to traverse
        default: Default value if key not found
        
    Returns:
        Value at nested key path or default
    """
    result = data
    for key in keys:
        if isinstance(result, dict):
            result = result.get(key)
        else:
            return default
        if result is None:
            return default
    return result


def timestamp_to_iso(timestamp: Optional[float] = None) -> str:
    """
    Convert Unix timestamp to ISO 8601 format.
    
    Args:
        timestamp: Unix timestamp (uses current time if None)
        
    Returns:
        ISO 8601 formatted string
    """
    if timestamp is None:
        dt = datetime.utcnow()
    else:
        dt = datetime.utcfromtimestamp(timestamp)
    return dt.isoformat() + 'Z'


def iso_to_timestamp(iso_string: str) -> float:
    """
    Convert ISO 8601 string to Unix timestamp.
    
    Args:
        iso_string: ISO 8601 formatted string
        
    Returns:
        Unix timestamp
    """
    # Handle both with and without microseconds
    for fmt in ['%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ']:
        try:
            dt = datetime.strptime(iso_string, fmt)
            return dt.timestamp()
        except ValueError:
            continue
    raise ValueError(f"Unable to parse ISO string: {iso_string}")


def calculate_age_days(created_at: str) -> int:
    """
    Calculate age in days from ISO timestamp.
    
    Args:
        created_at: ISO 8601 formatted creation timestamp
        
    Returns:
        Age in days
    """
    created_timestamp = iso_to_timestamp(created_at)
    age_seconds = time.time() - created_timestamp
    return int(age_seconds / 86400)


def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted string (e.g., "2d 3h 15m")
    """
    if seconds < 60:
        return f"{int(seconds)}s"
    
    minutes = int(seconds / 60)
    if minutes < 60:
        return f"{minutes}m"
    
    hours = int(minutes / 60)
    remaining_minutes = minutes % 60
    if hours < 24:
        return f"{hours}h {remaining_minutes}m"
    
    days = int(hours / 24)
    remaining_hours = hours % 24
    return f"{days}d {remaining_hours}h"


class APIClient:
    """Base API client with retry logic and error handling."""
    
    def __init__(self, base_url: str, headers: Optional[Dict] = None, timeout: int = 30):
        """
        Initialize API client.
        
        Args:
            base_url: Base URL for API
            headers: Default headers for requests
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.headers = headers or {}
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    @retry_with_backoff(max_retries=3)
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make GET request.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            Response JSON
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.debug(f"GET {url}")
        
        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    @retry_with_backoff(max_retries=3)
    def post(self, endpoint: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make POST request.
        
        Args:
            endpoint: API endpoint
            data: Form data
            json_data: JSON data
            
        Returns:
            Response JSON
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.debug(f"POST {url}")
        
        response = self.session.post(url, data=data, json=json_data, timeout=self.timeout)
        response.raise_for_status()
        return response.json() if response.text else {}
    
    @retry_with_backoff(max_retries=3)
    def put(self, endpoint: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make PUT request.
        
        Args:
            endpoint: API endpoint
            data: Form data
            json_data: JSON data
            
        Returns:
            Response JSON
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.debug(f"PUT {url}")
        
        response = self.session.put(url, data=data, json=json_data, timeout=self.timeout)
        response.raise_for_status()
        return response.json() if response.text else {}
    
    @retry_with_backoff(max_retries=3)
    def delete(self, endpoint: str) -> bool:
        """
        Make DELETE request.
        
        Args:
            endpoint: API endpoint
            
        Returns:
            True if successful
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.debug(f"DELETE {url}")
        
        response = self.session.delete(url, timeout=self.timeout)
        response.raise_for_status()
        return True


def validate_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    """
    Validate webhook signature.
    
    Args:
        payload: Request payload
        signature: Signature from header
        secret: Webhook secret
        
    Returns:
        True if signature is valid
    """
    import hmac
    import hashlib
    
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    # Compare in constant time to prevent timing attacks
    return hmac.compare_digest(
        f"sha256={expected_signature}",
        signature
    )


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to append if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def extract_issue_number(text: str) -> Optional[int]:
    """
    Extract issue/PR number from text.
    
    Args:
        text: Text containing issue number
        
    Returns:
        Issue number or None
    """
    import re
    match = re.search(r'#(\d+)', text)
    return int(match.group(1)) if match else None


def batch_list(items: List, batch_size: int = 100):
    """
    Split list into batches.
    
    Args:
        items: List to batch
        batch_size: Size of each batch
        
    Yields:
        Batches of items
    """
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]


class RateLimiter:
    """Simple rate limiter for API calls."""
    
    def __init__(self, calls_per_second: float = 1.0):
        """
        Initialize rate limiter.
        
        Args:
            calls_per_second: Maximum calls per second
        """
        self.min_interval = 1.0 / calls_per_second
        self.last_call = 0.0
    
    def wait(self):
        """Wait if necessary to respect rate limit."""
        elapsed = time.time() - self.last_call
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_call = time.time()
