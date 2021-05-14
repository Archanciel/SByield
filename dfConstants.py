'''
This file ontains multi langages constant tuples. The first element in
the tuple is the constant value for the english (default) langage. The
second is the french translation. Adding a langage is very simple: you
just add a supplementary element in the tuple.
'''
GB = 0
FR = 1
DEPOSIT_SHEET_HEADER_OWNER = ('OWNER', 'PROPR')
MERGED_SHEET_HEADER_EARNING_NEW_NAME = ('EARNING', 'REVENU')
DEPOSIT_YIELD_HEADER_DATE_FROM = ('FROM', 'DE')
DEPOSIT_YIELD_HEADER_DATE_TO = ('TO', 'A')
PROC_DEPWITHDR = ('DEP/WITHDR', 'DEPOTS/RETRAITS')
PROC_DEP = ('DEPOSITS   /', 'DEPÔTS  /')
PROC_WITHDR = ('  WITHDRAWALS', ' RETRAITS')
PROC_AMOUNT =  ('AMOUNT', 'MONTANT')
PROC_DATE_FROM_RATE = ('DEP RATE', 'VAL DAT DEP')
PROC_CURRENT_RATE = ('CUR RATE', 'VAL ACT')
PROC_CAPITAL_GAIN = ('CAP GAIN', 'PL-VAL CAP')
PROC_CAPITAL_GAIN_PERCENT = ('IN %', 'EN %')
PROC_YIELD = ('YIELD', 'INTÉRÊTS')
PROC_YIELD_SHORT = ('YLD ', 'INT ')
PROC_TOTAL = 'TOTAL '
PROC_YIELD_DAYS = ('DAYS', ' JOURS')
PROC_YIELD_AMT_PERCENT = ('Y %', 'INT %')
PROC_YEAR_YIELD_PERCENT = ('YR Y %', 'INT ANN %')
PROC_TOTAL_INCLUDE_YIELD = ('Tot incl yield', 'Tot incl intérêts')

PROC_TOTAL_INCLUDE_YIELD_HELP = ('total in those 2 columns includes the generated yield total', 'le total dans ces 2 colonnes inclut le total des intérêts générés')
PROC_CURRENT_RATE_HELP = ('deposit/withdrawal value at the date from rate', 'valeur des dépôts/retraits au taux en vigeur à la date du dépôt/retrait')
