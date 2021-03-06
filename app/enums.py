from enum import Enum

class Unit(str, Enum):

    HOUR = 'hour'
    DAY = 'day'


class TAX(Enum):

    SALES = 21.0 # %
    INCOME_BOX1 = 19.17 # % income tax 
    INCOME_BOX2 = 37.07 # % income tax
    INCOME_BOX3 = 49.50 # % income tax
    INCOME_DEFAULT_BOX = 60.00 # % default percentage