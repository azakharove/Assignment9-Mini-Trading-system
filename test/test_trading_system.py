"""Unit tests for Mini Trading System."""

import unittest
import json
import os
from fix_parser import FixParser
from order import Order, OrderState
from risk_engine import RiskEngine
from logger import Logger


class TestFixParser(unittest.TestCase):
    """Test FIX message parser."""
    
    def setUp(self):
        self.parser = FixParser()
    
    def test_parse_valid_message(self):
        """Test parsing a valid FIX message."""
        msg = "8=FIX.4.2|35=D|55=AAPL|54=1|38=100|40=2|10=128"
        result = self.parser.parse(msg)
        
        self.assertEqual(result['55'], 'AAPL')
        self.assertEqual(result['54'], '1')
        self.assertEqual(result['38'], '100')
    
    def test_parse_missing_symbol(self):
        """Test that missing symbol raises ValueError."""
        msg = "8=FIX.4.2|35=D|54=1|38=100|40=2|10=128"
        with self.assertRaises(ValueError) as ctx:
            self.parser.parse(msg)
        self.assertIn('Symbol', str(ctx.exception))
    
    def test_parse_missing_side(self):
        """Test that missing side raises ValueError."""
        msg = "8=FIX.4.2|35=D|55=AAPL|38=100|40=2|10=128"
        with self.assertRaises(ValueError) as ctx:
            self.parser.parse(msg)
        self.assertIn('Side', str(ctx.exception))
    
    def test_parse_missing_quantity(self):
        """Test that missing quantity raises ValueError."""
        msg = "8=FIX.4.2|35=D|55=AAPL|54=1|40=2|10=128"
        with self.assertRaises(ValueError) as ctx:
            self.parser.parse(msg)
        self.assertIn('OrderQty', str(ctx.exception))


class TestOrder(unittest.TestCase):
    """Test Order class and state transitions."""
    
    def test_order_creation(self):
        """Test order initialization."""
        order = Order('AAPL', 100, '1')
        self.assertEqual(order.symbol, 'AAPL')
        self.assertEqual(order.qty, 100)
        self.assertEqual(order.side, '1')
        self.assertEqual(order.state, OrderState.NEW)
    
    def test_valid_transition_new_to_acked(self):
        """Test valid transition from NEW to ACKED."""
        order = Order('AAPL', 100, '1')
        order.transition(OrderState.ACKED)
        self.assertEqual(order.state, OrderState.ACKED)
    
    def test_valid_transition_new_to_rejected(self):
        """Test valid transition from NEW to REJECTED."""
        order = Order('AAPL', 100, '1')
        order.transition(OrderState.REJECTED)
        self.assertEqual(order.state, OrderState.REJECTED)
    
    def test_valid_transition_acked_to_filled(self):
        """Test valid transition from ACKED to FILLED."""
        order = Order('AAPL', 100, '1')
        order.transition(OrderState.ACKED)
        order.transition(OrderState.FILLED)
        self.assertEqual(order.state, OrderState.FILLED)
    
    def test_valid_transition_acked_to_canceled(self):
        """Test valid transition from ACKED to CANCELED."""
        order = Order('AAPL', 100, '1')
        order.transition(OrderState.ACKED)
        order.transition(OrderState.CANCELED)
        self.assertEqual(order.state, OrderState.CANCELED)
    
    def test_invalid_transition(self):
        """Test that invalid transitions don't change state."""
        order = Order('AAPL', 100, '1')
        order.transition(OrderState.FILLED)  # Can't go from NEW to FILLED
        self.assertEqual(order.state, OrderState.NEW)


class TestRiskEngine(unittest.TestCase):
    """Test Risk Engine."""
    
    def setUp(self):
        self.risk = RiskEngine(max_order_size=1000, max_position=2000)
    
    def test_order_within_limits(self):
        """Test that order within limits passes."""
        order = Order('AAPL', 500, '1')
        result = self.risk.check(order)
        self.assertTrue(result)
    
    def test_order_exceeds_size_limit(self):
        """Test that oversized order is rejected."""
        order = Order('AAPL', 1500, '1')
        with self.assertRaises(ValueError) as ctx:
            self.risk.check(order)
        self.assertIn('exceeds max', str(ctx.exception))
    
    def test_position_update_buy(self):
        """Test position update for buy order."""
        order = Order('AAPL', 100, '1')
        self.risk.update_position(order)
        self.assertEqual(self.risk.positions['AAPL'], 100)
    
    def test_position_update_sell(self):
        """Test position update for sell order."""
        order = Order('AAPL', 100, '2')
        self.risk.update_position(order)
        self.assertEqual(self.risk.positions['AAPL'], -100)
    
    def test_position_limit_exceeded(self):
        """Test that position limit is enforced."""
        # First order
        order1 = Order('AAPL', 1500, '1')
        # Manually update position to test limit
        self.risk.positions['AAPL'] = 1500
        
        # Second order that would exceed limit (within order size limit)
        order2 = Order('AAPL', 600, '1')
        with self.assertRaises(ValueError) as ctx:
            self.risk.check(order2)
        self.assertIn('would exceed max', str(ctx.exception))
    
    def test_multiple_symbols(self):
        """Test risk tracking across multiple symbols."""
        order1 = Order('AAPL', 500, '1')
        order2 = Order('MSFT', 300, '2')
        
        self.risk.check(order1)
        self.risk.update_position(order1)
        
        self.risk.check(order2)
        self.risk.update_position(order2)
        
        self.assertEqual(self.risk.positions['AAPL'], 500)
        self.assertEqual(self.risk.positions['MSFT'], -300)


class TestLogger(unittest.TestCase):
    """Test Logger functionality."""
    
    def setUp(self):
        self.test_file = "test_events.json"
        self.logger = Logger(self.test_file)
    
    def tearDown(self):
        # Clean up test file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_log_event(self):
        """Test logging an event."""
        self.logger.log("TestEvent", {"key": "value"})
        self.assertEqual(len(self.logger.events), 1)
        self.assertEqual(self.logger.events[0]['event_type'], "TestEvent")
        self.assertEqual(self.logger.events[0]['data'], {"key": "value"})
    
    def test_log_multiple_events(self):
        """Test logging multiple events."""
        self.logger.log("Event1", {"a": 1})
        self.logger.log("Event2", {"b": 2})
        self.assertEqual(len(self.logger.events), 2)
    
    def test_save_to_file(self):
        """Test saving events to JSON file."""
        self.logger.log("TestEvent", {"key": "value"})
        self.logger.save()
        
        # Verify file exists and contains correct data
        self.assertTrue(os.path.exists(self.test_file))
        
        with open(self.test_file, 'r') as f:
            data = json.load(f)
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['event_type'], "TestEvent")
    
    def test_timestamp_in_events(self):
        """Test that events include timestamps."""
        self.logger.log("TestEvent", {"key": "value"})
        self.assertIn('timestamp', self.logger.events[0])


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    def setUp(self):
        self.parser = FixParser()
        self.risk = RiskEngine(max_order_size=1000, max_position=2000)
        self.logger = Logger("test_integration.json")
    
    def tearDown(self):
        if os.path.exists("test_integration.json"):
            os.remove("test_integration.json")
    
    def test_successful_order_flow(self):
        """Test complete flow of a successful order."""
        raw = "8=FIX.4.2|35=D|55=AAPL|54=1|38=500|40=2|10=128"
        
        # Parse
        msg = self.parser.parse(raw)
        
        # Create order
        order = Order(msg["55"], int(msg["38"]), msg["54"])
        
        # Risk check
        self.assertTrue(self.risk.check(order))
        
        # Acknowledge
        order.transition(OrderState.ACKED)
        self.assertEqual(order.state, OrderState.ACKED)
        
        # Update and fill
        self.risk.update_position(order)
        order.transition(OrderState.FILLED)
        self.assertEqual(order.state, OrderState.FILLED)
        
        # Check position
        self.assertEqual(self.risk.positions['AAPL'], 500)
    
    def test_rejected_order_flow(self):
        """Test complete flow of a rejected order."""
        raw = "8=FIX.4.2|35=D|55=AAPL|54=1|38=1500|40=2|10=128"
        
        # Parse
        msg = self.parser.parse(raw)
        
        # Create order
        order = Order(msg["55"], int(msg["38"]), msg["54"])
        
        # Risk check should fail
        with self.assertRaises(ValueError):
            self.risk.check(order)
        
        # Reject order
        order.transition(OrderState.REJECTED)
        self.assertEqual(order.state, OrderState.REJECTED)


if __name__ == '__main__':
    unittest.main()

