__author__ = 'Андрей'

import os, pygame
from pygame.locals import *
from Header import *



class ResManager:
    # При инициализации класса мы указываем где у нас что находится.
    def __init__(self,
                 data_dir = 'data',
                 image_dir = 'image',
                 sound_dir = 'sound',
                 music_dir = 'music'):
        # Это корневой каталог ресурсов
        self.data_dir = data_dir
        # Это каталог с изображениями
        self.image_dir = image_dir
        # Это каталог со звуками
        self.sound_dir = sound_dir
        # Это каталог с музыкой
        self.music_dir = music_dir

        self.imgDict ={}



    # Этот метод загружает файл по имени.
    def get_image(self, name):
        # Получаем имя нужного нам файла вместе с путями к нему.
        fullname = os.path.join(self.data_dir,
                                os.path.join(self.image_dir, name))

        try:
            # Пробуем загрузить изображение
            image = pygame.image.load(fullname)
        except pygame.error:
            # Если это не удалось сообщаем об этом и кидаем исключение
            # на выход, так как отсутствие нужно изображения,
            # критичная ошибка.
            print('Cannot load image: {0}'.format(name))

            raise SystemExit
        else:
            # Мы используем изображения с поддержкой альфа канала,
            # потому и конвертируем изображение в формат удобный pygame c
            # учетом этого самого альфа канала.
            image = image.convert_alpha()

            return image

    def loadImage(self):
        self.imgDict = self.get_image_dict(["background.jpg",
                                           "point_black.png",
                                           "point_white.png",
                                           "playing_field.png"])
        self.imgDict["background.jpg"]=pygame.transform.scale(self.imgDict["background.jpg"],
                                                         (WINDOW_WIDTH,
                                                          WINDOW_HEIGHT))
        self.imgDict["playing_field.png"]=pygame.transform.scale(self.imgDict["playing_field.png"],
                                                            (int(WINDOW_HEIGHT/5*4),
                                                             int(WINDOW_HEIGHT/5*4)))
        self.imgDict["point_white.png"]=pygame.transform.scale(self.imgDict["point_white.png"],
                                                          (int(WINDOW_HEIGHT/10),
                                                           int(WINDOW_HEIGHT/10)))
        self.imgDict["point_black.png"]=pygame.transform.scale(self.imgDict["point_black.png"],
                                                          (int(WINDOW_HEIGHT/10),
                                                           int(WINDOW_HEIGHT/10)))

    def get_image_dict(self,img_names):
        dct={}
        for name in img_names:
            dct[name]=self.get_image(name)
        return dct


