import heapq
from collections import Counter
import json

# Алгоритм Хаффмана
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(text):
    frequency = Counter(text)
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]


def huffman_codes(node, prefix="", code_map=None):
    if code_map is None:
        code_map = {}

    if node.char is not None:
        code_map[node.char] = prefix
    else:
        huffman_codes(node.left, prefix + "0", code_map)
        huffman_codes(node.right, prefix + "1", code_map)

    return code_map


def huffman_encoding(text):
    root = build_huffman_tree(text)
    code_map = huffman_codes(root)
    return ''.join(code_map[char] for char in text), code_map


# Алгоритм Шеннона-Фано
def shannon_fano(freq_dict):
    items = sorted(freq_dict.items(), key=lambda item: item[1], reverse=True)
    code_map = {}

    def split(items):
        total = sum([item[1] for item in items])
        running_sum = 0
        for i, item in enumerate(items):
            running_sum += item[1]
            if running_sum >= total / 2:
                return items[:i + 1], items[i + 1:]

    def recursive_build(items, prefix=""):
        if len(items) == 1:
            code_map[items[0][0]] = prefix or "0"
            return
        left, right = split(items)
        recursive_build(left, prefix + "0")
        recursive_build(right, prefix + "1")

    recursive_build(items)
    return code_map


def shannon_encoding(text):
    frequency = Counter(text)
    code_map = shannon_fano(frequency)
    return ''.join(code_map[char] for char in text), code_map


# Запись закодированного текста в бинарный файл
def write_binary_file(file_path, encoded_text):
    binary_file_path = file_path.replace(".txt", "_encoded")
    with open(binary_file_path, 'wb') as binary_file:
        byte_array = bytearray()
        for i in range(0, len(encoded_text), 8):
            byte_chunk = encoded_text[i:i + 8]
            byte_array.append(int(byte_chunk, 2))
        binary_file.write(byte_array)


# Сохранение таблицы кодов в JSON формате
def write_code_map(file_path, code_map):
    code_map_file_path = file_path.replace(".txt", "_code_map.json")
    with open(code_map_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(code_map, json_file, ensure_ascii=False, indent=4)


# Кодирование файла и запись закодированных данных
def encode_file(file_path, method="huffman"):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    if method == "huffman":
        encoded_text, code_map = huffman_encoding(text)
    elif method == "shannon":
        encoded_text, code_map = shannon_encoding(text)
    else:
        raise ValueError("Неизвестный метод кодирования")

    # Запись закодированного текста в бинарный файл
    write_binary_file(file_path, encoded_text)
    write_code_map(file_path, code_map)

    return encoded_text, code_map


# Пример использования
def main():
    file_path = input("Введите путь к текстовому файлу (.txt): ")
    print("Выберите метод кодирования:")
    print("1. Хаффман")
    print("2. Шеннон-Фано")
    choice = input("Ваш выбор (1/2): ")

    if choice == '1':
        method = "huffman"
    elif choice == '2':
        method = "shannon"
    else:
        print("Неверный выбор!")
        return

    encode_file(file_path, method)
    print(f"Файл {file_path} успешно закодирован и сохранен как {file_path.replace('.txt', '_encoded')}, таблица кодов сохранена в {file_path.replace('.txt', '_code_map.json')}.")


if __name__ == "__main__":
    main()
