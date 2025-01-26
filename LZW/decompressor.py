def decompress(input_file, output_file):
    # Инициализируем словарь с начальными символами ASCII
    dictionary = {i: chr(i) for i in range(256)}
    dict_size = 256

    # Читаем сжатые данные
    with open(input_file, 'rb') as file:
        data = []
        while (chunk := file.read(2)):
            data.append(int.from_bytes(chunk, byteorder='big'))

    # Алгоритм LZW для разжатия
    w = chr(data.pop(0))
    result = [w]
    for k in data:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError("Ошибка в данных.")

        result.append(entry)

        # Добавляем новую последовательность в словарь
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        w = entry

    # Записываем разжатый результат в файл
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(''.join(result))

    print("Разжатие завершено.")


# Использование
decompress('compressed.txt', 'decompressed.txt')
