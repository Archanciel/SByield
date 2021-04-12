from sbyieldexception import SBYieldException


class UnsupportedCryptoFiatPairError(SBYieldException):
	"""
	Exception raised when the crypto/fiat pair is not supported in the
	crypto fiat exchange CSV file.
	"""

	def __init__(self,
                 crypto,
                 fiat,
                 cryptoFiatExchangeCsvFilePathName):
		errorMsg = '{}/{} pair not supported. Add adequate information to {} and retry.'.format(crypto, fiat, cryptoFiatExchangeCsvFilePathName)

		super(UnsupportedCryptoFiatPairError, self).__init__(msg=errorMsg)
