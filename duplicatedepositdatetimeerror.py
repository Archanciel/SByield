from sbyieldexception import SBYieldException


class DuplicateDepositDateTimeError(SBYieldException):
    """
    Exception raised when the deposit CSV file contains a deposit whose date is the same
    as the date of another deposit..
    """
    def __init__(self,
                 depositCsvFilePathName,
                 owner,
                 depositDate,
                 depositAmount):
        errorMsg = 'CSV file {} contains a deposit of {} for owner {} with a deposit ' + \
                   'date {} which is identical to another deposit date. Change the date by ' + \
                   'increasing the time second by 1 and retry.'
        errorMsg = errorMsg.format(depositCsvFilePathName,
                                                   depositAmount,
                                                   owner,
                                                   depositDate)

        super(DuplicateDepositDateTimeError, self).__init__(msg=errorMsg)
