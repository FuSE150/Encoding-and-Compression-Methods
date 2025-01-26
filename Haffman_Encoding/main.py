from collections import Counter
import heapq
from graphviz import Digraph

def visualize_tree(node, graph=None, parent=None, edge_label=""):
    if graph is None:
        graph = Digraph('HuffmanTree')

    if node is not None:
        node_id = str(id(node))  # уникальный идентификатор узла
        if node.char is not None:  # если это листовой узел (символ)
            graph.node(node_id, f"{node.char}\n{node.freq}\n{edge_label}")
        else:  # если это внутренний узел
            graph.node(node_id, f"({node.freq})")

        if parent is not None:
            graph.edge(str(id(parent)), node_id, label=edge_label)  # добавляем соединение с пометкой

        # Рекурсивно визуализируем левые и правые дочерние узлы
        if node.left:
            visualize_tree(node.left, graph, node, "0")  # для левого - "0"
        if node.right:
            visualize_tree(node.right, graph, node, "1")  # для правого - "1"

    return graph

# Узел дерева Хаффмана
class Node:
    def __init__(self, char, freq):
        self.char = char  # символ
        self.freq = freq  # частота символа
        self.left = None  # левый дочерний элемент
        self.right = None  # правый дочерний элемент

    # Для работы с приоритетной очередью (кучей)
    def __lt__(self, other):
        return self.freq < other.freq


# Построение дерева Хаффмана
def build_huffman_tree(text):
    # Подсчет частоты символов
    frequency = Counter(text)

    # Создаем очередь с приоритетом для символов
    heap = [Node(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    # Построение дерева Хаффмана
    while len(heap) > 1:
        # Два символа с наименьшей частотой
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        # Создаем новый внутренний узел с суммой частот
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        # Добавляем новый узел обратно в очередь
        heapq.heappush(heap, merged)

    # Корень дерева Хаффмана
    return heap[0]


# Генерация кодов Хаффмана
def generate_huffman_codes(node, prefix="", huffman_codes={}):
    if node is None:
        return

    # Если это листовой узел
    if node.char is not None:
        huffman_codes[node.char] = prefix

    generate_huffman_codes(node.left, prefix + "0", huffman_codes)
    generate_huffman_codes(node.right, prefix + "1", huffman_codes)

    return huffman_codes


# Кодирование строки
def huffman_encode(text):
    # Строим дерево Хаффмана
    root = build_huffman_tree(text)

    # Генерируем коды Хаффмана
    huffman_codes = generate_huffman_codes(root)

    # Кодируем текст
    encoded_text = ''.join([huffman_codes[char] for char in text])

    return encoded_text, huffman_codes


# Декодирование строки
def huffman_decode(encoded_text, huffman_codes):
    reverse_huffman_codes = {v: k for k, v in huffman_codes.items()}

    decoded_text = ""
    buffer = ""
    for bit in encoded_text:
        buffer += bit
        if buffer in reverse_huffman_codes:
            decoded_text += reverse_huffman_codes[buffer]
            buffer = ""

    return decoded_text


# Пример использования
if __name__ == "__main__":
    text = "Сегодня был жаркий день, я сидел на лавочке в парке и ел мороженное"

    encoded_text, huffman_codes = huffman_encode(text)
    print(f"Encoded text: {encoded_text}")
    print(f"Huffman Codes: {huffman_codes}")

    # Визуализация дерева Хаффмана
    root = build_huffman_tree(text)
    graph = visualize_tree(root)
    graph.render('huffman_tree', format='png', view=True)

    decoded_text = huffman_decode(encoded_text, huffman_codes)
    print(f"Decoded text: {decoded_text}")
