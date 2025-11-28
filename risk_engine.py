# risk_engine.py
class RiskEngine:
    """Risk management engine to validate orders against limits."""
    
    def __init__(self, max_order_size=1000, max_position=2000):
        """
        Initialize risk engine with limits.
        
        Args:
            max_order_size: Maximum size for a single order
            max_position: Maximum net position per symbol
        """
        self.max_order_size = max_order_size
        self.max_position = max_position
        self.positions = {}  # symbol -> net position

    def check(self, order) -> bool:
        """
        Validate order against risk limits.
        
        Args:
            order: Order object to validate
            
        Returns:
            True if order passes all checks
            
        Raises:
            ValueError: If order violates risk limits
        """
        # Check order size
        if order.qty > self.max_order_size:
            raise ValueError(f"Order size {order.qty} exceeds max {self.max_order_size}")
        
        # Check position limit
        current_pos = self.positions.get(order.symbol, 0)
        
        # Calculate new position (1 = buy, 2 = sell)
        qty_signed = order.qty if order.side == '1' else -order.qty
        new_pos = current_pos + qty_signed
        
        if abs(new_pos) > self.max_position:
            raise ValueError(
                f"Position {new_pos} would exceed max {self.max_position} for {order.symbol}"
            )
        
        return True

    def update_position(self, order):
        """
        Update position after order fill.
        
        Args:
            order: Filled order to update position with
        """
        if order.symbol not in self.positions:
            self.positions[order.symbol] = 0
        
        # Update position (1 = buy adds, 2 = sell subtracts)
        qty_signed = order.qty if order.side == '1' else -order.qty
        self.positions[order.symbol] += qty_signed