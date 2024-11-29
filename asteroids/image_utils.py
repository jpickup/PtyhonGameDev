import pygame

def rotate(image, pos, originPos, angle):
    '''
    Rotate the source image at point pos around the origin pos by the specied angle in degrees

    Returns the rotated image and its rect
    '''
    # offset from pivot to center
    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    
    # rotated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # rotated image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
    return (rotated_image, rotated_image_rect)

def mask(sprite):
    return pygame.mask.from_surface(sprite.image.convert_alpha())

def intersects(sprite1, sprite2):
    ''' check if the visible parts of the two sprites intersect with each other '''
    # If the rects don't collide then no point checking masks, which is much more expensive
    if not sprite1.rect.colliderect(sprite2.rect):
        return False
    else:
        offset = (
            sprite2.rect.left - sprite1.rect.left,
            sprite2.rect.top - sprite1.rect.top)
        mask1 = mask(sprite1)
        mask2 = mask(sprite2)
        return mask1.overlap(mask2, offset)