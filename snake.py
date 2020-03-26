#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# license: AGPL-3.0 
#
# autor: filhoweuler (https://github.com/filhoweuler)
# ajustes: bwb0de
#

import pygame, random

def on_grid_random():
    
    x = 0
    y = 0

    position = random.randint(0, 3)
    
    if position == 0:
        x = -1
        y = random.randint(0, altura_tela)
    
    elif position == 1:
        x = random.randint(0, largura_tela)
        y = -1
    
    elif position == 2:
        x = largura_tela + 1
        y = random.randint(0, altura_tela)

    elif position == 4:
        x = random.randint(0, largura_tela)
        y = altura_tela + 1

    return [x * escala, y * escala]

def collision(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])




branco = 255, 255, 255
vermelho = 255, 0, 0
vermelho_escuro = 200, 0, 0
verde = 0, 255, 0
cinza = 28, 28, 28
cinza_claro = 80, 80, 80
preto = 0, 0, 0
azul = 0, 0, 255
marrom = 222, 184, 135

#Variáveis globais de configuração do jogo
init_direction = "Descendo"
score = 0
init_game_speed = 15
escala = 15
largura_tela = 60
altura_tela = 60
cor_serpente = branco
color_mouse = cinza_claro
color_frog = verde
color_rabbit = marrom
color_grid = cinza
color_background = preto

#Definição da janela do jogo e da taxa de frames inicial
pygame.init()
largura = escala * largura_tela
altura = escala * altura_tela
screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()


#Instâncias do jogo
class Snake:
    def __init__(self):
        self.corpo = [(largura/2, altura/2), (largura/2+escala, altura/2), (largura/2+(2*escala), altura/2)]
        self.pele = pygame.Surface((escala,escala))
        self.pele.fill(cor_serpente)
        self.direction = init_direction
    
    def size_increment(self, size):
        n = size
        while n:
            serpente.corpo.append((-escala,-escala))
            global score, game_speed
            score += 1
            game_speed += 0.05
            n -= 1    

class Food:
    def __init__(self, cor):
        self.posicao = on_grid_random()
        self.pele = pygame.Surface((escala,escala))
        self.pele.fill(cor)
        self.time_count = 0
        self.time_to_move = random.randint (15, 75)
        self.moving = False
        self.movement_direction = False
        self.steps = 0
        self.min_steps = 5
        self.max_steps = 20
        self.step_size = escala * 1

    def move(self):
        if not self.moving:
            self.time_count += 1

        if self.time_count > self.time_to_move:
            self.time_count = 0
            self.time_to_move = random.randint (15, 85)
            self.moving = True
            self.check_movement_direction = True
            self.steps = random.randint (self.min_steps, self.max_steps)

        if self.moving:
            self.steps -= 1
            if self.check_movement_direction:
                if self.posicao[0] >= largura / 2 and self.posicao[1] >= altura / 2:
                    self.movement_direction = 'para direita e para cima'
                elif self.posicao[0] < largura / 2 and self.posicao[1] < altura / 2:
                    self.movement_direction = 'para esquerda e para baixo'
                elif self.posicao[0] < largura / 2 and self.posicao[1] >= altura / 2:
                    self.movement_direction = 'para esquerda e para cima'
                elif self.posicao[0] >= largura / 2 and self.posicao[1] < altura / 2:
                    self.movement_direction = 'para direita e para baixo'
            self.check_movement_direction = False

        
        if self.movement_direction == 'para direita e para baixo':
            step_direction = random.randint(0,1)
            if step_direction == 0:
                self.posicao[step_direction] -= self.step_size
            elif step_direction == 1:
                self.posicao[step_direction] += self.step_size
        
        elif self.movement_direction == 'para direita e para cima':
            step_direction = random.randint(0,1)
            self.posicao[step_direction] -= self.step_size

        elif self.movement_direction == 'para esquerda e para cima':
            step_direction = random.randint(0,1)
            if step_direction == 0:
                self.posicao[step_direction] += self.step_size
            elif step_direction == 1:
                self.posicao[step_direction] -= self.step_size
        
        elif self.movement_direction == 'para esquerda e para baixo':
            step_direction = random.randint(0,1)
            self.posicao[step_direction] += self.step_size

        if not self.steps:
            self.moving = False
            self.movement_direction = False


class Mouse(Food):
    def __init__(self, cor):
        super(Mouse, self).__init__(cor)

class Frog(Food):
    def __init__(self, cor):
        super(Frog, self).__init__(cor)
        self.step_size = escala * 5
        self.min_steps = 1
        self.max_steps = 2

class Rabbit(Food):
    def __init__(self, cor):
        super(Rabbit, self).__init__(cor)
        self.step_size = escala * 2
        self.min_steps = 6
        self.max_steps = 12
    

# Crinando instancias
serpente = Snake()
mouse = Mouse(color_mouse)
frog = Frog(color_frog)
rabbit = Rabbit(color_rabbit)

#Outras variáveis globais
font = pygame.font.Font('freesansbold.ttf', 18)
game_speed = init_game_speed
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
                elif event.key == pygame.K_DOWN and serpente.direction != "Subindo":
                    serpente.direction = "Descendo"
                elif event.key == pygame.K_LEFT and serpente.direction != "para Direita":
                    serpente.direction = "para Esquerda"
                elif event.key == pygame.K_RIGHT and serpente.direction != "para Esquerda":
                    serpente.direction = "para Direita"
                
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()


        
        ### Regras de colisão
        if collision(serpente.corpo[0], mouse.posicao):
            mouse.posicao = on_grid_random()
            serpente.size_increment(3)

        elif collision(serpente.corpo[0], frog.posicao):
            frog.posicao = on_grid_random()
            serpente.size_increment(1)

        elif collision(serpente.corpo[0], rabbit.posicao):
            rabbit.posicao = on_grid_random()
            serpente.size_increment(5)


        # Verificando tempo de reposicionamento da mouse especial
        frog.move()
        mouse.move()
        rabbit.move()

        # Verificando se a serpente colide com as bordas
        if serpente.corpo[0][0] == largura or serpente.corpo[0][1] == altura or serpente.corpo[0][0] < 0 or serpente.corpo[0][1] < 0:
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
            serpente.corpo[0] = (serpente.corpo[0][0], serpente.corpo[0][1] - escala)
        if serpente.direction == "Descendo":
            serpente.corpo[0] = (serpente.corpo[0][0], serpente.corpo[0][1] + escala)
        if serpente.direction == "para Direita":
            serpente.corpo[0] = (serpente.corpo[0][0] + escala, serpente.corpo[0][1])
        if serpente.direction == "para Esquerda":
            serpente.corpo[0] = (serpente.corpo[0][0] - escala, serpente.corpo[0][1])

       
        ### Limpa a tela para redesenhar os objetos
        screen.fill(color_background)
        
  
        ### Desenhando objetos 
        # Desenha a grade 
        for x in range(0, largura, escala):
            #pygame.draw.line(screen, color_grid, (x, 0), (x, largura))
            pygame.draw.line(screen, color_grid, (x, 0), (x, altura))
        for y in range(0, altura, escala):
            #pygame.draw.line(screen, color_grid, (0, y), (altura, y))
            pygame.draw.line(screen, color_grid, (0, y), (largura, y))
        
        # Atualiza a pontuação
        pygame.display.set_caption('Snake | score: {}'.format(score))

        # Desenha a cobra e a maçã em suas respectivas posições
        screen.blit(mouse.pele, mouse.posicao)
        screen.blit(frog.pele, frog.posicao)
        screen.blit(rabbit.pele, rabbit.posicao)
        for pos in serpente.corpo:
            screen.blit(serpente.pele, pos)

        pygame.display.update()
    
    else:
        ### Limpa a tela para redesenhar os objetos
        screen.fill(color_background)


        clock.tick(10)
        game_over_font = pygame.font.Font('freesansbold.ttf', largura // 10)
        game_over_screen = game_over_font.render('Fim de jogo!', True, verde)
        restart_font = pygame.font.Font('freesansbold.ttf', largura // 25)
        restart_screen = restart_font.render('F2 para recomeçar,  ESC para sair...', True, verde)
        game_over_rect = game_over_screen.get_rect()
        game_over_rect.midtop = (largura / 2, (altura / 2) - escala * 5)
        restart_rect = restart_screen.get_rect() 
        restart_rect.midtop = (largura / 2, escala * 2 + (altura / 2))
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
            game_speed = init_game_speed
            serpente = Snake()
            mouse = Mouse(color_mouse)
            frog = Frog(color_frog)
            rabbit = Rabbit(color_rabbit)
            score = 0
        
        pygame.display.update()