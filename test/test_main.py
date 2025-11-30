from main import process_order
from fix_parser import FixParser
from risk_engine import RiskEngine
from logger import Logger


def test_process_order_success():
    """Test processing a successful order."""
    fix = FixParser()
    risk = RiskEngine(max_order_size=1000, max_position=2000)
    logger = Logger("test_main_1.json")
    
    raw = "8=FIX.4.2|35=D|55=AAPL|54=1|38=500|40=2|10=128"
    process_order(raw, fix, risk, logger)
    
    assert risk.positions['AAPL'] == 500
    assert len(logger.events) == 2  # Created and Filled


def test_process_order_size_rejection():
    """Test processing an order that exceeds size limit."""
    fix = FixParser()
    risk = RiskEngine(max_order_size=1000, max_position=2000)
    logger = Logger("test_main_2.json")
    
    raw = "8=FIX.4.2|35=D|55=GOOGL|54=1|38=1500|40=2|10=131"
    process_order(raw, fix, risk, logger)
    
    assert 'GOOGL' not in risk.positions or risk.positions['GOOGL'] == 0
    assert len(logger.events) == 2  # Created and Rejected


def test_process_order_position_rejection():
    """Test processing an order that exceeds position limit."""
    fix = FixParser()
    risk = RiskEngine(max_order_size=1000, max_position=2000)
    logger = Logger("test_main_3.json")
    
    # Setup existing position
    risk.positions['AAPL'] = 1500
    
    raw = "8=FIX.4.2|35=D|55=AAPL|54=1|38=600|40=2|10=132"
    process_order(raw, fix, risk, logger)
    
    assert risk.positions['AAPL'] == 1500  # Position unchanged
    assert len(logger.events) == 2  # Created and Rejected


def test_process_order_invalid_message():
    """Test processing an invalid FIX message."""
    fix = FixParser()
    risk = RiskEngine(max_order_size=1000, max_position=2000)
    logger = Logger("test_main_4.json")
    
    raw = "8=FIX.4.2|35=D|54=1|38=500"  # Missing required symbol field
    process_order(raw, fix, risk, logger)
    
    assert len(logger.events) == 1  # Only error logged

