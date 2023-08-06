import logging
import pytest
import uuid
from pygame.math import Vector2
import pygame
import random
import cv2
import math

from .base_render import BaseRender
from .env_render import EnvRender
from gobigger.utils import Colors, GRAY, BLACK, RED, YELLOW, GREEN, to_aliased_circle


class RealtimeRender(EnvRender):
    '''
    Overview:
        Used in real-time games, giving a global view
    '''
    def __init__(self, width, height, background=(255,255,255), padding=(0,0), cell_size=10, only_render=False):
        super(RealtimeRender, self).__init__(width, height, background=background, padding=padding, 
                                             cell_size=cell_size, only_render=only_render)

    def fill(self, server, direction=None, fps=0, last_time=0, player_num_per_team=3):
        self.screen.fill((0, 43, 54))

        # for x in range(0, self.width, self.cell_size):
        #     pygame.draw.line(self.screen, GRAY, (x, 0), (x, self.height))
        # for y in range(0, self.height, self.cell_size):
        #     pygame.draw.line(self.screen, GRAY, (0, y), (self.width, y))

        # Render all balls
        for ball in server.food_manager.get_balls():
            pygame.draw.circle(self.screen, (253, 246, 227), ball.position, ball.radius)
        for ball in server.thorns_manager.get_balls():
            pygame.draw.polygon(self.screen, (107, 194, 12), to_aliased_circle(ball.position, ball.radius))
        for ball in server.spore_manager.get_balls():
            pygame.draw.circle(self.screen, YELLOW, ball.position, ball.radius)
        for index, player in enumerate(server.player_manager.get_players()):
            for ball in player.get_balls():
                # pygame.draw.circle(self.screen, Colors[int(ball.team_name)][int(ball.owner)%player_num_per_team], ball.position, ball.radius)
                pygame.draw.circle(self.screen, Colors[int(ball.team_name)][0], ball.position, ball.radius)
                font_size = int(ball.radius/1.6)
                font = pygame.font.SysFont('arial', max(font_size, 4), True)
                txt = font.render('{}'.format(chr(int(ball.owner)%player_num_per_team+65)), True, (255,255,255))
                txt_rect = txt.get_rect(center=(ball.position.x, ball.position.y))
                self.screen.blit(txt, txt_rect)

        # for debug
        font= pygame.font.SysFont('Menlo', 15, True)

        team_name_size = {}
        for player in server.player_manager.get_players():
            if player.team_name not in team_name_size:
                team_name_size[player.team_name] = player.get_total_size()
            else:
                team_name_size[player.team_name] += player.get_total_size()
        team_name_size = sorted(team_name_size.items(), key=lambda d: d[1], reverse=True)
        for index, (team_name, team_size) in enumerate(team_name_size):
            pos_txt= font.render('{}: {:.5f}'.format(team_name, team_size), 1, RED)
            self.screen.blit(pos_txt, (20, 10+10*(index*2+1)))

        fps_txt = font.render(
            'fps: ' + str(fps), 1, RED)
        last_time_txt = font.render(
            'last_time: ' + str(last_time), 1, RED)
        self.screen.blit(fps_txt, (20, self.height_full - 30))
        self.screen.blit(last_time_txt, (20, self.height_full - 50))

    
    def show(self):
        pygame.display.update()
        self.fpsClock.tick(self.FPS)

    def close(self):
        pygame.quit()


class RealtimePartialRender(EnvRender):
    '''
    Overview:
        Used in real-time games to give the player a visible field of view. The corresponding player can be obtained by specifying the player name. The default is the first player
    '''
    def __init__(self, width, height, background=(255,255,255), padding=(0,0), cell_size=10, 
                 scale_up_ratio=1.5, vision_x_min=100, vision_y_min=100, player_name=None, only_render=False):
        super(RealtimePartialRender, self).__init__(width, height, background=background, padding=padding, 
                                                    cell_size=cell_size, scale_up_ratio=scale_up_ratio, 
                                                    vision_x_min=vision_x_min, vision_y_min=vision_y_min,
                                                    only_render=only_render)
        self.player_name = player_name

    def fill(self, server, direction=None, fps=0, last_time=0, player_num_per_team=3):
        if self.player_name is None:
            player = server.player_manager.get_players()[0]
        else:
            player = server.player_manager.get_player_by_name(self.player_name)
        rectangle = self.get_rectangle_by_player(player)

        screen = pygame.Surface((self.width, self.height))
        screen.fill((0, 43, 54))
        # for x in range(0, self.width, self.cell_size):
        #     pygame.draw.line(screen, GRAY, (x, 0), (x, self.height))
        # for y in range(0, self.height, self.cell_size):
        #     pygame.draw.line(screen, GRAY, (0, y), (self.width, y))

        for ball in server.food_manager.get_balls():
            pygame.draw.circle(screen, (253, 246, 227), ball.position, ball.radius)
        for ball in server.thorns_manager.get_balls():
            pygame.draw.polygon(screen, (107, 194, 12), to_aliased_circle(ball.position, ball.radius))
        for ball in server.spore_manager.get_balls():
            pygame.draw.circle(screen, YELLOW, ball.position, ball.radius)
        for index, player in enumerate(server.player_manager.get_players()):
            for ball in player.get_balls():
                # pygame.draw.circle(screen, Colors[int(ball.team_name)][int(ball.owner)%player_num_per_team], ball.position, ball.radius)
                pygame.draw.circle(screen, Colors[int(ball.team_name)][0], ball.position, ball.radius)
                font_size = int(ball.radius/1.6)
                font = pygame.font.SysFont('arial', max(font_size, 4), True)
                txt = font.render('{}'.format(chr(int(ball.owner)%player_num_per_team+65)), True, (255,255,255))
                txt_rect = txt.get_rect(center=(ball.position.x, ball.position.y))
                screen.blit(txt, txt_rect)

        screen_data = pygame.surfarray.array3d(screen)

        screen_data = self.get_clip_screen(screen_data, rectangle)
        player_surface = pygame.pixelcopy.make_surface(screen_data)
        screen_data = pygame.transform.scale(player_surface, (self.width, self.height))
        self.screen.blit(screen_data, (0, 0))

        # for debug
        font= pygame.font.SysFont('Menlo', 15, True)

        team_name_size = {}
        for player in server.player_manager.get_players():
            if player.team_name not in team_name_size:
                team_name_size[player.team_name] = player.get_total_size()
            else:
                team_name_size[player.team_name] += player.get_total_size()
        team_name_size = sorted(team_name_size.items(), key=lambda d: d[1], reverse=True)
        for index, (team_name, team_size) in enumerate(team_name_size):
            pos_txt= font.render('{}: {:.5f}'.format(team_name, team_size), 1, RED)
            self.screen.blit(pos_txt, (20, 10+10*(index*2+1)))

        fps_txt = font.render('fps: ' + str(fps), 1, RED)
        last_time_txt = font.render('last_time: ' + str(last_time), 1, RED)
        self.screen.blit(fps_txt, (20, self.height_full - 30))
        self.screen.blit(last_time_txt, (20, self.height_full - 50))
    
    def show(self):
        pygame.display.update()
        self.fpsClock.tick(self.FPS)

    def close(self):
        pygame.quit()
