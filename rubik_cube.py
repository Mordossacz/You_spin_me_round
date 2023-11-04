import pygame, queue, random
import you_spin_me_round as spin
import numpy as np

def center_point_self(figures):
    x, y, z, ll = 0, 0, 0, 0
    for figure in figures:
        for p in figure.points:
            x, y, z = np.add((x, y, z), p)
            ll += 1
    return x / ll, y / ll, z / ll

class Rubik_cube:
    def __init__(self):
        self.figures = []
        self.a1, self.a2, self.a3 = np.deg2rad(90), np.deg2rad(180), np.deg2rad(360)
        self.angle_s = (0, 0, 0)
        self.rotation_speed = 0

    def add_angle(self, angle):
        self.angle_s = np.add(angle, self.angle_s)
        self.angle_s = self.angle_s[0] % self.a3, self.angle_s[1] % self.a3, self.angle_s[2] % self.a3

    def generate(self, size, ssize, gap):  # ssize - size of small cube wich is in color
        ssize /= 2
        a1, a2 = self.a1, self.a2
        self.size = size; self.ssize = ssize; self.gap = gap
        for x in range(3):  # orange (back)
            for y in range(3):
                self.figures.append(spin.Figure((255, 128, 0)))
                a = self.figures[-1]
                a.cube(ssize, ssize, 2)
                a.submit(a.move((0, 0, size/-2)))
                a.submit(a.move(((x-1) * size, (y-1) * size, -1 * size)))
        for x in range(3):  # red (front)
            for y in range(3):
                self.figures.append(spin.Figure((255, 0, 0)))
                a = self.figures[-1]
                a.cube(ssize, ssize, 2)
                a.submit(a.move((0, 0, size / 2)))
                a.submit(a.move(((x - 1) * size, (y - 1) * size, size)))
        for x in range(3):  # green (down)
            for z in range(3):
                self.figures.append(spin.Figure((0, 255, 0)))
                a = self.figures[-1]
                a.cube(ssize, ssize, 2)
                a.submit(a.rotate((0, 0, a1)))
                a.submit(a.move((0, size / 2, 0)))
                a.submit(a.move(((x - 1) * size, size, (z - 1) * size)))
        for x in range(3):  # blue (up)
            for z in range(3):
                self.figures.append(spin.Figure((0, 0, 255)))
                a = self.figures[-1]
                a.cube(ssize, ssize, 2)
                a.submit(a.rotate((0, 0, a1)))
                a.submit(a.move((0, size / -2, 0)))
                a.submit(a.move(((x - 1) * size, -1 * size, (z - 1) * size)))
        for z in range(3):  # yellow (right)
            for y in range(3):
                self.figures.append(spin.Figure((255, 255, 0)))
                a = self.figures[-1]
                a.cube(ssize, ssize, 2)
                a.submit(a.rotate((0, a1, 0)))
                a.submit(a.move((size / 2, 0, 0)))
                a.submit(a.move((size, (y - 1) * size, (z - 1) * size)))
        for z in range(3):  # white (left)
            for y in range(3):
                self.figures.append(spin.Figure((255, 255, 255)))
                a = self.figures[-1]
                a.cube(ssize, ssize, 2)
                a.submit(a.rotate((0, a1, 0)))
                a.submit(a.move((size / -2, 0, 0)))
                a.submit(a.move((-1 * size, (y - 1) * size, (z - 1) * size)))

        ssize = (size-gap)/2  # now it's size of black cube that builds rubik cube
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    self.figures.append(spin.Figure((5, 5, 5)))
                    a = self.figures[-1]
                    a.cube(ssize, ssize, ssize)
                    a.submit(a.move(((i - 1) * size, (j - 1) * size, (k-1) * size)))

    def rotate(self, angle):
        all_surfaces = []
        for fig in self.figures:
            points = fig.rotate(angle)
            for j in fig.surfaces:
                all_surfaces.append([points[x] for x in j[:-1]] + [j[-1]])
        return all_surfaces

    def change_fixed_direction(self):
        angle = np.multiply(np.round(np.divide(self.angle_s, self.a1)), self.a1)
        for fig in self.figures:
            fig.submit(fig.rotate(angle))

    def F(self, prim=1):
        for fig in self.figures:
            if fig.center_point_self()[2] > self.size/2 + self.gap:
                fig.submit(fig.rotate((prim * self.a1/self.rotation_speed, 0, 0)))

    def B(self, prim=1):
        for fig in self.figures:
            if fig.center_point_self()[2] < -1* (self.size / 2 + self.gap):
                fig.submit(fig.rotate((-1 * prim * self.a1 / self.rotation_speed, 0, 0)))

    def L(self, prim=1):
        for fig in self.figures:
            if fig.center_point_self()[0] < -1 * (self.size/2 + self.gap):
                fig.submit(fig.rotate((0, 0, -1 * prim * self.a1/self.rotation_speed)))

    def R(self, prim=1):
        for fig in self.figures:
            if fig.center_point_self()[0] > (self.size/2 + self.gap):
                fig.submit(fig.rotate((0, 0, prim * self.a1/self.rotation_speed)))

    def U(self, prim=1):
        for fig in self.figures:
            if fig.center_point_self()[1] < -1 * (self.size / 2 + self.gap):
                fig.submit(fig.rotate((0, -1 * prim * self.a1 / self.rotation_speed, 0)))

    def D(self, prim=1):
        for fig in self.figures:
            if fig.center_point_self()[1] > self.size/2 + self.gap:
                fig.submit(fig.rotate((0, prim * self.a1/self.rotation_speed, 0)))


def rubik_cube():
    pygame.init()
    #font = pygame.font.SysFont('arial.tff', 25)
    angle = (0, 0, 0)
    xx, yy, zz = 500, 500, 500
    screen = pygame.display.set_mode((xx, yy), pygame.NOFRAME)
    clock = pygame.time.Clock()
    tick_time = 100
    speed = 0.01  # speed change on click

    rcube = Rubik_cube()
    rcube.generate(70, 55, 4)

    rotation_key = queue.Queue()
    rotation_speed = 10
    rcube.rotation_speed = 10

    a = [rcube.F, rcube.B, rcube.L, rcube.R, rcube.U, rcube.D]; b = [-1, 1]
    for i in range(20):
        x, y = random.randint(0,5), random.randint(0,1)
        for j in range(rotation_speed): rotation_key.put((a[x], b[y]))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    angle = (0, 0, 0)
                if event.key == pygame.K_m:
                    rcube.change_fixed_direction()
                    rcube.angle_s = (0, 0, 0)
                    angle = (0, 0, 0)

                elif event.key == pygame.K_UP:
                    angle = np.add(angle, (0, 0, speed))
                elif event.key == pygame.K_DOWN:
                    angle = np.add(angle, (0, 0, -1*speed))
                elif event.key == pygame.K_RIGHT:
                    angle = np.add(angle, (0, speed, 0))
                elif event.key == pygame.K_LEFT:
                    angle = np.add(angle, (0, -1*speed, 0))
                elif event.key == pygame.K_0:
                    angle = np.add(angle, (speed, 0, 0))
                elif event.key == pygame.K_9:
                    angle = np.add(angle, (-1*speed, 0, 0))

                keys = pygame.key.get_pressed()
                prim = 1
                if keys[pygame.K_LSHIFT]: prim = -1

                if event.key == pygame.K_f:
                    for i in range(rotation_speed): rotation_key.put((rcube.F, prim))
                elif event.key == pygame.K_b:
                    for i in range(rotation_speed): rotation_key.put((rcube.B, prim))
                elif event.key == pygame.K_l:
                    for i in range(rotation_speed): rotation_key.put((rcube.L, prim))
                elif event.key == pygame.K_r:
                    for i in range(rotation_speed): rotation_key.put((rcube.R, prim))
                elif event.key == pygame.K_u:
                    for i in range(rotation_speed): rotation_key.put((rcube.U, prim))
                elif event.key == pygame.K_d:
                    for i in range(rotation_speed): rotation_key.put((rcube.D, prim))

        try:
            func = rotation_key.get(False)
            func[0](func[1])
        except queue.Empty:pass

        all_surfaces = rcube.rotate(rcube.angle_s)
        surface_sorted = sorted(all_surfaces,
                                key=lambda x: spin.center_point(x[:-1])[2])
        for surface_points in surface_sorted:
            vect1 = np.subtract(surface_points[1], surface_points[0])
            vect2 = np.subtract(surface_points[2], surface_points[0])
            perpendicular_vect = np.cross(vect1, vect2)  # it's perpandicular to surface_points

            dist_ratio = -1 * perpendicular_vect[0] / np.sqrt(perpendicular_vect[0]**2 +
                                                         perpendicular_vect[1]**2 +
                                                         perpendicular_vect[2]**2)
            color = (surface_points[-1][0] * dist_ratio / 3 + surface_points[-1][0] * 2 / 3,
                     surface_points[-1][1] * dist_ratio / 3 + surface_points[-1][1] * 2 / 3,
                     surface_points[-1][2] * dist_ratio / 3 + surface_points[-1][2] * 2 / 3)

            if perpendicular_vect[2] < 0: # checking if screen is facing towards us
                pos = [(i[0:-1][0] + xx//2,
                        i[0:-1][1] + yy//2) for i in surface_points[:-1]]

                pygame.draw.polygon(screen, color, pos)

        rcube.add_angle(angle)
        pygame.display.flip()
        screen.fill((40,40,40))
        clock.tick(tick_time)

rubik_cube()