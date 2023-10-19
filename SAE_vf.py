#!/usr/bin/python3
from www import *
import random
import time
B="fond"
# Groupe 17 : CUISSET Mattéo; Abdelkader DAi, Yanis ...
# TYPESEND définis le type de d'intéraction des joueurs pour jouer un coup.
# TYPESEND = 'form' => utilisation d'un formulaire (Q4)
# TYPESEND = 'link' => utilisation de lien (Q5)
# PS désolé pour la personne lisan ce code, il n'y a aucune doc string suite à un petit contre-temps ;)
TYPESEND = 'link'
nav.allowDL(['style.css'])

def init(h : int =6,w : int =7, debug : bool=False) -> list:
    if debug:
        return [[i for i in range(h)] for j in range(w)]
    else:
        return [list([B]*h) for j in range(w)]
    
def visual(L : list[list[str]]):
    nav.write("<main>")
    for i in range(len(L[0])):
        for j in range(len(L)):
            nav.write(f"""<div id="{L[j][len(L[0])-1-i]}"></div>""")
    nav.write("</main>")
        
def ie(L : list[list[str]], j :int) -> int:
    global n
    nav.beginPage()
    print(str(nav.path)[-1])
    if nav.path=="/":
        enter=int(nav.form.get("colone",10))-1
    elif nav.path in [f'/{i}' for i in range(7)]:
        enter = int(str(nav.path)[-1])
    else:
        nav.write("<html><body>La page demandée n'existe pas.</body></html>")
        nav.endPage()
        return False
    if enter!=9 and B in L[enter]:
        update(L, j, enter)
        n += 1
        if estRempli(L) or rangee4(L, j) or colonne4(L, j) or diagonal4(L, j):
            nav.write(
                f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Connect 4</title><link rel="stylesheet" href="style.css"></head><body><h1>Round number {n}, it's {["reds","yellows"][j]}' turn but ...</h1>""")
            if rangee4(L, j) or colonne4(L, j) or diagonal4(L, j):
                nav.write(
                    f"""<h1 style="color: red;">They won !!!</h1>""")
            elif estRempli(L):
                nav.write("""<h1 style="color: red;">Équality !!!</h1>""")
            visual(L)
            nav.endPage()
            return True
        j = (j+1)%2
    navsend(L, j, TYPESEND)
    ie(L,j)
    
 
def lastinc(L : list[list[str]], c : int):
    i=len(L[0])-1
    while i>=0 and L[c][i]==B:
        i-=1
    return i+1
    
def update(L : list[list[str]], j  : int, c : int):
    L[c][lastinc(L,c)]=["rouge","jaune"][j]
        
def estRempli(L : list[list[str]]) -> bool:
    return not B in [L[i][-1] for i in range(len(L))]

def rangee4(L : list[list[str]], j  : int) -> bool:
    for k in range(len(L[0])):
        n=0
        for i in range(len(L)):
            n=n+1 if L[i][len(L[0])-1-k]==["rouge","jaune","fond"][j] else 0
            if n==4:
                return True
    return False

def colonne4(L : list[list[str]], j  : int) -> bool:
    for i in range(len(L)):
        n=0
        for k in L[i]:
            n=n+1 if k==["rouge","jaune","fond"][j] else 0
            if n==4:
                return True
    return False

def diagonal4(L : list[list[str]], j : int) -> bool:
    for x in range(1+len(L)-4):
        y,n=0,0
        while x+y<len(L) and y<len(L[0]):
            n=n+1 if L[x+y][y]==["rouge","jaune","fond"][j] else 0
            if n==4:
                return True
            y+=1
    for y in range(1,1+len(L[0])-4):
        x,n=0,0
        while x<len(L) and y+x<len(L[0]):
            n=n+1 if L[x][y+x]==["rouge","jaune","fond"][j] else 0
            if n==4:
                return True
            x+=1
    for x in range(1+len(L)-4):
        y,n=0,0
        while x+y<len(L) and y<len(L[0]):
            n=n+1 if L[len(L)-1-x-y][y]==["rouge","jaune","fond"][j] else 0
            if n==4:
                return True
            y+=1
    for y in range(1,1+len(L[0])-4):
        x,n=0,0
        while x<len(L) and y+x<len(L[0]):
            n=n+1 if L[len(L)-1-x][x+y]==["rouge","jaune","fond"][j] else 0
            if n==4:
                return True
            x+=1
    return False
            
def gagne(P : list[list[str]], j : int) -> bool:
    return (rangee4(P,j) or colonne4(P,j) or diagonal4(P,j))

def terminal(P : list[list[str]], j : int) -> bool:
    return (gagne(P,j) or estRempli(P))

def navsend(P: list[list[str]], j: int, typesend :str):
    if typesend=='form':
        nav.write(f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Connect 4</title><link rel="stylesheet" href="style.css"></head><body><h1>Round number {n}, it's {["reds","yellows"][j]}' turn to play :</h1>"""); visual(P); nav.write("""<form method="POST" id="form1"><input type="submit" name="colone" value="1"><input type="submit" name="colone" value="2"><input type="submit" name="colone" value="3"><input type="submit" name="colone" value="4"><input type="submit" name="colone" value="5"><input type="submit" name="colone" value="6"><input type="submit" name="colone" value="7"></form></body></html>"""); nav.endPage()
    elif typesend=='link':
        nav.write(f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Connect 4</title><link rel="stylesheet" href="style.css"></head><body><h1>Round number {n}, it's {["reds","yellows"][j]}' turn to play :</h1><section><a href="/0"><div id="{["red","yellow"][j]}choice"></div></a><a href="/1"><div id="{["red","yellow"][j]}choice"></div></a><a href="/2"><div id="{["red","yellow"][j]}choice"></div></a><a href="/3"><div id="{["red","yellow"][j]}choice"></div></a><a href="/4"><div id="{["red","yellow"][j]}choice"></div></a><a href="/5"><div id="{["red","yellow"][j]}choice"></div></a><a href="/6"><div id="{["red","yellow"][j]}choice"></div></a></section>"""); visual(P); nav.write("""<</body></html>"""); nav.endPage()
    else:
        print("""Unknown or unexpected "typesend" values...""")

def newgame():
    global n
    P=init()
    j=random.randint(0,1)
    c=True
    n=0
    nav.beginPage(); nav.write(f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Connect 4</title><link rel="stylesheet" href="style.css"></head><body><h1>Connect 4</h1><form method="POST" id="form"><input type="submit" name="begin" value="Begin"></form></body></html>"""); nav.endPage()
    while c:
        c= not ie(P,j)
        
newgame()
