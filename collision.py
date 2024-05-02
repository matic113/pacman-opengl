def is_colliding_rect(rect1, rect2):
    if hasattr(rect1, "rect"):
        rect1 = rect1.rect
    if hasattr(rect2, "rect"):
        rect2 = rect2.rect

    if rect1.right < rect2.left:
        return False
    if rect1.left > rect2.right:
        return False
    if rect1.bottom > rect2.top:
        return False
    if rect1.top < rect2.bottom:
        return False
    return True


def is_colliding_walls(player, walls):
    for wall in walls:
        if (
            player.rect.right > wall.rect.left
            and player.rect.left < wall.rect.right
            and player.rect.bottom < wall.rect.top
            and player.rect.top > wall.rect.bottom
        ):
            return True
    return False
