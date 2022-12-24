from threading import Thread, Semaphore
import random
import time
import dining_philosophers as visuals


'''
tutma durumunu kaydetme?


'''


class DiningPhilosophers:
    def __init__(self, number_of_philosophers, meal_size=9):
        self.meal_sizes = [meal_size for _ in range(number_of_philosophers)] # yemekler ayarlanmış.
        self.chopstick = [Semaphore(value=1) for _ in range(number_of_philosophers)]
        self.status = ['WAITING' for _ in range(number_of_philosophers)]
        #chopstick tutma listesi yeniden tanımlanmalı.
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
                self.chopstick_holders[i] = ' /   '
                #belli süre bekliyor.
                time.sleep(random.random())
                # 2. chopstick i alıyor.
                if self.chopsticks[j].acquire(timeout=1):
                    self.chopstick_holders[i] = ' / \\ ' #2 elle tutuyor.
                    self.status[i] = '  E  '  # yeme durumuna geçiyor.
                    time.sleep(random.random())  # bekliyor.
                    self.meals[i] -= 1 # yemeği azalıyor.
                    self.chopsticks[j].release()  # chopstick in birini bırakıyor.
                    self.chopstick_holders[i] = ' /   '  # sağdaki gitti.
                self.chopsticks[i].release()  # diğerini bırakıyor.
                self.chopstick_holders[i] = '     '  # 2side yok.
                self.status[i] = '  T  '  # boşta durumuna geçiyor.


def main():
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
    while sum(dining_philosophers.meals) > 0:
        #burada console da sürekli olarak görsel güncelleme yapılması sağlanmış.
        # buna cidden ihtiyaç varmı?
        time.sleep(0.1)
    for philosopher in philosophers:
        philosopher.join()


if __name__ == "__main__":
    main()
