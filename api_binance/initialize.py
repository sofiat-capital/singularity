
from MasterAPI import MasterAPI

api = MasterAPI()

api.DataBaseAPI.CreateCategory('cryptocoin')

############################################################
api.DataBaseAPI.CreateProduct(productName = 'BTCUSDT',
                              categoryName = 'cryptocoin')

api.DataBaseAPI.CreateProduct(productName = 'ETHUSDT',
                              categoryName = 'cryptocoin')
############################################################

ETH = api.BinanceAPI.CandleStick(symbol = 'ETHUSDT', interval='1d', limit=1000)
BTC = api.BinanceAPI.CandleStick(symbol = 'BTCUSDT', interval='1d', limit=1000)

api.DataBaseAPI.InsertDayCandle(ETH)
api.DataBaseAPI.InsertDayCandle(BTC)
