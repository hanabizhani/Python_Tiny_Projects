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

from Counter import Counter

counter = Counter(3,1)

#Calling getter method for caounter value
print(counter.val)
print("-"*30)

#Calling setter method and then getter method for counter value
counter.val = 5
print("Counter value is: ", counter.val)
print("-"*30)

#Increment value
counter.increment()
print("-"*30)

#Calling getter method for increment value
print(counter.incr)
print("-"*30)

#Calling setter method and then getter method for increment value
counter.incr = 10
print("Increment value is:", counter.incr)
print("-"*30)

#Increment value
counter.increment()
print("-"*30)

#Call __rep__ magic method
print(counter)
print("-"*30)


#Increas counter value with another value
counter.increase(12)
print("-"*30)

#Call __add__ and __radd__ magic method
otherCounter = Counter(5, 1)
counter.val = counter + otherCounter
print(counter)
counter.val = otherCounter + counter
print(counter)

counter.val = counter + 10
print(counter)
counter.val = 10 + counter
print(counter)
print("-"*30)

#Call __eq__ magic method
print("Equality of otherCounter and counter: ", counter == otherCounter)
otherCounter.val = counter.val
print("-"*5)
print("Equality of otherCounter and counter after otherCounter.val = counter.val: ", counter == otherCounter)

print("-"*5)
print("Equality of counter value with 10: ", counter == 10) 

counter.val = 10
print("-"*5)
print("Equality of counter value with 10 after set counter value to 10: ", counter == 10) 
print("-"*30)

print("counter class: \n", counter)
print("-"*5)
print("otherCounter class: \n", otherCounter)
print("-"*5)

#Call __ne__ magic method
print("Equality of otherCounter and counter: ", counter != otherCounter)

#Call __lt__ and __gt__ magic method
print("Is counter < otherCounter: ", counter < otherCounter) 
print("Is counter > otherCounter: ", counter > otherCounter) 

counter = otherCounter
print(counter)
print(otherCounter)
#Call __le__ and __ge__ magic method
print("Is counter <= otherCounter: ", counter <= otherCounter) 
print("Is counter >= otherCounter: ", counter >= otherCounter) 
print("-"*30)

#Call resetCounter method
print(counter.resetCounter())
print(counter.resetCounter(10, 2))

#Calling help method
#print(help(counter))

