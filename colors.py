def rgb_to_hsv(r, g, b):
    M = max(r, g, b)
    m = min(r, g, b)
    C = M - m
    
    if C == 0:
        H = 0
    elif M == r:
        H = (g - b)/C%6
    elif M == g:
        H = (b - r)/C + 2
    else:
        H = (r - g)/C + 4
    
    return 60*H, C/M, M


def hsv_to_rgb(h, s, v):
    C = v*s
    H = h/60
    X = C*(1 - abs(H%2 - 1))
    if 0 <= H < 1:
        r, g, b = C, X, 0
    elif 1 <= H < 2:
        r, g, b = X, C, 0
    elif 2 <= H < 3:
        r, g, b = 0, C, X
    elif 3 <= H < 4:
        r, g, b = 0, X, C
    elif 4 <= H < 5:
        r, g, b = X, 0, C
    else:
        r, g, b = C, 0, X

    m = v - C
    return r + m, g + m, b + m


def interpolate(a, b, p):
    return a + p*(b - a)

def rgb_interp(c0, c1, p):
    # H1, S1, V1 = rgb_to_hsv(c0[0], c0[1], c0[2])
    # H2, S2, V2 = rgb_to_hsv(c1[0], c1[1], c1[2])

    # H = interpolate(H1, H2, p)
    # S = interpolate(S1, S2, p)
    # V = interpolate(V1, V2, p)

    # return hsv_to_rgb(H, S, V)
    r1, g1, b1 = c0
    r2, g2, b2 = c1
    r = interpolate(r1, r2, p)
    g = interpolate(g1, g2, p)
    b = interpolate(b1, b2, p)
    return r, g, b

# I stole this color pallete from:
#http://www.pygame.org/project-Mandelbrot+Set+Viewer-698-.html
pallete = [
    (25, 7, 26), 
    (9, 1, 47),
    (4, 4, 73), 
    (0, 7, 100), 
    (12, 44, 138), 
    (24, 82, 177), 
    (57, 125, 209),
    (134, 181, 229), 
    (211, 236, 248),
    (241, 233, 191),
    (248, 201, 95),
    (255, 170, 0), 
    (204, 108, 0),
    (153, 87, 0),
    (106, 52, 3),
    (66, 30, 15), 
]

pallete = map(lambda c: map((255.0).__rdiv__, c),  pallete)    
    
