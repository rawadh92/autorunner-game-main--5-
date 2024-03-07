import pygame
import sys
import random
import os
from player import Player
from obstacle import Obstacle, BlueObstacle
from bonus import Coin, BriseBrick
from player import Background
class GameParameters:
    def __init__(self):
        pygame.init()
        # Paramètres du jeu
        self.screen_sizes = [(800, 600), (1024, 768), (1920, 1080), pygame.display.Info().current_w, pygame.display.Info().current_h]
        self.current_screen_size_index = 0
        self.width_ratio = 1
        self.height_ratio = 1
        self.width, self.height = self.screen_sizes[self.current_screen_size_index]
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.fps_options = [60, 120, 144, 240]
        self.current_fps_index = 0
        self.FPS = self.fps_options[self.current_fps_index]
        self.volume = 0.5
        self.volume_step = 0.1
        self.game_over = False
        self.total_coin_count = 0  # Nombre total de pièces collectées par tous les joueurs
        self.player_coin_count = 0  # Nombre de pièces collectées par le joueur actuel
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()                                           # Faut changer le path pour que ça marche (pour vous)
        self.menu_sound = pygame.mixer.Sound(r'C:\Users\Hammo\Downloads\autorunner-game-main (3)\autorunner-game-main\subway_hagar\drillfr4.mp3')
        self.menu_background = pygame.image.load(os.path.join(r"C:\Users\Hammo\Downloads\autorunner-game-main (3)\autorunner-game-main\subway_hagar\images\menu_background.jpg")).convert()
        pygame_icon = pygame.image.load(r'C:\Users\Hammo\Downloads\autorunner-game-main (3)\autorunner-game-main\subway_hagar\images\icon.jpg')
        pygame.display.set_icon(pygame_icon)
        pygame.display.set_caption("Subway hagar")
        self.background = Background(r'C:\Users\Hammo\Downloads\autorunner-game-main (5)\autorunner-game-main\subway_hagar\images\moving_background.png', self.width, self.height)
        self.obstacle_image = pygame.image.load(r"C:\Users\Hammo\Downloads\autorunner-game-main (5)\autorunner-game-main\subway_hagar\images\buche.jpg")
        self.player_images = [pygame.image.load(r'C:\Users\Hammo\Downloads\autorunner-game-main (5)\autorunner-game-main\subway_hagar\sprite_image\Sanji.png'),
                              pygame.image.load(r'C:\Users\Hammo\Downloads\autorunner-game-main (5)\autorunner-game-main\subway_hagar\sprite_image\zoro.png'),
                              pygame.image.load(r'C:\Users\Hammo\Downloads\autorunner-game-main (5)\autorunner-game-main\subway_hagar\sprite_image\Mario.png'),
                              pygame.image.load(r'C:\Users\Hammo\Downloads\autorunner-game-main (5)\autorunner-game-main\subway_hagar\sprite_image\Luffy.png'),
                              pygame.image.load(r'C:\Users\Hammo\Downloads\autorunner-game-main (5)\autorunner-game-main\subway_hagar\sprite_image\dragon.png'),
                              pygame.image.load(r'C:\Users\Hammo\Downloads\autorunner-game-main (5)\autorunner-game-main\subway_hagar\sprite_image\crane.png'),
                              pygame.image.load(r'C:\Users\Hammo\Downloads\autorunner-game-main (5)\autorunner-game-main\subway_hagar\sprite_image\crane_skin.png'),
                              pygame.image.load(r'C:\Users\Hammo\Downloads\autorunner-game-main (5)\autorunner-game-main\subway_hagar\sprite_image\chien.png'),
                              pygame.image.load(r'C:\Users\Hammo\Downloads\autorunner-game-main (5)\autorunner-game-main\subway_hagar\sprite_image\ange.png')]
        #couleur
        self.white = (255, 255, 255)
        self.player_initial_x = self.width * 0.2
        self.player_initial_y = self.height * 0.8
        self.obstacle_initial_x = self.width
        self.obstacle_initial_y = self.height * 0.8
        self.player_images_resized = [pygame.transform.scale(image, (int(self.width * 0.1), int(self.height * 0.15))) for image in self.player_images]
        self.obstacle_image = pygame.transform.scale(self.obstacle_image, (int(self.width * 0.1), int(self.height * 0.1)))

        # Groupe de sprites
        self.all_sprites = pygame.sprite.Group()
        self.obstacles_group = pygame.sprite.Group()
        self.coins_group = pygame.sprite.Group()
        
        self.player = Player(200,100)
        self.player = Player(self.width // 2, self.height // 2)
        self.all_sprites.add(self.player)
        self.current_player_index = 0
        self.all_sprites.add(self.player)
        self.player_unlocked = [False] * (len(self.player_images) - 1)


        # Variables pour le score et les statistiques
        self.score = 0
        self.yellow_coins_collected = 0
        self.blue_coins_collected = 0
        self.blue_obstacles_destroyed = 0
        self.blue_coins_owned = 0  # Nombre de pièces bleues que le joueur possède
        self.font = pygame.font.Font(None, int(0.036 * self.width))  # Adapter la taille de la police

        self.all_sprites = pygame.sprite.Group()
        self.obstacles_group = pygame.sprite.Group()
        self.coins_group = pygame.sprite.Group()
    def increase_screen_size(self):
        self.current_screen_size_index = (self.current_screen_size_index + 1) % len(self.screen_sizes)
        self.width, self.height = self.screen_sizes[self.current_screen_size_index]
        self.screen = pygame.display.set_mode((self.width, self.height))

    def decrease_screen_size(self):     
        self.current_screen_size_index = (self.current_screen_size_index - 1) % len(self.screen_sizes)
        self.width, self.height = self.screen_sizes[self.current_screen_size_index]
        self.screen = pygame.display.set_mode((self.width, self.height))

    def increase_fps(self):
        self.current_fps_index = (self.current_fps_index + 1) % len(self.fps_options)
        self.FPS = self.fps_options[self.current_fps_index]

    def decrease_fps(self):
        self.current_fps_index = (self.current_fps_index - 1) % len(self.fps_options)
        self.FPS = self.fps_options[self.current_fps_index]

    def increase_volume(self):
        self.volume = min(1.0, self.volume + self.volume_step)

    def decrease_volume(self):
        self.volume = max(0.0, self.volume - self.volume_step)

    def create_obstacle(self):
        obstacle = Obstacle()
        self.all_sprites.add(obstacle)
        self.obstacles_group.add(obstacle)

    def create_blue_obstacle(self):
        blue_obstacle = BlueObstacle()
        self.all_sprites.add(blue_obstacle)
        self.obstacles_group.add(blue_obstacle)

    def create_coin(self):
        coin = Coin()
        self.all_sprites.add(coin)
        self.coins_group.add(coin)

    def create_brise_brick(self):
        brise_brick = BriseBrick()
        self.all_sprites.add(brise_brick)
        self.coins_group.add(brise_brick)

    def save_coin_count(self):
        self.coin_count += 1

    def start_game(self):
        pygame.init()
        
        
        while True:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            dt = self.clock.tick(self.FPS)



            # Gestion des collisions avec les obstacles
            obstacles_collected = pygame.sprite.spritecollide(self.player, self.obstacles_group, False)
            for obstacle in obstacles_collected:
                if isinstance(obstacle, BlueObstacle):
                    if self.blue_coins_owned > 0:
                        obstacle.reset()
                        self.blue_obstacles_destroyed += 1
                        self.score += 10
                        self.blue_coins_owned -= 1
                    else:
                        self.show_game_over_screen(self.score)
                else:
                    self.show_game_over_screen(self.score)

            # Gestion des collisions avec les pièces
            coins_collected = pygame.sprite.spritecollide(self.player, self.coins_group, True)
            for coin in coins_collected:
                if isinstance(coin, Coin):
                    self.yellow_coins_collected += 1
                    self.score += 10
                elif isinstance(coin, BriseBrick):
                    self.blue_coins_collected += 1
                    self.score += 100
                    self.blue_coins_owned += 1

            # Création d'obstacles
            if random.randint(0, 200) < 2:
                self.create_obstacle()

            # Création d'obstacles bleus
            if random.randint(0, 500) < 1:
                self.create_blue_obstacle()

            # Création de pièces
            if random.randint(0, 500) < 8:
                self.create_coin()

            # Création de pièces brise brick
            if random.randint(0, 500) < 2:
                self.create_brise_brick()

            # Augmentation de la difficulté
            if pygame.time.get_ticks() % 10000 == 0:
                for obstacle in self.obstacles_group:
                    obstacle.speed += 1

            # Dessin
            self.screen.blit(self.background.image, self.background.rect)
            self.all_sprites.draw(self.screen)


            # Affichage des statistiques en haut à droite
            score_text = self.font.render("Score: {}".format(self.score), True, (0, 0, 0))
            yellow_coins_text = self.font.render("Yellow Coins: {}".format(self.yellow_coins_collected), True, (0, 0, 0))
            blue_coins_text = self.font.render("Blue Coins: {}".format(self.blue_coins_collected), True, (0, 0, 0))
            blue_obstacles_text = self.font.render("Obstacles Destroyed: {}".format(self.blue_obstacles_destroyed), True, (0, 0, 0))
            blue_coins_owned_text = self.font.render("Blue Coins Owned: {}".format(self.blue_coins_owned), True, (0, 0, 0))

            self.screen.blit(score_text, (self.width - 150, 20))
            self.screen.blit(yellow_coins_text, (self.width - 220, 60))
            self.screen.blit(blue_coins_text, (self.width - 200, 100))
            self.screen.blit(blue_obstacles_text, (self.width - 270, 140))
            self.screen.blit(blue_coins_owned_text, (self.width - 250, 180))
            self.player.réagir(event_list)

            # Mise à jour des sprites
            self.all_sprites.update()
            self.player.updat(dt)
            self.player.draw(self.screen)
            pygame.display.flip()
            
            
            
            
    def show_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.blit(pygame.transform.scale(self.menu_background, (self.width, self.height)), (0, 0))
            font = pygame.font.Font(None, int(0.036 * self.width))  # Adapter la taille de la police
            pygame.mixer.Sound.play(self.menu_sound)

            title_text = font.render("Subway hagar", True, (255, 255, 255))
            self.screen.blit(title_text, (self.width/2 - title_text.get_width()/2, self.height * 0.1))

            play_text = font.render("Jouer", True, (255, 255, 255))
            play_rect = play_text.get_rect(center=(self.width/2, self.height * 0.3))
            self.screen.blit(play_text, play_rect)

            settings_text = font.render("Paramètres", True, (255, 255, 255))
            settings_rect = settings_text.get_rect(center=(self.width/2, self.height * 0.4))
            self.screen.blit(settings_text, settings_rect)

            characters_text = font.render("Personnages", True, (255, 255, 255))
            characters_rect = characters_text.get_rect(center=(self.width/2, self.height * 0.35))
            self.screen.blit(characters_text, characters_rect)

            quit_text = font.render("Quitter", True, (255, 0, 0))
            quit_rect = quit_text.get_rect(center=(self.width/2, self.height * 0.45))  # Ajustez la position verticale
            self.screen.blit(quit_text, quit_rect)  

            mx, my = pygame.mouse.get_pos()

            if play_rect.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0] == 1:
                    self.start_game()

            if settings_rect.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0] == 1:
                    self.show_settings()

            if characters_rect.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0] == 1:
                    self.choose_character()

            if quit_rect.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0] == 1:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()            
    def choose_character(self):
        font = pygame.font.Font(None, int(self.width * 0.045))
        mx, my = 0, 0
        arrow_left_text = font.render("<", True, (255, 255, 255))
        arrow_left_rect = arrow_left_text.get_rect(center=(self.width/2 - 100, self.height * 0.4))
        arrow_right_text = font.render(">", True, (255, 255, 255))
        arrow_right_rect = arrow_right_text.get_rect(center=(self.width/2 + 100, self.height * 0.4))
        back_text = font.render("Retour", True, (255, 255, 0))
        back_rect = back_text.get_rect(topleft=(self.width * 0.02, self.height * 0.02))
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if arrow_left_rect.collidepoint((mx, my)):
                        self.current_player_index = (self.current_player_index - 1) % len(self.player_images)
                        self.player.image = self.player_images[self.current_player_index]
                    elif arrow_right_rect.collidepoint((mx, my)):
                        self.current_player_index = (self.current_player_index + 1) % len(self.player_images)
                        self.player.image = self.player_images[self.current_player_index]
                    elif back_rect.collidepoint((mx, my)):
                        self.show_menu()

            self.screen.blit(self.menu_background, (0, 0))
            title_text = font.render("Choisir personnage", True, (255, 255, 255))
            self.screen.blit(title_text, (self.width/2 - title_text.get_width()/2, self.height * 0.15))
            current_player_image = self.player_images[self.current_player_index]
            self.screen.blit(current_player_image, (self.width/2 - current_player_image.get_width()/2, self.height * 0.4))
            self.screen.blit(arrow_left_text, arrow_left_rect)
            self.screen.blit(arrow_right_text, arrow_right_rect)
            self.screen.blit(back_text, back_rect)

            pygame.display.update()

    
    def show_game_over_screen(self, final_score):
        game_over = True

        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Afficher l'écran de game over
            self.screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 36)

            game_over_text = font.render("Game Over", True, (255, 0, 0))
            self.screen.blit(game_over_text, (self.width/2 - game_over_text.get_width()/2, 50))

            score_text = font.render("Score: {}".format(final_score), True, (255, 255, 255))
            self.screen.blit(score_text, (self.width/2 - score_text.get_width()/2, 150))

            recap_text = font.render("Récapitulatif", True, (255, 255, 255))
            self.screen.blit(recap_text, (self.width/2 - recap_text.get_width()/2, 200))

            

            # Affiche le récapitulatif 
            recap_y = 250
            recap_spacing = 30

            recap_lines = [
                "Yellow Coins Collected: {}".format(self.yellow_coins_collected),
                "Blue Coins Collected: {}".format(self.blue_coins_collected),
                "Blue Obstacles Destroyed: {}".format(self.blue_obstacles_destroyed),
                
            ]

            for line in recap_lines:
                line_text = font.render(line, True, (255, 255, 255))
                self.screen.blit(line_text, (self.width/2 - line_text.get_width()/2, recap_y))
                recap_y += recap_spacing

            restart_text = font.render("Rejouer", True, (0, 255, 0))
            restart_rect = restart_text.get_rect(center=(self.width/2 - 50, recap_y))
            self.screen.blit(restart_text, restart_rect)

            menu_text = font.render("Menu principal", True, (0, 0, 255))
            menu_rect = menu_text.get_rect(center=(self.width/2, recap_y + recap_spacing))  
            self.screen.blit(menu_text, menu_rect)

            quit_text = font.render("Quitter", True, (255, 0, 0))
            quit_rect = quit_text.get_rect(center=(self.width/2 + 50, recap_y))
            self.screen.blit(quit_text, quit_rect)

            mx, my = pygame.mouse.get_pos()

            if restart_rect.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0] == 1:
                    # Réinitialiser complètement le jeu
                    self.reset_game()
                    game_over = False

            if menu_rect.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0] == 1:
                    self.reset_game()
                    self.show_menu()

            if quit_rect.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0] == 1:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

    def reset_game(self):
        # Réinitialiser les paramètres du jeu à leurs valeurs initiales
        self.score = 0
        self.yellow_coins_collected = 0
        self.blue_coins_collected = 0
        self.blue_obstacles_destroyed = 0
        self.blue_coins_owned = 0
        # Réinitialiser d'autres paramètres selon les besoins (position du joueur, vitesse des obstacles, etc.)
        # ...

        # Réinitialiser les groupes de sprites
        self.all_sprites.empty()
        self.obstacles_group.empty()
        self.coins_group.empty()

        # Réinitialiser le joueur
        self.player = Player(200, 100)
        self.all_sprites.add(self.player)
        
        
    def show_settings(self):
        # Définir les variables pour la barre de volume
        volume_bar_length = 200
        volume_bar_height = 20
        volume_bar_x = (self.width - volume_bar_length) / 2
        volume_bar_y = 550
        pygame.mixer.music.load(r'C:\Users\Hammo\Downloads\autorunner-game-main (3)\autorunner-game-main\subway_hagar\drillfr4.mp3')  # Remplacez 'votre_fichier_audio.mp3' par le chemin de votre fichier audio
        pygame.mixer.music.play(-1)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    # Gestion des événements de clic
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()

                    # Gérer le choix des FPS en cliquant sur une case
                    for i, rect in enumerate(fps_rects):
                        if rect.collidepoint((mx, my)):
                            if i == 0:
                                self.FPS = 60
                            elif i == 1:
                                self.FPS = 120
                            elif i == 2:
                                self.FPS = 144
                            elif i == 3:
                                self.FPS = 240
                    
                    for i, rect in enumerate(size_rects):
                        if rect.collidepoint((mx, my)):
                            if i == 0:
                                self.width, self.height = 800, 600
                                self.screen = pygame.display.set_mode((self.width, self.height))
                            elif i == 1:
                                self.width, self.height = 1024, 768
                                self.screen = pygame.display.set_mode((self.width, self.height))
                            elif i == 2:
                                self.width, self.height = pygame.display.list_modes()[0]
                                self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)

                            # Réajuster les dimensions de l'image de fond pour remplir tout l'écran
                            self.menu_background = pygame.transform.scale(self.menu_background, (self.width, self.height))

                            # Recalculer la position de la barre de volume
                            volume_bar_x = (self.width - volume_bar_length) / 2
                            volume_bar_y = 550


                    # Gérer le choix de la taille 
                    # d'écran en cliquant sur une case
                    for i, rect in enumerate(size_rects):
                        if rect.collidepoint((mx, my)):
                            if i == 0:
                                self.width, self.height = 800, 600
                                self.screen = pygame.display.set_mode((self.width, self.height))
                            elif i == 1:
                                self.width, self.height = 1024, 768
                                self.screen = pygame.display.set_mode((self.width, self.height))
                            elif i == 2:
                                self.width, self.height = pygame.display.list_modes()[0]
                                self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)

            # Dessiner l'écran de paramètres
            self.screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 36)

            title_text = font.render("Paramètres", True, (255, 255, 255))
            self.screen.blit(title_text, (self.width/2 - title_text.get_width()/2, 100))
            
            # Bouton de retour
            return_text = font.render("Retour", True, (255, 255, 0))
            return_rect = return_text.get_rect(topleft=(20, 20))
            self.screen.blit(return_text, return_rect)

            mx, my = pygame.mouse.get_pos()

            if return_rect.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0] == 1:
                    return

            fps_text = font.render("FPS", True, (255, 255, 255))
            self.screen.blit(fps_text, (self.width/2 - 250, 200))

            fps_options = ["60", "120", "144", "240"]
            fps_rects = []

            for i, option in enumerate(fps_options):
                option_text = font.render(option, True, (255, 255, 255))
                option_rect = option_text.get_rect(center=(self.width/2 + (i - 1.5) * 100, 250))
                fps_rects.append(option_rect)
                self.screen.blit(option_text, option_rect)

            # Afficher les options pour la taille de l'écran sous forme de cases
            size_text = font.render("Taille de l'écran", True, (255, 255, 255))
            self.screen.blit(size_text, (self.width/2 - 320, 350))

            size_options = ["800x600", "1024x768", "Plein écran"]
            size_rects = []

            for i, option in enumerate(size_options):
                option_text = font.render(option, True, (255, 255, 255))
                option_rect = option_text.get_rect(center=(self.width/2 + (i - 1) * 200, 400))
                size_rects.append(option_rect)
                self.screen.blit(option_text, option_rect)

            # Barre de volume
            volume_bar_rect = pygame.Rect(volume_bar_x, volume_bar_y, volume_bar_length, volume_bar_height)
            pygame.draw.rect(self.screen, (255, 255, 255), volume_bar_rect)

            # Remplissage de la barre de volume en fonction du volume actuel
            volume_fill_length = int(volume_bar_length * self.volume)
            volume_fill_rect = pygame.Rect(volume_bar_x, volume_bar_y, volume_fill_length, volume_bar_height)
            pygame.draw.rect(self.screen, (0, 255, 0), volume_fill_rect)

            # Gérer le volume en cliquant et en faisant glisser la barre de volume
            # Gérer le volume en cliquant et en faisant glisser la barre de volume
            if pygame.mouse.get_pressed()[0]:
                mx, my = pygame.mouse.get_pos()
                if volume_bar_rect.collidepoint((mx, my)):
                    self.volume = max(0, min(1, (mx - volume_bar_x) / volume_bar_length))
                    # Mettre à jour le volume de tous les sons
                    pygame.mixer.music.set_volume(self.volume)
                    self.menu_sound.set_volume(self.volume)  # Assurez-vous d'ajuster le volume de tous les sons utilisés dans votre jeu



            pygame.display.update()
        
