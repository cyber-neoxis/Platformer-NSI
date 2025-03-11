import pyxel



class Maps() :
    def __init__(self, n_map:int):
        self.n_map = n_map
        self.block = []
        if self.n_map == 0 :
            self.block = [pyxel.tilemaps[0].pget(i,j) for i in range(3,13) for j in range(3,13)]
            for i in range(16):
                self.block.append(pyxel.tilemaps[0].pget(0, i))
                self.block.append(pyxel.tilemaps[0].pget(i, 0))
                self.block.append(pyxel.tilemaps[0].pget(15, i))
                self.block.append(pyxel.tilemaps[0].pget(i, 15))
        elif self.n_map == 1 :
            self.block = []
    
    def is_solide(self, x:int, y:int):
        return True if pyxel.tilemaps[0].pget(x//8,y//8) in self.block else False
    
    def update(self,):
        pass

    def draw(self, px:int, py:int) :
        pyxel.bltm(0,0,0,0,0,128,128)




class Character :
    def __init__(self):
        self.w = 8
        self.h = 8
        self.x = 16
        self.y = 112
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
        #haut bas par défaut
        if pyxel.btn(pyxel.KEY_UP):
            self.y = max(0, self.y-self.speed)
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y = min(pyxel.height-self.h, self.y + self.speed)

    def draw(self):
        if self.in_motion and pyxel.frame_count % 6 < 3 :
            pyxel.blt(self.x, self.y, 0, 16,0, self.w*self.direction, self.h, colkey=0)
        else :
            pyxel.blt(self.x, self.y, 0, 8,0, self.w*self.direction, self.h, colkey=0)

class App :
    def __init__(self):
        pyxel.init(128,128, title="First game", fps=30, quit_key=pyxel.KEY_Q)
        pyxel.load("1.pyxres")
        #Block solide
        self.block = [pyxel.tilemaps[0].pget(i,j) for i in range(3,13) for j in range(3,13)]
        for i in range(16):
            self.block.append(pyxel.tilemaps[0].pget(0, i))
            self.block.append(pyxel.tilemaps[0].pget(i, 0))
            self.block.append(pyxel.tilemaps[0].pget(15, i))
            self.block.append(pyxel.tilemaps[0].pget(i, 15))
        self.kerix = Character()
        pyxel.run(self.update, self.draw)

    def update(self):
        self.kerix.update()


    def draw(self):
        pyxel.cls(14)
        #..
        if pyxel.frame_count == 0 :
            for i in range(10) :
                for j in range(10):
                    print(pyxel.tilemaps[0].pget(i,j))
        self.kerix.draw()
App()