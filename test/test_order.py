from order import Order, OrderState


def test_order_creation():
    """Test order initialization."""
    order = Order('AAPL', 100, '1')
    assert order.symbol == 'AAPL'
    assert order.qty == 100
    assert order.side == '1'
    assert order.state == OrderState.NEW


def test_valid_transition_new_to_acked():
    """Test valid transition from NEW to ACKED."""
    order = Order('AAPL', 100, '1')
    order.transition(OrderState.ACKED)
    assert order.state == OrderState.ACKED


def test_valid_transition_new_to_rejected():
    """Test valid transition from NEW to REJECTED."""
    order = Order('AAPL', 100, '1')
    order.transition(OrderState.REJECTED)
    assert order.state == OrderState.REJECTED


def test_valid_transition_acked_to_filled():
    """Test valid transition from ACKED to FILLED."""
    order = Order('AAPL', 100, '1')
    order.transition(OrderState.ACKED)
    order.transition(OrderState.FILLED)
    assert order.state == OrderState.FILLED


def test_valid_transition_acked_to_canceled():
    """Test valid transition from ACKED to CANCELED."""
    order = Order('AAPL', 100, '1')
    order.transition(OrderState.ACKED)
    order.transition(OrderState.CANCELED)
    assert order.state == OrderState.CANCELED


def test_invalid_transition():
    """Test that invalid transitions don't change state."""
    order = Order('AAPL', 100, '1')
    order.transition(OrderState.FILLED)  # Can't go from NEW to FILLED
    assert order.state == OrderState.NEW

