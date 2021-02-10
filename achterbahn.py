# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 12:34:18 2021

@author: rober
"""
from typing import Generator

def achterbahn1(n: int) -> int:
    turn=0
    max=0
    while n!=1:
      if n%2==1:
        n=3*n+1
      else:
        n=n/2
      turn +=1  
      if max<n:
          max=n
      #print("turn:"+str(turn)+" n: "+str(n)+" max: "+str(max))
    return turn

def achterbahn2()->Generator[int, None, None]:
    yield 87
    yield 33
    yield 22
    
def infinite_sequence():
    #num = 0
    yield 2
    yield 2
    yield 2
    #while num<10:
    #    yield num
    #    num += 1


if __name__ == "__main__":
    print (achterbahn1(129))

    