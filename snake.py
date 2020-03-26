#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# license: AGPL-3.0 
#
# autor: filhoweuler (https://github.com/filhoweuler)
# ajustes: bwb0de
#

import pygame, random

def on_grid_random():
    x = random.randint(0,59)
    y = random.randint(0,59)
    return (x * 10, y * 10)

def collision(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])

branco = 255,255,255
vermelho = 255,0,0

#Definição da janela do jogo e da taxa de frames inicial
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Snake - pyGame')
clock = pygame.time.Clock()
game_speed = 14

#Instâncias do jogo
class Snake:
    def __init__(self):
        self.corpo = [(200, 200), (210, 200), (220,200)]
        self.pele = pygame.Surface((10,10))
        self.pele.fill(branco)
        self.direction = "Descendo"

serpente = Snake()

class Food:
    def __init__(self):
        self.posicao = on_grid_random()
        self.pele = pygame.Surface((10,10))
        self.pele.fill(vermelho)

comida = Food()

#Outras variáveis globais
serpente.direction = "Descendo"
font = pygame.font.Font('freesansbold.ttf', 18)
score = 0
game_over = False
restart = False

while True:
    if not game_over:
        clock.tick(game_speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and serpente.direction != "Descendo":
                    serpente.direction = "Subindo"
                if event.key == pygame.K_DOWN and serpente.direction != "Subindo":
                    serpente.direction = "Descendo"
                if event.key == pygame.K_LEFT and serpente.direction != "para Direita":
                    serpente.direction = "para Esquerda"
                if event.key == pygame.K_RIGHT and serpente.direction != "para Esquerda":
                    serpente.direction = "para Direita"

        
        ### Regras de colisão
        if collision(serpente.corpo[0], comida.posicao):
            comida.posicao = on_grid_random()
            serpente.corpo.append((0,0))
            score = score + 1
            game_speed += 0.05
            
        # Verificando se a serpente colide com as bordas
        if serpente.corpo[0][0] == 600 or serpente.corpo[0][1] == 600 or serpente.corpo[0][0] < 0 or serpente.corpo[0][1] < 0:
            game_over = True
        
        # Verificando se a serpente colide com o próprio corpo
        for i in range(1, len(serpente.corpo) - 1):
            if serpente.corpo[0][0] == serpente.corpo[i][0] and serpente.corpo[0][1] == serpente.corpo[i][1]:
                game_over = True
        
        ### Atualizando o valor da posição da serpente
        for i in range(len(serpente.corpo) - 1, 0, -1):
            serpente.corpo[i] = (serpente.corpo[i-1][0], serpente.corpo[i-1][1])
            
        # Movendo a cabeça conforme direção da serpente.
        if serpente.direction == "Subindo":
            serpente.corpo[0] = (serpente.corpo[0][0], serpente.corpo[0][1] - 10)
        if serpente.direction == "Descendo":
            serpente.corpo[0] = (serpente.corpo[0][0], serpente.corpo[0][1] + 10)
        if serpente.direction == "para Direita":
            serpente.corpo[0] = (serpente.corpo[0][0] + 10, serpente.corpo[0][1])
        if serpente.direction == "para Esquerda":
            serpente.corpo[0] = (serpente.corpo[0][0] - 10, serpente.corpo[0][1])

       
        ### Limpa a tela para redesenhar os objetos
        screen.fill((0,0,0))
        
  
        ### Desenhando objetos 
        # Desenha a grade 
        for x in range(0, 600, 10):
            pygame.draw.line(screen, (20, 40, 40), (x, 0), (x, 600))
        for y in range(0, 600, 10):
            pygame.draw.line(screen, (20, 40, 40), (0, y), (600, y))
        
        # Atualiza a pontuação
        pygame.display.set_caption('Snake - pyGame - score: {}'.format(score))

        # Desenha a cobra e a maçã em suas respectivas posições
        screen.blit(comida.pele, comida.posicao)
        for pos in serpente.corpo:
            screen.blit(serpente.pele, pos)

        pygame.display.update()
    
    else:
        clock.tick(10)
        game_over_font = pygame.font.Font('freesansbold.ttf', 75)
        game_over_screen = game_over_font.render('Game Over', True, (255, 255, 255))
        restart_font = pygame.font.Font('freesansbold.ttf', 25)
        restart_screen = restart_font.render('Press F2 to restart game or ESC to quit', True, (0, 255, 0))
        game_over_rect = game_over_screen.get_rect()
        game_over_rect.midtop = (600 / 2, (600 / 2) - 100)
        restart_rect = restart_screen.get_rect() 
        restart_rect.midtop = (600 / 2, 20 + (600 / 2))
        screen.blit(game_over_screen, game_over_rect)
        screen.blit(restart_screen, restart_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F2:
                    restart = True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()


        if restart:
            game_over = False
            restart = False
            game_speed = 14
            serpente = Snake()
            comida = Food()
            score = 0
        
        pygame.display.update()