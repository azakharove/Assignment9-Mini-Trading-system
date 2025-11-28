"""Integration tests for the complete system."""

import os
from fix_parser import FixParser
from order import Order, OrderState
from risk_engine import RiskEngine
from logger import Logger


def test_successful_order_flow():
    """Test complete flow of a successful order."""
    parser = FixParser()
    risk = RiskEngine(max_order_size=1000, max_position=2000)
    logger = Logger("test_integration_1.json")
    
    raw = "8=FIX.4.2|35=D|55=AAPL|54=1|38=500|40=2|10=128"
    
    # Parse
    msg = parser.parse(raw)
    
    # Create order
    order = Order(msg["55"], int(msg["38"]), msg["54"])
    
    # Risk check
    assert risk.check(order) == True
    
    # Acknowledge
    order.transition(OrderState.ACKED)
    assert order.state == OrderState.ACKED
    
    # Update and fill
    risk.update_position(order)
    order.transition(OrderState.FILLED)
    assert order.state == OrderState.FILLED
    
    # Check position
    assert risk.positions['AAPL'] == 500


def test_rejected_order_flow():
    """Test complete flow of a rejected order."""
    parser = FixParser()
    risk = RiskEngine(max_order_size=1000, max_position=2000)
    logger = Logger("test_integration_2.json")
    
    raw = "8=FIX.4.2|35=D|55=AAPL|54=1|38=1500|40=2|10=128"
    
    # Parse
    msg = parser.parse(raw)
    
    # Create order
    order = Order(msg["55"], int(msg["38"]), msg["54"])
    
    # Risk check should fail
    try:
        risk.check(order)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    # Reject order
    order.transition(OrderState.REJECTED)
    assert order.state == OrderState.REJECTED


def test_multiple_orders_with_logging():
    """Test processing multiple orders with full logging."""
    test_file = "test_integration_3.json"
    parser = FixParser()
    risk = RiskEngine(max_order_size=1000, max_position=2000)
    logger = Logger(test_file)
    
    messages = [
        "8=FIX.4.2|35=D|55=AAPL|54=1|38=500|40=2|10=128",
        "8=FIX.4.2|35=D|55=MSFT|54=2|38=300|40=2|10=129",
    ]
    
    for raw in messages:
        msg = parser.parse(raw)
        order = Order(msg["55"], int(msg["38"]), msg["54"])
        logger.log("OrderCreated", msg)
        
        try:
            risk.check(order)
            order.transition(OrderState.ACKED)
            risk.update_position(order)
            order.transition(OrderState.FILLED)
            logger.log("OrderFilled", {
                "symbol": order.symbol,
                "qty": order.qty,
                "side": order.side
            })
        except ValueError as e:
            order.transition(OrderState.REJECTED)
            logger.log("OrderRejected", {"symbol": order.symbol, "reason": str(e)})
    
    logger.save()
    
    # Verify results
    assert risk.positions['AAPL'] == 500
    assert risk.positions['MSFT'] == -300
    assert len(logger.events) == 4  # 2 creates + 2 fills
    
    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)


if __name__ == '__main__':
    test_successful_order_flow()
    test_rejected_order_flow()
    test_multiple_orders_with_logging()
    print("All integration tests passed!")

