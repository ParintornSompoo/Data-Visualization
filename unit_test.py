import pandas as pd
import unittest
from function import is_datetime, transform_range, reverse_transform_range

class TestStringMethods(unittest.TestCase):

    def test_datetime(self):
        # check if string is a datetime dimensions
        self.assertTrue(is_datetime("order date"))
        self.assertTrue(is_datetime("order-date"))
        self.assertTrue(is_datetime("order Date"))
        self.assertTrue(is_datetime("ORDER DATE"))
        self.assertTrue(is_datetime("ORDER_DATE"))

        self.assertTrue(is_datetime("Ship Date"))
        self.assertFalse(is_datetime("Ship Mode"))
        self.assertFalse(is_datetime("Category"))

        # measurements is not a datetime dimensions
        for word in ["Sales","Quantity","Discount","Profit"]:
            self.assertFalse(is_datetime(word))

    def test_transform_range(self):
        '''
        transform range is use in slider to get the value 
        from slider widget that have range from 0 to 100
        to any range

        Parameters:
        agrs1 (number): value from slider (0 - 100)
        agrs2 (list) : list of new range [x1, x2]
        '''
        # transform from range (0-100) to new range
        _range = [0, 200]
        self.assertEqual(transform_range(50, _range), 100)

        _range = [0, 500]
        self.assertEqual(transform_range(75, _range), 375)

        _range = [200, 1000]
        self.assertEqual(transform_range(0, _range), 200)
        self.assertEqual(transform_range(100, _range), 1000)

        _range = [-1000, 1000]
        self.assertEqual(transform_range(0, _range), -1000)
        self.assertEqual(transform_range(25, _range), -500)
        self.assertEqual(transform_range(50, _range), 0)
        self.assertEqual(transform_range(100, _range), 1000)

    def test_reverse_transform_range(self):
        '''
        reverse transform range is use to convert value 
        from data to set slider postion between 0 and 100

        Parameters:
        args1 (number): value from between range (x)
        agrs2 (list): list of range [x1, x2]
        '''
        # transform from any range to (0-100)
        _range = [0, 1000]
        self.assertEqual(reverse_transform_range(10, _range), 1)
        self.assertEqual(reverse_transform_range(100, _range), 10)
        self.assertEqual(reverse_transform_range(1000, _range), 100)

        _range = [50, 100]
        self.assertEqual(reverse_transform_range(75, _range), 50)
        self.assertEqual(reverse_transform_range(90, _range), 80)
        self.assertEqual(reverse_transform_range(100, _range), 100)

        _range = [-100, 100]
        self.assertEqual(reverse_transform_range(-50, _range), 25)
        self.assertEqual(reverse_transform_range(0, _range), 50)
        self.assertEqual(reverse_transform_range(50, _range), 75)
    
if __name__ == '__main__':
    unittest.main()