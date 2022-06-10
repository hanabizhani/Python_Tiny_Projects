"""
#################################################################################
|                                                                               |
|                                .::::::::::.                                   |
|                              .::``::::::::::.                                 |
|                              :::..:::::::::::                                 |
|                              ````````::::::::                                 |
|                      .::::::::::::::::::::::: iiiiiii,                        |
|                   .:::::::::::::::::::::::::: iiiiiiiii.                      |
|                   ::::::::::::::::::::::::::: iiiiiiiiii                      |
|                   ::::::::::::::::::::::::::: iiiiiiiiii                      |
|                   :::::::::: ,,,,,,,,,,,,,,,,,iiiiiiiiii                      |
|                   :::::::::: iiiiiiiiiiiiiiiiiiiiiiiiiii                      |
|                   `::::::::: iiiiiiiiiiiiiiiiiiiiiiiiii`                      |
|                      `:::::: iiiiiiiiiiiiiiiiiiiiiii`                         |
|                              iiiiiiii,,,,,,,,                                 |
|                              iiiiiiiiiii''iii                                 |
|                              `iiiiiiiiii..ii`                                 |
|                                `iiiiiiiiii`                                   |
|                                                                               |
|                      ____        _   _                                        |
|                     |  _ \ _   _| |_| |__   ___  _ __                         |
|                     | |_) | | | | __| '_ \ / _ \| '_ \                        |
|                     |  __/| |_| | |_| | | | (_) | | | |                       |
|                     |_|    \__, |\__|_| |_|\___/|_| |_|                       |
|                            |___/                                              |
|                                                                               |
#################################################################################
Author: Hana Bizhani
Date: 06/10/2022
"""
class Counter:
    def __init__(self, v: int=0, i: int=1) -> None:
        self._val = v
        self._incr = i
        
    def _set_val(self, value):
        print("Set Counter Value with ", value)
        self._val = value
        
    def __add__(self, otherCounter):
        print("Magic method __add__ is called")
        if isinstance(otherCounter, Counter):
            return self.increase_counter(otherCounter)
        else:
            return self.increase(otherCounter)
        
    
    def __radd__(self, otherCounter):
        print("Magic method __radd__ is called")
        return self.__add__(otherCounter)
        
    def _get_val(self):
        print("Get Counter Value")
        return self._val
    
    def __repr__(self) -> str:
        print("Magic method __rep__ is called")
        return str(self._val)
    
    def _set_incr(self, i):
        print("Set increment Value with ", i)
        self._incr = i
     
    def _get_incr(self) -> int:
        print("Get increment value")
        return self._incr
        
    def change_incr_value(self, i) -> None:
        self._incr = i    
    
    def increase(self, num) -> None:
        print("counter value before increse is : ", self._val)
        self._val += num
        print("Value increased by %d successfully" %num)
        print("counter value after increase is : ", self._val)
        return self._val
        
    def increase_counter(self, otherCounter) -> int:
        print("Counter value increased with other class counter value")
        return self._val + otherCounter._val
    
    def increment(self) -> None:
        print("counter value before increment is : ", self._val)
        self._val += self._incr
        print("Value incremented with %d successfully" %self._incr)
        print("counter value after increment is : ", self._val)
        
    def __eq__(self, otherCounter) -> bool:
        print("Magic method __eq__ is called")
        if isinstance(otherCounter, Counter):
            return self._val == otherCounter._val
        else:
            return self._val == otherCounter
        
    def __ne__(self, otherCounter) -> bool:
        print("Magic method __ne__ is called")
        return not self.__eq__(otherCounter)
    
    def __lt__(self, otherCounter) -> bool:
        print("Magic method __lt__ is called")
        if isinstance(otherCounter, Counter):
            return self._val < otherCounter._val
        else:
            return self._val < otherCounter
        
    def __gt__(self, otherCounter) -> bool:
        print("Magic method __gt__ is called")
        return not (self.__lt__(otherCounter) and self.__eq__(otherCounter))
    
    def __ge__(self, otherCounter) -> bool:
        print("Magic method __ge__ is called")
        return (self.__gt__(otherCounter) or self.__eq__(otherCounter))
    
    def __le__(self, otherCounter) -> bool:
        print("Magic method __le__ is called")
        return (self.__lt__(otherCounter) or self.__eq__(otherCounter))
            
        
    val = property(
        fget=_get_val,
        fset=_set_val,
        doc="This is counter value property"
    )
    
    incr = property(
        fget=_get_incr,
        fset=_set_incr,
        doc="This is a increment value property"
    )
    