from sbyieldexception import SBYieldException


class TooLateDepositDateError(SBYieldException):
    """
    Exception raised when the deposit CSV file contains a deposit whose date is after the
    last yield payment date. Handkling this case in the SBDepositYieldComputer class
    would unusefully complexify its code.
    """
    def __init__(self, depositCsvFilePathName, owner, depositDate, depositAmount, lastYieldPaymentDate):
        errorMsg = "CSV file {} contains a deposit of {} for owner {} with a deposit \
date {} after the last payment date {}".format(depositCsvFilePathName,
                                               depositAmount,
                                               owner,
                                               depositDate,
                                               lastYieldPaymentDate)
        super(TooLateDepositDateError, self).__init__(msg=errorMsg)
