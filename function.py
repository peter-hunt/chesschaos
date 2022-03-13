from pygame.surface import Surface

__all__ = ['get_surface']


def get_surface(size, color=None):
    surface = Surface(size).convert_alpha()
    if color is not None:
        surface.fill(color)
    return surface
