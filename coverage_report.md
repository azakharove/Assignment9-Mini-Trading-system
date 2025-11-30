# Coverage Report - Mini Trading System

## Test Summary

**Date**: November 30, 2025  
**Total Tests**: 27  
**Tests Passed**: 27  
**Tests Failed**: 0  
**Success Rate**: 100%

## Code Coverage

| Module          | Statements | Missing | Coverage |
|-----------------|------------|---------|----------|
| fix_parser.py   | 16         | 2       | 88%      |
| logger.py       | 14         | 0       | 100%     |
| main.py         | 38         | 15      | 61%      |
| order.py        | 21         | 1       | 95%      |
| risk_engine.py  | 19         | 0       | 100%     |
| **TOTAL**       | **108**    | **18**  | **83%**  |

## Test Breakdown

### Part 1: FIX Message Parser (4 tests)
- Parse valid FIX message
- Validate missing symbol detection
- Validate missing side detection
- Validate missing quantity detection

### Part 2: Order Lifecycle Simulator (6 tests)
- Order initialization
- State transitions: NEW to ACKED, NEW to REJECTED
- State transitions: ACKED to FILLED, ACKED to CANCELED
- Invalid transition handling

### Part 3: Risk Check Engine (6 tests)
- Order within limits validation
- Order size limit enforcement
- Position updates for buy/sell orders
- Position limit enforcement
- Multi-symbol risk tracking

### Part 4: Event Logger (4 tests)
- Single and multiple event logging
- JSON file persistence
- Timestamp inclusion

### Part 5: Main Integration (4 tests)
- Successful order processing
- Size limit rejection
- Position limit rejection
- Invalid message handling

### Part 6: Integration Tests (3 tests)
- Complete successful order flow
- Complete rejected order flow
- Multiple orders with full logging

## Running Tests

```bash
# Run all tests
pytest test/ -v

# Run with coverage
python -m coverage run --source=. -m pytest test/
python -m coverage report --omit="test/*"

# Run individual component tests
pytest test/test_fix_parser.py
pytest test/test_order.py
pytest test/test_risk_engine.py
pytest test/test_logger.py
pytest test/test_main.py
pytest test/test_integration.py
```

