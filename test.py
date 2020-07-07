
from oandapyV20 import API
import oandapyV20.endpoints.trades as trades
import json

api = API(access_token="e84d432149ffdfa8ced7d52b864d7983-154be793312cd00759bef280e66b57c0", environment="live")
accountID = "001-004-4069941-004"

r = trades.TradesList(accountID)
# show the endpoint as it is constructed for this call
print("REQUEST:{}".format(r))
rv = api.request(r)
print("RESPONSE:\n{}".format(json.dumps(rv, indent=2)))
