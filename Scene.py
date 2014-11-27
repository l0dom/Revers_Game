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
        self.display.blit(self.manager.imgDict["background-load"],(0,0))


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

    def mouseEvent(self, mouseUp):
        mouse = pygame.mouse.get_pos()

        index = 0
        x = self.x
        y = self.y
        for item in self.menu:
            if self.index == index:
                if mouseIn(mouse, (x, y), (x+item['select'].get_rect().w,y+item['select'].get_rect().h)):
                    self.index = index
                    if mouseUp :
                        self.call()
                        break
                y += item['select'].get_rect().h
            else:
                if mouseIn(mouse, (x, y), (x+item['no select'].get_rect().w,y+item['no select'].get_rect().h)):
                    self.index = index
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
    def __init__(self, *argv):
        Scene.__init__(self, *argv)
        self.menu = Menu((5,5))

    def _event(self, event):
        if not self.is_end():
            self.menu.mouseEvent(event)
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
        self.display.blit(self.manager.imgDict["background"],(0,0))
        self.menu.draw(self.display)

class MainMenu(MenuScene):
    def __init__(self, *argv):
        MenuScene.__init__(self, *argv)

    def openNewGame(self):
        self.set_next_scene(SelectOpponent())
        self.the_end()

    def OpenOptions(self):
        self.set_next_scene(Dialog("it`s not work",MainMenu()))
        self.the_end()

    def OpenAbout(self):
        self.set_next_scene(Dialog("Made by Lodom",MainMenu()))
        self.the_end()

    def exit(self):
        self.set_next_scene(LoadScene())
        self.the_end()

    def _start(self):
        # Именно таким образом мы можем получить текст в pygame
        # В данном случае мы используем системный шрифт.
        font      = pygame.font.SysFont("Monospace", 30, bold=False, italic=False)
        font_bold = pygame.font.SysFont("Monospace", 40, bold=True, italic=False)
        item = "NewGame"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.openNewGame)
        item = "Options"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.OpenOptions)
        item = "About"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.OpenAbout)
        item = "Exit"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.exit)


class SelectOpponent(MenuScene):
    def back(self):
        self.set_next_scene(MainMenu())
        self.the_end()

    def versusPC(self):
        self.properties["player"]=playerPC
        self.set_next_scene(SelectGameType(self.properties))
        self.the_end()

    def oneComputer(self):
        self.properties["player"]=playerMan
        self.set_next_scene(SelectGameType(self.properties))
        self.the_end()

    def twoComputers(self):
        self.properties["player"]=playerOnline
        self.set_next_scene(SelectOnline(self.properties))
        self.the_end()

    def _start(self):
        self.properties = {}
        self.properties["online start"] = None
        self.properties["size"]=8
        # Именно таким образом мы можем получить текст в pygame
        # В данном случае мы используем системный шрифт.
        font      = pygame.font.SysFont("Monospace", 30, bold=False, italic=False)
        font_bold = pygame.font.SysFont("Monospace", 40, bold=True, italic=False)
        item = "back"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.back)
        item = "Versus PC"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.versusPC)
        item = "One Computer"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.oneComputer)
        item = "Two computers"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.twoComputers)
class SelectOnline(MenuScene):
    def __init__(self,properties):
        self.properties = properties
        self.menu = Menu((5,5))
    def back(self):
        self.set_next_scene(SelectOpponent())
        self.the_end()

    def openClient(self):
        self.properties["online start"] = startClient
        self.properties["game type"] = "revers"
        self.set_next_scene(SelectIP(self.properties))
        self.the_end()

    def openHost(self):
        self.properties["online start"] = startHost
        self.set_next_scene(SelectGameType(self.properties))
        self.the_end()

    def _start(self):
        # Именно таким образом мы можем получить текст в pygame
        # В данном случае мы используем системный шрифт.
        font      = pygame.font.SysFont("Monospace", 30, bold=False, italic=False)
        font_bold = pygame.font.SysFont("Monospace", 40, bold=True, italic=False)
        item = "back"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.back)
        item = "Client"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.openClient)
        item = "Host"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.openHost)
class SelectOptions(MenuScene):
    pass
class SelectGameType(MenuScene):
    def __init__(self,properties):
        self.properties = properties
        self.menu = Menu((5,5))
    def back(self):
        if self.properties["online start"] is None:
            self.set_next_scene(SelectOpponent())
        else:
            self.set_next_scene(SelectOnline(self.properties))
        self.the_end()
    def startRevers(self):
        self.properties["game type"]="revers"
        self.set_next_scene(SelectGameSize(self.properties))
        self.the_end()
    def startReversBH(self):
        self.properties["game type"]="reversBH"
        self.set_next_scene(SelectGameSize(self.properties))
        self.the_end()
    def _start(self):
        # Именно таким образом мы можем получить текст в pygame
        # В данном случае мы используем системный шрифт.
        font      = pygame.font.SysFont("Monospace", 30, bold=False, italic=False)
        font_bold = pygame.font.SysFont("Monospace", 40, bold=True, italic=False)
        item = "back"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.back)
        item = "Original Revers"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.startRevers)
        item = "Revers with Black Hall"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.startReversBH)

class SelectGameSize(MenuScene):
    def __init__(self,properties):
        self.properties = properties
        self.menu = Menu((5,5))
    def back(self):
        self.set_next_scene(SelectGameType(self.properties))
        self.the_end()
    def startFour(self):
        self.properties["size"]=4
        self.set_next_scene(GameScene(self.properties))
        self.the_end()
    def startSix(self):
        self.properties["size"]=6
        self.set_next_scene(GameScene(self.properties))
        self.the_end()
    def startEight(self):
        self.properties["size"]=8
        self.set_next_scene(GameScene(self.properties))
        self.the_end()
    def startTen(self):
        self.properties["size"]=10
        self.set_next_scene(GameScene(self.properties))
        self.the_end()


    def _start(self):
        # Именно таким образом мы можем получить текст в pygame
        # В данном случае мы используем системный шрифт.
        font      = pygame.font.SysFont("Monospace", 30, bold=False, italic=False)
        font_bold = pygame.font.SysFont("Monospace", 40, bold=True, italic=False)
        item = "back"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.back)
        item = "4x4"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.startFour)
        item = "6x6"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.startSix)
        item = "8x8"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.startEight)
        item = "10x10"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.startTen)

class SelectIP(MenuScene):
    pass

class Dialog(MenuScene):
    def __init__ (self,message,next_scene):
        self.set_next_scene(next_scene)
        self.message=message
        self.menu = Menu((5,5))


    def _start(self):
        # Именно таким образом мы можем получить текст в pygame
        # В данном случае мы используем системный шрифт.
        font      = pygame.font.SysFont("Monospace", 30, bold=False, italic=False)
        font_bold = pygame.font.SysFont("Monospace", 40, bold=True, italic=False)
        self.font=font_bold
        item = "ok"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.the_end)

    def _draw(self, dt):
        self.display.blit(self.manager.imgDict["background-2"],(0,0))
        self.menu.draw(self.display)
        self.display.blit(self.font.render(self.message,True,(0,0,0)),
                          (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))



#Games
class GameScene(Scene):
    def __init__(self, properties):
        self.prop = properties

    def _start(self):
        self.interface=Interface(self.display,self.manager.getTransformImgDict(self.prop["size"]),self.prop["size"])
        self.game = GameConstructor(interface=self.interface,
                                    size=self.prop["size"],
                                    gameType=self.prop["game type"],
                                    playerOne=playerMan,
                                    playerTwo=self.prop["player"],
                                    onlineStart=self.prop["online start"])

    def _event(self, event):
        self.game._event(event)
        if self.game.end:
            if self.prop["online start"]==startHost:
                self.game.server.close()
            self.set_next_scene(Dialog(self.game.message,MainMenu()))
            self.the_end()


    def _update(self, dt):
        self.game.update(dt)

    def _draw(self, dt):
        self.game.draw()




