# test_calculator.py
import unittest
from interior_wall_assembly import map_network

import json
import difflib


def test_compare_dicts(res, exp):
    left = json.dumps(res, indent=2, sort_keys=True)
    right = json.dumps(exp, indent=2, sort_keys=True)

    diff = difflib.unified_diff(left.splitlines(
        True), right.splitlines(True), fromfile="left", tofile="right")
    assert 0, "\n" + "".join(diff)


class TestMapNetwork(unittest.TestCase):

    def test_single_value(self):

        input = {
            "type": "hvac_duct",
            "length": 3,
            "out": {
                "type": "hvac_duct",
                "length": 3
            }
        }

        expected = [
            {
                "type": "hvac_duct",
                "length": 3,
                "components": [
                    {
                        "name": "out",
                        "location": {
                            "x": 3
                        },
                        "components": [
                            {
                                "type": "hvac_duct",
                                "length": 3,
                                "components": [
                                    {
                                        "name": "out",
                                        "location": {
                                            "x": 3
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]

        result = map_network(input)
        print(json.dumps(result, indent=2, sort_keys=True))

        # test_compare_dicts(result, expected)
        # self.assertDictEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
