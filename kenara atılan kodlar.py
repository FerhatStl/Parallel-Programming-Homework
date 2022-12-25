# satır 130 dan itibaren silinenler ile beraber dining philosophers

philosopher_0 = Character(6, 0, (WIDTH // 2 + 10, HEIGHT // 2 + 30))  # kel
philosopher0States = [Character(6, 0, (WIDTH // 2 + 10, HEIGHT // 2 + 30)),
                      Character(6, 4, (WIDTH // 2 + 10, HEIGHT // 2 + 30)),
                      Character(6, 5, (WIDTH // 2 + 10, HEIGHT // 2 + 30))]

philosopher_1 = Character(0, 0, (WIDTH // 2 + 90, HEIGHT // 2 + 30))  # mavi bere
philosopher1States = [Character(0, 0, (WIDTH // 2 + 90, HEIGHT // 2 + 30)),
                      Character(0, 4, (WIDTH // 2 + 90, HEIGHT // 2 + 30)),
                      Character(0, 5, (WIDTH // 2 + 90, HEIGHT // 2 + 30))]

philosopher_2 = Character(4, -2, (WIDTH // 2 + 160, HEIGHT // 2 + 100))  # Turuncu saçlı
philosopher2States = [Character(4, -2, (WIDTH // 2 + 160, HEIGHT // 2 + 100))]

philosopher_3 = Character(10, 1, (WIDTH // 2 + 45, HEIGHT // 2 + 180))  # yeşil uzaylı
philosopher3States = [Character(10, 1, (WIDTH // 2 + 45, HEIGHT // 2 + 180)),
                      Character(10, 5, (WIDTH // 2 + 45, HEIGHT // 2 + 180)),
                      Character(10, 6, (WIDTH // 2 + 45, HEIGHT // 2 + 180))]

philosopher_4 = Character(2, 2, (WIDTH // 2 - 65, HEIGHT // 2 + 100))  # kahverengi saçlı
philosopher4States = [Character(2, 2, (WIDTH // 2 - 65, HEIGHT // 2 + 100)),
                      Character(2, 8, (WIDTH // 2 - 65, HEIGHT // 2 + 100)),
                      Character(2, 7, (WIDTH // 2 - 65, HEIGHT // 2 + 100))]

chopstick_0 = Chopstick(225, (WIDTH // 2 + 0, HEIGHT // 2 - 60))
chopstick0States = [Chopstick(190, (WIDTH // 2 - 20, HEIGHT // 2 - 60)),  # 0ın SOL EL (ihtiyar)
                    Chopstick(225, (WIDTH // 2 + 0, HEIGHT // 2 - 60)),  # 0 ın solundakinin normal konumu
                    Chopstick(260, (WIDTH // 2 + 20, HEIGHT // 2 - 60))]  # mavilinin sağ eli

chopstick_1 = Chopstick(160, (WIDTH // 2 + 55, HEIGHT // 2 - 35))
chopstick1States = [Chopstick(190, (WIDTH // 2 + 45, HEIGHT // 2 - 60)),  # mavilinin sol eli
                    Chopstick(160, (WIDTH // 2 + 55, HEIGHT // 2 - 35)),  # mavilinin solundakinin normali
                    Chopstick(160, (WIDTH // 2 + 75, HEIGHT // 2 - 35))]  # gözlüklünün sağ eli

chopstick_2 = Chopstick(75, (WIDTH // 2 + 40, HEIGHT // 2 + 10))
chopstick2States = [Chopstick(70, (WIDTH // 2 + 20, HEIGHT // 2 + 10)),  # yeşilin sağ eli
                    Chopstick(75, (WIDTH // 2 + 40, HEIGHT // 2 + 10)),  # normali
                    Chopstick(130, (WIDTH // 2 + 80, HEIGHT // 2 + -5))]  # gözlüklünün sol eli

chopstick_3 = Chopstick(15, (WIDTH // 2 - 40, HEIGHT // 2 + 10))
chopstick3States = [Chopstick(-15, (WIDTH // 2 - 75, HEIGHT // 2 + -5)),  # soldaki adamın sağ eli
                    Chopstick(15, (WIDTH // 2 - 40, HEIGHT // 2 + 10)),  # normali
                    Chopstick(15, (WIDTH // 2 - 20, HEIGHT // 2 + 10))]  # yeşilin sol eli

chopstick_4 = Chopstick(290, (WIDTH // 2 - 55, HEIGHT // 2 - 35))
chopstick4States = [Chopstick(290, (WIDTH // 2 - 75, HEIGHT // 2 - 35)),  # soldaki adamın sol eli
                    Chopstick(290, (WIDTH // 2 - 55, HEIGHT // 2 - 35)),  # normali
                    Chopstick(250, (WIDTH // 2 - 55, HEIGHT // 2 - 65))]  # 0 ın sağ eli

# TEST ALANI
chopstick_alpha = Chopstick(45, (WIDTH // 2 - 0, HEIGHT // 2 - 0))
# Chopsticklerde rotasyona 45 diyince sola 45 derece dönüyor ve tam yukarı bakıyor.
# 225 ise tam sağa bakıyor.
# Height2 yi arttırmak aşağıya ve Width/2 yi arttırmak sağa gitmesi demek.

# bu aşağıdaki 2 taneyi kullanmayacağız o7
# bununla konumları test ettim hangisinin hangisi olduğunu artık biliyoruz.
chopstick_test = Chopstick(290, (WIDTH // 2 - 75, HEIGHT // 2 - 35))
