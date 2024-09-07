import unittest
from Operation import Operation  # Adjust import as necessary

class TestSimulation(unittest.TestCase):
    def test_simulation_run(self):
        operation = Operation(truck_count=10, station_count=5)
        operation.simulate()
        # Check if the simulation ran correctly
        self.assertGreater(len(operation.truck_times), 0)
        self.assertGreater(len(operation.station_loads), 0)

if __name__ == '__main__':
    unittest.main()
