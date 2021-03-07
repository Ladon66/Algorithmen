#
#
#            Sandheap
#
# 

from typing import List, Tuple
import pygame
from pygame.locals import *
import matplotlib.pyplot as plt
fig, ax = plt.subplots()

pygame.init()
Color0= (255, 255, 255 )
Color1= (189, 174, 198 )
Color2= (156, 138, 165 )
Color3= (115, 44, 123 )
Color4= ( 66, 28, 82 )
farben=[Color0,Color1,Color2,Color3,Color4, (255,0,0)]

DISPLAY=pygame.display.set_mode((603,603),0,32)
DISPLAY.fill(Color0)

class Ground:
    def __init__(self,n=11):
       self._grid:List[List[n]]=[[0 for c in range (n)] for r in range (n)]    
       self.mitte:int = n // 2
       self._worklist=[]
       self.n=n
    
    def drop(self,r,c):
        self._grid[r][c] +=1
        if self._grid[r][c] == 5:
            t:Tuple=(r,c)
            self._worklist.append(t)
    
    def resetwl(self)->None:
        self._worklist=[]

    def lawine(self, t:Tuple):
        (row, column)=t
        self._grid[row][column]-=4
        self._grid[row-1][column]+=1
        if self._grid[row-1][column]==5:
            t:Tuple=(row-1,column)
            self._worklist.append(t)
        self._grid[row+1][column]+=1
        if self._grid[row+1][column]==5:
            t:Tuple=(row+1,column)
            self._worklist.append(t)
        self._grid[row][column-1]+=1
        if self._grid[row][column-1]==5:
            t:Tuple=(row,column-1)
            self._worklist.append(t)
        self._grid[row][column+1]+=1
        if self._grid[row][column+1]==5:
            t:Tuple=(row,column+1)
            self._worklist.append(t)

    def count(self)->int:
        i:int=0
        for c in range (self.n):
            for r in range (self.n):
               i=i+self._grid[r][c]
        return (i)  

    def male(self)->None:
        for c in range (self.n):
            for r in range (self.n):
                pygame.draw.rect(DISPLAY,farben[self._grid[r][c]],(r*3,c*3,3,3))

    def __repr__(self) -> str:
        s=''
        i:int=0
        for c in range (self.n):
            for r in range (self.n):
               s += str(self._grid[r][c])
               i=i+self._grid[r][c]
            s +='\n'        
        return s+'_'+str(i)   

s1:Ground=Ground(200)
count=70000
while count>0:
    count -=1
    s1.drop(s1.mitte, s1.mitte)
    for t in s1._worklist:
        s1.lawine(t)
    s1.resetwl()
print (s1.count())

s1.male()

pygame.display.flip()
pygame.event.clear()
while True:
    event = pygame.event.wait()
    if event.type == QUIT:
        pygame.quit()
    elif event.type == KEYDOWN:
        if event.key == K_f:
            pygame.quit()
