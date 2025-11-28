from fix_parser import FixParser
from order import Order, OrderState
from risk_engine import RiskEngine
from logger import Logger

def process_order(raw_msg: str, fix: FixParser, risk: RiskEngine, log: Logger):
    """Process a single FIX order message through the trading system."""
    try:
        # Parse FIX message
        msg = fix.parse(raw_msg)
        
        # Create order
        order = Order(msg["55"], int(msg["38"]), msg["54"])
        log.log("OrderCreated", msg)
        
        try:
            # Risk check
            risk.check(order)
            
            # Acknowledge order
            order.transition(OrderState.ACKED)
            
            # Update position and fill
            risk.update_position(order)
            order.transition(OrderState.FILLED)
            log.log("OrderFilled", {
                "symbol": order.symbol, 
                "qty": order.qty,
                "side": order.side
            })
        except ValueError as e:
            # Risk check failed
            order.transition(OrderState.REJECTED)
            log.log("OrderRejected", {"symbol": order.symbol, "reason": str(e)})
    except Exception as e:
        # Parse error or other exception
        log.log("Error", {"message": str(e), "raw": raw_msg})
        print(f"[ERROR] {e}")

def main():
    """Main entry point - process multiple FIX messages."""
    fix = FixParser()
    risk = RiskEngine(max_order_size=1000, max_position=2000)
    log = Logger()
    
    # Sample FIX messages
    messages = [
        "8=FIX.4.2|35=D|55=AAPL|54=1|38=500|40=2|10=128",
        "8=FIX.4.2|35=D|55=AAPL|54=1|38=800|40=2|10=129",
        "8=FIX.4.2|35=D|55=MSFT|54=2|38=300|40=2|10=130",
        "8=FIX.4.2|35=D|55=GOOGL|54=1|38=1500|40=2|10=131",  # Should fail - too large
        "8=FIX.4.2|35=D|55=AAPL|54=1|38=900|40=2|10=132",    # Should fail - position limit
    ]
    
    print("="*60)
    print("Mini Trading System - Processing Orders")
    print("="*60)
    
    for raw_msg in messages:
        print()
        process_order(raw_msg, fix, risk, log)
    
    print()
    print("="*60)
    log.save()
    print(f"Final Positions: {risk.positions}")

if __name__ == "__main__":
    main()