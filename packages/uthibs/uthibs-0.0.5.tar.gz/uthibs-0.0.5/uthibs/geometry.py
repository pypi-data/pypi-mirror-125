# Making imports
import numpy as np

# Constant values 
ROUND = 8


def is_crossing(x1, y1, x2, y2, x3, y3, x4, y4):
    a1, b1 = get_a_b_2_pts(x1, y1, x2, y2)
    a2, b2 = get_a_b_2_pts(x3, y3, x4, y4)

    # Cas particuliers
    if a1 == a2:
        if b1 == b2:
            # print("Droites identiques")
            return False
        # print("Droites parallèles")
        return False

    # Cas général
    if (a1 == 'vert') & (a2 == 'vert'):
        # print('Vert both')
        return False
    elif a1 == 'vert':
        # print('Vert a1')
        x_inter = b1
        y_inter = a2 * x_inter + b2
        if ((y_inter - y1) * (y_inter - y2)) < 0:
            return True
        return False

    #    elif a2 == 'vert':
    #        # print('Vert a2')
    #        x_inter = b2
    #        y_inter = a1*x_inter+b1
    #        if ((y_inter - y1) * (y_inter - y2)) < 0:
    #            return True
    #        return False

    else:
        x_inter = (b2 - b1) / (a1 - a2)

    if ((x_inter - x1) * (x_inter - x2)) < 0 and (x_inter - x3) * (x_inter - x4) < 0:
        return True
    return False


def get_a_b_hauteur_pt(a_dr, b_dr, x1, y1):
    a = -1 / a_dr
    b = y1 - a * x1
    return np.round(a, ROUND), np.round(b, ROUND)


def get_a_b_bissectrice(x1, y1, x2, y2, x3, y3):
    x_m = (x1 + x2) / 2
    y_m = (y1 + y2) / 2
    a, b = get_a_b_2_pts(x_m, y_m, x3, y3)
    return np.round(a, ROUND), np.round(b, ROUND)


def get_a_b_2_pts(x1, y1, x2, y2):
    if x2 == x1:
        # print('Droite verticale')
        return 'vert', x1

    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1
    return np.round(a, ROUND), np.round(b, ROUND)
