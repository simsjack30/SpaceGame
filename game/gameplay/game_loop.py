import random
import sys
import pygame

from objects.player import Player
from objects.enemy import Enemy, LungeEnemy, WanderEnemy
from display.background import Background
from display import button

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption('Main Menu')
        pygame.font.init()
        self.hud_font = pygame.font.SysFont('Arial', 24)

        self.background_group = pygame.sprite.Group()
        self.background_group.add(Background((2280 / 2, 1720 / 2)))

        self.clock = pygame.time.Clock()
        self.world_width, self.world_height = 2280, 1720
        self.rounds = [[2,2,0],[3,3,2],[4,0,4],[8,8,0],[6,6,8]]
        self.current_round = 0
        self.bullets_group = pygame.sprite.Group()
        self.player = Player((self.world_width / 2, self.world_height / 2), self.bullets_group)
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.enemies_group = pygame.sprite.Group()
        self.start_button = button.Button(500, 400, pygame.image.load('assets/start_btn.png').convert_alpha())
        self.scene = 1
        self.game_over_message = ""

    def update_camera(self, player_rect, screen_width, screen_height, world_width, world_height):
        camera_x = player_rect.centerx - screen_width // 2
        camera_y = player_rect.centery - screen_height // 2
        camera_x = max(0, min(camera_x, world_width - screen_width))
        camera_y = max(0, min(camera_y, world_height - screen_height))
        return camera_x, camera_y

    def draw_hud(self, round_number, enemies_left):
        round_text_x = self.screen.get_width() - 220
        enemies_text_x = self.screen.get_width() - 220
        text_y = 10

        round_text = self.hud_font.render(f'Round: {round_number}', True, (255, 255, 255))
        enemies_text = self.hud_font.render(f'Enemies Left: {enemies_left}', True, (255, 255, 255))

        self.screen.blit(round_text, (round_text_x, text_y))
        self.screen.blit(enemies_text, (enemies_text_x, text_y + 30))

    def run(self):
        self.spawn_enemies(self.current_round)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill((0, 0, 0))

            if self.scene == 1:
                self.screen.fill((202, 228, 241))
                if self.start_button.draw(self.screen):
                    self.scene = 2

            elif self.scene == 2:
                self.player_group.update()
                self.enemies_group.update()
                self.bullets_group.update()
                if pygame.sprite.spritecollideany(self.player_group.sprite, self.enemies_group):
                    self.player_group.sprite.take_damage(10)
                collisions = pygame.sprite.groupcollide(self.bullets_group, self.enemies_group, True, False)
                for bullet, enemies in collisions.items():
                    for enemy in enemies:
                        enemy.take_damage(bullet.damage)
                camera_offset = self.update_camera(self.player_group.sprite.rect, 1280, 720, self.world_width, self.world_height)
                self.player_group.sprite.update_camera_offset(camera_offset)
                for group in [self.background_group, self.player_group, self.enemies_group, self.bullets_group]:
                    for sprite in group:
                        offset_pos = sprite.rect.topleft - pygame.math.Vector2(camera_offset)
                        self.screen.blit(sprite.image, offset_pos)
                self.player_group.sprite.draw_health_bar(self.screen)

                self.draw_hud(self.current_round + 1, len(self.enemies_group))

                pygame.display.update()
                self.clock.tick(60)
                if self.player_group.sprite.health <= 0:
                    self.scene = 3
                    self.game_over_message = "You Lost, Try Again"
                if self.check_round_completion():
                    self.current_round += 1
                    if self.current_round >= len(self.rounds):
                        self.scene = 3
                        self.game_over_message = "You Won! Congratulations!"
                    else:
                        self.reset_player_position(self.player_group.sprite, 1280, 720)
                        self.spawn_enemies(self.current_round)

            elif self.scene == 3:
                self.screen.fill((202, 228, 241))
                message_text = self.hud_font.render(self.game_over_message, True, (0, 0, 0))
                text_rect = message_text.get_rect(center=(1280 // 2, 720 // 2 - 50))
                self.screen.blit(message_text, text_rect)
                if self.start_button.draw(self.screen):
                    self.current_round = 0
                    self.player_group.sprite.health = self.player_group.sprite.max_health
                    self.enemies_group.empty()
                    self.bullets_group.empty()
                    self.spawn_enemies(self.current_round)
                    self.scene = 2

            pygame.display.update()

    def spawn_enemies(self, round_index):
        enemy_counts = self.rounds[round_index]
        for i in range(enemy_counts[0]):
            self.enemies_group.add(Enemy(self.random_spawn_position(), self.player, self.enemies_group))
        for i in range(enemy_counts[1]):
            self.enemies_group.add(LungeEnemy(self.random_spawn_position(), self.player, self.enemies_group))
        for i in range(enemy_counts[2]):
            self.enemies_group.add(WanderEnemy(self.random_spawn_position(), self.player, self.enemies_group))

    def random_spawn_position(self):
        if random.choice([True, False]):
            x = random.choice([-100, 1280 + 100])
            y = random.randint(0, 1720)
        else:
            x = random.randint(0, 1280)
            y = random.choice([-100, 1720 + 100])
        return x, y

    def check_round_completion(self):
        if not self.enemies_group:
            return True
        return False
    
    def reset_player_position(self, player, screen_width, screen_height):
        player.rect.center = (screen_width // 2, screen_height // 2)