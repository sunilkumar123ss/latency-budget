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

    def test_invalid(self):
        for stages in [[{'name': 'a', 'duration_ms': -1}], [{'name': 'a', 'duration_ms': 1, 'depends_on': ['missing']}], [{'name': 'a', 'duration_ms': 1}] * 2]:
            with self.assertRaises(ValueError):
                analyze(stages, 1)
        with self.assertRaises(ValueError):
            analyze([], float('nan'))

    def test_long_chain_without_recursion(self):
        stages = [{'name': str(i), 'duration_ms': 1, 'depends_on': [str(i - 1)] if i else []} for i in range(500)]
        self.assertEqual(analyze(stages, 500)['estimated_latency_ms'], 500)

    def test_empty(self):
        self.assertEqual(analyze([], 0)['estimated_latency_ms'], 0)
if __name__ == '__main__':
    unittest.main()
