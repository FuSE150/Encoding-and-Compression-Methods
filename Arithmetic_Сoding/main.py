import tkinter as tk
from tkinter import messagebox
import sys

class ArithmeticCoding:
    def __init__(self, probabilities, precision=50):
        self.probabilities = probabilities
        self.intervals = self._build_intervals()

    def _build_intervals(self):
        # Построить интервалы для символов на основе вероятностей.
        intervals = {}
        low = 0.0
        for char, prob in self.probabilities.items():
            high = low + prob
            intervals[char] = (low, high)
            low = high
        return intervals

    def encode(self, text):
        # Закодировать текст в число.
        low, high = 0.0, 1.0
        for char in text:
            char_low, char_high = self.intervals[char]
            range_ = high - low
            high = low + range_ * char_high
            low = low + range_ * char_low
        return (low + high) / 2

    def decode(self, code, length):
        # Декодировать число обратно в текст.
        text = []
        for _ in range(length):
            for char, (char_low, char_high) in self.intervals.items():
                if char_low <= code < char_high:
                    text.append(char)
                    code = (code - char_low) / (char_high - char_low)
                    break
        return ''.join(text)


class ArithmeticCodingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Arithmetic Coding")

        self.ac = ArithmeticCoding(probabilities)

        self.create_widgets()

    def create_widgets(self):
        self.text_label = tk.Label(self.root, text="Введите текст для кодирования:")
        self.text_label.pack()

        self.text_entry = tk.Entry(self.root, width=50)
        self.text_entry.pack()

        self.encode_button = tk.Button(self.root, text="Закодировать", command=self.encode_text)
        self.encode_button.pack()

        self.encoded_label = tk.Label(self.root, text="Закодированное значение:")
        self.encoded_label.pack()

        self.encoded_value = tk.Label(self.root, text="")
        self.encoded_value.pack()

        self.decode_button = tk.Button(self.root, text="Декодировать", command=self.decode_text)
        self.decode_button.pack()

        self.decoded_label = tk.Label(self.root, text="Декодированный текст:")
        self.decoded_label.pack()

        self.decoded_text = tk.Label(self.root, text="")
        self.decoded_text.pack()

        self.size_label = tk.Label(self.root, text="Размеры:")
        self.size_label.pack()

        self.size_text = tk.Label(self.root, text="")
        self.size_text.pack()

    def encode_text(self):
        text = self.text_entry.get()
        if not text:
            messagebox.showerror("Ошибка", "Введите текст для кодирования!")
            return

        original_size = sys.getsizeof(text)
        encoded_value = self.ac.encode(text)

        # Обновляем GUI с результатами кодирования
        self.encoded_value.config(text=f"{encoded_value:.50f}")

        # Отображаем размер до и после сжатия
        encoded_size = sys.getsizeof(encoded_value)
        self.size_text.config(text=f"До сжатия: {original_size} байт\nПосле сжатия: {encoded_size} байт")

    def decode_text(self):
        encoded_value = self.encoded_value.cget("text")
        if not encoded_value:
            messagebox.showerror("Ошибка", "Сначала закодируйте текст!")
            return

        try:
            encoded_value = float(encoded_value)
            text_length = len(self.text_entry.get())
            decoded_text = self.ac.decode(encoded_value, text_length)
            self.decoded_text.config(text=decoded_text)
        except ValueError:
            messagebox.showerror("Ошибка", "Ошибка при декодировании!")


# Вероятности символов
probabilities = {
    'a': 0.0575, 'b': 0.0128, 'c': 0.0263, 'd': 0.0285, 'e': 0.0913, 'f': 0.0173,
    'g': 0.0133, 'h': 0.0313, 'i': 0.0599, 'j': 0.0006, 'k': 0.0084, 'l': 0.0335,
    'm': 0.0235, 'n': 0.0596, 'o': 0.0689, 'p': 0.0192, 'q': 0.0008, 'r': 0.0508,
    's': 0.0567, 't': 0.0706, 'u': 0.0334, 'v': 0.0069, 'w': 0.0119, 'x': 0.0073,
    'y': 0.0164, 'z': 0.0007, ' ': 0.1928
}

if __name__ == "__main__":
    root = tk.Tk()
    app = ArithmeticCodingGUI(root)
    root.mainloop()
