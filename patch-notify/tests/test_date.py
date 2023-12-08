import unittest
from datetime import date
from src.utils.date import find_patch_dates

## The main aim of the test suite is to test if the find patch dates function is working correctly 
## even with the variation in the months of a year

class TestFunctionResult(unittest.TestCase):
    def testIfResultIsDict(self):
        result = type(find_patch_dates()) is dict
        self.assertEqual(True, result)

    def testIfKeysExists(self):
        pass

class TestNovSchedule(unittest.TestCase):
    def testSecondThu(self):
        dates = find_patch_dates(2023,11)
        self.assertEqual(dates['2nd Thu'], date(2023,11,16), 'Found Date Should be Equal to November 16, 2023')
    
    def testThirdThu(self):
        dates = find_patch_dates(2023,11)
        self.assertEqual(dates['3rd Thu'], date(2023,11,23), 'Found Date Should be Equal to November 23, 2023')

    def testFourthThu(self):
        dates = find_patch_dates(2023,11)
        self.assertEqual(dates['4th Thu'], date(2023,11,30), 'Found Date Should be Equal to November 30, 2023')
    
    def testThirdTue(self):
        dates = find_patch_dates(2023,11)
        self.assertEqual(dates['3rd Tue'], date(2023,11,21), 'Found Date Should be Equal to November 21, 2023')

    def testFourthTue(self):
        dates = find_patch_dates(2023,11)
        self.assertEqual(dates['4th Tue'], date(2023,11,28), 'Found Date Should be Equal to November 28, 2023')


class TestOctSchedule(unittest.TestCase):
    def testSecondThu(self):
        dates = find_patch_dates(2023,10)
        self.assertEqual(dates['2nd Thu'], date(2023,10,12), 'Found Date Should be Equal to October 12, 2023')
    
    def testThirdThu(self):
        dates = find_patch_dates(2023,10)
        self.assertEqual(dates['3rd Thu'], date(2023,10,19), 'Found Date Should be Equal to October 19, 2023')

    def testFourthThu(self):
        dates = find_patch_dates(2023,10)
        self.assertEqual(dates['4th Thu'], date(2023,10,26), 'Found Date Should be Equal to October 26, 2023')
    
    def testThirdTue(self):
        dates = find_patch_dates(2023,10)
        self.assertEqual(dates['3rd Tue'], date(2023,10,17), 'Found Date Should be Equal to October 17, 2023')

    def testFourthTue(self):
        dates = find_patch_dates(2023,10)
        self.assertEqual(dates['4th Tue'], date(2023,10,24), 'Found Date Should be Equal to October 24, 2023')


class TestJuneSchedule(unittest.TestCase):
    def testSecondThu(self):
        dates = find_patch_dates(2023,6)
        self.assertEqual(dates['2nd Thu'], date(2023,6,15), 'Found Date Should be Equal to June 15, 2023')
    
    def testThirdThu(self):
        dates = find_patch_dates(2023,6)
        self.assertEqual(dates['3rd Thu'], date(2023,6,22), 'Found Date Should be Equal to June 22, 2023')

    def testFourthThu(self):
        dates = find_patch_dates(2023,6)
        self.assertEqual(dates['4th Thu'], date(2023,6,29), 'Found Date Should be Equal to June 29, 2023')
    
    def testThirdTue(self):
        dates = find_patch_dates(2023,6)
        self.assertEqual(dates['3rd Tue'], date(2023,6,20), 'Found Date Should be Equal to June 20, 2023')

    def testFourthTue(self):
        dates = find_patch_dates(2023,6)
        self.assertEqual(dates['4th Tue'], date(2023,6,27), 'Found Date Should be Equal to June 27, 2023')


if __name__ == '__main__':
    unittest.main()