"""
Google Sheets formatting utilities.
Applies conditional formatting and styling to dashboard.
"""
import logging
from typing import Dict, Any, List

try:
    from googleapiclient.discovery import build
    from google.oauth2 import service_account
except ImportError:
    logging.warning("Google API libraries not installed")

logger = logging.getLogger(__name__)


class SheetsFormatter:
    """Applies formatting to Google Sheets."""
    
    def __init__(self, service, sheet_id: str):
        """
        Initialize formatter.
        
        Args:
            service: Google Sheets API service
            sheet_id: Google Sheet ID
        """
        self.service = service
        self.sheet_id = sheet_id
    
    def get_sheet_id_by_name(self, sheet_name: str) -> int:
        """
        Get sheet ID by name.
        
        Args:
            sheet_name: Name of the sheet tab
            
        Returns:
            Sheet ID
        """
        try:
            sheet_metadata = self.service.spreadsheets().get(
                spreadsheetId=self.sheet_id
            ).execute()
            
            for sheet in sheet_metadata['sheets']:
                if sheet['properties']['title'] == sheet_name:
                    return sheet['properties']['sheetId']
            
            raise ValueError(f"Sheet '{sheet_name}' not found")
        except Exception as e:
            logger.error(f"Failed to get sheet ID: {e}")
            raise
    
    def apply_quality_score_formatting(self, sheet_name: str, column_index: int):
        """
        Apply conditional formatting for quality scores.
        
        Green: >= 85
        Yellow: 70-84
        Red: < 70
        
        Args:
            sheet_name: Name of the sheet tab
            column_index: Column index (0-based)
        """
        sheet_id = self.get_sheet_id_by_name(sheet_name)
        
        requests = []
        
        # Green (>= 85)
        requests.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'sheetId': sheet_id,
                        'startColumnIndex': column_index,
                        'endColumnIndex': column_index + 1,
                        'startRowIndex': 1
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'NUMBER_GREATER_THAN_EQ',
                            'values': [{'userEnteredValue': '85'}]
                        },
                        'format': {
                            'backgroundColor': {'red': 0.7, 'green': 0.9, 'blue': 0.7}
                        }
                    }
                },
                'index': 0
            }
        })
        
        # Yellow (70-84)
        requests.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'sheetId': sheet_id,
                        'startColumnIndex': column_index,
                        'endColumnIndex': column_index + 1,
                        'startRowIndex': 1
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'NUMBER_BETWEEN',
                            'values': [
                                {'userEnteredValue': '70'},
                                {'userEnteredValue': '84'}
                            ]
                        },
                        'format': {
                            'backgroundColor': {'red': 1.0, 'green': 0.9, 'blue': 0.6}
                        }
                    }
                },
                'index': 1
            }
        })
        
        # Red (< 70)
        requests.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'sheetId': sheet_id,
                        'startColumnIndex': column_index,
                        'endColumnIndex': column_index + 1,
                        'startRowIndex': 1
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'NUMBER_LESS',
                            'values': [{'userEnteredValue': '70'}]
                        },
                        'format': {
                            'backgroundColor': {'red': 0.9, 'green': 0.6, 'blue': 0.6}
                        }
                    }
                },
                'index': 2
            }
        })
        
        self._execute_requests(requests)
    
    def apply_velocity_formatting(self, sheet_name: str, column_index: int):
        """
        Apply conditional formatting for velocity.
        
        Bright Green: > 1.5x
        Green: 0.8-1.5x
        Yellow: 0.5-0.8x
        Red: < 0.5x
        
        Args:
            sheet_name: Name of the sheet tab
            column_index: Column index (0-based)
        """
        sheet_id = self.get_sheet_id_by_name(sheet_name)
        
        requests = []
        
        # Bright Green (> 1.5x)
        requests.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'sheetId': sheet_id,
                        'startColumnIndex': column_index,
                        'endColumnIndex': column_index + 1,
                        'startRowIndex': 1
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'NUMBER_GREATER',
                            'values': [{'userEnteredValue': '1.5'}]
                        },
                        'format': {
                            'backgroundColor': {'red': 0.5, 'green': 1.0, 'blue': 0.5}
                        }
                    }
                },
                'index': 0
            }
        })
        
        # Green (0.8-1.5x)
        requests.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'sheetId': sheet_id,
                        'startColumnIndex': column_index,
                        'endColumnIndex': column_index + 1,
                        'startRowIndex': 1
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'NUMBER_BETWEEN',
                            'values': [
                                {'userEnteredValue': '0.8'},
                                {'userEnteredValue': '1.5'}
                            ]
                        },
                        'format': {
                            'backgroundColor': {'red': 0.7, 'green': 0.9, 'blue': 0.7}
                        }
                    }
                },
                'index': 1
            }
        })
        
        self._execute_requests(requests)
    
    def apply_blocker_formatting(self, sheet_name: str, column_index: int):
        """
        Apply conditional formatting for blockers.
        
        Green: 0
        Yellow: 1-2
        Red + Bold: 3+
        
        Args:
            sheet_name: Name of the sheet tab
            column_index: Column index (0-based)
        """
        sheet_id = self.get_sheet_id_by_name(sheet_name)
        
        requests = []
        
        # Green (0)
        requests.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'sheetId': sheet_id,
                        'startColumnIndex': column_index,
                        'endColumnIndex': column_index + 1,
                        'startRowIndex': 1
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'NUMBER_EQ',
                            'values': [{'userEnteredValue': '0'}]
                        },
                        'format': {
                            'backgroundColor': {'red': 0.7, 'green': 0.9, 'blue': 0.7}
                        }
                    }
                },
                'index': 0
            }
        })
        
        # Yellow (1-2)
        requests.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'sheetId': sheet_id,
                        'startColumnIndex': column_index,
                        'endColumnIndex': column_index + 1,
                        'startRowIndex': 1
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'NUMBER_BETWEEN',
                            'values': [
                                {'userEnteredValue': '1'},
                                {'userEnteredValue': '2'}
                            ]
                        },
                        'format': {
                            'backgroundColor': {'red': 1.0, 'green': 0.9, 'blue': 0.6}
                        }
                    }
                },
                'index': 1
            }
        })
        
        # Red + Bold (3+)
        requests.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'sheetId': sheet_id,
                        'startColumnIndex': column_index,
                        'endColumnIndex': column_index + 1,
                        'startRowIndex': 1
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'NUMBER_GREATER_THAN_EQ',
                            'values': [{'userEnteredValue': '3'}]
                        },
                        'format': {
                            'backgroundColor': {'red': 0.9, 'green': 0.6, 'blue': 0.6},
                            'textFormat': {'bold': True}
                        }
                    }
                },
                'index': 2
            }
        })
        
        self._execute_requests(requests)
    
    def format_header_row(self, sheet_name: str):
        """
        Format header row with bold text and background color.
        
        Args:
            sheet_name: Name of the sheet tab
        """
        sheet_id = self.get_sheet_id_by_name(sheet_name)
        
        requests = [{
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 0,
                    'endRowIndex': 1
                },
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': {'red': 0.2, 'green': 0.3, 'blue': 0.5},
                        'textFormat': {
                            'bold': True,
                            'foregroundColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0}
                        },
                        'horizontalAlignment': 'CENTER'
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
            }
        }]
        
        self._execute_requests(requests)
    
    def _execute_requests(self, requests: List[Dict]):
        """
        Execute batch update requests.
        
        Args:
            requests: List of request objects
        """
        try:
            body = {'requests': requests}
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.sheet_id,
                body=body
            ).execute()
            
            logger.info(f"Applied {len(requests)} formatting rules")
        except Exception as e:
            logger.error(f"Failed to apply formatting: {e}")
            raise
    
    def apply_all_formatting(self):
        """Apply all standard formatting to dashboard."""
        logger.info("Applying dashboard formatting...")
        
        try:
            # Format headers for all sheets
            for sheet_name in ['Daily_Metrics', 'Weekly_Trends', 'Team_Performance', 
                               'Bot_Reports', 'Executive_Dashboard']:
                self.format_header_row(sheet_name)
            
            # Apply conditional formatting
            self.apply_quality_score_formatting('Daily_Metrics', 7)  # Quality score column
            self.apply_quality_score_formatting('Team_Performance', 5)  # Quality score column
            
            logger.info("Formatting complete")
        except Exception as e:
            logger.error(f"Failed to apply all formatting: {e}")
            raise
