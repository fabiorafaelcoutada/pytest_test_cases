import random
import threading
import time

class CircularBuffer:
    def __init__(self):
        self.capacity = 10
        self.buffer = [None] * self.capacity
        self.head = 0
        self.tail = 0
        self.size = 0
        self.lock = threading.Lock()

    def add(self, item):
        with self.lock:
            self.buffer[self.tail] = item
            self.tail = (self.tail + 1) % self.capacity

            if self.size < self.capacity:
                self.size += 1
            else:
                self.head = (self.head + 1) % self.capacity

    def get_last_10(self):
        with self.lock:
            if self.size == 0:
                return []
            start = self.tail - self.size if self.size < self.capacity else self.tail
            return [self.buffer[i % self.capacity] for i in range(start, start + self.size)]

def read_temperature_sensor():
    return round(random.uniform(-50, 50), 2)

class SensorDataLogger:
    def __init__(self):
        self.buffer = CircularBuffer()
        self.stop_event = threading.Event()

    def sensor_reading_task(self):
        while True:  # Infinite loop
            temp = read_temperature_sensor()
            print(f"Sensor Reading: {temp}°C")
            self.buffer.add(temp)
            time.sleep(1)

    def data_display_task(self):
        while True:  # Infinite loop
            time.sleep(5)
            readings = self.buffer.get_last_10()
            if readings:
                print("\n--- Buffer Contents (10 most recent) ---")
                for reading in readings:
                    print(f"{reading}°C")
                print("----------------------\n")

    def start(self):
        sensor_thread = threading.Thread(target=self.sensor_reading_task)
        display_thread = threading.Thread(target=self.data_display_task)

        sensor_thread.start()
        display_thread.start()

        return sensor_thread, display_thread

    def stop(self):
        self.stop_event.set()

def main():
    logger = SensorDataLogger()
    sensor_thread, display_thread = logger.start()

    try:
        time.sleep(30)
    finally:
        logger.stop()
        sensor_thread.join()
        display_thread.join()

if __name__ == "__main__":
    main()