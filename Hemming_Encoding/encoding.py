def to_binary(char):
    # Преобразуем символ в двоичный вид UTF-16 (16 бит на символ)
    binary_representation = format(ord(char), '016b')
    print(f"Символ: {char}, UTF-16: {binary_representation}")
    return binary_representation


def hamming_encode_4bit(data_block):
    # Кодирование 4-битного блока методом Хэмминга
    d1, d2, d3, d4 = int(data_block[0]), int(data_block[1]), int(data_block[2]), int(data_block[3])

    # Вычисляем контрольные биты
    p1 = d1 ^ d2 ^ d4  # контрольный бит 1
    p2 = d1 ^ d3 ^ d4  # контрольный бит 2
    p3 = d2 ^ d3 ^ d4  # контрольный бит 4

    # Формируем 7-битный код
    encoded_block = f"{p1}{p2}{d1}{p3}{d2}{d3}{d4}"

    # Добавляем бит чётности к этому блоку
    total_ones = sum(int(bit) for bit in encoded_block)
    parity_bit = 0 if total_ones % 2 == 0 else 1

    # Возвращаем 8-битный код
    final_block = encoded_block + str(parity_bit)
    print(f"4-битный блок: {data_block}, Код Хэмминга с битом чётности: {final_block}")

    return final_block


def encode_file_hamming(input_text):
    # Преобразуем текст в двоичное представление
    print("\n=== Преобразование символов в двоичный вид (UTF-16) ===")
    binary_data = ''.join([to_binary(char) for char in input_text])

    # Разбиваем на блоки по 4 бита
    print("\n=== Разбиение на блоки по 4 бита ===")
    blocks = [binary_data[i:i + 4] for i in range(0, len(binary_data), 4)]
    print(f"Блоки: {blocks}")

    # Кодируем каждый блок методом Хэмминга
    print("\n=== Кодирование каждого 4-битного блока методом Хэмминга ===")
    encoded_blocks = [hamming_encode_4bit(block) for block in blocks]

    # Собираем все закодированные блоки в одно сообщение
    final_message = ''.join(encoded_blocks)

    return final_message


# Считывание данных из файла input.txt
with open("input.txt", "r", encoding="utf-8") as file:
    input_text = file.read().strip()  # Считываем и убираем лишние пробелы/переносы строк

# Кодирование файла методом Хэмминга
print("\n=== Начало процесса кодирования ===")
encoded_message = encode_file_hamming(input_text)

# Сохранение закодированного сообщения в файл output.txt
with open("output.txt", "w") as file:
    file.write(encoded_message)

print("\nЗакодированное сообщение успешно сохранено в output.txt")
