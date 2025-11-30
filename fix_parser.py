class FixParser:
    """Parse FIX protocol messages into structured dictionaries."""
    
    def parse(self, raw_msg: str) -> dict:
        """
        Parse a FIX message string into a dictionary.
        
        Args:
            raw_msg: FIX message string with fields separated by '|'
            
        Returns:
            Dictionary mapping FIX tags to values
            
        Raises:
            ValueError: If required fields are missing
        """
        # Split by delimiter and parse tag=value pairs
        fields = raw_msg.split('|')
        msg_dict = {}
        
        for field in fields:
            if '=' in field:
                tag, value = field.split('=', 1)
                msg_dict[tag] = value
        
        # Validate required fields
        required_tags = {
            '55': 'Symbol',
            '54': 'Side',
            '38': 'OrderQty'
        }
        
        for tag, name in required_tags.items():
            if tag not in msg_dict:
                raise ValueError(f"Missing required field: {name} (tag {tag})")
        
        return msg_dict

if __name__ == "__main__":
    msg = "8=FIX.4.2|35=D|55=AAPL|54=1|38=100|40=2|10=128"
    print(FixParser().parse(msg))