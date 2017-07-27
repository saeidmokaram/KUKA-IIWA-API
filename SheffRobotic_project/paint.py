import pygame, random

def paint():
    #screen = pygame.display.set_mode((460,330),pygame.FULLSCREEN)
    screen = pygame.display.set_mode((460,380))
    screen_colour = (255, 255, 255)
    screen.fill(screen_colour)

    pygame.draw.rect(screen, (255, 0, 0),(0,330,230,50))
    pygame.draw.rect(screen, (0, 255, 0),(230,330,230,50))

    draw_on = False
    last_pos = (0, 0)
    pen_color = (0, 0, 0)
    radius = 5

    def roundline(srf, color, start, end, radius=1):
        dx = end[0]-start[0]
        dy = end[1]-start[1]
        distance = max(abs(dx), abs(dy))
        for i in range(distance):
            x = int( start[0]+float(i)/distance*dx)
            y = int( start[1]+float(i)/distance*dy)
            pygame.draw.circle(srf, color, (x, y), radius)

    lines = []
    line = []
    drowing = True
    try:
        while drowing:
            e = pygame.event.wait()
            if e.type == pygame.QUIT:
                raise StopIteration
            if e.type == pygame.MOUSEBUTTONDOWN:
                #color = (random.randrange(256), random.randrange(256), random.randrange(256))
                pygame.draw.circle(screen, pen_color, e.pos, radius)

                if 0<=e.pos[0] and e.pos[0]<=230 and 330<=e.pos[1] and e.pos[1]<=380:
                    screen.fill(screen_colour)
                    pygame.draw.rect(screen, (255, 0, 0), (0, 330, 230, 50))
                    pygame.draw.rect(screen, (0, 255, 0), (230, 330, 230, 50))
                    lines = []
                    line = []
                elif 230<=e.pos[0] and e.pos[0]<=460 and 330<=e.pos[1] and e.pos[1]<=380:
                    drowing = False
                    break
                else:
                    draw_on = True

            if e.type == pygame.MOUSEBUTTONUP:
                draw_on = False
                if len(line):
                    lines.append(line)
                line = []

            if e.type == pygame.MOUSEMOTION:
                if draw_on:
                    pygame.draw.circle(screen, pen_color, e.pos, radius)
                    roundline(screen, pen_color, e.pos, last_pos, radius)
                last_pos = e.pos
                if draw_on:
                    (x,y) = e.pos
                    if len(line):
                        if line[-1][0]>x+3 or line[-1][1]>y+3:
                            line.append([y+420, x-230])
                    else:
                        line.append([y + 420, x - 230])

            pygame.display.flip()

        return lines

    except StopIteration:
        print 'painting ERROR!'


#print paint()