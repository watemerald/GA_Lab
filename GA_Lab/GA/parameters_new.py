import json

class Properties(object):
    """Properties used in running of Genetic Algorithms"""
    def __init__(self):
        super(Properties, self).__init__()
        self._N = 500
        self._ndim = 1
        self._pm = 0.1
        self._pc = 0.1
        self._coding = 'bin'
        self._crossover = '1'
        self._mutation = '1-point'
        self._distance_measure = 'euclidean'
        self._csp = 0.15
        self._cs = int(self._csp*self._N)
        self._cf = 3
        self._sp = 0.01
        self._s = int(self._sp*self._N)
        self._sigma = 0.0001
        self._method = 'worst_among_most_similar'

    def __repr__(self):
        return json.dumps({
        'N': self._N,
        'dimensions': self._ndim,
        'p_m': self._pm,
        'p_c': self._pc,
        'coding': self._coding,
        'crossover': self._crossover,
        'mutation': self._mutation,
        'distance_measure': self._distance_measure,
        'crowding_selection': self._cs,
        'crowding_factor': self._cf,
        'subpopulation_size': self._s,
        'sigma': self._sigma,
        'method': self._method
        })

    def __str__(self):
        return self.__repr__()

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self,value):
        self._method = value

    @property
    def sigma(self):
        return self._sigma

    @sigma.setter
    def sigma(self,value):
        self._sigma = value

    @property
    def s(self):
        return self._s

    @s.setter
    def s(self,value):
        self._sp = value
        self._s = int(value* self.N)

    @property
    def sp(self):
        return self._sp

    @property
    def cf(self):
        return self._cf

    @cf.setter
    def cf(self,value):
        self._cf = value

    @property
    def cs(self):
        return self._cs

    @cs.setter
    def cs(self,value):
        self._csp = value
        self._cs = int(value * self.N)

    @property
    def csp(self):
        return self._csp

    @property
    def distance_measure(self):
        return self._distance_measure

    @distance_measure.setter
    def distance_measure(self,value):
        self._distance_measure = value

    @property
    def mutation(self):
        return self._mutation

    @mutation.setter
    def mutation(self,value):
        self._mutation = value

    @property
    def crossover(self):
        return self._crossover

    @crossover.setter
    def crossover(self,value):
        self._crossover = value

    @property
    def coding(self):
        return self._coding

    @coding.setter
    def coding(self,value):
        self._coding = value

    @property
    def pc(self):
        return self._pc

    @pc.setter
    def pc(self,value):
        self._pc = value

    @property
    def pm(self):
        return self._pm

    @pm.setter
    def pm(self,value):
        self._pm = value

    @property
    def ndim(self):
        return self._ndim

    @ndim.setter
    def ndim(self,value):
        self._ndim = value

    @property
    def N(self):
        return self._N

    @N.setter
    def N(self,value):
        self._N = value


parameters = Properties()

__all__ = ['parameters']
