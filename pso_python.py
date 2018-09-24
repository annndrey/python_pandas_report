from __future__ import division
import random
import math


# the function to optimize (minimize)
def rastriginfun(X):
    """
    Rastrigin function
    """
    n = len(X)
    return 10 * n + sum([((x)**2 - 10 * math.cos(2 * math.pi * (x))) for x in X])


class Particle:
    def __init__(self, x0, w, c1, c2):
        # particle position
        self.position_i = []
        # particle velocity
        self.velocity_i = []
        # best position individual
        self.pos_best_i = []
        # best error individual
        self.err_best_i = -1
        # error individual
        self.err_i = -1
        self.w = w
        self.c1 = c1
        self.c2 = c2

        for i in range(0, num_dimensions):
            self.velocity_i.append(random.uniform(-1, 1))
            self.position_i.append(x0[i])

    # evaluate current fitness
    def evaluate(self, costFunc):
        self.err_i = costFunc(self.position_i)

        # check to see if the current position is an individual best
        if self.err_i < self.err_best_i or self.err_best_i == -1:
            self.pos_best_i = self.position_i
            self.err_best_i = self.err_i

    # update new particle velocity
    def update_velocity(self, pos_best_g):
        # constant inertia weight (how much to weigh the previous velocity)
        w = self.w
        # cognative constant
        c1 = self.c1
        # social constant
        c2 = self.c2

        for i in range(0, num_dimensions):
            r1 = random.random()
            r2 = random.random()

            vel_cognitive = c1 * r1 * (self.pos_best_i[i] - self.position_i[i])
            vel_social = c2 * r2 * (pos_best_g[i] - self.position_i[i])
            self.velocity_i[i] = w * self.velocity_i[i] + \
                vel_cognitive + vel_social

    # update the particle position
    def update_position(self, bounds):
        for i in range(0, num_dimensions):
            self.position_i[i] = self.position_i[i] + self.velocity_i[i]

            # adjust maximum position
            if self.position_i[i] > bounds[1]:
                self.position_i[i] = bounds[1]

            # adjust minimum position
            if self.position_i[i] < bounds[0]:
                self.position_i[i] = bounds[0]


class PSO():
    def __init__(self, costFunc, x0, bounds, num_particles, maxiter, w, c1, c2):
        global num_dimensions

        num_dimensions = len(x0)
        # best error for group
        err_best_g = -1
        # best position for group
        pos_best_g = []

        # establish the swarm
        swarm = []
        for i in range(0, num_particles):
            swarm.append(Particle(x0, w, c1, c2))

        # begin optimization loop
        i = 0
        while i < maxiter:
            # print i,err_best_g
            # cycle through particles in swarm and evaluate fitness
            for j in range(0, num_particles):
                swarm[j].evaluate(costFunc)

                # determine if current particle is the best (globally)
                if swarm[j].err_i < err_best_g or err_best_g == -1:
                    pos_best_g = list(swarm[j].position_i)
                    err_best_g = float(swarm[j].err_i)

            # cycle through swarm and update velocities and position
            for j in range(0, num_particles):
                swarm[j].update_velocity(pos_best_g)
                swarm[j].update_position(bounds)
            i += 1

        # print final results
        print "PSO w={0}, c1={1}, c2={2}, best_err={3}".format(w, c1, c2, err_best_g, pos_best_g)


def RS(func, iterations, bounds, dimension):
    # initialize the "best found"
    best_f = 9999.0
    best_x = [None] * dimension

    for i in range(iterations):
        new_x = [random.uniform(bounds[0], bounds[1])
                 for d in xrange(dimension)]
        new_f = func(new_x)
        if new_f < best_f:
            best_f = new_f
            best_x = new_x

    print "RSO {0} iters, best_f={1}".format(iterations, best_f, best_x)


if __name__ == "__main__":
    # initial settings
    numparticles = 30
    numiterations = 1000
    dimension = 30
    bounds = [-5.12, 5.12]
    initial = [random.uniform(bounds[0], bounds[1]) for x in xrange(dimension)]

    params = [
        {"w": 0.729844, "c": 1.496180},
        {"w": 0.4, "c": 1.2},
        {"w": 1.0, "c": 2.0},
        {"w": -1.0, "c": 2.0}
    ]
    # repeat each experiment 5 times
    rep = 5
    for par in params:
        for r in xrange(5):
            print("*" * 40 + " Particle Swarm Optimization. REP %s. " %
                  r + "*" * 40)
            print(par)
            PSO(rastriginfun, initial, bounds, num_particles=numparticles,
                maxiter=numiterations, w=par['w'], c1=par['c'], c2=par['c'])
    for r in xrange(5):
        print("*" * 40 + " Random search. REP %s. " % r + "*" * 40)
        RS(rastriginfun, numiterations, bounds, dimension)
