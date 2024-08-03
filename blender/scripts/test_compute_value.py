# test_calculator.py
import unittest
from interior_wall_assembly import get_value


class TestGetValue(unittest.TestCase):

    def test_single_value(self):
        result = get_value(1)
        self.assertEqual(result, 1)

    def test_array(self):
        result = get_value([1, 2])
        self.assertEqual(result, 3)

    def test_nested_array(self):
        result = get_value([1, [2, [3, 4]]])
        self.assertEqual(result, 10)

    def test_sum_function(self):
        result = get_value({"fn": "sum", "args": [1, 2]})
        self.assertEqual(result, 3)

    def test_nested_sum_function(self):
        result = get_value({
            "fn": "sum",
            "args": [
                1,
                {
                    "fn": "sum",
                    "args": [
                        2,
                        3
                    ]
                }
            ]
        })
        self.assertEqual(result, 6)


if __name__ == "__main__":
    unittest.main()
