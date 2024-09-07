import unittest
from Operation import Operation, MiningTruck, UnloadStation  # Adjust import as necessary

class TestOperation(unittest.TestCase):
    def test_find_min_wait_station(self):
        operation = Operation(truck_count=5, station_count=3)
        # Add trucks to stations to create varying queue lengths
        # You might need to adjust this based on your exact logic
        operation.stations[0].add_truck(MiningTruck(id=1))
        operation.stations[1].add_truck(MiningTruck(id=2))
        min_wait_station = operation.find_min_wait_station()
        self.assertEqual(min_wait_station.id, 0)

    # Add more tests for other methods as needed

if __name__ == '__main__':
    unittest.main()
