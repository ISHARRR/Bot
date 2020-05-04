
import oandapyV20
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.definitions.accounts as defaccounts

print (defaccounts.GuaranteedStopLossOrderMode, '\n')

client = oandapyV20.API(access_token="ace07448fdbcddf1d24c76db4f654abd-0673bb236877d296d74b63fef2d9be08")
accountID = "101-004-14591208-001"
r = accounts.AccountDetails(accountID)
client.request(r)
print (r.response)
