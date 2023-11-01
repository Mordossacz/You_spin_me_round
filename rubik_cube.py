# zarzucone na razie

import pygame, sys, time
import you_spin_me_round as spin
import numpy as np

class Rubik_cube:
    def __init__(self):
        self.figures = {(i, j, k):[] for i in range(3) for j in range(3) for k in range(3)}
        self.a1, self.a2, self.a3 = np.deg2rad(90), np.deg2rad(180), np.deg2rad(360)
        self.angle_s = (0, 0, 0)

    def add_angle(self, angle):
        self.angle_s = np.add(angle, self.angle_s)
        self.angle_s = self.angle_s[0] % self.a3, self.angle_s[1] % self.a3, self.angle_s[2] % self.a3

    def generate(self, size, ssize, gap):  # ssize - size of small cube wich is in color
        ssize /= 2
        a1, a2 = self.a1, self.a2
        for x in range(3):  # orange (back)
            for y in range(3):
                self.figures[(x, y, 0)].append(spin.Figure((255, 128, 0)))
                a = self.figures[(x, y, 0)][-1]
                a.cube(ssize, ssize, 2)
                a.submit(a.move((0, 0, size/-2)))
                a.submit(a.move(((x-1) * size, (y-1) * size, -1 * size)))
        for x in range(3):  # red (front)
            for y in range(3):
                self.figures[(x, y, 2)].append(spin.Figure((255, 0, 0)))
                a = self.figures[(x, y, 2)][-1]
                a.cube(ssize, ssize, 2)
                a.submit(a.move((0, 0, size / 2)))
                a.submit(a.move(((x - 1) * size, (y - 1) * size, size)))
        for x in range(3):  # green (down)
            for z in range(3):
                self.figures[(x, 2, z)].append(spin.Figure((0, 255, 0)))
                a = self.figures[(x, 2, z)][-1]
                a.cube(ssize, ssize, 2)
                a.submit(a.rotate((0, 0, a1)))
                a.submit(a.move((0, size / 2, 0)))
                a.submit(a.move(((x - 1) * size, size, (z - 1) * size)))
        for x in range(3):  # blue (up)
            for z in range(3):
                self.figures[(x, 0, z)].append(spin.Figure((0, 0, 255)))
                a = self.figures[(x, 0, z)][-1]
                a.cube(ssize, ssize, 2)
                a.submit(a.rotate((0, 0, a1)))
                a.submit(a.move((0, size / -2, 0)))
                a.submit(a.move(((x - 1) * size, -1 * size, (z - 1) * size)))
        for z in range(3):  # yellow (right)
            for y in range(3):
                self.figures[(2, y, z)].append(spin.Figure((255, 255, 0)))
                a = self.figures[(2, y, z)][-1]
                a.cube(ssize, ssize, 2)
                a.submit(a.rotate((0, a1, 0)))
                a.submit(a.move((size / 2, 0, 0)))
                a.submit(a.move((size, (y - 1) * size, (z - 1) * size)))
        for z in range(3):  # white (left)
            for y in range(3):
                self.figures[(0, y, z)].append(spin.Figure((255, 255, 255)))
                a = self.figures[(0, y, z)][-1]
                a.cube(ssize, ssize, 2)
                a.submit(a.rotate((0, a1, 0)))
                a.submit(a.move((size / -2, 0, 0)))
                a.submit(a.move((-1 * size, (y - 1) * size, (z - 1) * size)))

        ssize = (size-gap)/2  # now it's size of black cube that builds rubik cube
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    self.figures[(i, j, k)].append(spin.Figure((5, 5, 5)))
                    a = self.figures[(i, j, k)][-1]
                    a.cube(ssize, ssize, ssize)
                    a.submit(a.move(((i - 1) * size, (j - 1) * size, (k-1) * size)))
        del self.figures[1, 1, 1]

    def center_point_self(self, figures):
        x, y, z, ll = 0, 0, 0, 0
        for figure in figures:
            for p in figure.points:
                x, y, z = np.add((x, y, z), p)
                ll += 1
        return x/ll, y/ll, z/ll

    def submit_rot(self, new):
        for i in new:
            self.figures[i] = new[i]

    def F(self, prim=False):
        new_points = {}
        for key, value in self.figures.items():
            if key[2] == 2:
                if key[0] == 0:
                    new_points[(2-key[1], 0, key[2])] = value
                if key[1] == 0:
                    new_points[(2, key[0], key[2])] = value
                if key[0] == 2:
                    new_points[(2-key[1], 2, key[2])] = value
                if key[1] == 2:
                    new_points[(0, key[0], key[2])] = value

                for fig in value:
                    fig.submit(fig.rotate((self.angle_s[0]*-1, self.angle_s[1]*-1, self.angle_s[2]*-1)))
                    fig.submit(fig.rotate((self.a1, 0, 0)))
                    fig.submit(fig.rotate((self.angle_s[0], self.angle_s[1], self.angle_s[2])))
        self.submit_rot(new_points)

    def B(self):
        pass

def rubik_cube():
    pygame.init()
    font = pygame.font.SysFont('arial.tff', 15)
    angle = (0, 0, 0)
    xx, yy, zz = 500, 500, 500
    screen = pygame.display.set_mode((xx, yy), pygame.NOFRAME)
    clock = pygame.time.Clock()
    tick_time = 100
    speed = 0.01  # speed change on click

    rcube = Rubik_cube()
    rcube.generate(70, 55, 4)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    angle = (0, 0, 0)
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

                elif event.key == pygame.K_f:
                    rcube.F()

        # for coordinates in rcube.figures.items():
        #     print(coordinates, '\n')
        for coordinates in sorted(rcube.figures.values(), key= lambda x: rcube.center_point_self(x)[2]):
            for cube in sorted(coordinates, key= lambda x: x.center_point_self()[2]):
                # drawing 1 figure
                cube.submit(cube.rotate(angle))
                surface_sorted = sorted(cube.surfaces,
                                        key=lambda x: cube.center_point([cube.points[i] for i in x])[2])
                for surface_points in surface_sorted:
                    vect1 = np.subtract(cube.points[surface_points[1]], cube.points[surface_points[0]])
                    vect2 = np.subtract(cube.points[surface_points[2]], cube.points[surface_points[0]])
                    perpendicular_vect = np.cross(vect1, vect2)  # it's perpandicular to surface_points

                    dist_ratio = -1 * perpendicular_vect[0] / np.sqrt(perpendicular_vect[0]**2 +
                                                                 perpendicular_vect[1]**2 +
                                                                 perpendicular_vect[2]**2)
                    color = (cube.col[0]*dist_ratio/3 + cube.col[0]*2/3,
                             cube.col[1]*dist_ratio/3 + cube.col[1]*2/3,
                             cube.col[2]*dist_ratio/3 + cube.col[2]*2/3)

                    if perpendicular_vect[2] < 0: # checking if screen is facing towards us
                        pos = [(cube.points[i][0:-1][0] + xx//2,
                                cube.points[i][0:-1][1] + yy//2) for i in surface_points]

                        pygame.draw.polygon(screen, color, pos)
                        #pygame.draw.polygon(screen, (0, 0, 0), pos, width=3)  # with lines on edges

                # pygame.display.flip()
                # print(x, cube.center_point_self())
                # time.sleep(1)

        # drawing center
        #pygame.draw.circle(screen, (255, 255, 255), (xx/2, yy/2), 4)

        rcube.add_angle(angle)
        print(rcube.angle_s)
        pygame.display.flip()
        screen.fill((40,40,40))
        clock.tick(tick_time)

rubik_cube()