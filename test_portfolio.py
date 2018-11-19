import unittest
import pandas as pd
from portfolio import CalculatePefromance

class TestStringMethods(unittest.TestCase):

	def test_asset(self):
		cur = pd.Series(data= [1.000000, 1.007755295269852, 1.015939909620219],index=['2014-01-13','2014-01-14','2014-01-15'])
		a = CalculatePefromance()
		s=a.calculate_asset_performance('2014-01-13','2014-01-15')
		self.assertEqual(cur.tolist(), s.tolist()) 	

	def test_currency(self):
		cur = pd.Series(data= [1.000000, 0.9995677462752235, 0.9972344424222758],index=['2014-01-13','2014-01-14','2014-01-15'])
		a = CalculatePefromance()
		s=a.calculate_currency_performance('2014-01-13','2014-01-15')
		self.assertEqual(cur.tolist(), s.tolist())
	
	def test_total(self):
		cur = pd.Series(data= [1.000000, 1.0269211604721888, 1.0328451530521658],index=['2014-01-13','2014-01-14','2014-01-15'])
		a = CalculatePefromance()
		s=a.calculate_total_performance('2014-01-13','2014-01-15')
		self.assertEqual(cur.tolist(), s.tolist())		