# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 12:10:20 2021

@author: rober
"""

from enum import Enum
from typing import List, NamedTuple
import copy

class Cell(str, Enum):
    EMPTY = "."
    STONE = "X"
    UNUSED = " "


class BrettLocation(NamedTuple):
    row: int
    column: int
 
class Zug(NamedTuple):
    von:BrettLocation
    via:BrettLocation
    bis:BrettLocation
    
    def __repr__(self)->str:
        return("[({},{}),({},{}),({},{})]".format(self.von.row, self.von.column, \
                                                  self.via.row, self.via.column, \
                                                  self.bis.row, self.bis.column))
    
#Zug = Tuple[BrettLocation, BrettLocation, BrettLocation]
minSteine:int=99
anzLoesungen:int=0

class Brett:

    def __init__(self) -> None:
        # Grundlegende Instanzvariablen initialisieren
        self._rows: int = 9
        self._columns: int = 9
        self._xelegung=[[0,0,0,1,1,1,0,0,0],
                        [0,0,0,1,1,1,0,0,0],
                        [0,0,0,1,1,1,0,0,0],
                        [1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,2,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1],
                        [0,0,0,1,1,1,0,0,0],
                        [0,0,0,1,1,1,0,0,0],
                        [0,0,0,1,1,1,0,0,0],
                        ]
        self._belegung=[[0,0,0,2,2,2,0,0,0],
                        [0,0,0,2,2,2,0,0,0],
                        [0,0,0,1,1,2,0,0,0],
                        [2,2,2,1,1,1,2,2,2],
                        [2,2,2,1,2,1,1,2,2],
                        [2,2,2,1,1,1,2,2,2],
                        [0,0,0,1,1,1,0,0,0],
                        [0,0,0,2,2,2,0,0,0],
                        [0,0,0,2,2,2,0,0,0],
                        ]

        self._grid: List[List[Cell]] = [[Cell.UNUSED for c in range(self._columns)] for r in range(self._rows)]

        # Das Gitter mit leeren Zellen füllen
        for r in range(len(self._belegung)):
           for c in range(len(self._belegung[r])):
               if self._belegung[r][c] == 1:
                   self._grid[r][c]=Cell.STONE
               elif self._belegung[r][c] == 2:
                   self._grid[r][c]=Cell.EMPTY
               else:
                   self._grid[r][c]=Cell.UNUSED
        self._gueltigeZuege: List[Zug] = self.finde_gueltige_zuege()
        
    

    def finde_gueltige_zuege(self)->List[Zug]:
        l:List[Zug]=[]
        for r in range (self._rows):
            for c in range (self._columns):
                bl:BrettLocation=BrettLocation(r,c)
                # nach rechts suchen:
                if r+2<self._rows and self._grid[bl.row][bl.column] != Cell.UNUSED and \
                    self._grid[bl.row+1][bl.column] != Cell.UNUSED and \
                    self._grid[bl.row+2][bl.column] != Cell.UNUSED:
                    l.append(Zug(BrettLocation(bl.row,bl.column), BrettLocation(bl.row+1,bl.column), BrettLocation(bl.row+2,bl.column)))
                # nach links suchen:
                if r-2>=0 and self._grid[bl.row][bl.column] != Cell.UNUSED and \
                    self._grid[bl.row-1][bl.column] != Cell.UNUSED and \
                    self._grid[bl.row-2][bl.column] != Cell.UNUSED:
                    l.append(Zug(BrettLocation(bl.row,bl.column), BrettLocation(bl.row-1,bl.column), BrettLocation(bl.row-2,bl.column)))               # nach oben suchen:
                if c+2<self._columns and self._grid[bl.row][bl.column] != Cell.UNUSED and \
                    self._grid[bl.row][bl.column+1] != Cell.UNUSED and \
                    self._grid[bl.row][bl.column+2] != Cell.UNUSED:
                    l.append(Zug(BrettLocation(bl.row,bl.column), BrettLocation(bl.row,bl.column+1), BrettLocation(bl.row,bl.column+2)))
                # nach unten suchen:
                if c-2>=0 and self._grid[bl.row][bl.column]!=Cell.UNUSED and \
                    self._grid[bl.row][bl.column-1] != Cell.UNUSED and \
                    self._grid[bl.row][bl.column-2] != Cell.UNUSED:
                    l.append(Zug(BrettLocation(bl.row,bl.column), BrettLocation(bl.row,bl.column-1), BrettLocation(bl.row,bl.column-2)))
        return l

    def finde_moegliche_zuege(self)->List[Zug]:
        l:List[Zug]=[]
        for zug in self._gueltigeZuege:
            if self._grid[zug.von.row] [zug.von.column] == Cell.STONE and \
               self._grid[zug.via.row] [zug.via.column] == Cell.STONE and \
               self._grid[zug.bis.row] [zug.bis.column] == Cell.EMPTY:
                  l.append(zug)  
        return l         
    
        
    def zaehle_Steine(self)->int:
        zaehler:int=0
        for r in range (self._rows):
            for c in range (self._columns):
                if self._grid[r][c]==Cell.STONE:
                    zaehler+=1
        return zaehler
    
    def mach_zug(self,zug:Zug)->None:
        self._grid[zug.von.row] [zug.von.column] = Cell.EMPTY
        self._grid[zug.via.row] [zug.via.column] = Cell.EMPTY
        self._grid[zug.bis.row] [zug.bis.column] = Cell.STONE
        return
        
    # Eine schön formatierte Version des Labyrinths für die Ausgabe zurückgeben
    def __str__(self) -> str:
        output: str = ""
        for row in self._grid:
            output += "".join([c.value for c in row]) + "\n"
        return output

    # Einen Ziel-Erreichungstest brauchen wir zum Schluss auch:
    #def goal_test(self, ml: BrettLocation) -> bool:
    #    return ml == self.goal



def loese_Brett(b:Brett, zl:List[Zug])->List[Zug]:
    global minSteine
    global anzLoesungen
    #gz:List[Zug]=b.finde_moegliche_zuege()
    # Ohne den blöden deepcopy geht es nicht :(
    bb=copy.deepcopy(b)
    ll=copy.deepcopy(zl)
    for zug in b.finde_moegliche_zuege():
        nBrett:Brett = copy.deepcopy(bb)
        lz=copy.deepcopy(ll)
        nBrett.mach_zug(zug)
        #print(nBrett)
        #print ("Zugliste: ", gz)
        #benutzereingabe = input("Bitte Zahl eingeben ") 
        lz.append(zug) 
        if len(nBrett.finde_moegliche_zuege())==0:
            #print ("keine Züge mehr möglich ", str(nBrett.zaehle_Steine()))
            #print (nBrett)
            zz=nBrett.zaehle_Steine()
            if zz<minSteine:
                print ("min Steine:", str(zz))
                minSteine=zz
            if zz==1:
                print ("Super, nur noch 1 Stein übrig")
                print ("Zugliste: Länge: {}".format(len(lz)))
                print (lz)
                print (nBrett)
                print ("---------------------------------------------")
                anzLoesungen +=1
            return lz
        loese_Brett(nBrett, lz)





if __name__ == "__main__":
    m: Brett = Brett()
    mZugliste:List[Zug]=m.finde_gueltige_zuege()
    gZugliste:List[Zug]=m.finde_moegliche_zuege()
    print(m)
    #print ("Anzahl Steine:        {}".format(m.zaehle_Steine()))
    #print ("Anzahl mögliche Züge: {}".format(len(mZugliste)))
    #print ("mögliche Züge:", mZugliste)
    #print ("Anzahl gültige Züge:  {}".format(len(gZugliste)))
    benutzereingabe = input("Starte Lösungssuche mit Eingabe einer Zahl und Return: ") 
    rZugliste:List[Zug]=loese_Brett(m, [])
    print ("Gesamte Anzahl an Lösungen um auf einen Stein zu kommen:", str(anzLoesungen))
