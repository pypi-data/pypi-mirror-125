from decimal import Decimal

def decimal_default_proc(obj):
    """convert decimal value in dictionary to json format(called by json.dumps())

    :param obj: json object
    :type obj: object
    :raises TypeError: if cannot convert, raise type error
    :return: float(obj)
    :rtype: float
    """    
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError