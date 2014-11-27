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

    def get_image_dict(self,img_names):
        dct={}
        for name in img_names:
            dct[name]=self.get_image(name)
        return dct

    def loadImage(self):
        self.imgDict = self.get_image_dict(["background-3.jpg",
                                           "background-2.jpg",
                                           "background.jpg",
                                           "point_black.png",
                                           "point_white.png",
                                           "block_white.png",
                                           "block_black.png",
                                           "black_hall.png",
                                           "point.png"])
        self.imgDict["background"]=pygame.transform.scale(self.imgDict["background-3.jpg"],
                                                             (WINDOW_WIDTH,
                                                              WINDOW_HEIGHT))
        self.imgDict["background-2"]=pygame.transform.scale(self.imgDict["background-2.jpg"],
                                                             (WINDOW_WIDTH,
                                                              WINDOW_HEIGHT))
        self.imgDict["background-load"]=pygame.transform.scale(self.imgDict["background.jpg"],
                                                             (WINDOW_WIDTH,
                                                              WINDOW_HEIGHT))

    def getTransformImgDict(self,fieldSize):
        pixelSize=int(WINDOW_HEIGHT*4/5/fieldSize)
        transformDict= {}
        transformDict["background"]=self.imgDict["background-2.jpg"]
        transformDict["block_white"]=pygame.transform.scale(self.imgDict["block_white.png"],
                                                              (pixelSize,pixelSize))
        transformDict["block_black"]=pygame.transform.scale(self.imgDict["block_black.png"],
                                                              (pixelSize,pixelSize))
        transformDict["point_white"]=pygame.transform.scale(self.imgDict["point_white.png"],
                                                           (pixelSize,pixelSize))
        transformDict["point_black"]=pygame.transform.scale(self.imgDict["point_black.png"],
                                                           (pixelSize,pixelSize))
        transformDict["black_hall"]=pygame.transform.scale(self.imgDict["black_hall.png"],
                                                           (pixelSize,pixelSize))
        transformDict["point"]=pygame.transform.scale(self.imgDict["point.png"],
                                                      (pixelSize,pixelSize))
        return transformDict



