# title: Survival Collect
# author: Ali Dicko & Ervin
# desc: Projet NSI - Action-platformer
# site: https://github.com/cyber-neoxis/Platformer-NSI
# license: MIT
# version: 1.0

import pyxel
import random
# États du jeu
MENU = 0
JEU = 1
FIN = 2

def is_wall(px, py):
    """Vérifie si le joueur entre en collision avec un mur."""
    tile_x = (px + 4) // 8
    tile_y = (py + 4) // 8
    wall_tile = [(4,1),(5,0),(7,1),(6,0),  (4,0),(5,1),(7,0)]
    return pyxel.tilemaps[1].pget(tile_x, tile_y) in wall_tile

# ------------------------------------------------------------------
# Classe Clés
# ------------------------------------------------------------------
class Key:
    def __init__(self):
        self.x = 27  # Position fixe
        self.y = 53  # Position fixe
        self.is_visible = False
        self.spawn_time = pyxel.frame_count + random.randint(75, 180)  # 2.5 à 6 sec
   
    def update(self, player):
        if pyxel.frame_count >= self.spawn_time and not self.is_visible:
            self.is_visible = True
       
        if self.is_visible and abs(self.x - player.x) < 8 and abs(self.y - player.y) < 8:
            self.is_visible = False
            player.score_cle += 1
            self.spawn_time = pyxel.frame_count + random.randint(90, 270)
   
    def draw(self):
        if self.is_visible:
            pyxel.blt(self.x, self.y, 0, 33, 32, 4, 9, colkey=0)

# ------------------------------------------------------------------
# Classe Bullet
# ------------------------------------------------------------------
class Bullet:
    def __init__(self, x, y, speed, dir):
        self.x = x
        self.y = y-3
        self.speed = speed
        self.dir = dir
        self.is_alive = True
        self.lifetime = 180  # 180 frames = 6 secondes à 30 FPS

    def update(self):
        self.x += self.speed * self.dir
        self.lifetime -= 1  # Diminue la durée de vie
        if self.lifetime <= 0:  # Supprime après un certain temps
            self.is_alive = False

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 24, 33, 8, 8, colkey=0)

# ------------------------------------------------------------------
# Classe Enemy
# ------------------------------------------------------------------
class Enemy:
    def __init__(self, player_x, player_y, player_dir, sprite):
        distance = pyxel.rndi(50, 150)
        self.x = player_x + (distance * player_dir)
        self.y = player_y
        self.speed = 3
        self.dir = -player_dir
        self.is_alive = True
        self.last_shot_time = 0
        self.bullets = []
        self.sprite = sprite


    def update(self, player):
        # Déplacement horizontal vers le joueur
        if abs(self.x - player.x) > self.speed:
            if self.x < player.x:
                self.x += self.speed * 0.5
            else:
                self.x -= self.speed * 0.5

        # Déplacement vertical vers le joueur
        if abs(self.y - player.y) > self.speed:
            if self.y < player.y:
                self.y += self.speed
            else:
                self.y -= self.speed

        # Collision avec le joueur
        if abs(self.x - player.x) < 8 and abs(self.y - player.y) < 8:
            self.is_alive = False
            player.health -= 1

        # Collision avec les balles du joueur
        for bullet in player.bullet_list:
            if abs(self.x - bullet.x) < 8 and abs(self.y - bullet.y) < 8:
                self.is_alive = False
                bullet.is_alive = False

        # Tir de l'ennemi
        if pyxel.frame_count - self.last_shot_time >= 60:
            self.shoot()
            self.last_shot_time = pyxel.frame_count

        # Mise à jour des balles de l'ennemi
        for bullet in self.bullets:
            bullet.update()
            if abs(bullet.x - player.x) < 4 and abs(bullet.y - player.y) < 4:
                player.health -= 1
                bullet.is_alive = False

        self.bullets = [b for b in self.bullets if b.is_alive]

    def shoot(self):
        self.bullets.append(Bullet(self.x, self.y + 2, 3.5, self.dir))

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.sprite[0], self.sprite[1], 6, 6)
        for bullet in self.bullets:
            bullet.draw()

# ------------------------------------------------------------------
# Gestionnaire d'ennemis
# ------------------------------------------------------------------
class Enemysettings:
    def __init__(self):
        self.enemies = []
        self.last_spawn_time = 0

    def update(self, player):
        sprite = random.choice([(25,25), (25,17), (17,17), (17, 25)])

        if pyxel.frame_count - self.last_spawn_time >= 75 :
            self.enemies.append(Enemy(player.x, player.y, player.dir, sprite))
            self.last_spawn_time = pyxel.frame_count

        for enemy in self.enemies:
            enemy.update(player)

        self.enemies = [enemy for enemy in self.enemies if enemy.is_alive]

    def draw(self):
        for enemy in self.enemies:
            enemy.draw()
       
# ------------------------------------------------------------------
# Classe GameMap
# ------------------------------------------------------------------
class GameMap:
    def __init__(self):
        self.tilemap = pyxel.tilemaps[1]

    def is_solid(self, tile_x, tile_y):
        tile = self.tilemap.pget(tile_x, tile_y)
        # On considère les tuiles solides
        solide = [(i,j) for i in range(4,8) for j in range(0,2)]
        #solide.remove((7,1))
        return tile in solide
   
    def draw(self):
        pyxel.bltm(0, 0, 1, 0, 0, 191*8, 128)

# ------------------------------------------------------------------
# Classe Player unifiée (gravité, collisions, dash, tir)
# ------------------------------------------------------------------
class Player:
    def __init__(self):
        self.x = 16
        self.y = 88
        self.vy = 0          # Vitesse verticale
        self.speed = 3
        self.dir = 1
        self.health = 7*7
        self.bullet_list = []
        self.on_ground = False
        # Variables pour le dash
        self.dash_ready = True
        self.dash_speed = 1
        self.cooldown = 0
        self.score_cle = 0
        self.moved = False
        self.respawn_timer = 0
       
    def respawn(self):
        if self.y > pyxel.height:  # Si le joueur tombe hors écran
            if self.respawn_timer == 0:  # Vérifie qu'il peut respawn
                self.x, self.y = 16, 80
                self.vy = 0  # Réinitialise la vitesse pour éviter qu'il ne retombe immédiatement
                self.health -= 1
                self.respawn_timer = 60  # Ajoute un délai de 60 frames (2 secondes si 30 FPS)

        if self.respawn_timer > 0:
            self.respawn_timer -= 1  # Diminue le timer chaque frame

    def is_on_flame(self, tile_x, tile_y):
        """Vérifie si la tuile sous le joueur est une flamme."""
        flames_tiles = [(0, 2), (0, 3), (1, 2), (1, 3)]  # ID des flammes dans la tilemap
        return pyxel.tilemaps[1].pget(tile_x, tile_y) in flames_tiles
    
    def apply_gravity(self):
        GRAVITY = 0.6
        if not self.on_ground :
            self.vy += GRAVITY
        self.y += self.vy

    def check_collisions(self, game_map):
        """Vérifie les collisions avec le sol et le plafond"""
        tile_x = self.x // 8
        tile_y_below = (self.y + 8) // 8  # Tuile sous le joueur
        tile_y_above = (self.y - 1) // 8  # Tuile au-dessus du joueur

        # Vérifie si on touche le sol
        if game_map.is_solid(tile_x, tile_y_below):
            self.y = tile_y_below * 8 - 8
            self.vy = 0
            self.on_ground = True
        else:
            self.on_ground = False

        # Vérifie si on touche un mur au dessus
        if self.vy < 0 and game_map.is_solid(tile_x, tile_y_above):
            self.vy = 0  # Arrête le saut
            self.y = (tile_y_above + 1) * 8  # Replace sous le plafond

    def update(self, game_map):
        # Appliquer la gravité et vérifier les collisions
        self.apply_gravity()
        self.check_collisions(game_map)
        self.moved = False
        self.respawn()
    

        if self.is_on_flame(self.x // 8, self.y // 8):
            self.health -= 0.1  # Dégâts progressifs si le joueur marche sur une flamme

        # Gestion du dash
        if pyxel.frame_count - self.cooldown == 6*30:
            self.dash_ready = True
            self.speed = 3
    
        if pyxel.btn(pyxel.KEY_0) and self.dash_ready:
            self.cooldown = pyxel.frame_count
            self.speed *= 3
            self.dash_ready = False

        # Déplacements horizontaux
        if pyxel.btn(pyxel.KEY_RIGHT) and not is_wall(self.x + self.speed, self.y):
                self.dir = 1
                self.x = min(183*8, self.x + self.speed)
                self.moved = True

        if pyxel.btn(pyxel.KEY_LEFT) and not is_wall(self.x - self.speed, self.y):
                self.dir = -1
                self.x = max(0, self.x - self.speed)
                self.moved = True

        #Other Key
        if pyxel.tilemaps[1].pget((self.x + 4) // 8, (self.y + 4) // 8) == (4,4) :
            self.score_cle += 1

        # Saut (uniquement si au sol)
        if pyxel.btnp(pyxel.KEY_UP) and self.on_ground:
            self.vy = -6
        # Tir
        if pyxel.btnr(pyxel.KEY_SPACE):
            self.bullet_list.append(Bullet(self.x + (8 if self.dir == 1 else 0), self.y + 4, 4, self.dir))
        for bullet in self.bullet_list:
            bullet.update()
        self.bullet_list = [b for b in self.bullet_list if b.is_alive]

    def draw(self):
        #Animation de mouvement (24,0)
        if self.moved and pyxel.frame_count % 6 < 3 :
            pyxel.blt(self.x, self.y, 0, 16,0, 8*self.dir, 8, colkey=0)
        else :
            pyxel.blt(self.x, self.y, 0, 8,0, 8*self.dir, 8, colkey=0)
        for bullet in self.bullet_list:
            bullet.draw()

# ------------------------------------------------------------------
# Classe Game (états, score, mise à jour globale)
# ------------------------------------------------------------------
class App:
    def __init__(self):
        pyxel.init(128, 128, title="NSI Platformer", fps=30, quit_key=pyxel.KEY_Q)
        pyxel.load("1.pyxres")
        self.state = MENU
        self.player = Player()
        self.game_map = GameMap()
        self.enemy_manager = Enemysettings()
        self.score = 0
        self.best_score = 0
        self.key = Key()
        self.score_cle = 0  # Score des clés récupérées
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.state == MENU:
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.state = JEU
                self.score = 0
        elif self.state == JEU:
            self.player.update(self.game_map)
            self.enemy_manager.update(self.player)
            self.score += 1  # Score basé sur le temps
            self.key.update(self.player)
            if self.player.health <= 0:
                self.best_score = max(self.best_score, self.score//100)
                self.state = FIN
        elif self.state == FIN:
            pyxel.stop(0)
            if pyxel.btnp(pyxel.KEY_RETURN):
                #Réinitialisation des variables
                self.score = 0
                self.score_cle = 0
                self.player.health = 7
                self.enemy_manager.enemies = []
                self.enemy_manager.last_spawn_time = 0
                #Joueur
                self.player.bullet_list = []
                self.player.x = 16
                self.player.y = 64
                self.player.dir = 1
                self.state = JEU  # Redémarrage

    def draw(self):
        pyxel.cls(0)
        if self.state == MENU:
            pyxel.text(35, 50, "NSI PLATFORMER", pyxel.frame_count % 16)
            pyxel.text(28, 70, "Appuyez sur ENTREE", 7)
            pyxel.text(10,100 , "Ali Dicko, Rasolonirina Ervin", 4 )
        elif self.state == JEU:
            pyxel.camera(max(0,self.player.x - pyxel.width // 2), 0)
            self.game_map.draw()
            #Fly
            pyxel.blt(82*8,11*8,0,41,40,7,7)
            pyxel.blt(126*8,9*8,0,41,40,7,7)
            pyxel.blt(151*8,9*8,0,41,40,7,7)
            self.player.draw()
            self.enemy_manager.draw()
            self.key.draw()
            pyxel.camera()
            pyxel.text(5, 10, f"Cles: {self.player.score_cle}", 9)
            pyxel.text(5, 3, f"Score: {self.score//100}", 7)
            pyxel.text(5, 17, f"Vie : {round(self.player.health)}", 3)
        elif self.state == FIN:
            pyxel.text(40, 50, "Game Over", 8)
            pyxel.text(30, 70, f"Score: {self.score//100}", 7)
            pyxel.text(30, 90, f"Cles: {self.player.score_cle}", 9)
            pyxel.text(30, 80, f"Meilleur: {self.best_score}", 7)
            pyxel.text(20, 100, "ENTREE pour recommencer", 7)

App()