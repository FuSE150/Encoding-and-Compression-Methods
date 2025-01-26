from reedsolo import RSCodec, ReedSolomonError


def decode_file(input_file, output_file, num_error_symbols=4):
    rsc = RSCodec(num_error_symbols)
    with open(input_file, 'r') as file:
        hex_string = file.read().replace('\\x', '')
        encoded_data = bytes.fromhex(hex_string)
    print(f"Прочитанные закодированные данные: {encoded_data}")

    try:
        # Декодируем данные
        decoded_data, _, _ = rsc.decode(encoded_data)
        print(f"Декодированные данные: {decoded_data}")

        # Сравниваем данные перед декодированием и после, чтобы найти ошибки
        error_positions = []
        for i in range(min(len(encoded_data), len(decoded_data))):
            if encoded_data[i] != decoded_data[i]:
                error_positions.append(i)

        # Выводим результаты
        if error_positions:
            print(f"Найдено ошибок: {len(error_positions)}")
            print("Позиции ошибок:", error_positions)
        else:
            print("Ошибки не найдены.")

    except ReedSolomonError as e:
        print("Ошибка декодирования:", e)
        return

    # Сохраняем декодированные данные в новый файл
    with open(output_file, 'wb') as decoded_file:
        decoded_file.write(decoded_data)
    print(f"Декодированные данные успешно записаны в файл {output_file}")


if __name__ == "__main__":
    decode_file("encoded_text.txt", "decoded_text.txt")
