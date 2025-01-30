import cython
from libc.math cimport exp, sqrt, M_PI

cdef float normal_distributionC(float x, float nx=0, float o=1):
    return (1 / (o * sqrt(2 * M_PI))) * exp(-0.5 * ((x - nx) / o) ** 2)

cpdef float normal_distribution(float x, float nx=0, float o=1):
    return (1 / (o * sqrt(2 * M_PI))) * exp(-0.5 * ((x - nx) / o) ** 2)

cdef float F(float b, int n=10000):
    cdef int a = 0
    cdef float dx = (b - a) / n
    cdef float sum = 0

    cdef float xi
    cdef int i
    for i in range(n):
        xi = a + i * dx
        sum += normal_distributionC(xi) * dx
    return sum

cpdef (float, float, float) calculate(float ei, float es, float nx, float o, int n=10000):
    cdef float t2 = (es - nx) / o
    cdef float t1 = (ei - nx) / o
    cdef float p_suitable_parts = (F(t2, n) - F(t1, n)) * 100

    t2 = (ei - nx) / o
    t1 = (nx - 3 * o - nx) / o
    cdef float p_incorrigible_marriage = (F(t2, n) - F(t1, n)) * 100

    t2 = (nx + 3 * o - nx) / o
    t1 = (es - nx) / o
    cdef float p_fixable_marriage = (F(t2, n) - F(t1, n)) * 100

    return p_suitable_parts, p_incorrigible_marriage, p_fixable_marriage