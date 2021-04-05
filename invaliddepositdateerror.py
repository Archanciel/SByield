from sbyieldexception import SBYieldException


class InvalidDepositDateError(SBYieldException):
    """
    Exception raised when the deposit CSV file contains a deposit whose date is after the
    last yield payment date.
    """
    def __init__(self,
                 depositCsvFilePathName,
                 owner,
                 depositDate,
                 depositAmount,
                 yieldPaymentDate,
                 isTooLate=True):
        if isTooLate:
            errorMsg = "CSV file {} contains a deposit of {} for owner {} with a deposit \
date {} after the last payment date {}".format(depositCsvFilePathName,
                                                   depositAmount,
                                                   owner,
                                                   depositDate,
                                                   yieldPaymentDate)
        else:
            # in fact never happens !
            errorMsg = "CSV file {} contains a deposit of {} for owner {} with a deposit \
date {} before the first payment date {}".format(depositCsvFilePathName,
                                                 depositAmount,
                                                 owner,
                                                 depositDate,
                                                 yieldPaymentDate)

        super(InvalidDepositDateError, self).__init__(msg=errorMsg)
