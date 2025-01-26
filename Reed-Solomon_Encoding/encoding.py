from reedsolo import RSCodec


def encode_file(input_file, output_file, num_error_symbols=4):
    rsc = RSCodec(num_error_symbols)
    with open(input_file, 'rb') as file:
        data = file.read()

    # Кодируем данные
    encoded_data = rsc.encode(data)
    print(f"Оригинальные данные: {data}")
    print(f"Закодированные данные: {encoded_data}")

    # Конвертируем байты в строку с \x перед каждым байтом
    encoded_str = ''.join(f'\\x{byte:02x}' for byte in encoded_data)

    # Записываем результат в файл
    with open(output_file, 'w') as encoded_file:
        encoded_file.write(encoded_str)
    print(f"Данные успешно записаны в файл {output_file} в формате \\x...")


if __name__ == "__main__":
    encode_file("text.txt", "encoded_text.txt")
