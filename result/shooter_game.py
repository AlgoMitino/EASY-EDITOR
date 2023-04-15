#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer
class Gamesprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.size_x = size_x
        self.size_y = size_y
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.y = player_y
        self.rect.x = player_x
    def reset(self):
        win.blit(self.image,(self.rect.x, self.rect.y))

class PLAYER(Gamesprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_RIGHT] and self.rect.x < win_width -80:
            self.rect.x += self.speed
        if key_pressed[K_RIGHT] and self.rect.x > 5:
            self.rect.x -= self.speed
    def fire(self):
        bul = bullets(i_b, self.rect.centerx, self.rect.top, randint(6, 22), 30, 50)
        bulls.add(bul)

class ENEMY(Gamesprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            lost += 1

class bullets(Gamesprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class ASTEROID(Gamesprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            lost += 1

i_e = 'ufo.png'
i_b = 'bullet.png'
i_p = 'rocket.png'
a_p = 'asteroid.png'

score = 0
lost = 0
max_lost = 200
goal = 10
rel_time = 3
shoot_bul = 7






display.set_caption("UFO")
win_height = 900
win_width = 900
win = display.set_mode((win_height,win_width))
background = transform.scale(image.load('Ufo.jpg'), (900,700))
background2 = transform.scale(image.load('NLO.jpg'), (900,700))



pl = PLAYER(i_p, 450, win_height-290, 2, 50, 100)
cybs = sprite.Group()
for i in range(5):
    cyb = ENEMY(i_e, randint(80, win_width - 80), -40, randint(6, 22), 90, 50)
    cybs.add(cyb)

asts = sprite.Group()
for i in range(5):
    ast = ENEMY(a_p, randint(80, win_width - 80), -40, randint(80, 220), randint(80, 220), randint(10, 25))
    asts.add(ast)




bulls = sprite.Group()



mixer.init()
#mixer.music.load('space.ogg')
#mixer.music.play()
Kick = mixer.Sound('fire.ogg')


font.init()
font = font.SysFont('Arial', 80)
win_q = font.render('VICTORY', True, (224, 67, 56))
lose = font.render('YOU LOSE!', True, (224, 67, 56))






finish = False
game = True
clock = time.Clock()
FPS = 60
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #Kick.play()
                pl.fire()
    if not finish:
        win.blit(background,(0,0))
        text = font.render('Счёт' + str(score), True, (34, 88, 98))
        win.blit(text, (10,20))
        text_lose = font.render('Пропущено' + str(lost), 1, (34, 88, 98))
        win.blit(text_lose, (10,50))

    pl.update()
    cybs.update()
    bulls.update()
    asts.update()


    pl.reset()
    cybs.draw(win)
    bulls.draw(win)
    asts.draw(win)

    collides = sprite.groupcollide(cybs, bulls, True, True)
    for s in collides:
        score +=1
        cyb = ENEMY(i_e, randint(80, win_width - 80), -40, randint(6, 22), 90, 50)
        cybs.add(cyb)


        if sprite.spritecollide(pl, cybs, False) or lost >= max_lost:
            finish = True
            win.blit(background2,(0,0))
            #kick.play()
            win.blit(lose, (200,200))
                  


        if sprite.spritecollide (pl, asts, False) or lost >= max_lost:
            finish = True
            win.blit(background2,(0,0))
            # kick.play()
            win.blit(lose, (200,200))


        if score >= goal:
            finish = True
            win.blit(win_q, (200,200))


    display.update()
    clock.tick(FPS)
quit()









