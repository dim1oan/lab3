"""
Лабораторная работа №3 по дисциплине «Прикладное программирование»
Тема: Приложения с графическим интерфейсом
Вариант 1: Игра «Крестики-нолики» для двух игроков
Выполнил: студент группы ИДБ-25-15 Ткачук Д. В.
"""

import tkinter as tk
from tkinter import messagebox
from typing import List, Optional, Tuple


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
        self.root.geometry("450x520")
        self.root.minsize(360, 420)

        # Текущий игрок: 'X' начинает первым
        self.current_player: str = "X"
        self.game_over: bool = False

        # Матрица логического состояния игрового поля 3x3
        self.board: List[List[Optional[str]]] = [
            [None for _ in range(3)] for _ in range(3)
        ]

        # Матрица графических кнопок 3x3
        self.buttons: List[List[tk.Button]] = []

        # Построение меню и графического интерфейса
        self._create_menu()
        self._init_ui()

    def _create_menu(self) -> None:
        """Создание главного меню приложения."""
        self.menu_bar: tk.Menu = tk.Menu(self.root)

        # Меню «Игра»
        game_menu: tk.Menu = tk.Menu(self.menu_bar, tearoff=0)
        game_menu.add_command(label="Новая игра", command=self.reset_game, accelerator="Ctrl+N")
        game_menu.add_separator()
        game_menu.add_command(label="Выход", command=self.root.quit, accelerator="Alt+F4")
        self.menu_bar.add_cascade(label="Игра", menu=game_menu)

        # Меню «Справка»
        help_menu: tk.Menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Правила игры", command=self._show_rules)
        help_menu.add_command(label="Об авторе", command=self._show_about)
        self.menu_bar.add_cascade(label="Справка", menu=help_menu)

        self.root.config(menu=self.menu_bar)

        # Привязка горячей клавиши Ctrl+N к началу новой игры
        self.root.bind("<Control-n>", lambda event: self.reset_game())
        self.root.bind("<Control-N>", lambda event: self.reset_game())

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
                    font=("Arial", 28, "bold"),
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

        # Фиксация хода в матрице состояния
        self.board[row][col] = self.current_player

        # Отображение символа хода на кнопке
        color: str = "#1f77b4" if self.current_player == "X" else "#d62728"
        self.buttons[row][col].config(text=self.current_player, fg=color)

        # Проверка условий окончания игры (победа или ничья)
        winning_combo: Optional[List[Tuple[int, int]]] = self._check_win(self.current_player)

        if winning_combo is not None:
            self.game_over = True
            self._highlight_winner(winning_combo)
            winner_text: str = f"Победил игрок: {self.current_player}!"
            self.status_label.config(text=winner_text, fg="#2ca02c")
            messagebox.showinfo("Победа!", f"Поздравляем! Победил игрок {self.current_player}!")
            return

        if self._is_board_full():
            self.game_over = True
            self.status_label.config(text="Ничья!", fg="#ff7f0e")
            messagebox.showinfo("Ничья", "Игра завершилась вничью!")
            return

        # Передача хода следующему игроку
        self.current_player = "O" if self.current_player == "X" else "X"
        self.status_label.config(
            text=f"Ход игрока: {self.current_player}",
            fg="#000000"
        )

    def _check_win(self, player: str) -> Optional[List[Tuple[int, int]]]:
        """
        Проверка наличия выигрышной комбинации для указанного игрока.

        :param player: Символ игрока ('X' или 'O').
        :return: Список координат (row, col) выигрышных ячеек или None.
        """
        # Проверка горизонталей
        for row in range(3):
            if all(self.board[row][col] == player for col in range(3)):
                return [(row, col) for col in range(3)]

        # Проверка вертикалей
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return [(row, col) for row in range(3)]

        # Проверка главной диагонали
        if all(self.board[i][i] == player for i in range(3)):
            return [(i, i) for i in range(3)]

        # Проверка побочной диагонали
        if all(self.board[i][2 - i] == player for i in range(3)):
            return [(i, 2 - i) for i in range(3)]

        return None

    def _is_board_full(self) -> bool:
        """
        Проверка, заполнены ли все ячейки поля.

        :return: True, если свободных клеток не осталось, иначе False.
        """
        return all(self.board[row][col] is not None for row in range(3) for col in range(3))

    def _highlight_winner(self, combo: List[Tuple[int, int]]) -> None:
        """
        Подсветка выигрышных ячеек зеленым цветом.

        :param combo: Список координат победной комбинации.
        """
        for row, col in combo:
            self.buttons[row][col].config(bg="#c8e6c9", activebackground="#a5d6a7")

    def reset_game(self) -> None:
        """Сброс игрового поля и запуск нового раунда."""
        self.current_player = "X"
        self.game_over = False
        self.board = [[None for _ in range(3)] for _ in range(3)]

        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(
                    text="",
                    bg="#ffffff",
                    activebackground="#e0e0e0",
                    state=tk.NORMAL
                )

        self.status_label.config(
            text=f"Ход игрока: {self.current_player}",
            fg="#000000"
        )

    def _show_rules(self) -> None:
        """Отображение окна со справочной информацией о правилах игры."""
        rules_text: str = (
            "Правила игры «Крестики-нолики»:

"
            "1. Игра рассчитана на двух игроков (X и O).
"
            "2. Игроки по очереди ставят свои знаки на свободные клетки поля 3x3.
"
            "3. Первый игрок ходит крестиками (X).
"
            "4. Побеждает игрок, первым выстроивший ряд из 3 своих знаков "
            "по горизонтали, вертикали или диагонали.
"
            "5. Если поле заполнено и ни один игрок не составил линию, объявляется ничья."
        )
        messagebox.showinfo("Правила игры", rules_text)

    def _show_about(self) -> None:
        """Отображение окна с информацией об авторе программы."""
        about_text: str = (
            "Лабораторная работа №3
"
            "Дисциплина: «Прикладное программирование»
"
            "Тема: «Приложения с графическим интерфейсом»

"
            "Автор: Ткачук Дмитрий Владимирович
"
            "Группа: ИДБ-25-15
"
            "Вуз: ФГБОУ ВО «МГТУ «СТАНКИН»
"
            "Год: 2026"
        )
        messagebox.showinfo("Об авторе", about_text)

    def run(self) -> None:
        """Запуск главного цикла обработки событий приложения."""
        self.root.mainloop()


if __name__ == "__main__":
    app = TicTacToe()
    app.run()
