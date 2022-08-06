import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from calculator_ui import Ui_MainWindow
from PyQt6.QtGui import QFontDatabase
from typing import Union, Optional
from operator import add, sub, mul, truediv
from decimal import Decimal


class Calculator_app(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        QFontDatabase.addApplicationFont("fonts/Rubik-Regular.ttf")

        self.num = '0'  # entry number
        self.exp_num = ''   # expression number
        self.math_oper = ''  # math operator
        self.result = '0'
        self.max_length = 18
        self.expression_added = False
        self.calculated = False
        self.computed = False
        self.default_font_size = 16
        self.num_lable_font_size = 40

        self.math_operations = {
            '+': add,
            '-': sub,
            'x': mul,
            '/': truediv
        }

        # buttons
        self.digit_buttons = (
            self.ui.btn_0, self.ui.btn_1, self.ui.btn_2,
            self.ui.btn_3, self.ui.btn_4, self.ui.btn_5,
            self.ui.btn_6, self.ui.btn_7, self.ui.btn_8,
            self.ui.btn_9
        )
        self.operator_buttons = (
            self.ui.btn_addition, self.ui.btn_subtraction,
            self.ui.btn_multiplication, self.ui.btn_division
        )

        for btn in self.digit_buttons:
            btn.clicked.connect(self.add_digit)

        for btn in self.operator_buttons:
            btn.clicked.connect(self.add_expression)

        # actions
        self.ui.btn_backspace.clicked.connect(self.backspace)
        self.ui.btn_clear_num.clicked.connect(self.clear_num)
        self.ui.btn_clear_all.clicked.connect(self.clear_all)
        self.ui.btn_point.clicked.connect(self.add_point)
        self.ui.btn_negate.clicked.connect(self.add_negation)

        # math
        self.ui.btn_equals.clicked.connect(self.compute)

    def backspace(self):
        if len(self.num) != 1:
            if len(self.num) == 2 and '-' in self.num:
                self.num = '0'
            else:
                self.num = self.num[:-1]
        else:
            self.num = '0'

        if self.computed:
            self.clear_all()

        self.disable_buttons(False)
        self.ui.num_label.setText(self.num)
        self.adjust_labels_font_size()

    def clear_num(self):
        self.num = '0'
        self.ui.num_label.setText(self.num)
        self.adjust_labels_font_size()

        if self.computed:
            self.clear_all()

        self.disable_buttons(False)

    def clear_all(self):
        self.num = "0"
        self.exp_num = ''
        self.result = "0"
        self.math_oper = ''
        self.ui.num_label.setText(self.num)
        self.adjust_labels_font_size()
        self.ui.exp_label.setText(self.exp_num)
        self.expression_added = False
        self.calculated = False
        self.computed = False
        self.disable_buttons(False)

    def add_digit(self):
        btn = self.sender()

        if not self.computed and (self.num == '0' or self.expression_added):
            self.num = btn.text()
        elif self.computed:
            self.clear_all()
            self.num = btn.text()
        elif len(self.num) < self.max_length:
            self.num += btn.text()

        self.disable_buttons(False)
        self.ui.num_label.setText(self.num)
        self.adjust_labels_font_size()
        self.expression_added = False
        self.calculated = False
        self.computed = False

    def add_point(self):
        if self.expression_added:
            self.num = '0'
            self.expression_added = False

        if self.computed:
            self.clear_all()

        if '.' not in self.num:
            self.num += '.'

        self.ui.num_label.setText(self.num)
        self.adjust_labels_font_size()

    def add_negation(self):
        if '-' not in self.num:
            if self.num != '0':
                self.num = '-' + self.num
        else:
            self.num = self.num[1:]

        if self.computed:
            if self.result != '0':
                temp = '-' + self.result
                self.clear_all()
                self.num = temp

        self.ui.num_label.setText(self.num)
        self.adjust_labels_font_size()

    def add_expression(self):
        try:
            btn = self.sender()
            self.num = self.remove_trailing_zeros(self.num)

            if self.exp_num and not self.calculated and not self.expression_added:
                self.num = str(self.calculate(self.exp_num, self.num))
                self.result = self.num
            elif self.computed:
                self.num = self.result
                self.computed = False

            self.exp_num = self.num
            self.math_oper = btn.text()
            self.ui.num_label.setText(self.num)
            self.adjust_labels_font_size()
            self.ui.exp_label.setText(f'{self.exp_num} {self.math_oper}')
            self.expression_added = True

        except ZeroDivisionError:
            self.clear_all()
            self.disable_buttons(True)
            self.ui.num_label.setText('Деление на ноль невозможно')

    def compute(self):
        try:
            self.num = self.remove_trailing_zeros(self.num)

            if self.math_oper == '':
                self.result = self.num
                self.ui.exp_label.setText(f'{self.result} =')
            elif not self.calculated:
                self.result = str(self.calculate(self.exp_num, self.num))
                self.ui.exp_label.setText(f'{self.exp_num} {self.math_oper} {self.num} =')
            else:
                self.ui.exp_label.setText(f'{self.result} {self.math_oper} {self.num} =')
                self.result = str(self.calculate(self.result, self.num))

            self.ui.num_label.setText(self.result)
            self.adjust_labels_font_size()
            self.computed = True

        except ZeroDivisionError:
            self.clear_all()
            self.disable_buttons(True)
            self.ui.num_label.setText('Деление на ноль невозможно')
            self.adjust_labels_font_size()

    def calculate(self, f_num, s_num):
        num = Decimal(s_num)
        exp_num = Decimal(f_num)

        try:
            result = self.math_operations[self.math_oper](exp_num, num)
            self.calculated = True
            return self.remove_trailing_zeros(result)

        except ZeroDivisionError as error:
            raise ZeroDivisionError(error)

    def disable_buttons(self, disable: bool):
        self.ui.btn_subtraction.setDisabled(disable)
        self.ui.btn_addition.setDisabled(disable)
        self.ui.btn_multiplication.setDisabled(disable)
        self.ui.btn_division.setDisabled(disable)
        self.ui.btn_negate.setDisabled(disable)
        self.ui.btn_point.setDisabled(disable)

        color = 'color: #888;' if disable else 'color: white;'
        self.change_buttons_color(color)

    def change_buttons_color(self, css_color: str):
        self.ui.btn_subtraction.setStyleSheet(css_color)
        self.ui.btn_addition.setStyleSheet(css_color)
        self.ui.btn_multiplication.setStyleSheet(css_color)
        self.ui.btn_division.setStyleSheet(css_color)
        self.ui.btn_negate.setStyleSheet(css_color)
        self.ui.btn_point.setStyleSheet(css_color)

    def resizeEvent(self, event):
        self.adjust_labels_font_size()

    def get_num_text_width(self):
        return self.ui.num_label.fontMetrics().boundingRect(self.ui.num_label.text()).width()

    def get_exp_text_width(self):
        return self.ui.exp_label.fontMetrics().boundingRect(self.ui.exp_label.text()).width()

    def adjust_font_size(self, default_font_size, label, get_label_width_func, style):
        font_size = default_font_size

        while get_label_width_func() > label.width() - 10:
            font_size -= 1
            label.setStyleSheet(f'font-size: {str(font_size)}pt; {style}')

        font_size = 1

        while get_label_width_func() < label.width() - 30:
            font_size += 1

            if font_size > default_font_size:
                break

            label.setStyleSheet(f'font-size: {str(font_size)}pt; {style}')

    def adjust_labels_font_size(self):
        self.adjust_font_size(40, self.ui.num_label, self.get_num_text_width, 'border: none;')
        self.adjust_font_size(16, self.ui.exp_label, self.get_exp_text_width, 'color: #888; font-weight: 400;')

    @staticmethod
    def remove_trailing_zeros(number):
        num = str(float(number))
        return num[:-2] if num[-2:] == '.0' else num

    @staticmethod
    def str_to_num(str):
        return float(str) if '.' in str else int(str)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Calculator_app()
    window.show()

    sys.exit(app.exec())
