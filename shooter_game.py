from pygame import *
from random import randint
window = display.set_mode((700, 500))
display.set_caption("Space invaderz")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
mixer.init()
mixer.music.load("Phantom_from_Space.mp3")
mixer.music.play()
fire = mixer.Sound("fire.ogg")
font.init()
font1 = font.SysFont("Arial", 80)
font2 = font.SysFont("Arial", 36)
missed = 0
hit = 0
max_missed = 3
win = font1.render("You win!", True, (0, 255, 0))
lose = font1.render("You lose!", True, (255, 0, 0))
game = 1
finish = 0
clock = time.Clock()
fps = 60
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 635:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx - 30, self.rect.top, -15)
        bullets.add(bullet)
        fire.play()
class Enemy(GameSprite):
    def update(self):
        global missed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = 50 * randint(1, 13)
            missed += 1
        self.rect.y += self.speed
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
class Asteroid(GameSprite):
    def update(self):
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = 50 * randint(1, 13)
        self.rect.y += self.speed
hero = Player("rocket.png", 0, 400, 5)
ufo1 = Enemy("ufo.png", 250, 0, 1)
ufo2 = Enemy("ufo.png", 350, 0, 1)
ufo3 = Enemy("ufo.png", 450, 0, 1)
ufo4 = Enemy("ufo.png", 550, 0, 1)
ufo5 = Enemy("ufo.png", 650, 0, 1)
asteroid1 = Asteroid("asteroid.png", 100, 0, 2)
asteroid2 = Asteroid("asteroid.png", 650, 0, 2)
ufos = sprite.Group()
ufos.add(ufo1)
ufos.add(ufo2)
ufos.add(ufo3)
ufos.add(ufo4)
ufos.add(ufo5)
bullets = sprite.Group()
asteroids = sprite.Group()
asteroids.add(asteroid1)
asteroids.add(asteroid2)
for i in range(1, 6):
    ufo = Enemy("ufo.png", 50 * randint(1, 13), -40, randint(1, 4))
    ufos.add(ufo)
for j in range(1, 4):
    asteroid = Enemy("asteroid.png", 50 * randint(1, 13), -40, randint(1, 4))
    asteroids.add(asteroid)
while game:
    for events in event.get():
        if events.type == QUIT:
            game = 0
        elif events.type == KEYDOWN:
            if events.key == K_SPACE:
                hero.fire()
    if not finish:
        window.blit(background, (0, 0))
        text = font2.render("Score: " + str(hit), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text2 = font2.render("Missed: " + str(missed), 1, (255, 255, 255))
        window.blit(text2, (10, 50))
        keys_pressed = key.get_pressed()
        hero.reset()
        ufos.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        hero.update()
        ufos.update()
        bullets.update()
        asteroids.update()
        collides = sprite.groupcollide(ufos, bullets, True, True)
        for c in collides:
            hit += 1
            ufo = Enemy("ufo.png", 50 * randint(1, 13), 0, randint(1, 4))
            ufos.add(ufo)
        if sprite.spritecollide(hero, ufos, False) or sprite.spritecollide(hero, asteroids, False) or missed >= max_missed:
            finish = True
            window.blit(lose, (200, 200))
        if hit >= 10:
            finish = True
            window.blit(win, (200, 200))
        display.update()
    else:
        finish = False
        hit = 0
        missed = 0
        for b in bullets:
            b.kill()
        for u in ufos:
            u.kill()
        for a in asteroids:
            a.kill()
        time.delay(3000)
        for i in range(1, 6):
            ufo = Enemy("ufo.png", 50 * randint(1, 13), -40, randint(1, 4))
            ufos.add(ufo)
        for j in range(1, 4):
            asteroid = Enemy("asteroid.png", 50 * randint(1, 13), -40, randint(1, 4))
            asteroids.add(asteroid)
    clock.tick(fps)