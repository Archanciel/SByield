import json
import sys
import ssl
import urllib.request
from urllib.error import HTTPError, URLError

from bs4 import BeautifulSoup

from datetimeutil import DateTimeUtil
from resultdata import ResultData

MINUTE_PRICE_DAY_NUMBER_LIMIT = 7   # if the request date is older than current time - this value,
                                    # the price returned is a day close price, not a minute price !

IDX_DATA_ENTRY_TO = 1

class PriceRequester:
    """
    """
    def __init__(self):
        try:
            #since ssl prevents requesting the data from CryptoCompare
            #when run from Kivy GUI, it must be disabled
            self.ctx = ssl.create_default_context()
            self.ctx.check_hostname = False
            self.ctx.verify_mode = ssl.CERT_NONE
        except AttributeError:
            #occurs when run in QPython under Python 3.2
            self.ctx = None

    def getCurrentPrice(self, crypto, unit, exchange):
        url = "https://min-api.cryptocompare.com/data/price?fsym={}&tsyms={}&e={}".format(crypto, unit, exchange)
        resultData = ResultData()

        resultData.setValue(ResultData.RESULT_KEY_CRYPTO, crypto)
        resultData.setValue(ResultData.RESULT_KEY_UNIT, unit)
        resultData.setValue(ResultData.RESULT_KEY_EXCHANGE, exchange)
        resultData.setValue(ResultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_RT)

        try:
            if self.ctx == None:
                #here, run in QPython under Python 3.2
                webURL = urllib.request.urlopen(url)
            else:
                webURL = urllib.request.urlopen(url, context=self.ctx)
        except HTTPError as e:
            resultData.setError('ERROR - could not complete request ' + url + '. Reason: ' + str(e.reason) + '.')
        except URLError as e:
            resultData.setError('ERROR - No internet. Please connect and retry !')
        except: 
            the_type, the_value, the_traceback = sys.exc_info()
            resultData.setError('ERROR - could not complete request ' + url + '. Reason: ' + str(the_type) + '.')
        else:
            page = webURL.read()
            soup = BeautifulSoup(page, 'html.parser')
            dic = json.loads(soup.prettify())
            
            if unit in dic:
                resultData.setValue(ResultData.RESULT_KEY_PRICE_TIME_STAMP, DateTimeUtil.utcNowTimeStamp())
                resultData.setValue(ResultData.RESULT_KEY_PRICE, dic[unit]) #current price is indexed by unit symbol in returned dic
            else:
                resultData = self._handleProviderError(dic, resultData, url, crypto, unit, exchange, isRealTime=True)

        return resultData

    def _handleProviderError(self, dic, resultData, url, crypto, unit, exchange, isRealTime):
        if 'Message' in dic.keys():
            errorMessage = dic['Message']
            errorMessage = errorMessage.replace('-', '/') # useful for msg containing a coin pair
            
            if not isRealTime:
                errorMessage = self._uniformiseErrorMessage(errorMessage, crypto, unit, exchange)
            else:
                errorMessage = errorMessage.rstrip(' .')
                errorMessage = errorMessage.replace('fsym', 'Symbol')

            resultData.setError('PROVIDER ERROR - ' + errorMessage + '.')
        else:
            resultData.setError('PROVIDER ERROR - ' + 'Request ' + url + ' did not return any data.')

        return resultData


    def _uniformiseErrorMessage(self, errorMessage, crypto, unit, exchange):
        '''
        this method transform the provider error msg returned by the historical price queries
        (histo minute and histo day so they look identical to the error msg returned for the same
        cause by the RT price request.

        Histo error msg: e param is not valid the market does not exist for this coin pair
        RT error msg ex: Binance market does not exist for this coin pair (BTC-ETH)

        :param errorMessage:
        :param crypto:
        :param unit:
        :param exchange:
        :return: transformed errorMessage
        '''

        return errorMessage.replace('e param is not valid the', exchange) + ' ({}/{})'.format(crypto, unit)

if __name__ == '__main__':
    pr = PriceRequester()

