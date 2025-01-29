import math
from typing import Tuple


def normal_distribution(x: float, nx: float = 0, o: float = 1) -> float:
    """
    Вычисляет значение плотности вероятности стандартного нормального распределения в точке x.
    Т.к. мы используем стандартное распределение, то математическое ожидание nx = 0 и стандартное отклонение o = 1.
    (по формуле см. теор. часть первую страницу)
    """
    return (1 / (o * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((x - nx) / o) ** 2)


def F(b: float, n: int = 10000) -> float:
    """
    Вычисляет приближенное значение интеграла от 0 до b функции плотности вероятности стандартного
    нормального распределения.
    :param b: Конечная точка интегрирования. Верхний предел интеграла.
    :param n: Количество разбиений интервала интегрирования. Чем больше n, тем точнее будет результат
    """
    a = 0  # начальная точка интегрирования
    dx = (b - a) / n  # ширина каждого разбиения (шаг интегрирования).
    sum: float = 0  # переменная для накопления суммы значений функции на каждом шаге.

    for i in range(n):
        xi = a + i * dx  # вычисление текущей точки на интервале интегрирования.
        sum += normal_distribution(xi) * dx  # добавление площади прямоугольника с высотой func(xi) и шириной dx к общей сумме.

    return sum


def calculate(ei: float, es: float, nx: float, o: float, n: int = 10000) -> Tuple[float, float, float]:
    """
    Подсчёт количества годных деталей и брака
    :param ei: нижнее предельное отклонение
    :param es: верхнее предельное отклонение
    :param nx: наладочный размер
    :param o: среднее квадратичное отклонение
    :param n: Точность вычислений
    :return: в процентах количество годных деталей, количество неисправимого брака, исправимого брака
    """
    # Определение количества годных деталей
    t2: float = (es - nx) / o
    t1: float = (ei - nx) / o
    p_suitable_parts: float = (F(t2, n) - F(t1, n)) * 100
    # print(f"Количество годных деталей: {p_suitable_parts}%")

    # Определение неисправимого брака
    t2: float = (ei - nx) / o
    t1: float = (nx - 3 * o - nx) / o
    p_incorrigible_marriage: float = (F(t2, n) - F(t1, n)) * 100
    # print(f"Определение неисправимого брака {p_incorrigible_marriage}%")

    # Определение исправимого брака
    t2: float = (nx + 3 * o - nx) / o
    t1: float = (es - nx) / o
    p_fixable_marriage: float = (F(t2, n) - F(t1, n)) * 100
    # print(f"Определение исправимого брака {p_fixable_marriage}%")

    return p_suitable_parts, p_incorrigible_marriage, p_fixable_marriage
