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

def checkcollision(bb1, bb2, padding = 10):
    """
    ボックスにどれくらい重なりがあるかを確認する
    Calculate the Intersection over Union (IoU) of two bounding boxes.

    Parameters
    ----------
    bb1 : dict
        Keys: {'x1', 'x2', 'y1', 'y2'}
        The (x1, y1) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner
    bb2 : dict
        Keys: {'x1', 'x2', 'y1', 'y2'}
        The (x, y) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner

    Returns
    -------
    float
        in [0, 1]
    """

    bb1['x1'] += padding
    bb1['x2'] -= padding
    bb2['x1'] += padding
    bb2['x2'] -= padding
    bb1['y1'] += padding
    bb1['y2'] -= padding
    bb2['y1'] += padding
    bb2['y2'] -= padding

    assert bb1['x1'] < bb1['x2']
    assert bb1['y1'] < bb1['y2']
    assert bb2['x1'] < bb2['x2']
    assert bb2['y1'] < bb2['y2']

    # determine the coordinates of the intersection rectangle
    x_left = max(bb1['x1'], bb2['x1'])
    y_top = max(bb1['y1'], bb2['y1'])
    x_right = min(bb1['x2'], bb2['x2'])
    y_bottom = min(bb1['y2'], bb2['y2'])

    if x_right < x_left or y_bottom < y_top:
        return False
    else:
        return True