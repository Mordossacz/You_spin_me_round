# sources:
# https://en.wikipedia.org/wiki/Rotation_matrix
# https://www.obliczeniowo.com.pl/65

import pygame, sys
import numpy as np


def center_point(surface):
    x, y, z, ll = 0, 0, 0, len(surface)
    for i in surface:
        x, y, z = np.add((x, y, z), i)
    return x / ll, y / ll, z / ll

class Figure:
    def __init__(self, col):
        self.points = list()
        self.surfaces = ()
        self.col = col

    def sandglass(self, x, y, z):
        self.points += [(x, y, z)]
        self.points += [(x, y, z * -1)]
        self.points += [(0, 0, 0)]
        self.points += [(x * -1, y, z)]
        self.points += [(x * -1, y, z * -1)]
        self.points += [(x, -1 * y, z)]
        self.points += [(x, -1 * y, -1 * z)]
        self.points += [(-1 * x, -1 * y, z)]
        self.points += [(-1 * x, -1 * y, -1 * z)]

        self.surfaces = ((0, 2, 3, self.col),
                         (0, 1, 2, self.col),
                         (0, 3, 4, 1, self.col),
                         (4, 2, 1, self.col),
                         (4, 3, 2, self.col),
                         (5, 7, 2, self.col),
                         (5, 2, 6, self.col),
                         (5, 6, 8, 7, self.col),
                         (8, 6, 2, self.col),
                         (8, 2, 7, self.col))

    def pyramid(self, x, y, z):
        self.points += [(x, y, z)]
        self.points += [(x, y, z * -1)]
        self.points += [(0, -1 * y, 0)]
        self.points += [(x * -1, y, z)]
        self.points += [(x * -1, y, z * -1)]

        self.surfaces = ((0, 2, 3, self.col),
                         (0, 1, 2, self.col),
                         (0, 3, 4, 1, self.col),
                         (4, 2, 1, self.col),
                         (4, 3, 2, self.col))

    def cube(self, x, y, z):
        self.points +=[(x, y, z)]
        self.points +=[(x, y, z * -1)]
        self.points +=[(x, y * -1, z)]
        self.points +=[(x, y * -1, z * -1)]
        self.points +=[(x * -1, y, z)]
        self.points +=[(x * -1, y, z * -1)]
        self.points +=[(x * -1, y * -1, z)]
        self.points +=[(x * -1, y * -1, z * -1)]

        self.surfaces = ((0, 2, 6, 4, self.col),
                         (0, 1, 3, 2, self.col),
                         (0, 4, 5, 1, self.col),
                         (7, 6, 2, 3, self.col),
                         (7, 3, 1, 5, self.col),
                         (7, 5, 4, 6, self.col))

    # def center_point_self(self):
    #     x, y, z, ll = 0, 0, 0, len(self.points)
    #     for p in self.points:
    #         x, y, z = np.add((x, y, z), p)
    #     return x/ll, y/ll, z/ll

    def submit(self, new_points):
        self.points = new_points.copy()

    def rotate(self, angle):
        a, b, c = angle
        rot_points = list()
        for pos in self.points:
            rot_pos = np.dot(
    [[np.cos(a)*np.cos(b), np.cos(a)*np.sin(b)*np.sin(c) - np.sin(a)*np.cos(c), np.cos(a)*np.sin(b)*np.cos(c) + np.sin(a)*np.sin(c)],
    [np.sin(a)*np.cos(b), np.sin(a)*np.sin(b)*np.sin(c) + np.cos(a)*np.cos(c), np.sin(a)*np.sin(b)*np.cos(c) - np.cos(a)*np.sin(c)],
    [-1*np.sin(b), np.cos(b)*np.sin(c), np.cos(b)*np.cos(c)]]
                 ,
                 [[pos[0]], [pos[1]], [pos[2]]])
            rot_points.append(tuple(i[0] for i in rot_pos))
        return rot_points

    def move(self, vect):
        moved_points = list()
        for pos in self.points:
            moved_points.append(np.add(pos, vect))
        return moved_points



def spin_me_round(size=(100, 100, 100), figure='cube', color=(0, 160, 160),
                  pre_move=(0, 0, 0), pre_angle=(0, 0, 0), angle=(0, 0, 0)):
    pygame.init()
    angle = np.deg2rad(angle)
    xx, yy, zz = 500, 500, 500
    surface = pygame.display.set_mode((xx, yy), pygame.NOFRAME)
    clock = pygame.time.Clock()
    tick_time = 100
    speed = 0.001

    cube = Figure(color)
    if figure == 'cube':
        cube.cube(size[0], size[1], size[2])
    elif figure == 'pyramid':
        cube.pyramid(size[0], size[1], size[2])
    elif figure == 'sandglass':
        cube.sandglass(size[0], size[1], size[2])

    cube.submit(cube.move(pre_move))
    cube.submit(cube.rotate(np.deg2rad(pre_angle)))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    angle = (0, 0, 0)

                keys = pygame.key.get_pressed()
                if keys[pygame.K_m]:
                    move = (0, 0, 0)
                    if event.key == pygame.K_UP:
                        move = (10, 0, 0)
                    elif event.key == pygame.K_DOWN:
                        move = (-10, 0, 0)
                    elif event.key == pygame.K_RIGHT:
                        move = (0, 10, 0)
                    elif event.key == pygame.K_LEFT:
                        move = (0, -10, 0)
                    elif event.key == pygame.K_0:
                        move = (0, 0, 10)
                    elif event.key == pygame.K_9:
                        move = (0, 0, -10)
                    cube.submit(cube.move(move))
                elif event.key == pygame.K_UP:
                    angle = np.add(angle, (speed, 0, 0))
                elif event.key == pygame.K_DOWN:
                    angle = np.add(angle, (-1*speed, 0, 0))
                elif event.key == pygame.K_RIGHT:
                    angle = np.add(angle, (0, speed, 0))
                elif event.key == pygame.K_LEFT:
                    angle = np.add(angle, (0, -1*speed, 0))
                elif event.key == pygame.K_0:
                    angle = np.add(angle, (0, 0, speed))
                elif event.key == pygame.K_9:
                    angle = np.add(angle, (0, 0, -1*speed))

        cube.submit(cube.rotate(angle))
        surface_sorted = sorted(cube.surfaces,
                                key=lambda x: center_point([cube.points[i] for i in x[:-1]])[2])
        for surface_points in surface_sorted:
            vect1 = np.subtract(cube.points[surface_points[1]], cube.points[surface_points[0]])
            vect2 = np.subtract(cube.points[surface_points[2]], cube.points[surface_points[0]])
            perpendicular_vect = np.cross(vect1, vect2)  # it's perpandicular to surface_points

            dist_ratio = -1 * perpendicular_vect[0] / np.sqrt(perpendicular_vect[0]**2 +
                                                         perpendicular_vect[1]**2 +
                                                         perpendicular_vect[2]**2)
            color = (surface_points[-1][0]*dist_ratio/3 + surface_points[-1][0]*2/3,
                     surface_points[-1][1]*dist_ratio/3 + surface_points[-1][1]*2/3,
                     surface_points[-1][2]*dist_ratio/3 + surface_points[-1][2]*2/3)

            if perpendicular_vect[2] < 0: # checking if surface is facing towards us
                pos = [(cube.points[i][0:-1][0] + xx//2,
                        cube.points[i][0:-1][1] + yy//2) for i in surface_points[:-1]]

                pygame.draw.polygon(surface, color, pos)
                #pygame.draw.polygon(surface, (0, 0, 0), pos, width=3)  # with lines on edges

            # drawing center
            #pygame.draw.circle(surface, (255, 255, 255), (xx/2, yy/2), 4)

        # drawing vertices
        # for pos in cube.points:
        #     x = pos[0]+xx/2
        #     y = pos[1]+yy/2
        #     pygame.draw.circle(surface, (150, 150, 150), (x+2, y+2), 4)

        pygame.display.flip()
        surface.fill((0,0,0))
        clock.tick(tick_time)

#spin_me_round(size=(100, 100, 100),figure='sandglass', pre_angle=(0, 0, 0), angle=(0, 0.3, 0))