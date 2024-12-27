import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, TextBox
import numpy as np

from typing import Tuple, List

from logic import normal_distribution, calculate


def build_graph(ax: plt.Axes, nx: float, o: float) -> Tuple[np.ndarray, List[float], plt.Line2D]:
    """
    Построение графика "Распределение деталей по качеству"
    :param ax: объект класса Axes, представляющий собой область для построения графика
    :param nx: наладочный размер
    :param o: среднее квадратичное отклонение
    :return: массивы данных для построения графика нормального распределения
    """
    x: np.ndarray = np.linspace(nx - 3*o, nx + 3*o, 1000)
    y: List[float] = [normal_distribution(xi, nx, o) for xi in x]
    line, = ax.plot(x, y, label='Нормальное распределение')
    return x, y, line


def fill_areas(ax: plt.Axes, ei: float, es: float, nx: float, o: float) -> None:
    """
    Закрашивает области для наглядности
    :param ax: объект класса Axes, представляющий собой область для построения графика
    :param ei: нижнее предельное отклонение
    :param es: верхнее предельное отклонение
    :param nx: наладочный размер
    :param o: среднее квадратичное отклонение
    """
    x_suitable = np.linspace(ei, es, 100)
    y_suitable = [normal_distribution(xi, nx, o) for xi in x_suitable]
    ax.fill_between(x_suitable, y_suitable, color='green', alpha=0.3, label='Годные детали')

    x_incorrigible = np.linspace(nx - 4*o, ei, 100)
    y_incorrigible = [normal_distribution(xi, nx, o) for xi in x_incorrigible]
    ax.fill_between(x_incorrigible, y_incorrigible, color='red', alpha=0.3, label='Неисправимый брак')

    x_fixable = np.linspace(es, nx + 4*o, 100)
    y_fixable = [normal_distribution(xi, nx, o) for xi in x_fixable]
    ax.fill_between(x_fixable, y_fixable, color='orange', alpha=0.3, label='Исправимый брак')


def add_text(ax: plt.Axes, nx: float, o: float, y: List[float], suitable_parts: float, incorrigible_marriage: float, fixable_marriage: float):
    """
    Добавление текста с информацией о браках
    :param ax: объект класса Axes, представляющий собой область для построения графика
    :param nx: наладочный размер
    :param o: среднее квадратичное отклонение
    :param y: значения плотности вероятности нормального распределения в каждой точке x
    :param suitable_parts: % годных деталей
    :param incorrigible_marriage: % неисправимого брака
    :param fixable_marriage: % исправимого брака
    """
    ax.text(nx - 3.5*o, 0.8 * max(y),
             f'Годные детали: {suitable_parts}%\n'
             f'Неисправимый брак: {incorrigible_marriage}%\n'
             f'Исправимый брак: {fixable_marriage}%',
             bbox=dict(facecolor='white', alpha=0.8))


def start_ui() -> None:
    """Запуск ui-приложения"""
    def update(val):
        ei = ei_slider.val
        es = es_slider.val
        nx = nx_slider.val
        o = o_slider.val

        x = np.linspace(nx - 3 * o, nx + 3 * o, 1000)
        y = [normal_distribution(xi, nx, o) for xi in x]
        line.set_data(x, y)

        ax.clear()
        ax.plot(x, y, lw=2, label='Нормальное распределение')
        suitable_parts, incorrigible_marriage, fixable_marriage = calculate(ei, es, nx, o)
        fill_areas(ax, ei, es, nx, o)
        add_text(ax, nx, o, y, suitable_parts, incorrigible_marriage, fixable_marriage)
        ax.set_xlabel('Значение')
        ax.set_ylabel('Плотность вероятности')
        ax.set_title('Распределение деталей по качеству')
        ax.legend()
        ax.grid(True)
        fig.canvas.draw_idle()

    def reset_sliders(event):
        """Устанавливает значение слайдеров по умолчанию"""
        ei_slider.reset()
        es_slider.reset()
        nx_slider.reset()
        o_slider.reset()

    ei: float = 0.006  # 0.002
    es: float = 0.055  # 0.035
    nx: float = 0.026  # 0.014
    o: float = 0.012  # 0.009

    str_ei = str(ei)
    str_es = str(es)
    str_nx = str(nx)
    str_o = str(o)
    suitable_parts, incorrigible_marriage, fixable_marriage = calculate(ei, es, nx, o)

    # Создание фигуры и осей
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.2, bottom=0.4)

    x, y, line = build_graph(ax, nx, o)
    fill_areas(ax, ei, es, nx, o)
    add_text(ax, nx, o, y, suitable_parts, incorrigible_marriage, fixable_marriage)

    # Создание слайдеров
    ax_ei = fig.add_axes((0.25, 0.25, 0.65, 0.03))
    ax_es = fig.add_axes((0.25, 0.20, 0.65, 0.03))
    ax_nx = fig.add_axes((0.25, 0.15, 0.65, 0.03))
    ax_o = fig.add_axes((0.25, 0.10, 0.65, 0.03))

    ei_slider = Slider(ax_ei, 'ниж. предельное отклонение ei', 0.001, 0.08, valinit=ei)
    es_slider = Slider(ax_es, 'верх. предельное отклонение es', 0.01, 0.08, valinit=es)
    nx_slider = Slider(ax_nx, 'наладочный размер nx', 0.01, 0.06, valinit=nx)
    o_slider = Slider(ax_o, 'среднее квадратичное откл. o', 0.001, 0.06, valinit=o)

    # Привязка функции обновления к слайдерам
    ei_slider.on_changed(update)
    es_slider.on_changed(update)
    nx_slider.on_changed(update)
    o_slider.on_changed(update)

    # Кнопка сброса слайдеров
    resetax = fig.add_axes((0.8, 0.025, 0.1, 0.04))
    buttonReset = Button(resetax, 'Reset sliders', hovercolor='0.975')

    buttonReset.on_clicked(reset_sliders)

    # Поля ввода для обновления значений по умолчанию
    def set_default_value_sliders(text, slider):
        ydata: float = float(text)
        slider.valinit = ydata
        slider.reset()

    ax_box_ei: plt.Axes = fig.add_axes((0.05, 0.75, 0.05, 0.055))
    ax_box_es: plt.Axes = fig.add_axes((0.05, 0.65, 0.05, 0.055))
    ax_box_nx: plt.Axes = fig.add_axes((0.05, 0.55, 0.05, 0.055))
    ax_box_o: plt.Axes = fig.add_axes((0.05, 0.45, 0.05, 0.055))

    ei_text_box: TextBox = TextBox(ax_box_ei, 'ei ', initial=str_ei)
    es_text_box: TextBox = TextBox(ax_box_es, 'es ', initial=str_es)
    nx_text_box: TextBox = TextBox(ax_box_nx, 'nx ', initial=str_nx)
    o_text_box: TextBox = TextBox(ax_box_o, 'o ', initial=str_o)

    ei_text_box.on_submit(lambda val: set_default_value_sliders(val, ei_slider))
    es_text_box.on_submit(lambda val: set_default_value_sliders(val, es_slider))
    nx_text_box.on_submit(lambda val: set_default_value_sliders(val, nx_slider))
    o_text_box.on_submit(lambda val: set_default_value_sliders(val, o_slider))

    def reset_textbox(event):
        """Устанавливает значение текстбоксов по умолчанию"""
        ei_text_box.set_val(str_ei)
        es_text_box.set_val(str_es)
        nx_text_box.set_val(str_nx)
        o_text_box.set_val(str_o)

    # Кнопка сброса текстбоксов
    resetax_box = fig.add_axes((0.05, 0.35, 0.1, 0.055))
    buttonReset_box = Button(resetax_box, 'Reset textbox', hovercolor='0.975')

    buttonReset_box.on_clicked(reset_textbox)

    # Добавление текста
    ax.set_title('Расчёт процента годных деталей')
    ax.set_xlabel('Значение')
    ax.set_ylabel('Плотность вероятности')
    ax.legend()
    ax.grid(True)
    manager: plt.FigureManagerBase = plt.get_current_fig_manager()
    manager.resize(1080, 720)
    plt.show()

