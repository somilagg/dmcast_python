import unittest
from dmcast2 import dmcast2 as DMC
from dmcast2 import date as d 

class TestClass(unittest.TestCase):

	def test_isleap(self):
		dmc2 = DMC()
		self.assertEqual(dmc2.isleap(2000), 1)
		self.assertEqual(dmc2.isleap(1900), 0)
		self.assertEqual(dmc2.isleap(1996), 1)
		self.assertEqual(dmc2.isleap(1997), 0)

	def test_gre2jul(self):
		dmc2 = DMC()
		dt = d()
		dt.da_year = 1997
		dt.da_mon = 3
		self.assertEqual(dmc2.gre2jul(dt), 368)

		dt.da_year = 2000
		dt.da_mon = 11
		self.assertEqual(dmc2.gre2jul(dt), 377)

	def test_jul2gre(self):
		dmc2 = DMC()
		dt = d()
		dt.da_year = 1997
		jd = 0
		dt2 = dmc2.jul2gre(jd, dt)
		self.assertEqual(dt2.da_day, 0)
		self.assertEqual(dt2.da_mon, 1)

		jd = 32
		dt2 = dmc2.jul2gre(jd, dt)
		self.assertEqual(dt2.da_day, 1)
		self.assertEqual(dt2.da_mon, 2)

		jd = 62
		dt2 = dmc2.jul2gre(jd, dt)
		self.assertEqual(dt2.da_day, 3)
		self.assertEqual(dt2.da_mon, 3)

		dt.da_year = 2000
		jd = 62
		dt2 = dmc2.jul2gre(jd, dt)
		self.assertEqual(dt2.da_day, 2)
		self.assertEqual(dt2.da_mon, 3)

if __name__ == '__main__':
	unittest.main()