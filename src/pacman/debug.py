import pygame

pygame.init()
font = pygame.font.Font(None, 30)


def debug(info: object, position: tuple[int, int] = (10, 10)) -> None:
    """Display debug information on the screen."""

    display_surface = pygame.display.get_surface()
    debug_surface = font.render(str(info), True, "white")
    debug_rect = debug_surface.get_rect(topleft=position)
    pygame.draw.rect(display_surface, "black", debug_rect)
    display_surface.blit(debug_surface, debug_rect)
