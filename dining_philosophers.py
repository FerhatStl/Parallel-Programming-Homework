import os
import sys
import time
from random import random
from threading import Semaphore, Thread

import pygame
import asyncio

'''
Gördüğüm kadarıyla bu kod sadece görsellerin görünmesi için yapılmış. Ayriyetten yazılan başka bir kodun buradaki chopstick
lerin konumunu kullanma durumuna göre güncellemesi gerekiyor.
'''

# Fixes the File not found error when running from the command line.
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class BackgroundFurniture(pygame.sprite.Sprite):
    def __init__(self, image_file, location, scale_factor=1.0, horizontal_flip=False, vertical_flip=False):
        super().__init__()
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.flip(self.image, horizontal_flip, vertical_flip)
        self.image = pygame.transform.scale(
            self.image,
            (
                int(self.image.get_width() * scale_factor),
                int(self.image.get_height() * scale_factor)
            )
        )
        self.rect = self.image.get_rect(center=location)


class Chair(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        super().__init__()
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 4, self.image.get_height() * 4))
        self.rect = self.image.get_rect(center=location)


class Character(pygame.sprite.Sprite):
    def __init__(self, character_id, state_id, location):
        super().__init__()
        self.image = pygame.image.load("assets/characters.png")
        self.rect = self.image.get_rect(center=location)
        self.image = self.image.subsurface(pygame.Rect(abs(state_id) * 16, character_id * 16, 16, 16))
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 4, self.image.get_height() * 4))
        if state_id < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        self.direction = "right"
        self.moving = False
        self.speed = 5


class Text:
    def __init__(self, text, location, font_size=20, font_color=(0, 0, 0)):
        self.text = text
        self.font = pygame.font.Font("assets/PressStart2P.ttf", font_size)
        self.text_surface = self.font.render(self.text, True, font_color)
        self.text_rect = self.text_surface.get_rect(center=location)


class Meal(pygame.sprite.Sprite):
    def __init__(self, location):
        super().__init__()
        self.image = pygame.image.load("assets/spaghetti_full.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 1, self.image.get_height() * 1))
        self.rect = self.image.get_rect(center=location)


class Chopstick(pygame.sprite.Sprite):
    def __init__(self, angle, location):
        super().__init__()
        self.image = pygame.image.load("assets/chopstick.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 0.3, self.image.get_height() * 0.3))
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=location)


WIDTH = 800
HEIGHT = 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dining Philosophers")
screen.fill((255, 255, 255))
clock = pygame.time.Clock()

background_group = pygame.sprite.Group()
background_group.add(
    [
        BackgroundFurniture("assets/floor.png", (x, y))
        for x in range(0, WIDTH + 100, 62) for y in range(0, HEIGHT + 100, 46)
    ]
)

background_group.add(BackgroundFurniture("assets/carpet.png", (WIDTH // 2, HEIGHT // 2), 12))
background_group.add(BackgroundFurniture("assets/fireplace.png", (WIDTH // 2, 60), 4))
background_group.add(BackgroundFurniture("assets/music_player.png", (720, 90), 4))
background_group.add(BackgroundFurniture("assets/sofa_front.png", (560, 80), 4))
background_group.add(BackgroundFurniture("assets/sofa_single_right.png", (740, 200), 4))
background_group.add(BackgroundFurniture("assets/stairs.png", (700, 440), 4, True))
background_group.add(BackgroundFurniture("assets/desk.png", (170, 120), 3))
background_group.add(BackgroundFurniture("assets/table_horizontal.png", (WIDTH // 2, HEIGHT // 2), 4))

title_text = Text("Dining Philosophers", (WIDTH // 2 - 100, HEIGHT - 50), 24, (200, 255, 200))

meal_0 = Meal((WIDTH // 2 - 40, HEIGHT // 2 - 50))
meal_1 = Meal((WIDTH // 2 + 40, HEIGHT // 2 - 50))
meal_2 = Meal((WIDTH // 2 + 60, HEIGHT // 2 - 15))
meal_3 = Meal((WIDTH // 2 + 0, HEIGHT // 2 - 10))
meal_4 = Meal((WIDTH // 2 - 60, HEIGHT // 2 - 15))
meal_group = pygame.sprite.Group()
meal_group.add([meal_0, meal_1, meal_2, meal_3, meal_4])

meal0_size = Text("TEXT", (WIDTH // 2 - 40, HEIGHT // 2 - 50), 10, (0, 0, 0))
meal1_size = Text("TEXT", (WIDTH // 2 + 40, HEIGHT // 2 - 50), 10, (0, 0, 0))
meal2_size = Text("TEXT", (WIDTH // 2 + 60, HEIGHT // 2 - 15), 10, (0, 0, 0))
meal3_size = Text("TEXT", (WIDTH // 2 + 0, HEIGHT // 2 - 10), 10, (0, 0, 0))
meal4_size = Text("TEXT", (WIDTH // 2 - 60, HEIGHT // 2 - 15), 10, (0, 0, 0))

philosopher_group = pygame.sprite.Group()
chair_0 = Chair("assets/chair_front_2.png", (WIDTH // 2 - 40, HEIGHT // 2 - 110))
chair_1 = Chair("assets/chair_front_2.png", (WIDTH // 2 + 40, HEIGHT // 2 - 110))
chair_2 = Chair("assets/chair_right_2.png", (WIDTH // 2 + 130, HEIGHT // 2 - 10))
chair_3 = Chair("assets/chair_back_2.png", (WIDTH // 2, HEIGHT // 2 + 100))
chair_4 = Chair("assets/chair_left_2.png", (WIDTH // 2 - 130, HEIGHT // 2 - 10))

philosopher_0 = Character(6, 0, (WIDTH // 2 + 10, HEIGHT // 2 + 30))  # kel
philosopher0States = [Character(6, 0, (WIDTH // 2 + 10, HEIGHT // 2 + 30)),
                      Character(6, 4, (WIDTH // 2 + 10, HEIGHT // 2 + 30)),
                      Character(6, 5, (WIDTH // 2 + 10, HEIGHT // 2 + 30))]

philosopher_1 = Character(0, 0, (WIDTH // 2 + 90, HEIGHT // 2 + 30))  # mavi bere
philosopher_2 = Character(4, -2, (WIDTH // 2 + 160, HEIGHT // 2 + 100))  # Turuncu saçlı
philosopher_3 = Character(10, 1, (WIDTH // 2 + 45, HEIGHT // 2 + 180))  # yeşil uzaylı
philosopher_4 = Character(2, 2, (WIDTH // 2 - 65, HEIGHT // 2 + 100))  # kahverengi saçlı

chopstick_0 = Chopstick(225, (WIDTH // 2 + 0, HEIGHT // 2 - 60))
chopstick_1 = Chopstick(160, (WIDTH // 2 + 55, HEIGHT // 2 - 35))
chopstick_2 = Chopstick(75, (WIDTH // 2 + 40, HEIGHT // 2 + 10))
chopstick_3 = Chopstick(15, (WIDTH // 2 - 40, HEIGHT // 2 + 10))
chopstick_4 = Chopstick(290, (WIDTH // 2 - 55, HEIGHT // 2 - 35))


# TEST ALANI
#chopstick_alpha = Chopstick(45, (WIDTH // 2 - 0, HEIGHT // 2 - 0))
# Chopsticklerde rotasyona 45 diyince sola 45 derece dönüyor ve tam yukarı bakıyor.
# 225 ise tam sağa bakıyor.
# Height2 yi arttırmak aşağıya ve Width/2 yi arttırmak sağa gitmesi demek.

# bu aşağıdaki 2 taneyi kullanmayacağız o7
# bununla konumları test ettim hangisinin hangisi olduğunu artık biliyoruz.

# ÇALIŞMA ALANI
# liste de sol1,sağ1,sol2,sağ2 şeklinde ilerlicez.
chopstick_list = [Chopstick(190, (WIDTH // 2 - 20, HEIGHT // 2 - 60)),  # 0sol
                  Chopstick(250, (WIDTH // 2 - 55, HEIGHT // 2 - 65)),  # 0sağ
                  Chopstick(190, (WIDTH // 2 + 45, HEIGHT // 2 - 60)),  # 1sol mavi bere
                  Chopstick(260, (WIDTH // 2 + 20, HEIGHT // 2 - 60)),  # 1sağ
                  Chopstick(130, (WIDTH // 2 + 80, HEIGHT // 2 + -5)),  # 2sol turuncu
                  Chopstick(160, (WIDTH // 2 + 75, HEIGHT // 2 - 35)),  # 2sağ
                  Chopstick(15, (WIDTH // 2 - 20, HEIGHT // 2 + 10)),  # 3sol yeşil
                  Chopstick(70, (WIDTH // 2 + 20, HEIGHT // 2 + 10)),  # 3sağ
                  Chopstick(290, (WIDTH // 2 - 75, HEIGHT // 2 - 35)),  # 4sol kahverengi
                  Chopstick(-15, (WIDTH // 2 - 75, HEIGHT // 2 + -5))  # 4sağ
                  ]

philosopher_group.add(
    [
        chair_0, chair_1, chair_2, chair_4,
        philosopher_0,
        philosopher_1,
        philosopher_2,
        philosopher_3,
        philosopher_4,
        chair_3,
    ]
)
'''
Yemeklerin altına-üstüne kalan haklar yazmalı.
chopsticklerin muhtemel konumları kaydedilmeli. if ile kullanım belirlenmeli
if doğru ise yemekten bir hak eksitilmeli.
'''

chopstick_group = pygame.sprite.Group()
chopstick_group.add([chopstick_0, chopstick_1, chopstick_2, chopstick_3, chopstick_4])
philosophers = [philosopher_0,
                philosopher_1,
                philosopher_2,
                philosopher_3,
                philosopher_4]

# Bir chopstick in aktif olup olmama durumu listesi. Chopstickler buna göre çizilecek.
chopstick_activity_list = [0 for _ in range(len(chopstick_list))]


async def visual_main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pass

        # chopstickleri her seferinde kontrol edip ekleyecek kısım
        active_chopstick_group = pygame.sprite.Group()
        for i in range(len(chopstick_list)):
            if chopstick_activity_list[i] == 1:
                active_chopstick_group.add(chopstick_list[i])

        background_group.draw(screen)
        screen.blit(title_text.text_surface, title_text.text_rect)
        meal_group.draw(screen)
        philosopher_group.draw(screen)
        # chopstick_group.draw(screen) # chopsticklerin asıl yerini çizer
        active_chopstick_group.draw(screen)  # chopsticklerin o anki konumlarını çizer.
        pygame.display.update()
        clock.tick(60)


class DiningPhilosophers:
    def __init__(self, number_of_philosophers, meal_size=9):
        self.meals = [meal_size for _ in range(number_of_philosophers)]  # yemekler ayarlanmış.
        self.chopsticks = [Semaphore(value=1) for _ in range(number_of_philosophers)]
        self.status = ['WAITING' for _ in range(number_of_philosophers)]
        # yeni liste her bir stick için 1 artırıcak. 2 durumu yeme, 1 durumu tek stickle bekleme 0 durumu ise sticksiz.
        self.chopstick_holders = [0 for _ in range(number_of_philosophers)]
        self.number_of_philosophers = number_of_philosophers

    def philosopher(self, i):
        j = (i + 1) % self.number_of_philosophers
        while self.meals[i] > 0:
            self.status[i] = '  T  '
            time.sleep(random.random())
            self.status[i] = '  _  '
            # chopstick aldığında sol tarafına alıyor ve tutmaya sol kısımı ekliyor.
            if self.chopsticks[i].acquire(timeout=1):
                self.chopstick_holders[i] += 1
                # SOLUNA CHOPSTICK GELMELİ
                time.sleep(random.random())
                # 2. chopstick i alıyor.
                if self.chopsticks[j].acquire(timeout=1):
                    self.chopstick_holders[i] += 1
                    self.status[i] = '  E  '  # yeme durumuna geçiyor.
                    time.sleep(random.random())
                    self.meals[i] -= 1  # yemeği azalıyor.
                    self.chopsticks[j].release()  # chopstick in birini bırakıyor.
                    self.chopstick_holders[i] -= 1
                self.chopsticks[i].release()  # diğerini bırakıyor.
                self.chopstick_holders[i] = 0
                self.status[i] = '  T  '  # boşta durumuna geçiyor.


async def semaphore_main():
    # n filozof sayısı
    n = 5
    # m yemeğin büyüklüğü
    m = 7
    dining_philosophers = DiningPhilosophers(n, m)
    # philosphers listesi içine filozoflar kadar thread oluşturuyor.
    philosophers = [Thread(target=dining_philosophers.philosopher, args=(i,)) for i in range(n)]
    # threadleri başlatıyor.
    for philosopher in philosophers:
        philosopher.start()

    # burada console da sürekli olarak görsel güncelleme yapılması sağlanmış.
    # buna cidden ihtiyaç varmı?
    while sum(dining_philosophers.meals) > 0:
        print("=" * (n * 5))
        print("".join(map(str, dining_philosophers.status)), " : ",
              str(dining_philosophers.status.count('  E  ')))
        print("".join(map(str, dining_philosophers.chopstick_holders)))
        print("".join("{:3d}  ".format(m) for m in dining_philosophers.meals), " : ",
              str(sum(dining_philosophers.meals)))
        time.sleep(0.1)
    # threadlerin bitmesi bekleniyor.
    for philosopher in philosophers:
        philosopher.join()


if __name__ == "__main__":
    asyncio.run(visual_main())
    asyncio.run(semaphore_main())
