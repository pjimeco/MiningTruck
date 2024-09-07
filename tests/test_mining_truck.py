import unittest
from Operation import MiningTruck  

class TestMiningTruck(unittest.TestCase):
    def test_initial_state(self):
        truck = MiningTruck(id=1)
        self.assertEqual(truck.state, 'unstarted')
        self.assertEqual(truck.time_mining, 0.0)
        self.assertEqual(truck.time_traveling, 0.0)
        self.assertEqual(truck.time_waiting, 0.0)
        self.assertEqual(truck.time_unloading, 0.0)
        self.assertEqual(truck.time_remaining, 0.0)
        self.assertIsNone(truck.current_station)
        self.assertEqual(truck.load_count, 0)

    def test_start_mine(self):
        truck = MiningTruck(id=1)
        truck.start_mine()
        self.assertEqual(truck.state, 'mining')
        self.assertGreater(truck.time_remaining, 0)

    def test_start_travel_to_station(self):
        truck = MiningTruck(id=1)
        truck.start_travel_to_station()
        self.assertEqual(truck.state, 'travel_to_station')
        self.assertEqual(truck.time_remaining, 0.5)


if __name__ == '__main__':
    unittest.main()
