import pytest
from temp_log import CircularBuffer, SensorDataLogger, read_temperature_sensor
import threading
import time

def test_CircularBuffer_initially_empty():
    buffer = CircularBuffer()
    assert buffer.get_last_10() == []

def test_CircularBuffer_add_single_item():
    buffer = CircularBuffer()
    buffer.add(25.5)
    assert buffer.get_last_10() == [25.5]

def test_CircularBuffer_add_multiple_items():
    buffer = CircularBuffer()
    for i in range(15):
        buffer.add(i)
    assert buffer.get_last_10() == list(range(5, 15))

def test_CircularBuffer_add_items_up_to_capacity():
    buffer = CircularBuffer()
    for i in range(10):
        buffer.add(i)
    assert buffer.get_last_10() == list(range(10))

def test_CircularBuffer_add_items_beyond_capacity():
    buffer = CircularBuffer()
    for i in range(20):
        buffer.add(i)
    assert buffer.get_last_10() == list(range(10, 20))

def test_SensorDataLogger_initially_empty_buffer():
    logger = SensorDataLogger()
    assert logger.buffer.get_last_10() == []

def test_SensorDataLogger_add_sensor_readings():
    logger = SensorDataLogger()
    logger.buffer.add(25.5)
    assert logger.buffer.get_last_10() == [25.5]

def test_SensorDataLogger_start_and_stop_logging():
    logger = SensorDataLogger()
    sensor_thread, display_thread = logger.start()
    time.sleep(2)
    logger.stop()
    sensor_thread.join()
    display_thread.join()
    assert logger.stop_event.is_set()