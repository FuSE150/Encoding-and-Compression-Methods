from collections import Counter


# Функция для разделения списка символов по их вероятностям
def shannon_fano_split(symbols):
    total = sum([freq for _, freq in symbols])
    partial_sum = 0
    for i in range(len(symbols)):
        partial_sum += symbols[i][1]
        if partial_sum >= total / 2:
            return symbols[:i + 1], symbols[i + 1:]


# Рекурсивная функция для кодирования символов
def shannon_fano_recursive(symbols, prefix="", shannon_fano_codes={}):
    if len(symbols) == 1:
        char, _ = symbols[0]
        shannon_fano_codes[char] = prefix
        return

    # Разделяем символы на две группы
    left, right = shannon_fano_split(symbols)

    # Присваиваем "0" левым и "1" правым символам
    shannon_fano_recursive(left, prefix + "0", shannon_fano_codes)
    shannon_fano_recursive(right, prefix + "1", shannon_fano_codes)


# Генерация кодов Шеннона-Фано
def shannon_fano_encode(text):
    # Подсчет частоты символов
    frequency = Counter(text)

    # Сортировка символов по убыванию частоты
    symbols = sorted(frequency.items(), key=lambda item: item[1], reverse=True)

    # Генерация кодов Шеннона-Фано
    shannon_fano_codes = {}
    shannon_fano_recursive(symbols, "", shannon_fano_codes)

    # Кодирование текста
    encoded_text = ''.join([shannon_fano_codes[char] for char in text])

    return encoded_text, shannon_fano_codes


# Декодирование текста
def shannon_fano_decode(encoded_text, shannon_fano_codes):
    reverse_shannon_fano_codes = {v: k for k, v in shannon_fano_codes.items()}

    decoded_text = ""
    buffer = ""
    for bit in encoded_text:
        buffer += bit
        if buffer in reverse_shannon_fano_codes:
            decoded_text += reverse_shannon_fano_codes[buffer]
            buffer = ""

    return decoded_text


# Пример использования
if __name__ == "__main__":
    text = "привет, меня зовут Фьюз"

    encoded_text, shannon_fano_codes = shannon_fano_encode(text)
    print(f"Encoded text: {encoded_text}")
    print(f"Shannon-Fano Codes: {shannon_fano_codes}")

    decoded_text = shannon_fano_decode(encoded_text, shannon_fano_codes)
    print(f"Decoded text: {decoded_text}")
