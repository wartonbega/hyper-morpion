import pygame
import game
import terrain


pygame.init()
# prendre la resolution de l'ecran (pour plein ecran):
resolution = [pygame.display.Info().current_w, pygame.display.Info().current_h]

# creation de la fenetre
window = pygame.display.set_mode(size=(540, 540), flags=0)

# couleur de fond

# nom de la fenetre
pygame.display.set_caption("Simulation")

clock = pygame.time.Clock()

g = game.Game()

while True :

    window.fill((100, 100, 100))
    
    for event in pygame.event.get():
        # detection croix quitter :
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        
    g.actualiser(window)

    pygame.display.flip()

    clock.tick(30)  # 60 fps
