# title: Jojo invendor's
# author: Ali Dicko & Ervin
# desc: Projet NSI - Action-platformer
# site: https://github.com/cyber-neoxis/Platformer-NSI
# license: MIT
# version: Alpha

import pyxel
#from maps import Maps, Scene

#a = Maps(0)
#b = Scene(0)
class Bullet:
    def __init__(self, x, y, speed, dir) :
        self.x = x
        self.y = y
        self.dir = dir
        self.speed = speed
        self.is_alive = True

    def update(self): 
        if self.dir == 1 :
            self.x += self.speed
        else :
            self.x -= self.speed
        
        if (self.x > pyxel.width or self.y > pyxel.height
            or self.x < 0 or self.y < 0) :
            self.is_alive = False
        # if .. Contact avec ennemie
        # if .. Contact avec un obstacle


    def draw(self):
        #u = pyxel.frame_count // 4 % 4 * 8 + 16 (au cas ou il y aurait une deuxième texture)
        pyxel.blt(self.x, self.y,0, 24,33,8,1)

class Player:
    def __init__(self, x=16, y=112):
        self.bullet_liste = []
        #Mouvement
        self.x = x
        self.y = y 
        self.speed = 5
        self.moved = False
        self.dir = 1
        #Dash
        self.dash = False
        self.dash_ready = True
        self.dash_speed = 3
        self.cooldown = 0

    def update(self):
        self.moved = False

        #Dash
        if pyxel.frame_count - self.cooldown == 60 :
            self.speed = self.speed//self.dash_speed
            self.dash_ready = True

        if pyxel.btnr(pyxel.KEY_0) and self.dash_ready:
            self.cooldown = pyxel.frame_count
            self.speed = self.speed * self.dash_speed
            self.dash_ready = False
        
        #Deplacements (zqsd)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.dir = 1
            self.moved = True
            self.x = min(120, self.x + self.speed)

        if pyxel.btn(pyxel.KEY_LEFT):
            self.dir = -1
            self.moved = True
            self.x = max(0, self.x - self.speed)
        
        if pyxel.btn(pyxel.KEY_UP): #Remplacer par space
            self.moved = True
            self.y = max(0, self.y-self.speed)
        
        if pyxel.btn(pyxel.KEY_DOWN): #se baisser
            self.y = min(pyxel.height-8, self.y + self.speed)
        
        #tir
        if pyxel.btn(pyxel.KEY_K) :
            if self.dir == 1 :
                self.bullet_liste.append(Bullet(self.x+8, self.y+4, 3, self.dir))
            else :
                self.bullet_liste.append(Bullet(self.x, self.y+4, 3, self.dir))
        
        for i in self.bullet_liste :
            i.update()
            if i.is_alive == False :
                del i

        
        

    def draw(self):
        #Animation de mouvement (24,0)
        if self.moved and pyxel.frame_count % 6 < 3 :
            pyxel.blt(self.x, self.y, 0, 16,0, 8*self.dir, 8, colkey=0)
        else :
            pyxel.blt(self.x, self.y, 0, 8,0, 8*self.dir, 8, colkey=0)
        for i in self.bullet_liste :
            i.draw()
        

class App:
    def __init__(self):
        pyxel.init(128,128,title="NSI Platformer", fps=30,quit_key=pyxel.KEY_Q)
        pyxel.load("1.pyxres")
        self.Neoxis = Player()
        pyxel.run(self.update, self.draw)

    def update(self):
        self.Neoxis.update()

    def draw(self):
        pyxel.cls(0)
        #Maps
        pyxel.bltm(0,0,0,0,0,128,128)
        self.Neoxis.draw()
        

App()
