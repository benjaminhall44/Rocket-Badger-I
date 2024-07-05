import pygame,random,math
pygame.init()
screensize = [500,500]
BOUNCE = False
LOOP = False
STOP = True
BLACK_HOLE = False
DRAG = False
WARPED = False
WFACTOR = 1
AFACTOR = .02
screen = pygame.display.set_mode(screensize)
linefont = pygame.font.Font(None,30)
ROCKET = pygame.transform.scale(pygame.image.load("spaceship.png"),[32,32])
APPLE = pygame.transform.scale(pygame.image.load("apple.png"),[32,32])
def GetSign(num):
    if num > 0:
        return 1
    elif num < 0:
        return -1
    else:
        return 0

def AsymptoticCurve(r):
    return -1/(r+1) + 1

def animate():
    screen.fill([0,0,0])
    if WARPED:
        radius = ( (rocket_position[0] - (screensize[0] / 2)) ** 2 + (rocket_position[1] - (screensize[1] / 2)) ** 2 ) ** .5
        angle = math.asin((rocket_position[1] - (screensize[1] / 2)) / (.0001 + radius))
        wardedr = ((AsymptoticCurve(radius / screensize[0])) ** WFACTOR) * (screensize[0] / 2)
        wx = (screensize[0] / 2) + math.cos(angle) * wardedr * GetSign(rocket_position[0] - (screensize[0] / 2))
        wy = (screensize[1] / 2) + math.sin(angle) * wardedr
        screen.blit(ROCKET,[wx - 16,wy - 16])
        
        radius = ( (apple_position[0] - (screensize[0] / 2)) ** 2 + (apple_position[1] - (screensize[1] / 2)) ** 2 ) ** .5
        angle = math.asin((apple_position[1] - (screensize[1] / 2)) / (.0001 + radius))
        wardedr = ((AsymptoticCurve(radius / screensize[0])) ** WFACTOR) * (screensize[0] / 2)
        wx = (screensize[0] / 2) + math.cos(angle) * wardedr * GetSign(apple_position[0] - (screensize[0] / 2))
        wy = (screensize[1] / 2) + math.sin(angle) * wardedr
        screen.blit(APPLE,[wx - 16,wy - 16])
    else:
        screen.blit(ROCKET,[rocket_position[0] - 16,rocket_position[1] - 16])
        screen.blit(APPLE,[apple_position[0] - 16,apple_position[1] - 16])
    screen.blit(linefont.render(str(score),0,[255,255,0]),[10,10])
    pygame.display.flip()
rocket_position = [screensize[0] / 2,screensize[1] / 2]
apple_position = [random.randint(0,screensize[0]),random.randint(0,screensize[1])]
rocket_velocity = [0,0]
score = 0
Wdown = False
Sdown = False
Ddown = False
Adown = False
playing = True
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                Wdown = True
            elif event.key == pygame.K_s:
                Sdown = True
            elif event.key == pygame.K_d:
                Ddown = True
            elif event.key == pygame.K_a:
                Adown = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                Wdown = False
            elif event.key == pygame.K_s:
                Sdown = False
            elif event.key == pygame.K_d:
                Ddown = False
            elif event.key == pygame.K_a:
                Adown = False
    if (rocket_position[0] - apple_position[0]) ** 2 + (rocket_position[1] - apple_position[1]) ** 2 < 1024:
        score += 1
        apple_position = [random.randint(0,screensize[0]),random.randint(0,screensize[1])]
    if Wdown:
        rocket_velocity[1] -= AFACTOR
    if Sdown:
        rocket_velocity[1] += AFACTOR
    if Adown:
        rocket_velocity[0] -= AFACTOR
    if Ddown:
        rocket_velocity[0] += AFACTOR
    rocket_position[0] += rocket_velocity[0]
    rocket_position[1] += rocket_velocity[1]
    if STOP:
        if rocket_position[0] > screensize[0]:
            rocket_position[0] = screensize[0]
        elif rocket_position[0] < 0:
            rocket_position[0] = 0
        if rocket_position[1] > screensize[1]:
            rocket_position[1] = screensize[1]
        elif rocket_position[1] < 0:
            rocket_position[1] = 0
    if BOUNCE:
        if rocket_position[0] > screensize[0] or rocket_position[0] < 0:
            rocket_velocity[0] = -rocket_velocity[0]
            rocket_position[0] = screensize[0] - (rocket_position[0] % screensize[0])
        if rocket_position[1] > screensize[1] or rocket_position[1] < 0:
            rocket_velocity[1] = -rocket_velocity[1]
            rocket_position[1] = screensize[1] - (rocket_position[1] % screensize[1])
    if LOOP:
        if rocket_position[0] > screensize[0] or rocket_position[0] < 0:
            rocket_position[0] = rocket_position[0] % screensize[0]
        if rocket_position[1] > screensize[1] or rocket_position[1] < 0:
            rocket_position[1] = rocket_position[1] % screensize[1]
    if DRAG:
        rocket_velocity[0] *= .999
        rocket_velocity[1] *= .999
        if abs(rocket_velocity[0]) < .01:
            rocket_velocity[0] = 0
        if abs(rocket_velocity[1]) < .01:
            rocket_velocity[1] = 0
    if BLACK_HOLE:
        rocket_velocity[0] -= 500 *((rocket_position[0] - screensize[0] / 2)/((rocket_position[0] - screensize[0] / 2) ** 2 + (rocket_position[1] - screensize[1] / 2) ** 2) ** .5)/((rocket_position[0] - screensize[0] / 2) ** 2 + (rocket_position[1] - screensize[1] / 2) ** 2)
        rocket_velocity[1] -= 500*((rocket_position[1] - screensize[1] / 2)/((rocket_position[0] - screensize[0] / 2) ** 2 + (rocket_position[1] - screensize[1] / 2) ** 2) ** .5)/((rocket_position[0] - screensize[0] / 2) ** 2 + (rocket_position[1] - screensize[1] / 2) ** 2)
    animate()
    pygame.time.delay(10)

pygame.quit()
                
    
