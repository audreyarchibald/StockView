from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
from threading import Thread
import time

class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

class TradingApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print("OrderStatus - Id:", orderId, "Status:", status, "Filled:", filled, "Remaining:", remaining, "LastFillPrice:", lastFillPrice)

    def openOrder(self, orderId, contract, order, orderState):
        print("OpenOrder - Id:", orderId, "Symbol:", contract.symbol, "SecType:", contract.secType, "Exchange:", contract.exchange, "OrderType:", order.orderType, "OrderState:", orderState.status)

    def execDetails(self, reqId, contract, execution):
        print("ExecDetails: ", reqId, contract.symbol, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)

def run_loop():
    app.run()

app = IBapi()
app.connect('127.0.0.1', 7496, 123)
api_thread = Thread(target=run_loop, daemon=True)
api_thread.start()
time.sleep(1)  # Sleep interval to allow time for connection to server
