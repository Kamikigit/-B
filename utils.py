import pygame

def show_health_bar(screen, value, max_value, position, color = (0, 128, 0), background_color = (204, 204, 204)):
    """
    体力バーを表示する
    引数:
        value: 現在の値
        max_value: バーのmaxの値
        position: 体力バーを表示する場所(x, y)
        color: 色 (R, G, B)
        background_color: 背景色 (R, G, B)
    """
    x, y = position

    pygame.draw.rect(screen, background_color, (x, y, max_value, 10))
    pygame.draw.rect(screen, color, (x, y, value, 10))

def show_magic_point(screen, value, max_value, position, radius = 10, space = 10, color = (0, 0, 255), background_color = (204, 204, 204)):
    """
    MPを表示する
    引数:
        value: 現在の値
        max_value: MPのmaxの値
        position: MPを表示する場所(x, y)
        radius: 表示する円の半径
        color: 色 (R, G, B)
        background_color: 背景色 (R, G, B)
    """
    x, y = position
    for i in range(max_value):
        pygame.draw.circle(screen, background_color, (x + ((radius * 2 + space) * i), y), radius)
    for i in range(value):
        pygame.draw.circle(screen, color, (x + ((radius * 2 + space) * i), y), radius)
