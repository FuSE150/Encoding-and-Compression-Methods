def hamming_decode_8bit(encoded_block):
    # Извлекаем проверочные и данные биты
    p1, p2, d1, p3, d2, d3, d4 = map(int, encoded_block[:-1])

    # Вычисление синдрома ошибки
    s1 = (d1 ^ d2 ^ d4) != p1
    s2 = (d1 ^ d3 ^ d4) != p2
    s3 = (d2 ^ d3 ^ d4) != p3

    # Определение позиции ошибки на основании синдрома
    error_position = (s3 << 2) | (s2 << 1) | s1  # Сдвигаем и объединяем

    # Если есть ошибка (позиция не равна 0)
    if error_position:
        print(f"Обнаружена ошибка в позиции: {error_position} для блока: {encoded_block}")
        # Исправляем ошибку, инвертируя бит в этой позиции
        encoded_block = list(encoded_block)
        encoded_block[error_position - 1] = '1' if encoded_block[error_position - 1] == '0' else '0'
        encoded_block = ''.join(encoded_block)
        print(f"Исправленный блок: {encoded_block}")
    else:
        print(f"Ошибок не обнаружено для блока: {encoded_block}")

    # Проверка последнего бита на четность (партитетный бит)
    total_ones = sum(int(bit) for bit in encoded_block[:-1])  # исключаем последний бит
    parity_check = total_ones % 2
    received_parity = int(encoded_block[-1])

    # Если паритетный бит не соответствует, исправляем его
    if parity_check != received_parity:
        print(f"Обнаружена ошибка в паритетном бите для блока: {encoded_block}")
        # Инвертируем паритетный бит
        encoded_block = encoded_block[:-1] + str(1 - received_parity)
        print(f"Исправленный паритетный бит для блока: {encoded_block}")

    # Извлекаем исправленные проверочные и данные биты
    p1, p2, d1, p3, d2, d3, d4 = map(int, encoded_block[:-1])

    # Если ошибки нет, возвращаем 4 бита данных
    decoded_data = f"{d1}{d2}{d3}{d4}"
    print(f"Декодированные данные (4 бита): {decoded_data}")
    return decoded_data


def decode_file_hamming():
    # Получаем закодированное сообщение из файла
    with open("output.txt", "r") as file:
        encoded_message = file.read().strip()  # Считываем и убираем лишние пробелы/переносы строк

    # Разбиваем на блоки по 8 бит
    blocks = [encoded_message[i:i + 8] for i in range(0, len(encoded_message), 8)]
    decoded_bits = []

    for block in blocks:
        print(f"Обрабатываем блок: {block}")
        decoded_data = hamming_decode_8bit(block)
        if decoded_data:
            decoded_bits.append(decoded_data)

    # Объединяем все 4-битные данные в одну строку
    decoded_message = ''.join(decoded_bits)
    print(f"Объединенные декодированные данные: {decoded_message}")

    # Разбиваем по 16 бит и выводим итоговое сообщение
    original_message = [decoded_message[i:i + 16] for i in range(0, len(decoded_message), 16)]
    print(f"Исходные 16-битные блоки: {original_message}")

    # Преобразуем 16-битные данные обратно в символы
    final_message = ''.join(chr(int(original, 2)) for original in original_message if len(original) == 16)
    print(f"Исходное сообщение: {final_message}")

    # Запись декодированного сообщения в файл
    with open("decoded_message.txt", "w", encoding="utf-8") as file:
        file.write(final_message)

    print("Декодированное сообщение успешно сохранено в файл decoded_message.txt")


# Запускаем декодирование
if __name__ == "__main__":
    decode_file_hamming()
