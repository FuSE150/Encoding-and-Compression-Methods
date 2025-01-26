import json

# Чтение бинарного файла и преобразование в двоичную строку
def read_binary_file(file_path):
    with open(file_path, 'rb') as binary_file:
        byte_data = binary_file.read()
        binary_string = ''.join(f'{byte:08b}' for byte in byte_data)
    return binary_string


# Функция для чтения таблицы кодов из JSON файла
def read_code_map(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


# Декодирование текста с использованием таблицы кодов
def decode_text(encoded_text, code_map):
    reverse_code_map = {code: char for char, code in code_map.items()}
    decoded_text = ''
    current_code = ''
    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_code_map:
            decoded_text += reverse_code_map[current_code]
            current_code = ''
    return decoded_text


# Основная функция для декодирования файла
def decode_file(binary_file_path, code_map_file_path):
    encoded_text = read_binary_file(binary_file_path)
    code_map = read_code_map(code_map_file_path)

    decoded_text = decode_text(encoded_text, code_map)

    decoded_file_path = binary_file_path.replace("_encoded", "_decoded.txt")
    with open(decoded_file_path, 'w', encoding='utf-8') as decoded_file:
        decoded_file.write(decoded_text)

    return decoded_text


# Пример использования
def main():
    binary_file_path = input("Введите путь к закодированному файлу (_encoded): ")
    code_map_file_path = input("Введите путь к файлу с таблицей кодов (_code_map.json): ")

    decoded_text = decode_file(binary_file_path, code_map_file_path)
    print(f"Декодированный текст сохранен в {binary_file_path.replace('_encoded', '_decoded.txt')}")


if __name__ == "__main__":
    main()
