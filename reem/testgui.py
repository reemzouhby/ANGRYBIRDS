""""  1- cree birds badi jibun mn ramset 2sun 7t 7ewelehun dwayra kermel nnatetha   done
2-badi 7t lbahkgroun    done
3-l3asa krmel fini a3ml mvt llm8ayta lezem 2som lsling la cha2ften donee
4-7t l3asfur donee
5-idro lmvt de 3asa  donne
6-trajectoire d'oiseau avec path avecstudy of mvt of birds  donne """

"""" 

7-zid slideare lmas loiseau +scrollbarw for terre espace,lune  donnee 
"""



import math
import time
import pygame
import pymunk as pm

import pygame_gui
from pymunk.vec2d import Vec2d

class Bird:
    def __init__(self, distance,angle,v, x, y, space,gg,mass,xmouse,slingx,k):
        self.life = 30
        radius = 12
        
        inertia = pm.moment_for_circle(mass, 0, radius, (0, 0))
        body = pm.Body(mass, inertia)
        body.position = x, y
        body.mass=mass


        fx = -k * v * math.cos(angle)
        fy=-gg*100*mass-k*v*math.sin(angle)
        
        f=math.sqrt(fx**2+fy**2)
        
       
         #representer vecteur v
        impulsion = f*Vec2d(1,0)
        if xmouse<slingx:
            impulsion = f*Vec2d(1,0)

        else:
            impulsion = f*Vec2d(-1,0)

       

        angle = -angle
        #appliquer cette force sur l'oiseau 
        body.apply_impulse_at_local_point(impulsion.rotated(angle))

        shape = pm.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 5 #frottement

        space.add(body, shape)
        self.body = body
        self.shape = shape



# Initialiser le programme
pygame.init()
window = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Angry Birds BYREEM")

# Ajouter des images
redbird = pygame.image.load("red-bird3.png").convert_alpha()
backgroundterre = pygame.image.load("background.png").convert_alpha()
backgroundespace = pygame.image.load("backgroundespace.jpg").convert_alpha()
backgroundlune = pygame.image.load("backgroundlune.jpg").convert_alpha()
sling = pygame.image.load("sling-3.png").convert_alpha()

clock = pygame.time.Clock()
running = True

# Physics
space = pm.Space()
space.gravity = (0.0, -980.0)

birds = []

mousedistance = 0
lcorde = 90
angle = 0
xmouse = 0
ymouse = 0

mouse_pressed = False
t1 = 0
ticktonextcircle = 10
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
slingx, slingy = 135, 450
sling2x, sling2y = 160, 450

bird_path = []

font1 = pygame.font.SysFont("arial", 30, bold=True)
font2 = pygame.font.SysFont("arial", 40, bold=True)
font3 = pygame.font.SysFont("arial", 50, bold=True)

# Static lines for physics
corpstatique = pm.Body(body_type=pm.Body.STATIC)
lignestatic = [pm.Segment(corpstatique, (0.0, 60.0), (1800.0, 60.0), 0.0)]

for line in lignestatic:
    line.elasticity = 0.95
    line.friction = 1

space.add(corpstatique)
for line in lignestatic:
    space.add(line)


def topygame(p):
    return int(p.x), int(-p.y + 600)


def vector(p0, p1):
    a = p1[0] - p0[0]
    b = p1[1] - p0[1]
    return (a, b)


def unitvector(v):
    h = ((v[0] ** 2) + (v[1] ** 2)) ** 0.5
    if h == 0:
        h = 0.0000000000000000000001
    ua = v[0] / h
    ub = v[1] / h
    return (ua, ub)


def distance(xo, yo, x, y):
    dx = x - xo
    dy = y - yo
    d = ((dx ** 2) + (dy ** 2)) ** 0.5
    return d


def slingaction():
    global mousedistance
    global cordelengh
    global angle
    global xmouse
    global ymouse
    global vx, vy

    v = vector((slingx, slingy), (xmouse, ymouse))
    uv = unitvector(v)
    uv1 = uv[0]
    uv2 = uv[1]
    mousedistance = distance(slingx, slingy, xmouse, ymouse)
    pu = (uv1 * lcorde + slingx, uv2 * lcorde + slingy)
    lmax = 102
    xredbird = xmouse - 20
    yredbird = ymouse - 20
    if mousedistance > lcorde: #akbar mn lcorde
        pux, puy = pu
        pux -= 15
        puy -= 15
        pul = pux, puy

        window.blit(redbird, pul)
        
        pu2 = (uv1 * lmax + slingx, uv2 * lmax  + slingy)
        pygame.draw.line(window, (0, 0, 0), (slingx, slingy), pu2, 5)
        window.blit(redbird, pul)
        pygame.draw.line(window, (0, 0, 0), (sling2x, sling2y), pu2, 5)
    else:
        mousedistance += 10
        pu3 = (uv1 * mousedistance + slingx, uv2 * mousedistance + slingy)
        pygame.draw.line(window, (0, 0, 0), (slingx, slingy), pu3, 5)
        window.blit(redbird, (xredbird, yredbird))
        pygame.draw.line(window, (0, 0, 0), (sling2x, sling2y), pu3, 5)

    dy = ymouse - slingy
    dx = xmouse - slingx
    if dx == 0:
        dx = 0.0000000000000000000000001
    angle = math.atan((float(dy)) / dx)


# Initialiser pygame_gui
manager = pygame_gui.UIManager((1000, 600))

# barre de  masse de l'oiseau
massslider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((800, 100), (150, 30)),
    start_value=10,
    value_range=(1,20),
    manager=manager
)
masslabel = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((800, 70), (150, 30)),
    text="Masse de l'oiseau",
    manager=manager
)
# barre de l'oiseau 
draglider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((800, 200), (150, 30)),
    start_value=0.01,
    value_range=(0.01,1.2),
    manager=manager
)
masslabel = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((800, 170), (150, 30)),
    text="drag coefficient",
    manager=manager
)


# liste de gravite
gravitydropdown = pygame_gui.elements.UIDropDownMenu(
    options_list=["Terre", "Espace", "Lune"],
    starting_option="Terre",
    relative_rect=pygame.Rect((800, 150), (150, 30)),
    manager=manager
)

while running:
    deltat = clock.tick(50) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
          #krmel mch kl 7arakt mouse 3 cheche te5dha 
        if (pygame.mouse.get_pressed()[0] and xmouse > 10 and
                xmouse < 250 and ymouse > 37 and ymouse < 550):
            mouse_pressed = True
        if (event.type == pygame.MOUSEBUTTONUP and
                event.button == 1 and mouse_pressed):
            mouse_pressed = False
            t1 = time.time() * 1000
            xo = 154
            yo = 156

            birds.clear()
            bird_path.clear()

            mass = massslider.get_current_value()
            k = draglider.get_current_value()
            # gravitee selon la choix de l'utilisateur 
            selectedgravity = gravitydropdown.selected_option
            g = 9.8
            dy = ymouse - slingy
            dx = xmouse - slingx
            vx, vy = dx / 10, dy / 10
            v = math.sqrt(vx ** 2 + vy ** 2)
            if selectedgravity == "Terre":
                space.gravity = (0, -980)
                g = 9.8

            elif selectedgravity == "Espace":
                space.gravity = (0, 0)
                g = 0

            elif selectedgravity == "Lune":
                space.gravity = (0, -162)
                g = 1.62

            if mousedistance > lcorde:
                mousedistance = lcorde
                if xmouse < slingx + 5: #3lchmel
                    bird = Bird(mousedistance, angle, v, xo, yo, space, mass, g,xmouse,slingx,k)
                    
                    birds.append(bird)
                else:#3llyamin
                    bird = Bird(-mousedistance, angle, v, xo, yo, space, mass, g,xmouse,slingx,k)
                    birds.append(bird)

        manager.process_events(event)


    xmouse, ymouse = pygame.mouse.get_pos()
    window.fill((130, 200, 100)) #color of screen without background
    window.blit(backgroundterre, (0, 80))
    #2em part of sling
    rect = pygame.Rect(50, 0, 70, 220)
    window.blit(sling, (138, 420), rect)
    for point in bird_path:
        pygame.draw.circle(window, WHITE, point, 5, 0) #trajectoire 

    if mouse_pressed:
        slingaction()
    else:
        if time.time() * 1000 - t1 > 300:
            window.blit(redbird, (130, 426))
        else:
            pygame.draw.line(window, (0, 0, 0), (slingx, slingy - 8),
                             (sling2x, sling2y - 7), 5)

    for bird in birds:
        p = topygame(bird.shape.body.position)
        x, y = p
        x -= 22
        y -= 20
        window.blit(redbird, (x, y))
        pygame.draw.circle(window, RED, p, int(bird.shape.radius), 2)
        bird_path.append(p)

    dt = 1 / 100
    space.step(dt)#ode by pyrhon qui effectue la trajectoire 

    rect = pygame.Rect(0, 0, 60, 200)
    window.blit(sling, (120, 420), rect)

    if mouse_pressed:
        dy = ymouse - slingy
        dx = xmouse - slingx
        vx, vy = dx / 10, dy / 10
        v = math.sqrt(vx ** 2 + vy ** 2)
        vitessetext = font1.render("vitesse initial: {:.2f}".format(v) + " m/s", True, (255, 255, 255))
        angletext = font3.render("Angle d'implusion: {:.2f}".format(math.degrees(angle)) + " degree", True,
                                  (255, 255, 255))
        window.blit(vitessetext, (10, 10))
        window.blit(angletext, (10, 50))

    manager.update(deltat)
    manager.draw_ui(window)

    pygame.display.flip()

pygame.quit()