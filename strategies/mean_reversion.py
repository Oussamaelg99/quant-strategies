from AlgorithmImports import *

class MeanReversion(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2020, 1, 1)
        self.SetEndDate(2023, 1, 1)
        self.SetCash(100000)
        
        self.symbol = self.AddEquity("AAPL", Resolution.Daily).Symbol
        self.lookback = 20
        self.price_window = RollingWindow[float](self.lookback)

    def OnData(self, data):
        if not data.Bars.ContainsKey(self.symbol):
            return
        
        price = data.Bars[self.symbol].Close
        self.price_window.Add(price)
        
        if self.price_window.IsReady:
            mean = sum(self.price_window) / self.lookback
            if price < mean * 0.98:
                self.SetHoldings(self.symbol, 1)  # Buy
            elif price > mean * 1.02:
                self.SetHoldings(self.symbol, -1) # Sell
