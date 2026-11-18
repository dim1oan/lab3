"""
Лабораторная работа №3 по дисциплине «Прикладное программирование»
Тема: «Приложения с графическим интерфейсом»
Вариант 1: Игра «Крестики-нолики» для двух игроков
Выполнил: студент группы ИДБ-25-15 Ткачук Д. В.
"""

import sys
import tkinter as tk
from tkinter import messagebox
from typing import List, Optional, Tuple


class TicTacToe:
    """
    Класс, инкапсулирующий логику игры «Крестики-нолики»
    и её графический интерфейс на базе библиотеки Tkinter.
    """

    def __init__(self, root: Optional[tk.Tk] = None) -> None:
        """
        Инициализация главного окна приложения и базовых параметров игры.

        :param root: Корневое окно Tkinter (если None, создается новое).
        """
        try:
            self.root: tk.Tk = root if root is not None else tk.Tk()
            self.root.title("Крестики-нолики | Ткачук Д. В. ИДБ-25-15")
            self.root.geometry("450x520")
            self.root.minsize(360, 420)
        except (tk.TclError, Exception) as exc:
            messagebox.showerror("Критическая ошибка", f"Не удалось инициализировать окно: {exc}")
            sys.exit(1)

        # Текущий игрок: 'X' начинает первым
        self.current_player: str = "X"
        self.game_over: bool = False

        # Матрица логического состояния игрового поля 3x3 (None - пустая клетка)
        self.board: List[List[Optional[str]]] = [
            [None for _ in range(3)] for _ in range(3)
        ]

        # Матрица графических кнопок 3x3
        self.buttons: List[List[tk.Button]] = []

        # Построение меню и графического интерфейса с обработкой исключений
        self._create_menu()
        self._init_ui()

    def _create_menu(self) -> None:
        """
        Создание главного меню приложения (пункты «Игра» и «Справка»).
        Критический блок обернут в try-except для предотвращения сбоев UI.
        """
        try:
            self.menu_bar: tk.Menu = tk.Menu(self.root)

            # Меню «Игра»
            game_menu: tk.Menu = tk.Menu(self.menu_bar, tearoff=0)
            game_menu.add_command(label="Новая игра", command=self.reset_game, accelerator="Ctrl+N")
            game_menu.add_separator()
            game_menu.add_command(label="Тест обработки ошибки", command=self._trigger_test_error)
            game_menu.add_separator()
            game_menu.add_command(label="Выход", command=self._safe_exit, accelerator="Alt+F4")
            self.menu_bar.add_cascade(label="Игра", menu=game_menu)

            # Меню «Справка»
            help_menu: tk.Menu = tk.Menu(self.menu_bar, tearoff=0)
            help_menu.add_command(label="Правила игры", command=self._show_rules)
            help_menu.add_command(label="Об авторе", command=self._show_about)
            self.menu_bar.add_cascade(label="Справка", menu=help_menu)

            self.root.config(menu=self.menu_bar)

            # Привязка горячих клавиш и протокола закрытия окна
            self.root.bind("<Control-n>", lambda event: self.reset_game())
            self.root.bind("<Control-N>", lambda event: self.reset_game())
            self.root.protocol("WM_DELETE_WINDOW", self._safe_exit)

        except (tk.TclError, Exception) as exc:
            messagebox.showerror("Ошибка интерфейса", f"Ошибка создания главного меню: {exc}")

    def _init_ui(self) -> None:
        """
        Создание и адаптивное размещение элементов интерфейса (сетка и статус).
        Использует grid_rowconfigure и grid_columnconfigure для растягивания.
        """
        try:
            # Настройка адаптивности главного окна
            self.root.grid_rowconfigure(0, weight=0)  # Статус имеет фиксированную высоту
            self.root.grid_rowconfigure(1, weight=1)  # Игровое поле занимает всё свободное место
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

        except (tk.TclError, Exception) as exc:
            messagebox.showerror("Ошибка интерфейса", f"Ошибка инициализации игрового поля: {exc}")

    def _on_cell_click(self, row: int, col: int) -> None:
        """
        Безопасный обработчик нажатия на ячейку игрового поля.

        :param row: Индекс строки (0..2).
        :param col: Индекс столбца (0..2).
        """
        try:
            # Валидация индексов и состояния игры
            if not (0 <= row < 3 and 0 <= col < 3):
                raise IndexError(f"Некорректные координаты ячейки: ({row}, {col})")

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

        except (tk.TclError, IndexError, Exception) as exc:
            messagebox.showerror("Ошибка хода", f"Произошла ошибка при обработке нажатия: {exc}")

    def _check_win(self, player: str) -> Optional[List[Tuple[int, int]]]:
        """
        Проверка наличия выигрышной комбинации для указанного игрока.

        :param player: Символ игрока ('X' или 'O').
        :return: Список координат (row, col) выигрышных ячеек или None.
        """
        try:
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
        except Exception as exc:
            messagebox.showerror("Ошибка логики", f"Сбой при проверке условий победы: {exc}")
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
        try:
            for row, col in combo:
                self.buttons[row][col].config(bg="#c8e6c9", activebackground="#a5d6a7")
        except (tk.TclError, Exception) as exc:
            messagebox.showerror("Ошибка оформления", f"Не удалось выделить ячейки: {exc}")

    def reset_game(self) -> None:
        """Сброс игрового поля и запуск нового раунда игры."""
        try:
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
        except (tk.TclError, Exception) as exc:
            messagebox.showerror("Ошибка сброса", f"Не удалось перезапустить игру: {exc}")

    def _show_rules(self) -> None:
        """Отображение диалогового окна со справочной информацией о правилах."""
        try:
            rules_text: str = (
                "Правила игры «Крестики-нолики»:\n\n"
                "1. Игра рассчитана на двух игроков (X и O).\n"
                "2. Игроки по очереди ставят свои знаки на свободные клетки поля 3x3.\n"
                "3. Первый игрок ходит крестиками (X).\n"
                "4. Побеждает игрок, первым выстроивший ряд из 3 своих знаков "
                "по горизонтали, вертикали или диагонали.\n"
                "5. Если поле заполнено и победная комбинация не собрана, объявляется ничья."
            )
            messagebox.showinfo("Правила игры", rules_text)
        except (tk.TclError, Exception) as exc:
            messagebox.showerror("Ошибка", f"Не удалось отобразить правила: {exc}")

    def _show_about(self) -> None:
        """Отображение диалогового окна с информацией об авторе программы."""
        try:
            about_text: str = (
                "Лабораторная работа №3\n"
                "Дисциплина: «Прикладное программирование»\n"
                "Тема: «Приложения с графическим интерфейсом»\n\n"
                "Автор: Ткачук Дмитрий Владимирович\n"
                "Группа: ИДБ-25-15\n"
                "Вуз: ФГБОУ ВО «МГТУ «СТАНКИН»\n"
                "Год: 2026"
            )
            messagebox.showinfo("Об авторе", about_text)
        except (tk.TclError, Exception) as exc:
            messagebox.showerror("Ошибка", f"Не удалось отобразить информацию об авторе: {exc}")

    def _trigger_test_error(self) -> None:
        """
        Метод для демонстрации обработки исключительных ситуаций.
        Искусственно генерирует исключение для демонстрации диалогового окна ошибки.
        """
        try:
            # Имитация сбоя при выполнении критической операции
            raise RuntimeError("Демонстрация перехвата исключения: сбой пользовательского действия!")
        except Exception as exc:
            messagebox.showerror(
                "Тестовая ошибка (демонстрация try-except)",
                f"Успешно перехвачено исключение:\nТип: {type(exc).__name__}\nСообщение: {exc}"
            )

    def _safe_exit(self) -> None:
        """Безопасное завершение работы программы с подтверждением."""
        try:
            if messagebox.askyesno("Выход", "Вы действительно хотите выйти из игры?"):
                self.root.destroy()
        except (tk.TclError, Exception):
            self.root.destroy()

    def run(self) -> None:
        """Запуск главного цикла обработки событий приложения."""
        try:
            self.root.mainloop()
        except (tk.TclError, Exception) as exc:
            messagebox.showerror("Критическая ошибка", f"Сбой в главном цикле событий: {exc}")


if __name__ == "__main__":
    app = TicTacToe()
    app.run()
