import pandas as pd

class CalculatePefromance:
	"""Class fot calculating perfomances"""
	def __init__(self, path_to_currency='currencies.csv', path_to_prices='prices.csv', 
				 path_to_weight='weights.csv', path_to_exchanges='exchanges.csv'):
		self.path_to_currency = path_to_currency
		self.path_to_prices = path_to_prices
		self.path_to_weight = path_to_weight
		self.path_to_exchanges = path_to_exchanges
	

	def calculate_asset_performance(self, start_date, end_date) -> pd.Series:
		"""calculate asset perfomance
			:param start_date: start date
			:param end_date: end date
			:returns asset_perfomance: asset perfomance
		"""
		prices_df = pd.read_csv(self.path_to_prices, header=0, sep=',')
		weight_df = pd.read_csv(self.path_to_weight, header=0, sep=',') 

		prices_df = prices_df.set_index(pd.DatetimeIndex(prices_df.date))
		prices_df = prices_df.drop('date', axis=1)
		prices_df = prices_df.resample('D').ffill()
		prices_df = prices_df.fillna(method='ffill')
		
		assets = pd.DataFrame()
		asset_performance = pd.Series()

		weight_df = weight_df.rename(columns={'Unnamed: 0':'date'})
		weight_df = weight_df.set_index(pd.DatetimeIndex(weight_df.date))
		weight_df = weight_df.drop('date', axis=1)
		weight_df = weight_df.resample('D').ffill()
		weight_df = weight_df.fillna(method='ffill')

		cols = weight_df.columns.tolist()
		a, b = cols.index('US0527691069 US'), cols.index('DE0007164600 GR')
		cols[b], cols[a] = cols[a], cols[b]
		weight_df = weight_df[cols]
		
		delta = prices_df.diff()
		assets = delta.div(prices_df.shift())
		asset_sum = assets.multiply(weight_df).sum(axis=1)

		asset_performance = asset_performance.reindex(asset_sum.index)
		asset_performance.iloc[0] = 1.
		for i in range(1,asset_sum.size):
		    asset_performance[i] = asset_performance.iloc[i-1] * (1. + asset_sum.iloc[i])    		    

		return asset_performance[start_date:end_date]

	def calculate_currency_performance(self, start_date, end_date) -> pd.Series:
		"""calculate currency performance
			:param start_date: start date
			:param end_date: end date
			:returns cur_perf: currency performance
		"""
		ex_df = pd.read_csv(self.path_to_exchanges, header=0, sep=',')
		weight_df = pd.read_csv(self.path_to_weight, header=0, sep=',') 
		currency_df = pd.read_csv(self.path_to_currency, header=0, sep=',') 
		
		cur_perf = pd.Series()

		ex_df = ex_df.rename(columns={'Unnamed: 0':'date'})
		ex_df = ex_df.set_index(pd.DatetimeIndex(ex_df.date))
		ex_df = ex_df.drop('date', axis=1)
		ex_df = ex_df.resample('D').ffill()
		ex_df = ex_df.fillna(method='ffill')

		weight_df = weight_df.rename(columns={'Unnamed: 0':'date'})
		weight_df = weight_df.set_index(pd.DatetimeIndex(weight_df.date))
		weight_df = weight_df.drop('date', axis=1)
		weight_df = weight_df.resample('D').ffill()
		weight_df = weight_df.fillna(method='ffill')
		
		currency_df = currency_df.rename(columns={'Unnamed: 0':'assert'})
		currency_df = currency_df.set_index(['assert'])

		delta = ex_df.diff()
		cur = delta.div(ex_df.shift())

		currency_dict = currency_df.to_dict()['currency']
		weight_df = weight_df.rename(columns=currency_dict)
		weight_df = weight_df.groupby(weight_df.columns, axis=1).sum()
		weight_df = weight_df.drop('USD', axis=1)

		cf = cur.multiply(weight_df).sum(axis=1)

		cur_perf = cur_perf.reindex(cf.index)
		cur_perf.iloc[0] = 1.
		for i in range(1,cf.size):
		    cur_perf[i] = cur_perf.iloc[i-1] * (1. + cf.iloc[i])    

		return cur_perf[start_date:end_date]    


	def calculate_total_performance(self, start_date, end_date) -> pd.Series:
		"""calculate total portfolio performance
			:param start_date: start date
			:param end_date: end date
			:returns total_portf: total portfolio perfomance
		"""
		ex_df = pd.read_csv(self.path_to_exchanges, header=0, sep=',')
		price_df = pd.read_csv(self.path_to_prices, header=0, sep=',')
		weight_df = pd.read_csv(self.path_to_weight, header=0, sep=',') 
		
		ex_df = ex_df.rename(columns={'Unnamed: 0':'date'})
		ex_df = ex_df.set_index(pd.DatetimeIndex(ex_df.date))
		ex_df = ex_df.drop('date', axis=1)
		ex_df = ex_df.resample('D').ffill()
		ex_df = ex_df.fillna(method='ffill')

		price_df = price_df.set_index(pd.DatetimeIndex(price_df.date))
		price_df = price_df.drop('date', axis=1)
		price_df = price_df.resample('D').ffill()
		price_df = price_df.fillna(method='ffill')

		weight_df = weight_df.rename(columns={'Unnamed: 0':'date'})
		weight_df = weight_df.set_index(pd.DatetimeIndex(weight_df.date))
		weight_df = weight_df.drop('date', axis=1)
		weight_df = weight_df.resample('D').ffill()
		weight_df = weight_df.fillna(method='ffill')
		
		cols = weight_df.columns.tolist()
		a, b = cols.index('US0527691069 US'), cols.index('DE0007164600 GR')
		cols[b], cols[a] = cols[a], cols[b]
		weight_df = weight_df[cols]

		tmp = price_df.drop(['US0527691069 US','US6092071058 US'], axis=1)
		tmp['AT0000A18XM4 SW'] = tmp['AT0000A18XM4 SW'].multiply(ex_df['CHF'])
		tmp['BE0974268972 BB'] = tmp['BE0974268972 BB'].multiply(ex_df['EUR'])
		tmp['DE0007164600 GR'] = tmp['DE0007164600 GR'].multiply(ex_df['EUR'])
		price_df.update(tmp)
		
		tot_diff = price_df.diff()
		total = tot_diff.div(price_df.shift())
		total_sum = total.multiply(weight_df).sum(axis=1)
		total_portf = pd.Series()
		total_portf = total_portf.reindex(total_sum.index)
		total_portf.iloc[0] = 1.
		for i in range(1,total_sum.size):
		    total_portf[i] = total_portf.iloc[i-1] * (1. + total_sum.iloc[i])    
		
		return total_portf[start_date:end_date]
		