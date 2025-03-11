import pyxel

class Player:
    def __init__(self, x=16, y=112):
        self.x = x
        self.y = y 
        self.speed = 5
        self.moved = False
        self.dir = 1
        self.dash = False
        self.dash_ready = True
        self.dash_speed = 2
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
        
        #Deplacements
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.dir = 1
            self.moved = True
            self.x = min(120, self.x + self.speed)

        if pyxel.btn(pyxel.KEY_LEFT):
            self.dir = -1
            self.moved = True
            self.x = max(0, self.x - self.speed)
        
        if pyxel.btn(pyxel.KEY_UP):
            self.moved = True
            self.y = max(0, self.y-self.speed)
        
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y = min(pyxel.height-8, self.y + self.speed)
        
        

    def draw(self):
        #Animation de mouvement
        if self.moved and pyxel.frame_count % 6 < 3 :
            pyxel.blt(self.x, self.y, 0, 16,0, 8*self.dir, 8, colkey=0)
        else :
            pyxel.blt(self.x, self.y, 0, 8,0, 8*self.dir, 8, colkey=0)
        

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