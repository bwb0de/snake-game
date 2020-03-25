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

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


#Definição da janela do jogo e da taxa de frames inicial
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Snake - pyGame')
clock = pygame.time.Clock()
game_speed = 14

#Instâncias do jogo
snake = [(200, 200), (210, 200), (220,200)]
snake_skin = pygame.Surface((10,10))
snake_skin.fill((255,255,255))

apple_pos = on_grid_random()
apple = pygame.Surface((10,10))
apple.fill((255,0,0))

#Outras variáveis globais
snake_direction = DOWN
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
                if event.key == pygame.K_UP and snake_direction != DOWN:
                    snake_direction = UP
                if event.key == pygame.K_DOWN and snake_direction != UP:
                    snake_direction = DOWN
                if event.key == pygame.K_LEFT and snake_direction != RIGHT:
                    snake_direction = LEFT
                if event.key == pygame.K_RIGHT and snake_direction != LEFT:
                    snake_direction = RIGHT

        
        ### Regras de colisão
        if collision(snake[0], apple_pos):
            apple_pos = on_grid_random()
            snake.append((0,0))
            score = score + 1
            game_speed += 0.05
            
        # Verificando se a serpente colide com as bordas
        if snake[0][0] == 600 or snake[0][1] == 600 or snake[0][0] < 0 or snake[0][1] < 0:
            game_over = True
        
        # Verificando se a serpente colide com o próprio corpo
        for i in range(1, len(snake) - 1):
            if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
                game_over = True
        
        ### Atualizando o valor da posição da serpente
        for i in range(len(snake) - 1, 0, -1):
            snake[i] = (snake[i-1][0], snake[i-1][1])
            
        # Movendo a cabeça conforme direção da serpente.
        if snake_direction == UP:
            snake[0] = (snake[0][0], snake[0][1] - 10)
        if snake_direction == DOWN:
            snake[0] = (snake[0][0], snake[0][1] + 10)
        if snake_direction == RIGHT:
            snake[0] = (snake[0][0] + 10, snake[0][1])
        if snake_direction == LEFT:
            snake[0] = (snake[0][0] - 10, snake[0][1])

       
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
        screen.blit(apple, apple_pos)
        for pos in snake:
            screen.blit(snake_skin, pos)

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
            snake = [(200, 200), (210, 200), (220,200)]
            snake_skin = pygame.Surface((10,10))
            snake_skin.fill((255,255,255))
            score = 0
        
        pygame.display.update()