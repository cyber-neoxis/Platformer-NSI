import pyxel
from time import time

class Enemy :
    def __init__(self):
        self.x = 0
        self.vitesse = 5

    def update(self):
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x = max(0, self.x - self.vitesse)
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x = min(pyxel.width - 14, self.x + self.vitesse)
    
    def draw(self):
        pyxel.blt(self.x,pyxel.height-6,0,33,17,14,6)
        #Duplication devant
        a = 256- (self.x+14)
        b = a//14
        for i in range(b):
            pyxel.blt(self.x + 14*(i+1), pyxel.height-6, 0,33,17,14,6)
        #Duplication derrière
        a = 256-self.x
        b = a//14
        for i in range(b):
            pyxel.blt(self.x - 14*(i+1), pyxel.height-6, 0,33,17,14,6)

class Character :
    def __init__(self):
        self.w = 8
        self.h = 8
        self.x = 0
        self.y = pyxel.height - self.h
        self.speed = 5
        self.in_motion = False
        self.direction = 1

    def update(self):
        self.in_motion = False
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.direction = 1
            self.in_motion = True
            self.x = min(pyxel.width-self.w, self.x + self.speed)
        if pyxel.btn(pyxel.KEY_LEFT):
            self.direction = -1
            self.in_motion = True
            self.x = max(0, self.x - self.speed)

    def draw(self):
        if self.in_motion and pyxel.frame_count % 6 < 3 :
            pyxel.blt(self.x, self.y, 0, 16,0, self.w*self.direction, self.h, colkey=0)
        else :
            pyxel.blt(self.x, self.y, 0, 8,0, self.w*self.direction, self.h, colkey=0)

class Eclaireur :
    def __init__(self, x:int, y:int, replaced:bool):
        self.x = x
        self.y = y
        self.replaced = replaced
    
    def update(self):
        if pyxel.frame_count % 10 == 0 :
            self.x -= 5
    
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 25,17,6,6)

class App :
    def __init__(self):
        pyxel.init(128,128, title="Space opera", fps=30, quit_key=pyxel.KEY_Q)
        pyxel.load("1.pyxres")
        self.Neoxis = Character()
        self.Le_mechant = Enemy()
        self.eclaireurs = [Eclaireur(20, 20, False)]
        pyxel.run(self.update, self.draw)

    def update(self):
        self.Neoxis.update()
        self.Le_mechant.update()
        for eclaireur in self.eclaireurs :
            eclaireur.update()
            if eclaireur.x <= 0 and eclaireur.replaced == False:
                eclaireur.replaced = True
                self.eclaireurs.append(Eclaireur(pyxel.width, 20, False))
            if eclaireur.x <= -6 :
                self.eclaireurs.remove(eclaireur)
        if pyxel.frame_count %60 == 0 : print(len(self.eclaireurs), self.eclaireurs)

    def draw(self):
        pyxel.cls(14)
        #Maps
        pyxel.bltm(0,0,0,0,0,128,128)
        #Vaiseau
        pyxel.blt(50,50, 0, 0,32, 16,16, colkey=0)
        #Eclaireurs
        for eclaireur in self.eclaireurs :
            pyxel.blt(eclaireur.x, eclaireur.y, 0, 25,17,6,6 )
        self.Le_mechant.draw()
        self.Neoxis.draw()

App()