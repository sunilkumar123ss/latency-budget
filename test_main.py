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
