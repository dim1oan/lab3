"""
Лабораторная работа №3 по дисциплине «Прикладное программирование»
Тема: Приложения с графическим интерфейсом
Вариант 1: Игра «Крестики-нолики» для двух игроков
Выполнил: студент группы ИДБ-25-15 Ткачук Д. В.
"""

import tkinter as tk
from typing import List, Optional


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

        # Матрица логического состояния игрового поля 3x3
        self.board: List[List[Optional[str]]] = [
            [None for _ in range(3)] for _ in range(3)
        ]

        # Матрица графических кнопок 3x3
        self.buttons: List[List[tk.Button]] = []

        # Построение графического интерфейса
        self._init_ui()

    def _init_ui(self) -> None:
        """Создание и размещение элементов интерфейса (сетка и статус)."""
        # Настройка растягивания содержимого окна
        self.root.grid_rowconfigure(0, weight=0)  # Панель статуса фиксирована
        self.root.grid_rowconfigure(1, weight=1)  # Игровое поле занимает все пространство
        self.root.grid_columnconfigure(0, weight=1)

        # Информационная панель текущего статуса игры
        self.status_label: tk.Label = tk.Label(
            self.root,
            text=f"Ход игрока: {self.current_player}",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0",
            pady=10
        )
        self.status_label.grid(row=0, column=0, sticky="ew")

        # Контейнер для игрового поля 3x3
        self.grid_frame: tk.Frame = tk.Frame(self.root, bg="#cccccc", padx=5, pady=5)
        self.grid_frame.grid(row=1, column=0, sticky="nsew")

        # Настройка динамического масштабирования ячеек сетки
        for i in range(3):
            self.grid_frame.grid_rowconfigure(i, weight=1)
            self.grid_frame.grid_columnconfigure(i, weight=1)

        # Создание 9 кнопок игрового поля
        for row in range(3):
            button_row: List[tk.Button] = []
            for col in range(3):
                btn: tk.Button = tk.Button(
                    self.grid_frame,
                    text="",
                    font=("Arial", 24, "bold"),
                    bg="#ffffff",
                    activebackground="#e0e0e0",
                    relief="raised",
                    bd=2,
                    command=lambda r=row, c=col: self._on_cell_click(r, c)
                )
                btn.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)
                button_row.append(btn)
            self.buttons.append(button_row)

    def _on_cell_click(self, row: int, col: int) -> None:
        """
        Обработчик нажатия на ячейку игрового поля.

        :param row: Индекс строки (0..2).
        :param col: Индекс столбца (0..2).
        """
        if self.game_over or self.board[row][col] is not None:
            return

        # Установка хода в ячейку
        self.board[row][col] = self.current_player
        self.buttons[row][col].config(
            text=self.current_player,
            fg="#1f77b4" if self.current_player == "X" else "#d62728"
        )

        # Смена игрока
        self.current_player = "O" if self.current_player == "X" else "X"
        self.status_label.config(text=f"Ход игрока: {self.current_player}")

    def run(self) -> None:
        """Запуск главного цикла обработки событий приложения."""
        self.root.mainloop()


if __name__ == "__main__":
    app = TicTacToe()
    app.run()
