def compress(input_file, output_file):
    # Инициализируем словарь с начальными символами ASCII
    dictionary = {chr(i): i for i in range(256)}
    dict_size = 256
    w = ""
    result = []

    # Читаем данные из файла
    with open(input_file, 'r', encoding='utf-8') as file:
        data = file.read()

    # Алгоритм LZW для сжатия
    for c in data:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            # Добавляем новую последовательность в словарь
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    # Записываем оставшийся символ
    if w:
        result.append(dictionary[w])

    # Записываем сжатый результат в файл
    with open(output_file, 'wb') as file:
        for code in result:
            file.write(code.to_bytes(2, byteorder='big'))

    print("Сжатие завершено.")


# Использование
compress('text.txt', 'compressed.txt')
