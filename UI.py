import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, TextBox
import numpy as np

from typing import Tuple, List

from logic import normal_distribution, calculate


def build_graph(
    ax: plt.Axes, nx: float, o: float
) -> Tuple[np.ndarray, List[float], plt.Line2D]:
    """
    Построение графика "Распределение деталей по качеству"
    :param ax: объект класса Axes, представляющий собой область для построения графика
    :param nx: наладочный размер
    :param o: среднее квадратичное отклонение
    :return: массивы данных для построения графика нормального распределения
    """
    x: np.ndarray = np.linspace(nx - 3 * o, nx + 3 * o, 1000)
    y: List[float] = [normal_distribution(xi, nx, o) for xi in x]
    (line,) = ax.plot(x, y, label="Нормальное распределение")
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
    ax.fill_between(
        x_suitable, y_suitable, color="green", alpha=0.3, label="Годные детали"
    )

    x_incorrigible = np.linspace(nx - 4 * o, ei, 100)
    y_incorrigible = [normal_distribution(xi, nx, o) for xi in x_incorrigible]
    ax.fill_between(
        x_incorrigible,
        y_incorrigible,
        color="red",
        alpha=0.3,
        label="Неисправимый брак",
    )

    x_fixable = np.linspace(es, nx + 4 * o, 100)
    y_fixable = [normal_distribution(xi, nx, o) for xi in x_fixable]
    ax.fill_between(
        x_fixable, y_fixable, color="orange", alpha=0.3, label="Исправимый брак"
    )


def add_text(
    ax: plt.Axes,
    nx: float,
    o: float,
    y: List[float],
    suitable_parts: float,
    incorrigible_marriage: float,
    fixable_marriage: float,
):
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
    ax.text(
        nx - 3.5 * o,
        0.8 * max(y),
        f"Годные детали: {suitable_parts}%\n"
        f"Неисправимый брак: {incorrigible_marriage}%\n"
        f"Исправимый брак: {fixable_marriage}%",
        bbox=dict(facecolor="white", alpha=0.8),
    )


def start_ui() -> None:
    """Запуск ui-приложения"""

    def update(val):
        ei = ei_slider.val
        es = es_slider.val
        nx = nx_slider.val
        o = o_slider.val
        accuracy: int = int(accuracy_text_box.text)
        if (accuracy == 0):
            accuracy = initial_accuracy
        x = np.linspace(nx - 3 * o, nx + 3 * o, 1000)
        y = [normal_distribution(xi, nx, o) for xi in x]
        line.set_data(x, y)

        ax.clear()
        ax.plot(x, y, lw=2, label="Нормальное распределение")
        suitable_parts, incorrigible_marriage, fixable_marriage = calculate(ei, es, nx, o, accuracy)
        fill_areas(ax, ei, es, nx, o)
        draw_lines(ei, es, nx, o, True)
        add_text(ax, nx, o, y, suitable_parts, incorrigible_marriage, fixable_marriage)
        ax.set_xlabel("Значение")
        ax.set_ylabel("Плотность вероятности")
        ax.set_title("Распределение деталей по качеству")
        ax.legend()
        ax.grid(True)
        fig.canvas.draw_idle()

    def reset_sliders(event):
        """Устанавливает значение слайдеров по умолчанию"""
        ei_slider.reset()
        es_slider.reset()
        nx_slider.reset()
        o_slider.reset()

    def set_default_value_sliders(text: str, slider: Slider):
        """Обновляет дефолтные значения слайдеров"""
        ydata: float = float(text)
        slider.valinit = ydata
        slider.reset()

    def reset_textbox(event):
        """Устанавливает значение текстбоксов по умолчанию"""
        ei_text_box.set_val(str_ei)
        es_text_box.set_val(str_es)
        nx_text_box.set_val(str_nx)
        o_text_box.set_val(str_o)

    def fix_recommendation(event):
        """Смещает наладочный размер (nx) по рекомендации"""
        nx_text_box.set_val(str(round(nx + float(recommendation_tb.text), 3)))


    def draw_lines(ei: float, es: float, nx: float, o: float, isAgain=False):
        """Добавляем линии с обозначениями ei es +-3o nx"""
        nx_x, nx_y = [nx, nx], [0, max(y)]
        ei_x, ei_y = [ei, ei], [0, max(y)]
        es_x, es_y = [es, es], [0, max(y)]
        o_x, o_y = [nx - 3 * o, nx - 3 * o], [0, max(y) / 5]
        o_x2, o_y2 = [nx + 3 * o, nx + 3 * o], [0, max(y) / 5]
        # Значение по X -3o и +3o
        ox1_val = round(nx - 3 * o, 3)
        ox2_val = round(nx + 3 * o, 3)

        ax.plot(nx_x, nx_y, marker="p", color="green")
        ax.plot(ei_x, ei_y, marker="p", color="red")
        ax.plot(es_x, es_y, marker="p", color="orange")
        ax.plot(o_x, o_y, marker="p", color="gray")
        ax.plot(o_x2, o_y2, marker="p", color="gray")

        ax.text(nx, -2.3, f'nx={round(nx, 3)}', color='green', ha='center', va='bottom', backgroundcolor='white')
        ax.text(ei, -2.3, f'ei={round(ei, 3)}', color='red', ha='center', va='bottom', backgroundcolor='white')
        ax.text(es, -2.3, f'es={round(es, 3)}', color='orange', ha='center', va='bottom', backgroundcolor='white')
        ax.text(ox1_val, max(y) / 5, f'-3σ={ox1_val}', color='gray', ha='center', va='bottom',
                backgroundcolor='white')
        ax.text(ox2_val, max(y) / 5, f'+3σ={ox2_val}', color='gray', ha='center', va='bottom',
                backgroundcolor='white')

        if isAgain:
            recommendation_tb.set_val(str(round(ei - ox1_val, 3)))

    ei: float = 0.006  # 0.002
    es: float = 0.055  # 0.035
    nx: float = 0.026  # 0.014
    o: float = 0.012  # 0.009
    initial_accuracy: int = 1000

    str_ei = str(ei)
    str_es = str(es)
    str_nx = str(nx)
    str_o = str(o)
    str_ini_acc = str(initial_accuracy)

    suitable_parts, incorrigible_marriage, fixable_marriage = calculate(ei, es, nx, o, initial_accuracy)

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

    ei_slider = Slider(ax_ei, "ниж. предельное отклонение ei", 0.001, 0.08, valinit=ei)
    es_slider = Slider(ax_es, "верх. предельное отклонение es", 0.01, 0.08, valinit=es)
    nx_slider = Slider(ax_nx, "наладочный размер nx", 0.01, 0.06, valinit=nx)
    o_slider = Slider(ax_o, "среднее квадратичное откл. o", 0.001, 0.06, valinit=o)

    # Привязка функции обновления к слайдерам
    ei_slider.on_changed(update)
    es_slider.on_changed(update)
    nx_slider.on_changed(update)
    o_slider.on_changed(update)

    # Кнопка сброса слайдеров
    resetax = fig.add_axes((0.8, 0.025, 0.1, 0.04))
    buttonReset = Button(resetax, "Reset sliders", hovercolor="0.975")

    buttonReset.on_clicked(reset_sliders)

    # Добавляем текстбоксы
    ax_box_ei: plt.Axes = fig.add_axes((0.05, 0.75, 0.05, 0.055))
    ax_box_es: plt.Axes = fig.add_axes((0.05, 0.65, 0.05, 0.055))
    ax_box_nx: plt.Axes = fig.add_axes((0.05, 0.55, 0.05, 0.055))
    ax_box_o: plt.Axes = fig.add_axes((0.05, 0.45, 0.05, 0.055))
    ax_box_accuracy: plt.Axes = fig.add_axes((0.1, 0.90, 0.05, 0.055))

    ei_text_box: TextBox = TextBox(ax_box_ei, "ei ", initial=str_ei)
    es_text_box: TextBox = TextBox(ax_box_es, "es ", initial=str_es)
    nx_text_box: TextBox = TextBox(ax_box_nx, "nx ", initial=str_nx)
    o_text_box: TextBox = TextBox(ax_box_o, "o ", initial=str_o)
    accuracy_text_box: TextBox = TextBox(ax_box_accuracy, "Точность ", initial=str_ini_acc)

    ei_text_box.on_submit(lambda val: set_default_value_sliders(val, ei_slider))
    es_text_box.on_submit(lambda val: set_default_value_sliders(val, es_slider))
    nx_text_box.on_submit(lambda val: set_default_value_sliders(val, nx_slider))
    o_text_box.on_submit(lambda val: set_default_value_sliders(val, o_slider))
    accuracy_text_box.on_submit(lambda val: update(val))

    # Кнопка сброса текстбоксов
    resetax_box = fig.add_axes((0.05, 0.35, 0.1, 0.055))
    buttonReset_box = Button(resetax_box, "Reset textbox", hovercolor="0.975")

    buttonReset_box.on_clicked(reset_textbox)

    # Рекомендации по смещению наладочного размера
    recommendation_ax = fig.add_axes((0.4, 0.025, 0.07, 0.04))
    recommendation_tb = TextBox(recommendation_ax, "Рекомендуется сместить наладочный размер на ",
                                initial=str(round(ei - (nx - 3 * o), 3)))
    draw_lines(ei, es, nx, o)

    # Автоматическая поправка с помощью кнопки
    btn_rec_box = fig.add_axes((0.5, 0.025, 0.1, 0.04))
    btn_recommendation = Button(btn_rec_box, "Fix", hovercolor="0.975")
    btn_recommendation.on_clicked(fix_recommendation)
    # Добавление текста

    ax.set_title("Распределение деталей по качеству")
    ax.set_xlabel("Значение")
    ax.set_ylabel("Плотность вероятности")
    ax.legend()
    ax.grid(True)
    manager: plt.FigureManagerBase = plt.get_current_fig_manager()
    manager.resize(1080, 720)
    plt.show()
