from threading import Thread, Semaphore
import random
import time
#import dining_philosophers as visuals


'''
tutma durumunu kaydetme?


'''


class DiningPhilosophers:
    def __init__(self, number_of_philosophers, meal_size=9):
        self.meals = [meal_size for _ in range(number_of_philosophers)] # yemekler ayarlanmış.
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


def main():
    # n filozof sayısı
    n = 5
    meal_size = 7
    dining_philosophers = DiningPhilosophers(n, meal_size)
    # philosphers listesi içine filozoflar kadar thread oluşturuyor.
    philosophers = [Thread(target=dining_philosophers.philosopher, args=(i,)) for i in range(n)]
    # threadleri başlatıyor.
    for philosopher in philosophers:
        philosopher.start()
    while sum(dining_philosophers.meals) > 0:
        # update the screen
        print("=" * (n * 5))
        print("".join(map(str, dining_philosophers.status)), " : ",
              str(dining_philosophers.status.count('  E  ')))
        print("".join(map(str, dining_philosophers.chopstick_holders)))
        print("".join("{:3d}  ".format(m) for m in dining_philosophers.meals), " : ",
              str(sum(dining_philosophers.meals)))
        time.sleep(0.1)
    for philosopher in philosophers:
        philosopher.join()


if __name__ == "__main__":
    main()
