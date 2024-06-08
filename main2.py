from typing import Any
from pygame import *
from random import randint
 
# Звуки
mixer.init()
mixer.music.load('space.mp3')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
boom = mixer.Sound('boom.ogg')
# Картинки
img_back = "galaxy.png" 
img_hero = "rocket.png"
img_bullet = "bullet.png" 
# Шрифт та тексти
font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.Font(None, 36)

img_enemy = "ufo.png"
img_boss = "boss.png"
# Рахунки
score = 0
goal = 31
max_lost = 3
lost = 0
max_range = 6
min_range = 1
# Основний клас
class GameSprite(sprite.Sprite):

    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):

        sprite.Sprite.__init__(self)

        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        # Клас ворога
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost = lost + 1

     # Клас набою   
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
# Клас гравця
class Player(GameSprite):
 
    # Керування спрайтом
    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < 390:
            self.rect.y += self.speed
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        
 
    # Постріл
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
 
 
# Створення вікна
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
# Створення спрайта
ship = Player(img_hero, 300, win_height - 100, 80, 100, 20)
 
# Змінна "гра закінчилася": як тільки вона стає True, в основному циклі перестають працювати спрайти
finish = False
 
# Основний цикл гри:
run = True  

monsters = sprite.Group()
for i in range(min_range, max_range):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
bullets = sprite.Group()
 
while run:
    # Кнопка "Закрити"
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
 
    if not finish:
        # Оновлення фону
        window.blit(background, (0, 0))

        text = font2.render("Рахунок: " + str(score) + "/30", 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost) + "/" + str(max_lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
 
        # Рух спрайтів
        ship.update()
        monsters.update()
        bullets.update()

 
        # Оновлення спрайтів у новому місці
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        # Програш/Перемога
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            boom.play()
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
 
        display.update()
    # Цикл спрацьовує кожні 0.06 секунд
    time.delay(60)
