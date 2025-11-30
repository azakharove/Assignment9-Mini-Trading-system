from datetime import datetime
import json

class Logger:
    """Event logger for recording system activity."""
    
    def __init__(self, path="events.json"):
        """
        Initialize logger.
        
        Args:
            path: Path to save events JSON file
        """
        self.path = path
        self.events = []
    
    def log(self, event_type: str, data: dict):
        """
        Log an event with timestamp.
        
        Args:
            event_type: Type of event (e.g., 'OrderCreated')
            data: Event data dictionary
        """
        event = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'data': data
        }
        self.events.append(event)
        print(f"[LOG] {event_type} → {data}")

    def save(self):
        """Save all logged events to JSON file."""
        with open(self.path, 'w') as f:
            json.dump(self.events, f, indent=2)
        print(f"Events saved to {self.path}")