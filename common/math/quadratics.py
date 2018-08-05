import math

class Quadratic(object):
    '''
    Instantiate the class with a set contaning the A, B, C values of the quadratic equation.
    '''
    def __init__(self, quadratic_set):
        self.a = quadratic_set[0]
        self.b = quadratic_set[1]
        self.c = quadratic_set[2]
        self.vertex = (None, None)
        self.roots = (None, None)
        self.y_intercept = (None, None)
        self.discriminant = None
        self.points = {'x': [], 'y': []}
        self.degree = 2

    def solve(self, x):
        return self.a * math.pow(x, 2) + self.b * x + self.c

    def complete(self):
        self.quadratic_solve()
        self.calc_y_intercept()
        self.calc_vertex()

    def quadratic_solve(self, r=4):
        self.discriminant = math.pow(self.b, 2) - 4 * self.a * self.c
        if self.discriminant > 0:
            d = math.sqrt(self.discriminant)
        elif self.discriminant == 0:
            d = 0
        else:
            return None
        divisor = 2 * self.a
        x1 = round((-self.b + d) / divisor, r)
        x2 = round((-self.b - d) / divisor, r)
        self.roots = (x1, x2)

    def calc_vertex(self):
        x = -self.b / (2 * self.a)
        y = self.solve(x)
        self.vertex = (x, y)

    def calc_y_intercept(self):
        self.y_intercept = (0, self.c)

    def render(self, range_set):
        for i in range(range_set[0], range_set[1]):
            self.points['x'].append(i)
            self.points['y'].append(self.solve(i))

    def params(self):
        print('              [x]\t[y]')
        print('Vertex:       {0[0]},\t{0[1]}'.format(self.vertex))
        print('Y Intercept:  {0[0]},\t{0[1]}'.format(self.y_intercept))
        print('Roots:        {0[0]},\t{0[1]}'.format(self.roots))
        print('\nDiscriminant: {0}'.format(self.discriminant))

if __name__ == "__main__":
    Q = Quadratic((-3/2, -18, -48))
    Q.complete()
    Q.render((-20, 20))
    Q.params()
    '''
    for i in range(len(Q.points['x'])):
        print(Q.points['x'][i], Q.points['y'][i])
    '''

