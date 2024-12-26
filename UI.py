import matplotlib.pyplot as plt
import numpy
import numpy as np
from matplotlib.widgets import Slider

from typing import Tuple, List

from logic import normal_distribution, calculate

def build_graph(nx: float, o: float) -> Tuple[numpy.ndarray, List[float]]:
    """
    Построение графика
    :param nx: номинальный размер
    :param o: стандартное отклонение
    :return: массивы данных для построения графика нормального распределения
    """
    x: numpy.ndarray = np.linspace(nx - 3*o, nx + 3*o, 1000)
    y: List[float] = [normal_distribution(xi, nx, o) for xi in x]
    plt.plot(x, y, label='Нормальное распределение')
    return x, y


def fill_areas(ei: float, es: float, nx: float, o: float) -> None:
    """
    Закрашивает области для наглядности
    :param ei: нижний допуск
    :param es: верхний допуск
    :param nx: номинальный размер
    :param o: стандартное отклонение
    """
    x_suitable = np.linspace(ei, es, 100)
    y_suitable = [normal_distribution(xi, nx, o) for xi in x_suitable]
    plt.fill_between(x_suitable, y_suitable, color='green', alpha=0.3, label='Годные детали')

    x_incorrigible = np.linspace(nx - 4*o, ei, 100)
    y_incorrigible = [normal_distribution(xi, nx, o) for xi in x_incorrigible]
    plt.fill_between(x_incorrigible, y_incorrigible, color='red', alpha=0.3, label='Неисправимый брак')

    x_fixable = np.linspace(es, nx + 4*o, 100)
    y_fixable = [normal_distribution(xi, nx, o) for xi in x_fixable]
    plt.fill_between(x_fixable, y_fixable, color='orange', alpha=0.3, label='Исправимый брак')

def add_text(nx: float, o: float, y: List[float], suitable_parts: float, incorrigible_marriage: float, fixable_marriage: float):
    """
    Добавление текста с информацией о браках
    :param nx: номинальный размер
    :param o: стандартное отклонение
    :param y: значения плотности вероятности нормального распределения в каждой точке x
    :param suitable_parts: % годных деталей
    :param incorrigible_marriage: % неисправимого брака
    :param fixable_marriage: % исправимого брака
    """
    plt.text(nx - 3.5*o, 0.8 * max(y),
             f'Годные детали: {suitable_parts}%\n'
             f'Неисправимый брак: {incorrigible_marriage}%\n'
             f'Исправимый брак: {fixable_marriage}%',
             bbox=dict(facecolor='white', alpha=0.8))


def start_ui():
    ei: float = 0.002
    es: float = 0.035
    nx: float = 0.014
    o: float = 0.009

    suitable_parts, incorrigible_marriage, fixable_marriage = calculate(ei, es, nx, o)

    x, y = build_graph(nx, o)
    fill_areas(ei, es, nx, o)
    add_text(nx, o, y, suitable_parts, incorrigible_marriage, fixable_marriage)


    plt.title('Распределение деталей по качеству')
    plt.xlabel('Значение')
    plt.ylabel('Плотность вероятности')
    plt.legend()
    plt.grid(True)
    manager = plt.get_current_fig_manager()
    manager.resize(1080, 720)
    plt.show()