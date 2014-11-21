__author__ = 'Андрей'

import pygame
from Header import *
from Interface import Interface
from GameConstructor import *




class Scene:
    '''Abstract class'''
    def __init__(self, next_scene = None):
        self.__next_scene = next_scene

    def loop(self, dt):
        self.__event(pygame.event)
        self._update(dt)
        self._draw(dt)

    def start(self, display, manager):
        self.display = display
        self.manager = manager
        self._start()
        self.__end = False

    # Эту функцию стоит определит в потомке если в
    # сцене нужно что-то создать, например наш логотип.
    def _start(self):
        pass

    # Эта функция которая не должна вызываться вне этого класса,
    # ну и вы конечно поняли зачем нужно __.
    def __event(self, event):
        if len(event.get(pygame.QUIT)) > 0:
            self.__end = True
            self.set_next_scene(None)
            return

        self._event(event)

        # event.get() эквивалентен pygame.event.get()
        # передавая параметр в get мы говорим что именно
        # нас интересует из событий.
        for e in event.get(END_SCENE):
            if e.type == END_SCENE:
                self.__end = True

    # Эту функцию придется переопределить в потомке
    def _draw(self, dt):
        pass

    # и эту тоже
    def _event(self, event):
        pass

    # как и эту.
    def _update(self, dt):
        pass

    def next(self):
        return self.__next_scene

    def is_end(self):
        return self.__end

    def the_end(self):
        pygame.event.post(pygame.event.Event(END_SCENE))

    def set_next_scene(self, scene):
        self.__next_scene = scene

#Класс сцена загрузки
class LoadScene(Scene):
    def __init__(self, time = 500, *argv):
        Scene.__init__(self, *argv)
        self.run = 0
        self.time = time

    def _start(self):
        self.manager.loadImage()

    def _event(self, event):
        for e in event.get():
            if e.type == pygame.KEYDOWN:
                self.the_end()
        if pygame.mouse.get_pressed()[0]:
            self.the_end()


        if self.run>self.time:
            self.the_end()


    def _update(self, dt):
        self.run+=dt;

    def _draw(self, dt):
        self.display.blit(self.manager.imgDict["background.jpg"],(0,0))


#Класс эллементов меню
class Menu:
    def __init__(self, position = (0,0), loop = True):
        self.index = 0
        self.x = position[0]
        self.y = position[1]
        self.menu = list()
        self.click =False

    # Метод перемещающий нас в низ циклично по всем элементам.
    def down(self):
        self.index += 1
        if self.index >= len(self.menu):
            self.index = 0

    # Тоже самое но в вверх.
    def up(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.menu)-1

    def mouseEvent(self,mouseUp=False):
        mouse = pygame.mouse.get_pos()

        index = 0
        x = self.x
        y = self.y
        for item in self.menu:
            if self.index == index:
                if mouseIn(mouse, (x, y), (x+item['select'].get_rect().w,x+item['select'].get_rect().h)):
                    self.index = index
                    if mouseUp :
                        self.call()
                        print("a")
                y += item['select'].get_rect().h
            else:
                if mouseIn(mouse, (x, y), (x+item['select'].get_rect().w,y+item['select'].get_rect().h)):
                    self.index = index
                    if mouseUp :
                        self.call()
                        print("b")
                y += item['no select'].get_rect().h
            index += 1


    # Добавляет новый элемент, нужно передать 2 изображения.
    # На 1 не выбранный вид элемента.
    # На 2 выбранный элемент
    def add_menu_item(self, no_select, select, func):
        self.menu.append({ 'no select' : no_select,
                           'select' : select,
                           'func' : func })

    def call(self):
        self.menu[self.index]['func']()

    def draw(self, display):
        index = 0
        x = self.x
        y = self.y
        for item in self.menu:
            if self.index == index:
                display.blit(item['select'], (x, y))
                y += item['select'].get_rect().h
            else:
                display.blit(item['no select'], (x, y))
                y += item['no select'].get_rect().h
            index += 1

#Класс меню
class MenuScene(Scene):
    def item_call(self):
        print("item_call")
        self.the_end()

    def newGame(self):
        self.the_end()

    def NewGamePvP(self):
        self.set_next_scene(GameScene())
        self.the_end()

    def exit(self):
        self.set_next_scene(LoadScene(1500,None))
        self.the_end()

    def _start(self):
        self.menu = Menu((self.display.get_rect().w/20,
                          self.display.get_rect().h/20))

        # Именно таким образом мы можем получить текст в pygame
        # В данном случае мы используем системный шрифт.
        font      = pygame.font.SysFont("Monospace", 40, bold=False, italic=False)
        font_bold = pygame.font.SysFont("Monospace", 50, bold=True, italic=False)
        item = "Один игрок"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.newGame)
        item = "Два игрока"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.NewGamePvP)
        item = "Сетевая игра"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.item_call)
        item = "Настройки"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.item_call)
        item = "Как играть"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.item_call)
        item = "Выход"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.exit)

    def _event(self, event):
        self.menu.mouseEvent()
        for e in event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN:
                    self.menu.down()
                elif e.key == pygame.K_UP:
                    self.menu.up()
                elif e.key == pygame.K_RETURN:
                    self.menu.call()
            if e.type == pygame.MOUSEBUTTONUP:
                self.menu.mouseEvent(True)

    def _draw(self, dt):
        self.display.fill((255,255,255))
        self.manager.imgDict["background.jpg"],(0,0)
        self.menu.draw(self.display)

class GameScene(Scene):

    def _start(self):
        self.size = 4
        self.interface=Interface(self.display,self.manager.getTransformImgDict(self.size),self.size)
        self.game = GameConstructor(self.size,reversGVP,reversDescend,reversStart)

    def _event(self, event):
        for e in event.get():
            if e.type == pygame.MOUSEBUTTONUP:
                pair =  self.interface.event()
                if pair[0]!=-1:
                    self.game._descend(pair[0],pair[1])


    def _draw(self, dt):
        self.interface.draw(self.game.field,self.game.validPath)

