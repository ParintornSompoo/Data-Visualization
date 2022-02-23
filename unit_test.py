import pandas as pd
from pandas.testing import assert_frame_equal
import unittest
from function import is_datetime, transform_range, reverse_transform_range, get_filter_data, union_data

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

    def test_get_filter_data(self):
        '''
        test filter data function

        Parameters:
        data (pandas dataframe): data
        dimension filter (dict): selected dimension
        measurement filter (dict): selected measurement
        '''
        DATA = {"id":   ["a","a","b","b","c","c","c","d"],
                "value": [1,  2,  3,  4,  5,  6,  7,  8]}
        data = pd.DataFrame(DATA)

        df1 = pd.DataFrame({"id":["a","a"],"value": [1,  2]}).reset_index(drop=True)
        df2 = get_filter_data(data,{"id":"a"},{}).reset_index(drop=True)
        assert_frame_equal(df1, df2)

        df1 = pd.DataFrame({"id":["b","b"],"value": [3,  4]}).reset_index(drop=True)
        df2 = get_filter_data(data,{"id":"b"},{}).reset_index(drop=True)
        assert_frame_equal(df1, df2)

        df1 = pd.DataFrame({"id":["c","c","c"],"value": [5,  6,  7]}).reset_index(drop=True)
        df2 = get_filter_data(data,{"id":"c"},{}).reset_index(drop=True)
        assert_frame_equal(df1, df2)

        df1 = pd.DataFrame({"id":["c","c"],"value": [5,  6]}).reset_index(drop=True)
        df2 = get_filter_data(data,{"id":"c"},{"value":{"min":5,"max":6}}).reset_index(drop=True)
        assert_frame_equal(df1, df2)

        df1 = pd.DataFrame({"id":["c"],"value": [5]}).reset_index(drop=True)
        df2 = get_filter_data(data,{"id":"c"},{"value":{"min":5,"max":5}}).reset_index(drop=True)
        assert_frame_equal(df1, df2)

        df1 = pd.DataFrame({"id":["c","c"],"value": [6,  7]}).reset_index(drop=True)
        df2 = get_filter_data(data,{"id":"c"},{"value":{"min":6,"max":7}}).reset_index(drop=True)
        assert_frame_equal(df1, df2)

        df1 = pd.DataFrame({"id":["d"],"value": [8]}).reset_index(drop=True)
        df2 = get_filter_data(data,{"id":"d"},{"value":{"min":1,"max":8}}).reset_index(drop=True)
        assert_frame_equal(df1, df2)

        df1 = pd.DataFrame({"id":["a","a","b","b"],"value": [1,  2,  3,  4]}).reset_index(drop=True)
        df2 = get_filter_data(data,{},{"value":{"min":1,"max":4}}).reset_index(drop=True)
        assert_frame_equal(df1, df2)

        df1 = pd.DataFrame({"id":["c","c","c","d"],"value": [5,  6,  7,  8]}).reset_index(drop=True)
        df2 = get_filter_data(data,{},{"value":{"min":5,"max":8}}).reset_index(drop=True)
        assert_frame_equal(df1, df2)

    def test_union_data(self):
        DATA = {"id":   ["a","a","b","b","c","c","c","d"],
                "value": [1,  2,  3,  4,  5,  6,  7,  8]}
        data = pd.DataFrame(DATA).reset_index(drop=True)

        df1 = pd.DataFrame({"id":["a","a","b","b"],"value": [1,  2,  3,  4]})
        df2 = union_data(df1,"test_union.csv")
        assert_frame_equal(data, df2)

        df1 = pd.DataFrame({"id":["a","a","b","b"],"value": [1,  2,  3,  4]})
        df2 = union_data(df1,"test_union.xlsx")
        assert_frame_equal(data, df2)
        
if __name__ == '__main__':
    unittest.main()