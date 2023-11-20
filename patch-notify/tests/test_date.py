import unittest, calendar
from datetime import date
from src.utils.date import find_patch_dates

class TestNovemberSchedule(unittest.TestCase):
    def testSecondThu(self):
        dates = find_patch_dates(2023,11)
        self.assertEqual(dates['2nd Thu'], date(2023,11,16), 'Found Date Should be Equal to November 16, 2023')
    
    def testThirdThu(self):
        dates = find_patch_dates(2023,11)
        self.assertEqual(dates['3rd Thu'], date(2023,11,23), 'Found Date Should be Equal to November 16, 2023')

    def testFourthThu(self):
        dates = find_patch_dates(2023,11)
        self.assertEqual(dates['4th Thu'], date(2023,11,30), 'Found Date Should be Equal to November 16, 2023')
    
    def testThirdTue(self):
        dates = find_patch_dates(2023,11)
        self.assertEqual(dates['3rd Tue'], date(2023,11,21), 'Found Date Should be Equal to November 16, 2023')

    def testFourthTue(self):
        dates = find_patch_dates(2023,11)
        self.assertEqual(dates['4th Tue'], date(2023,11,28), 'Found Date Should be Equal to November 16, 2023')


if __name__ == '__main__':
    unittest.main()