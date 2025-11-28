"""Tests for Logger functionality."""

import json
import os
from logger import Logger


def test_log_event():
    """Test logging an event."""
    logger = Logger("test_events_1.json")
    logger.log("TestEvent", {"key": "value"})
    
    assert len(logger.events) == 1
    assert logger.events[0]['event_type'] == "TestEvent"
    assert logger.events[0]['data'] == {"key": "value"}


def test_log_multiple_events():
    """Test logging multiple events."""
    logger = Logger("test_events_2.json")
    logger.log("Event1", {"a": 1})
    logger.log("Event2", {"b": 2})
    
    assert len(logger.events) == 2


def test_save_to_file():
    """Test saving events to JSON file."""
    test_file = "test_events_3.json"
    logger = Logger(test_file)
    logger.log("TestEvent", {"key": "value"})
    logger.save()
    
    # Verify file exists and contains correct data
    assert os.path.exists(test_file)
    
    with open(test_file, 'r') as f:
        data = json.load(f)
    
    assert len(data) == 1
    assert data[0]['event_type'] == "TestEvent"
    
    # Cleanup
    os.remove(test_file)


def test_timestamp_in_events():
    """Test that events include timestamps."""
    logger = Logger("test_events_4.json")
    logger.log("TestEvent", {"key": "value"})
    
    assert 'timestamp' in logger.events[0]


if __name__ == '__main__':
    test_log_event()
    test_log_multiple_events()
    test_save_to_file()
    test_timestamp_in_events()
    print("All Logger tests passed!")

