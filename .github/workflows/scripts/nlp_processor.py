"""
NLP processor for Slack bot intent detection.
"""
import re
import logging
from typing import Dict, Any, Optional, List, Tuple

logger = logging.getLogger(__name__)


class Intent:
    """Intent constants."""
    STATUS_QUERY = 'status_query'
    ISSUE_INFO = 'issue_info'
    PR_INFO = 'pr_info'
    SEARCH = 'search'
    CREATE_ISSUE = 'create_issue'
    ASSIGN = 'assign'
    REPORT = 'report'
    BLOCKERS = 'blockers'
    HELP = 'help'
    UNKNOWN = 'unknown'


class NLPProcessor:
    """Natural language processing for bot commands."""
    
    def __init__(self):
        """Initialize NLP processor with intent patterns."""
        self.intent_patterns = {
            Intent.STATUS_QUERY: [
                r'\b(status|current|how\s+are\s+we|overview|dashboard)\b',
                r'\bwhat\'?s\s+the\s+status\b',
                r'\bgive\s+me\s+(the\s+)?status\b'
            ],
            Intent.ISSUE_INFO: [
                r'\bissue\s+#?(\d+)\b',
                r'\binfo\s+(about\s+)?issue\s+#?(\d+)\b',
                r'\bdetails\s+(of|for)\s+issue\s+#?(\d+)\b',
                r'\bshow\s+(me\s+)?issue\s+#?(\d+)\b'
            ],
            Intent.PR_INFO: [
                r'\bpr\s+#?(\d+)\b',
                r'\bpull\s+request\s+#?(\d+)\b',
                r'\binfo\s+(about\s+)?pr\s+#?(\d+)\b',
                r'\bshow\s+(me\s+)?pr\s+#?(\d+)\b'
            ],
            Intent.SEARCH: [
                r'\bsearch\s+(for\s+)?(.+)',
                r'\bfind\s+(.+)',
                r'\blook\s+for\s+(.+)',
                r'\bquery\s+(.+)'
            ],
            Intent.CREATE_ISSUE: [
                r'\bcreate\s+(an?\s+)?issue\s+["\'](.+)["\']',
                r'\bnew\s+issue\s+["\'](.+)["\']',
                r'\bopen\s+(an?\s+)?issue\s+["\'](.+)["\']'
            ],
            Intent.ASSIGN: [
                r'\bassign\s+#?(\d+)\s+to\s+@?(\w+)',
                r'\bgive\s+#?(\d+)\s+to\s+@?(\w+)',
                r'\bset\s+assignee\s+(of\s+)?#?(\d+)\s+to\s+@?(\w+)'
            ],
            Intent.REPORT: [
                r'\b(weekly|daily|monthly)\s+report\b',
                r'\breport\s+(weekly|daily|monthly)\b',
                r'\bgenerate\s+(a\s+)?report\b',
                r'\bshow\s+(me\s+)?(the\s+)?report\b'
            ],
            Intent.BLOCKERS: [
                r'\bblockers?\b',
                r'\bwhat\'?s\s+blocked\b',
                r'\bshow\s+(me\s+)?(the\s+)?blockers?\b',
                r'\bblocking\s+issues\b'
            ],
            Intent.HELP: [
                r'\bhelp\b',
                r'\bcommands?\b',
                r'\bwhat\s+can\s+you\s+do\b',
                r'\bhow\s+do\s+i\b'
            ]
        }
    
    def detect_intent(self, text: str) -> Tuple[str, Dict[str, Any]]:
        """
        Detect intent from user message.
        
        Args:
            text: User message text
            
        Returns:
            Tuple of (intent, entities)
        """
        text = text.lower().strip()
        
        # Try each intent pattern
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    entities = self._extract_entities(intent, match, text)
                    logger.info(f"Detected intent: {intent}, entities: {entities}")
                    return intent, entities
        
        return Intent.UNKNOWN, {}
    
    def _extract_entities(self, intent: str, match: re.Match, text: str) -> Dict[str, Any]:
        """
        Extract entities from regex match.
        
        Args:
            intent: Detected intent
            match: Regex match object
            text: Original text
            
        Returns:
            Dictionary of extracted entities
        """
        entities = {}
        
        if intent == Intent.ISSUE_INFO or intent == Intent.PR_INFO:
            # Extract issue/PR number
            groups = match.groups()
            for group in groups:
                if group and group.isdigit():
                    entities['number'] = int(group)
                    break
        
        elif intent == Intent.SEARCH:
            # Extract search query
            groups = match.groups()
            for group in groups:
                if group and len(group) > 2:
                    entities['query'] = group.strip()
                    break
        
        elif intent == Intent.CREATE_ISSUE:
            # Extract issue title
            groups = match.groups()
            for group in groups:
                if group and len(group) > 5:
                    entities['title'] = group.strip()
                    break
        
        elif intent == Intent.ASSIGN:
            # Extract issue number and assignee
            groups = match.groups()
            for i, group in enumerate(groups):
                if group:
                    if group.isdigit():
                        entities['number'] = int(group)
                    elif re.match(r'\w+', group):
                        entities['assignee'] = group
        
        elif intent == Intent.REPORT:
            # Extract report type
            groups = match.groups()
            for group in groups:
                if group and group in ['weekly', 'daily', 'monthly']:
                    entities['report_type'] = group
                    break
            if 'report_type' not in entities:
                entities['report_type'] = 'weekly'  # Default
        
        return entities
    
    def parse_slash_command(self, command: str, text: str) -> Tuple[str, Dict[str, Any]]:
        """
        Parse slash command.
        
        Args:
            command: Command name (without /)
            text: Command arguments
            
        Returns:
            Tuple of (intent, entities)
        """
        command = command.lower().strip()
        text = text.strip()
        
        # Map commands to intents
        command_map = {
            'status': Intent.STATUS_QUERY,
            'issue': Intent.ISSUE_INFO,
            'pr': Intent.PR_INFO,
            'search': Intent.SEARCH,
            'create': Intent.CREATE_ISSUE,
            'assign': Intent.ASSIGN,
            'blockers': Intent.BLOCKERS,
            'report': Intent.REPORT,
            'help': Intent.HELP
        }
        
        intent = command_map.get(command, Intent.UNKNOWN)
        entities = {}
        
        # Extract entities based on command
        if intent == Intent.ISSUE_INFO or intent == Intent.PR_INFO:
            # Extract number from text
            match = re.search(r'#?(\d+)', text)
            if match:
                entities['number'] = int(match.group(1))
        
        elif intent == Intent.SEARCH:
            entities['query'] = text
        
        elif intent == Intent.CREATE_ISSUE:
            # Extract title from quoted text or entire text
            match = re.search(r'["\'](.+)["\']', text)
            if match:
                entities['title'] = match.group(1)
            else:
                entities['title'] = text
        
        elif intent == Intent.ASSIGN:
            # Extract number and assignee
            parts = text.split()
            for part in parts:
                if part.startswith('#') or part.isdigit():
                    entities['number'] = int(part.lstrip('#'))
                elif part.startswith('@'):
                    entities['assignee'] = part.lstrip('@')
        
        elif intent == Intent.REPORT:
            # Extract report type
            for word in text.split():
                if word.lower() in ['weekly', 'daily', 'monthly']:
                    entities['report_type'] = word.lower()
                    break
            if 'report_type' not in entities:
                entities['report_type'] = 'weekly'
        
        return intent, entities
    
    def extract_mentions(self, text: str) -> List[str]:
        """
        Extract @mentions from text.
        
        Args:
            text: Text to parse
            
        Returns:
            List of mentioned usernames
        """
        mentions = re.findall(r'@(\w+)', text)
        return mentions
    
    def extract_issue_numbers(self, text: str) -> List[int]:
        """
        Extract issue/PR numbers from text.
        
        Args:
            text: Text to parse
            
        Returns:
            List of issue numbers
        """
        numbers = re.findall(r'#(\d+)', text)
        return [int(n) for n in numbers]
    
    def normalize_query(self, query: str) -> str:
        """
        Normalize search query.
        
        Args:
            query: Raw query text
            
        Returns:
            Normalized query
        """
        # Remove extra whitespace
        query = ' '.join(query.split())
        
        # Remove special characters except hyphen and underscore
        query = re.sub(r'[^\w\s\-]', '', query)
        
        return query.lower()
