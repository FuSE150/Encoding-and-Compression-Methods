import chardet
import codecs

SUPPORTED_ENCODINGS = ['utf-8', 'cp866', 'cp1251', 'maccyrillic', 'iso-8859-5']

def detected_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
    return encoding

def convert_encoding(input_file, output_file, target_encoding):
    if target_encoding not in SUPPORTED_ENCODINGS:
        raise ValueError(f"Целевая кодировка '{target_encoding}' не поддерживается")

    try:
        source_encoding = detected_encoding(input_file)
        print(f"Исходная кодировка файла: {source_encoding}")

        with open(input_file, 'r', encoding=source_encoding) as f:
            content = f.read()

        # Проверяем, поддерживается ли целевая кодировка
        try:
            codecs.lookup(target_encoding)
        except LookupError:
            raise ValueError(f"Кодировка '{target_encoding}' не поддерживается")

        with open(output_file, 'w', encoding=target_encoding) as f:
            f.write(content)

        print(f"Файл успешно преобразован в {target_encoding}")
    except Exception as e:
        print(f"Ошибка: {e}")

input_file = 'cp1251.txt' # Путь к исходному файлу
output_file = 'cp10007.txt' # Путь для сохранения преобразованного файла
target_encoding = 'maccyrillic' # Целевая кодировка

convert_encoding(input_file, output_file, target_encoding)
