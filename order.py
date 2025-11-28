# order.py
from enum import Enum, auto

class OrderState(Enum):
    NEW = auto()
    ACKED = auto()
    FILLED = auto()
    CANCELED = auto()
    REJECTED = auto()

class Order:
    """Represents an order with state management."""
    
    def __init__(self, symbol: str, qty: int, side: str):
        """
        Initialize an order.
        
        Args:
            symbol: Trading symbol (e.g., 'AAPL')
            qty: Order quantity
            side: Order side ('1' for buy, '2' for sell)
        """
        self.symbol = symbol
        self.qty = qty
        self.side = side
        self.state = OrderState.NEW

    def transition(self, new_state: OrderState):
        """
        Transition order to a new state.
        
        Args:
            new_state: Target OrderState
            
        Raises:
            ValueError: If transition is not allowed
        """
        allowed = {
            OrderState.NEW: {OrderState.ACKED, OrderState.REJECTED},
            OrderState.ACKED: {OrderState.FILLED, OrderState.CANCELED},
        }
        
        # Check if transition is allowed
        if self.state in allowed and new_state in allowed[self.state]:
            self.state = new_state
            print(f"Order {self.symbol} is now {new_state.name}")
        elif self.state == new_state:
            # Already in that state, no-op
            pass
        else:
            print(f"[WARNING] Invalid transition from {self.state.name} to {new_state.name}")