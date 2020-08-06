import os
import sys
import inspect
import unittest

current_dir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe()) + "/../")
)
sys.path.insert(0, current_dir)

from asg import UntangleConstraint
from entities import Point


class UntangleConstraintTest(unittest.TestCase):
    def test_point_relative_to_line(self):
        # Point on the line
        self.assertEqual(
            UntangleConstraint.point_loc_relative_to_line(
                (Point(1, 1), Point(2, 2)), Point(1.5, 1.5)
            ),
            0,
        )

        # Point below the line
        self.assertLess(
            UntangleConstraint.point_loc_relative_to_line(
                (Point(1, 1), Point(2, 2)), Point(1.7, 1.5)
            ),
            0,
        )

        # Point below the line
        self.assertGreater(
            UntangleConstraint.point_loc_relative_to_line(
                (Point(1, 1), Point(2, 2)), Point(1.3, 1.5)
            ),
            0,
        )

    def test_check_cross(self):
        self.assertTrue(
            UntangleConstraint.check_cross(
                (Point(1, 1), Point(2, 2)), (Point(1, 2), Point(2, 1))
            )
        )
        self.assertTrue(
            UntangleConstraint.check_cross(
                (Point(1, 1), Point(2, 2)), (Point(1, 2), Point(2, 2))
            )
        )
        self.assertFalse(
            UntangleConstraint.check_cross(
                (Point(1, 1), Point(2, 2)), (Point(1, 2), Point(2, 3))
            )
        )


if __name__ == "__main__":
    unittest.main()
