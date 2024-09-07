import unittest
from Operation import UnloadStation, MiningTruck  # Adjust import as necessary

class TestUnloadStation(unittest.TestCase):
    def test_add_truck(self):
        station = UnloadStation(id=1)
        truck = MiningTruck(id=1)
        station.add_truck(truck)
        self.assertIn(truck, station.queue)

    def test_remove_truck(self):
        station = UnloadStation(id=1)
        truck = MiningTruck(id=1)
        station.add_truck(truck)
        station.remove_truck()
        self.assertNotIn(truck, station.queue)

if __name__ == '__main__':
    unittest.main()
