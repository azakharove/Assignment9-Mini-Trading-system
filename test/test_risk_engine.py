
from order import Order
from risk_engine import RiskEngine


def test_order_within_limits():
    """Test that order within limits passes."""
    risk = RiskEngine(max_order_size=1000, max_position=2000)
    order = Order('AAPL', 500, '1')
    result = risk.check(order)
    assert result == True


def test_order_exceeds_size_limit():
    """Test that oversized order is rejected."""
    risk = RiskEngine(max_order_size=1000, max_position=2000)
    order = Order('AAPL', 1500, '1')
    
    try:
        risk.check(order)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert 'exceeds max' in str(e)


def test_position_update_buy():
    """Test position update for buy order."""
    risk = RiskEngine(max_order_size=1000, max_position=2000)
    order = Order('AAPL', 100, '1')
    risk.update_position(order)
    assert risk.positions['AAPL'] == 100


def test_position_update_sell():
    """Test position update for sell order."""
    risk = RiskEngine(max_order_size=1000, max_position=2000)
    order = Order('AAPL', 100, '2')
    risk.update_position(order)
    assert risk.positions['AAPL'] == -100


def test_position_limit_exceeded():
    """Test that position limit is enforced."""
    risk = RiskEngine(max_order_size=1000, max_position=2000)
    # Manually set position to test limit
    risk.positions['AAPL'] = 1500
    
    # Order that would exceed limit (within order size limit)
    order = Order('AAPL', 600, '1')
    
    try:
        risk.check(order)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert 'would exceed max' in str(e)


def test_multiple_symbols():
    """Test risk tracking across multiple symbols."""
    risk = RiskEngine(max_order_size=1000, max_position=2000)
    
    order1 = Order('AAPL', 500, '1')
    risk.check(order1)
    risk.update_position(order1)
    
    order2 = Order('MSFT', 300, '2')
    risk.check(order2)
    risk.update_position(order2)
    
    assert risk.positions['AAPL'] == 500
    assert risk.positions['MSFT'] == -300
