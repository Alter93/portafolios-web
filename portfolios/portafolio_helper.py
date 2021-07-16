import ast

import pandas


class PortafolioHelper:
    def __init__(self, filename = None, date = None, time = None):
        path = "../portfolio-opt/"
        self.portafolio = path + filename
        self.metadata = path + "data/" + date + "/metadata.csv"
        self.prices = path + "data/" + date + "/close_prices.csv"
        self.market = path + "data/" + date + "/market_daily.csv"
        self.time = int(time[0])

    def crear_listas(self):
        days = self.time * 248
        market = pandas.read_csv(self.market, index_col = 'Date')
        market = market.iloc[-days:]
        market = market.cumsum().rolling(7).mean()
        market = market.iloc[6:]
        market["0"] = market["0"] * 100
        y = list(market["0"])
        x = list(market.index)
        market_data = [x,y]

        prices = pandas.read_csv(self.prices, index_col = 'Date')
        prices = prices.iloc[-days:]
        prices = prices.pct_change(fill_method='ffill')
        prices = prices.cumsum().rolling(7).mean()
        simbolos = self.cargar_simbolos()

        simbolos_lista = []
        for simbolo in simbolos[:-1]:
            sim = simbolo["symbol"]
            simbolos_lista.append(sim)
            prices[sim] = (prices[sim] *
                               simbolo["percentage"])

        prices = prices[simbolos_lista]
        prices["pct_change"] = prices.sum(axis=1)
        x_p = list(prices.index)
        y_p = list(prices["pct_change"])
        port_data = [x_p, y_p]
        return market_data, port_data

    def cargar_simbolos(self):
        file = open(self.portafolio, "r")
        contents = file.read()
        dictionary = ast.literal_eval(contents)
        file.close()
        return dictionary
