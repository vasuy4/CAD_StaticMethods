import math
from typing import Tuple


def F(b):
    def func(z):
        return (1 / math.sqrt(2 * math.pi)) * math.exp(-(z * z) / 2)

    a = 0
    n = 10000
    dx = (b - a) / n
    sum = 0

    for i in range(n):
        xi = a + i * dx
        sum += func(xi) * dx

    return sum

def calculate(ei: float, es: float, nx: float, o: float) -> Tuple[float, float, float]:
    """
    Подсчёт количества годных деталей и брака
    :param ei: нижний допуск
    :param es: верхний допуск
    :param nx: номинальный размер
    :param o: стандартное отклонение
    :return: в процентах количество годных деталей, количество неисправимого брака, исправимого брака
    """
    # Определение количества годных деталей
    t2: float = (es-nx) / o
    t1: float = (ei-nx) / o
    p_suitable_parts: float = round((F(t2) - F(t1))*100, 2)
    print(f"Количество годных деталей: {p_suitable_parts}%")

    # Определение неисправимого брака
    t2: float = (ei-nx) / o
    t1: float = (nx - 3*o - nx) / o
    p_incorrigible_marriage: float = round((F(t2) - F(t1))*100, 2)
    print(f"Определение неисправимого брака {p_incorrigible_marriage}%")

    # Определение исправимого брака
    t2: float = (nx + 3 * o - nx) / o
    t1: float = (es-nx) / o
    p_fixable_marriage: float = round((F(t2) - F(t1))*100, 2)
    print(f"Определение исправимого брака {p_fixable_marriage}%")

    return p_suitable_parts, p_incorrigible_marriage, p_fixable_marriage


def normal_distribution(x: float, mu: float=0, sigma: float=1):
    """Вычисление значения плотности вероятности для нормального распределения (по формуле см. теор. часть)"""
    return (1 / (sigma * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((x - mu) / sigma) ** 2)
