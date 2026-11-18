"""
Лабораторная работа №3 по дисциплине «Прикладное программирование»
Тема: Приложения с графическим интерфейсом
Вариант 1: Игра «Крестики-нолики» для двух игроков
Выполнил: студент группы ИДБ-25-15 Ткачук Д. В.
"""

import tkinter as tk
from typing import Optional


class TicTacToe:
    """
    Класс, инкапсулирующий логику игры 'Крестики-нолики'
    и её графический интерфейс на базе библиотеки Tkinter.
    """

    def __init__(self, root: Optional[tk.Tk] = None) -> None:
        """
        Инициализация главного окна приложения и базовых параметров игры.

        :param root: Корневое окно Tkinter (если None, создается новое).
        """
        self.root: tk.Tk = root if root is not None else tk.Tk()
        self.root.title("Крестики-нолики | Ткачук Д. В. ИДБ-25-15")
        self.root.geometry("450x500")
        self.root.minsize(350, 400)

        # Текущий игрок: 'X' начинает первым
        self.current_player: str = "X"
        self.game_over: bool = False

    def run(self) -> None:
        """Запуск главного цикла обработки событий приложения."""
        self.root.mainloop()


if __name__ == "__main__":
    app = TicTacToe()
    app.run()
