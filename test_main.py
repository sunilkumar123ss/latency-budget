import unittest
try:
    from .main import analyze
except ImportError:
    from main import analyze

class BudgetTests(unittest.TestCase):

    def test_parallel_join_not_sum(self):
        stages = [{'name': 'a', 'duration_ms': 10}, {'name': 'b', 'duration_ms': 30}, {'name': 'join', 'duration_ms': 5, 'depends_on': ['a', 'b']}]
        r = analyze(stages, 40)
        self.assertEqual(r['estimated_latency_ms'], 35)
        self.assertEqual(r['critical_path'], ['b', 'join'])
        self.assertTrue(r['within_budget'])

    def test_unsorted_and_over_budget(self):
        r = analyze([{'name': 'b', 'duration_ms': 3, 'depends_on': ['a']}, {'name': 'a', 'duration_ms': 2}], 4)
        self.assertEqual(r['remaining_ms'], -1)

    def test_cycle(self):
        with self.assertRaises(ValueError):
            analyze([{'name': 'a', 'duration_ms': 1, 'depends_on': ['a']}], 10)
