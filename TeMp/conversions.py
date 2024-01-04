import numpy as np

def m_km(values, flag):
    """
    Flag of 0: m->km
    Flag of 1: km->m
    """
    if flag == 0:
        return np.array(values)*1000
    elif flag == 1:
        return np.array(values)/1000
    else: 
        print("enter a valid flag")

def gu_mgal(values, flag):
    """
    Flag of 0: gu->mgal
    Flag of 1: mgal->gu
    """
    if flag == 0:
        return np.array(values)/10
    elif flag == 1:
        return np.array(values)*10
    else: 
        print("enter a valid flag")

