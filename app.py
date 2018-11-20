from sources.world_trading_data.WorldTradingData import WorldTradingData

source = WorldTradingData()
source.update_data()

print(source.get_data())
