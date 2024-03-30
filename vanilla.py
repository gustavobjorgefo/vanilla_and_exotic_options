# import pandas as pd
import numpy as np
from scipy.stats import norm


class VanillaOptions():
    
    def __init__(self, type, strike, spot, riskfree, borrow, vol, venc):
        self.type = type
        self.strike = strike
        self.spot = spot
        self.riskfree = riskfree
        self.borrow = borrow
        self.vol = vol
        self.venc = venc
        self.fwdrate = self.fwd_calc()
        self.d1 = self.d1_calc()
        self.d2 = self.d2_calc()

    def fwd_calc(self):
        return (1+self.riskfree)/(1+self.borrow)-1
    
    def d1_calc(self):
        d1 = (np.log(self.spot/self.strike) + (self.fwdrate + self.vol*self.vol/2)*(self.venc/252)) / (self.vol * (self.venc/252)**(1/2))
        return d1

    def d2_calc(self):
        d2 = self.d1 - self.vol * (self.venc/252)**(1/2)
        return d2


    def black_scholes(self):        
        if self.type == 'call':
            price = self.spot * norm.cdf(self.d1) - self.strike * np.exp(-self.fwdrate*(self.venc/252)) * norm.cdf(self.d2)
        elif self.type == 'put':
            price = self.strike * np.exp(-self.fwdrate*(self.venc/252)) * norm.cdf(-self.d2) - self.spot * norm.cdf(-self.d1)
        return price
    

    def bs_delta(self):
        if self.type == 'call':
            delta = norm.cdf(self.d1)
        elif self.type == 'put':
            delta = -norm.cdf(-self.d1)
        return delta
    

    def bs_gamma(self):
        gamma = norm.cdf(self.d1)/(self.spot*self.vol*(self.venc/252)**(1/2))
        return gamma

    def bs_vega(self):
        pass

if __name__ == '__main__':
    call = VanillaOptions('call', strike=100, spot=100, riskfree=0.1065, borrow=0.0010, vol=0.30, venc=21)
    call_price = call.black_scholes()
    call_delta = call.bs_delta()
    call_gamma = call.bs_gamma()

    put = VanillaOptions('put', strike=100, spot=100, riskfree=0.1065, borrow=0.0010, vol=0.30, venc=21)
    put_price = put.black_scholes()
    put_delta = put.bs_delta()
    put_gamma = put.bs_gamma()

    print("Call price: {},\
          Delta: {},\
          Gamma: {}".format(call_price, call_delta, call_gamma))
    print("Put price: {},\
          Delta: {},\
          Gamma: {}".format(put_price, put_delta, put_gamma))
    print(call_delta-put_delta)