from pygame import*
from time import time as timer
from random import*

'''Шрифт'''
font.init()
font = font.SysFont('Arial Black', 50) #используемый текст
win = font.render('ТЫ ПОБЕДИЛ!', True, (128, 0, 0)) #текст победы
lose = font.render('ТЫ ПРОИГРАЛ(', True, (128, 0, 0)) #текст проигрыша

'''Перменные картинок'''
img_back = 'fon.png' #задний фон
img_hero = 'hero.png' #главный герой
img_enemy1 = 'enemy1.png' #враг 1
img_enemy2 = 'enemy2.png' #враг 2
img_enemy3 = 'enemy3.png' #враг 3
img_enemy4 = 'enemy4.png' #враг 3
img_goal = 'goal.png' #спрайт победы
img_point1 = 'point_1.png' #объект для победы(1)
img_point2 = 'point_2.png' #объект для победы(2)
img_point3 = 'point_3.png' #объект для победы(3)
img_swirl1 = 'swirl_1.png'
img_swirl2 = 'swirl_2.png' #объект оружие
img_cactus = 'cactus.png' #объект враг(припятствие)

'''Музыка'''
mixer.init() #подключение музыки
mixer.music.load('fon_music.ogg') #подключение музыки
mixer.music.play() #запуск музыки

'''Классы'''
#класс родитель для других спрайтов
class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, x, y, width, height, speed):
        #вызываем конструктор класса (Sprite)
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (width, height)) #подключение картинки
        self.speed = speed #скорость
        self.rect = self.image.get_rect() #область объекта 
        self.rect.x = x #по х
        self.rect.y = y #по у
    
    def reset(self):
        #отрисовка в окне
        window.blit(self.image, (self.rect.x, self.rect.y)) #каждая картика имеет свои координаты

#класс главного героя
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed() #подключаем клавиатуру
        if keys[K_LEFT] and self.rect.x > 5: #если зажата левая клавиша, и координаты по х больше 5...
            self.rect.x -= self.speed #...то скорость отнимается
        if keys[K_RIGHT] and self.rect.x < win_width - 50: #если зажата правая клавиша и координаты меньше 650...
            self.rect.x += self.speed #...то скороасть прибавляется
        if keys[K_UP] and self.rect.y > 5: #если зажата клавиша вверх и координаты по у больше 5...
            self.rect.y -= self.speed #...то скорость отнимается
        if keys[K_DOWN] and self.rect.y < win_height - 80: #если зажата клавиша вниз и координаты по у 420...
            self.rect.y += self.speed #...то скорость прибавляется
    #функция огонь (выстрел)
    def fire(self):
        swirl = Swirl(img_swirl1, self.rect.right, self.rect.centery, 30, 30, 2) #расположение вылета пуль
        swirls.add(swirl) #отрисовка в своей группе спрайта
    def fire2(self):
        swirl = Swirl2(img_swirl2, self.rect.left, self.rect.centery, 40, 30, 3)
        swirls.add(swirl)

#класс враг1
class Enemy1(GameSprite):
    side = 'left' #присваиваем значение аргументу
    def update(self): #придаём движение
        if self.rect.x <= 300: #если по х меньше или равно 300
            self.side = 'right' #то движение на право
        if self.rect.x >= 480: #если по ч больше или равно 480
            self.side = 'left' #то на лево
        if self.side == 'left': #если аргумент равняется 'лево'
            self.rect.x -= self.speed #скорость в сторону лево (то есть по координатам уменьшается)
        else:
            self.rect.x += self.speed #иначе скорость в сторону право (то есть по координатам увеличивается)

#класс враг2 (тоже самое, но смотря по координате у)
class Enemy2(GameSprite):
    side = 'up'
    def update(self):
        if self.rect.y <= 200:
            self.side = 'down'
        if self.rect.y >= 300:
            self.side = 'up'
        if self.side == 'up':
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

#класс враг3
class Enemy3(GameSprite):
    side = 'left'
    def update(self):
        if self.rect.x <= 100:
            self.side = 'right'
        if self.rect.x >= 200:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

#класс враг4 (почти точно так же как и предыдущие, но движение по диагонали, одновременно увеличивая координату по у и уменьшая по х (и наоборот))
class Enemy4(GameSprite):
    side = 'left'
    def update(self):
        if self.rect.x <= 480:
            self.side = 'right'
        if self.rect.x >= 620:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -= self.speed
            self.rect.y += self.speed
        else:
            self.rect.x += self.speed
            self.rect.y -= self.speed

#класс стен (полностью прописываем все свойста стен)
class Wall(sprite.Sprite):
    def __init__(self, red, green, blue, wall_x, wall_y, width, height):
        super().__init__()
        self.red = red #передаём цвет через три позиции rgb (r)
        self.green = green #g
        self.blue = blue #b
        self.w = width #ширина стены (стена по х)
        self.h = height #высота стены (стена по у)
        #расположение картинок
        self.image = Surface((self.w, self.h))
        self.image.fill((red, green, blue)) #заполнение стены цветом
        self.rect = self.image.get_rect() #каждая стена так же имеет свою область, дотронувшись до которой игра заканчивается и вы становитесь проигравшим
        #присваеваем стенам свою невидимую зону х и у
        self.rect.x = wall_x
        self.rect.y = wall_y

#класс оружия
class Swirl(GameSprite):
    def update(self): #придаём движение (во время атаки) вихрю
        self.rect.x += self.speed
        if self.rect.x > win_width+10: #при условии достигнуть координату win_width+10...
            self.kill() #убрать с игры вихри, чтобы не застревали за экраном

class Swirl2(GameSprite):
    def update(self): #придаём движение (во время атаки) вихрю
        self.rect.x -= self.speed
        if self.rect.x > win_width+10: #при условии достигнуть координату win_width+10...
            self.kill() #убрать с игры вихри, чтобы не застревали за экраном

'''Окно игры'''

win_width = 700 #ширина
win_height = 500 #высота
display.set_caption('Мистический Лабиринт') #название игрового окна
window = display.set_mode((win_width, win_height)) #отрисовка всего в window
back = transform.scale(image.load(img_back), (win_width, win_height)) #подгружаем задний фон трансформируем его под размеры экрана
clock = time.Clock() #время экрана
FPS = 60 #частота кадров

'''Персонажи '''
#каждому персонажу присваевается свои значение, которые они приобретают в классе
hero = Player(img_hero, 50, win_height - 80, 50, 50, 3) #главный герой
enemy1 = Enemy1(img_enemy1, 400, 400, 65, 65, 1) #враг 1 
enemy2 = Enemy2(img_enemy2, 300, 200, 65, 65, 2) #враг 2
enemy3 = Enemy3(img_enemy3, 60, 105, 65, 65, 1) #враг 3
enemy4 = Enemy4(img_enemy4, 620, 30, 65, 65, 3) #враг 4
fin = GameSprite(img_goal, win_width - 600, win_height - 470, 65, 65, 0) #спрайт условие победы
point_1 = GameSprite(img_point1, win_width - 100, win_height - 300, 65, 65, 0) #объект для победы(1)
point_2 = GameSprite(img_point2, win_width - 670, win_height - 300, 65, 65, 0) #объект для победы(2)
point_3 = GameSprite(img_point3, win_width - 210, win_height - 460, 65, 65, 0) #объект для победы(3)
cactus_1 = GameSprite(img_cactus, win_width - 200, win_height - 260, 65, 65, 0) #объект припятствие(1)
cactus_2 = GameSprite(img_cactus, win_width - 300, win_height - 385, 65, 65, 0) #объек5т припятствие(2)
cactus_3 = GameSprite(img_cactus, win_width - 650, win_height - 385, 65, 65, 0) #объект припятствие(3)

'''Стены'''
#порядок написания параметров для Wall: цвет, x, y, ширина, высота
w1 = Wall(139, 69, 19, 20, 20, win_width - 50, 10) #контурная стена
w2 = Wall(139, 69, 19, 20, 20, 10, win_height - 35) #контурная стена
w3 = Wall(139, 69, 19, 20, 480, 660, 10) #контурная стена
w4 = Wall(139, 69, 19, 670, 20, 10, win_height - 35) #контурная стена
w5 = Wall(139, 69, 19, 100, 100, 100, 10)
w6 = Wall(139, 69, 19, 170, 20, 10, 80)
w7 = Wall(139, 69, 19, 20, 170, 200, 10)
w8 = Wall(139, 69, 19, 20, 400, 160, 10)
w9 = Wall(139, 69, 19, 170, 330, 10, 70)
w10 = Wall(139, 69, 19, 100, 180, 10, 100)
w11 = Wall(139, 69, 19, 400, 180, 10, 200)
w12 = Wall(139, 69, 19, 400, 230, 200, 10)
w13 = Wall(139, 69, 19, 400, 20, 10, 100)
w14 = Wall(139, 69, 19, 500, 300, 100, 10)
w15 = Wall(139, 69, 19, 260, 320, 10, 170)
w16 = Wall(139, 69, 19, 300, 170, 200, 10)
w17 = Wall(139, 69, 19, 550, 20, 10, 100)
w18 = Wall(139, 69, 19, 260, 70, 150, 10)
w19 = Wall(139, 69, 19, 100, 240, 200, 10)
w20 = Wall(139, 69, 19, 550, 300, 10, 180)

'''Группы спрайтов'''
#название групп спрайтов
swirls = sprite.Group() #группа оружия (вихрь-оружие персонажа игры)
monsters = sprite.Group() #группа врагов
walls = sprite.Group() #группа стен
points = sprite.Group() #группа объектов для победы
cactus_s_ = sprite.Group() #группа не двигающихся объектов (враги)
#добавление объектов в свою группу
points.add(point_1)
points.add(point_2)
points.add(point_3)
monsters.add(enemy1)
monsters.add(enemy2)
monsters.add(enemy3)
monsters.add(enemy4)
cactus_s_.add(cactus_1)
cactus_s_.add(cactus_2)
cactus_s_.add(cactus_3)
walls.add(w1)
walls.add(w2)
walls.add(w3)
walls.add(w4)
walls.add(w5)
walls.add(w6)
walls.add(w7)
walls.add(w8)
walls.add(w9)
walls.add(w10)
walls.add(w11)
walls.add(w12)
walls.add(w13)
walls.add(w14)
walls.add(w15)
walls.add(w16)
walls.add(w17)
walls.add(w18)
walls.add(w19)
walls.add(w20)
#перед игровым цикло создаю переменную, которая будет хранить необходимые артифакты для выхода из лабиринта
hero_points = 0

'''Игровой цикл'''
game = True #условия начала действия 
finish = False #условия начала действия 
score = False 
while game: #активируем игру
    for e in event.get(): #активируем действия взаимодействия с игрой  
        if e.type == QUIT: #если действие равняется закрытию, то игра заканчивается
            game = False
        elif e.type == KEYDOWN: #если действие является нажатием клавиши вниз
            if e.key == K_SPACE: #в нашем случае, клавиша SPACE
                hero.fire()#герой стреляет
            elif e.key == K_TAB:
                hero.fire2()

    if finish != True: #если финиш не равняется "верно", то...
        window.blit(back, (0,0)) #отрисовываем задний фон
        hero.reset() #добавляем героя
        monsters.update() #двигаем монстров
        monsters.draw(window) #отрисовываем монстров
        fin.reset() #добавляем условие финиша
        points.draw(window) #отрисовка артифактов на игровом окне
        hero.update() #движение героя
        swirls.draw(window) #отрисовка оружия на игровом окне
        swirls.update() #подключение движения
        cactus_s_.draw(window) #отрисовка кактусов
        walls.draw(window) #отисовка стен в игровом окне
        sprite.groupcollide(swirls, walls, True, False) #запускаем взаимодействие меду нашим оружием и стенами, так, чтобы оружие исчезало при столкновении, а стена нет, поэтому сначала True (исчезновеине), а потом False (не исчезновение)
        sprite.groupcollide(swirls, monsters, True, True) #запускаем взаимодействие между нашим оружием и врагами, True/True значит с игры исчезае и оружие и враг
        sprite.groupcollide(swirls, cactus_s_, True, True)
        
        if score != True:
            finish = False
        if hero_points >= 3: #если победные баллы равняются 3
            score = True #то условие финиша выполняется
            
        if sprite.spritecollide(hero, walls, False): #ваимодействие героя и стены 
            finish = True #выпоняется условие проигрыша
            window.blit(lose, (200, 200)) #надпись оповещающая о проигрыше
        if sprite.spritecollide(hero, monsters, False): #взаимодействие героя и врагов
            finish = True #выполняется условие проигрыша
            window.blit(lose, (200, 200)) #надпись оповещающая о проигрыше
        if sprite.spritecollide(hero, cactus_s_, False): #взаимодействие героя и спрайтов кактуса
            finish = True #выполняется условие проигрыша
            window.blit(lose, (200, 200)) #надпись оповещающая о проигрыше
        if sprite.spritecollide(hero, points, True): #взаимодействие героя и артифактов (необходимых для набора баллов и прохождения игры)
            finish = False #условие финиша не выполняется
            hero_points += 1 #прибавляется балл в hero_points
        
        if sprite.collide_rect(hero, fin): #при выполнение условия, fin начинает работать и взаимодействие героя и финиша ведёт...
            finish = True #...к выполнению условия финиша
            window.blit(win, (200, 200)) #надпись оповещающая о победе
    
    display.update() #создание игрового окна, для прохождеия игры
    clock.tick(FPS) #настраиваем частоту кадров

        