import math
import random
import sys
from tkinter import *
from tkinter import messagebox
import pygame

pygame.init()
szerokosc = 1280
wysokosc = 720
fps = 60
tablica_kolorow = [(217, 91, 125), (15, 27, 64), (4, 140, 140), (242, 157, 53), (217, 56, 20)]
czarny = (0, 0, 0)
bialy = (255, 255, 255)
tablicaKropek = []
okno = pygame.display.set_mode((szerokosc, wysokosc))
czcionka = pygame.font.Font('freesansbold.ttf', 16)
pygame.display.set_caption("Agario By Hub")


def rysuj_okno(gracz, tablicaKropek, tablicaWrogow):
    okno.fill(bialy)
    pygame.draw.circle(okno, czarny, [gracz.x, gracz.y], int(gracz.wielkosc / 2 + 3))  # obwodka gracza
    pygame.draw.circle(okno, (37, 7, 255), [gracz.x, gracz.y], int(gracz.wielkosc / 2))  # gracz
    tekst = czcionka.render(str(gracz.punkty), True, bialy)
    tekstKwadrat = tekst.get_rect()
    tekstKwadrat.center = (gracz.x, gracz.y)
    okno.blit(tekst, tekstKwadrat)

    for wrog in tablicaWrogow:
        pygame.draw.circle(okno, czarny, [wrog.x, wrog.y], int(wrog.wielkosc / 2 + 3))  # obwodka wroga
        pygame.draw.circle(okno, wrog.kolor, [wrog.x, wrog.y], int(wrog.wielkosc / 2))  # wrog

    for kropka in tablicaKropek:
        kropka.rysujKropke()
    pygame.display.update()


def main():
    gracz = Gracz()
    wrog = Wrog()
    wrog1 = Wrog()
    wrog2 = Wrog()
    wrog3 = Wrog()
    wrog4 = Wrog()
    tablicaWrogow = [wrog, wrog1, wrog2,wrog3,wrog4]

    for i in range(0, 200):
        tablicaKropek.append(Kropka())

    czas = pygame.time.Clock()
    czyGrac = True

    while czyGrac:
        czas.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                czyGrac = False
        keys_pressed = pygame.key.get_pressed()
        gracz.ruch(keys_pressed)
        gracz.kolizjaKropki(tablicaKropek)
        gracz.kolizjaZwrogiem(tablicaWrogow)
        for wrog in tablicaWrogow:
            wrog.ruch()
            wrog.kolizjaKropki(tablicaKropek)
        rysuj_okno(gracz, tablicaKropek, tablicaWrogow)
    pygame.quit()


class Gracz:
    def __init__(self):
        self.wielkosc = 20
        self.x = 100
        self.y = 100
        self.predkosc = 5
        self.kolor = (0, 0, 0)
        self.punkty = 0

    def ruch(self, przycisk):
        if przycisk[pygame.K_a] and self.x > 20:
            self.x -= self.predkosc
        if przycisk[pygame.K_d] and self.x < szerokosc - 20:
            self.x += self.predkosc
        if przycisk[pygame.K_w] and self.y > 20:
            self.y -= self.predkosc
        if przycisk[pygame.K_s] and self.y < wysokosc - 20:
            self.y += self.predkosc

    def kolizjaKropki(self, kropki):
        for i in kropki:
            if liczOdleglosc((i.x, i.y), (self.x, self.y)) <= self.wielkosc / 2 and i.wielkosc < self.wielkosc:
                self.wielkosc += i.wielkosc / 6
                self.predkosc = self.predkosc * 0.998
                self.punkty += 1
                kropki.remove(i)
                tablicaKropek.append(Kropka())
                if self.punkty > 800:
                    koniecGry()

    def kolizjaZwrogiem(self, wrogowie):
        for i in wrogowie:
            if liczOdleglosc((i.x, i.y), (self.x, self.y)) <= self.wielkosc * 2 and i.wielkosc < self.wielkosc:
                self.wielkosc += i.wielkosc / 3
                self.predkosc = self.predkosc * 0.997
                self.punkty += int(i.wielkosc // 2)
                wrogowie.remove(i)
                if not wrogowie:
                    koniecGry()
            if liczOdleglosc((i.x, i.y), (self.x, self.y)) <= self.wielkosc / 2 and i.wielkosc > self.wielkosc:
                koniecGry()


def liczOdleglosc(a, b):
    x = math.fabs(a[0] - b[0])
    y = math.fabs(a[1] - b[1])
    return ((x ** 2) + (y ** 2)) ** 0.5


class Wrog:
    def __init__(self):
        self.wielkosc = random.randint(50, 100)
        self.x = random.randint(120, 1180)
        self.y = random.randint(120, 620)
        self.predkosc = 4
        self.kolor = (random.choice(tablica_kolorow))
        self.czas = pygame.time.get_ticks()
        self.przerwa = 1000
        self.wKtoraStroneX = True
        self.wKtoraStroneY = True

    def ruch(self):
        teraz = pygame.time.get_ticks()
        if teraz - self.czas >= self.przerwa:
            self.czas = teraz
            self.wKtoraStroneX = random.choice([True, False])
            self.wKtoraStroneY = random.choice([True, False])
        if self.wKtoraStroneX and self.x < szerokosc - 20:
            self.x += self.predkosc
        elif not self.wKtoraStroneX and self.x > 20:
            self.x -= self.predkosc
        if self.wKtoraStroneY and self.y < wysokosc - 20:
            self.y += self.predkosc
        elif not self.wKtoraStroneY and self.y > 20:
            self.y -= self.predkosc

    def kolizjaKropki(self, kropki):
        for i in kropki:
            if liczOdleglosc((i.x, i.y), (self.x, self.y)) <= self.wielkosc / 2 and i.wielkosc < self.wielkosc:
                self.wielkosc += i.wielkosc / 4
                self.predkosc = self.predkosc * 0.997
                kropki.remove(i)
                tablicaKropek.append(Kropka())


class Kropka:
    def __init__(self):
        self.wielkosc = random.randint(3, 5)
        self.x = random.randint(10, 1270)
        self.y = random.randint(10, 710)
        self.kolor = (random.choice(tablica_kolorow))

    def rysujKropke(self):
        pygame.draw.circle(okno, self.kolor, [self.x, self.y], self.wielkosc)


def koniecGry():
    Tk().wm_withdraw()
    messagebox.showinfo('Koniec Gry', 'OK')
    sys.exit()


if __name__ == "__main__":
    main()
