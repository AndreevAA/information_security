import random
import struct
import sys
import os


class Node:

    def __init__(self, value, freq, parent=None, left=None, right=None):
        self.value = value
        self.freq = freq
        self.parent = parent
        self.left = left
        self.right = right

    @staticmethod
    def sort_by_freq(node):
        return node.freq

    def __repr__(self):
        res = ""
        res += "\nValue: {}".format(self.value)
        res += "\nFreq: {}".format(self.freq)
        res += "\nParent: {}".format(id(self.parent))
        res += "\nLeft value: {}".format(id(self.left))
        res += "\nRignt value: {}".format(id(self.right))
        return res


class Huffman:

    def __init__(self, filename):
        self.table = self.make_frequency_table(filename)
        self.codes_table = self.make_codes_table()

    # создаем таблицу частот, где индекс в таблице = код символа ASCII
    def make_frequency_table(self, filename):
        table = [0] * 256
        with open(filename, "rb") as f:
            while True:
                s = f.read(1024)
                print(s)
                if not len(s):
                    break
                else:
                    for item in s:
                        table[item] += 1
        return table

        # строим таблицу кодов

    def make_codes_table(self):

        # создаем список свободных узлов
        nodes = []
        for i in range(len(self.table)):
            if self.table[i] > 0:
                nodes.append(Node(i, self.table[i]))

        leafs = []  # Список "листьев" дерева
        codes = []  # Таблица кодов

        # создаем дерево
        # создаем один узел, объединяя два узла с наименьшими весами, записываем в список

        if len(nodes) == 1:
            leafs.append(nodes[0])
            codes.append((nodes[0].value, "0"))
            return codes

        while len(nodes) > 1:
            nodes.sort(key=Node.sort_by_freq)  # сортируем узлы по весам
            left, right = nodes.pop(0), nodes.pop(0)  # выбираем два узла с наименьшими весами
            new_node = Node(None, left.freq + right.freq, None, left, right)  # создаем новый узел
            left.parent = new_node
            right.parent = new_node

            # добавляем листья в новый список
            if (left.value != None):
                leafs.append(left)

            if (right.value != None):
                leafs.append(right)

            # добавляем новый узел в список
            nodes.append(new_node)

        # создаем таблицу кодов
        for leaf in leafs:
            code = ""
            node = leaf
            # проход по дереву до корня
            while True:
                parent = node.parent
                if parent == None:
                    break
                if node == parent.left:
                    code += "0"
                if node == parent.right:
                    code += "1"
                node = parent
            codes.append((leaf.value, code[::-1]))  # добавляем в таблицу кортеж (символ, код)

        return codes

    def bit_str_to_byte(self, s):
        return struct.pack('B', int(s, 2))

    def find_code(self, num):
        for i in range(len(self.codes_table)):
            if self.codes_table[i][0] == num:
                return self.codes_table[i][1]

        raise "Incorrect code table!"

    def find_byte(self, code):
        for i in range(len(self.codes_table)):
            if self.codes_table[i][1] == code:
                return self.codes_table[i][0]

        return None

        # сжатие файла

    def compress(self, filename):

        codes_filename = "codes.txt"
        # создание файла с кодами
        with open(codes_filename, "w") as codes_f:
            for item in self.codes_table:
                codes_f.write("{} {}\n".format(item[0], item[1]))

        # сжатие
        zeroes = 0
        res_filename = "compressed_" + filename
        with open(filename, "rb") as f, open(res_filename, "wb") as res_f:
            code_str = ""
            while True:
                s = f.read(1024)
                if not len(s):
                    break
                else:
                    for item in s:
                        code = self.find_code(item)
                        code_str += code
                        if len(code_str) >= 8:
                            byte_str = code_str[:8]
                            code_str = code_str[8:]
                            byte = self.bit_str_to_byte(byte_str)
                            res_f.write(byte)

            # дописать биты, если размер кода не кратен 8
            if len(code_str) > 0:
                zeroes = 8 - len(code_str)
                for i in range(zeroes):
                    code_str += '0'
                byte = self.bit_str_to_byte(code_str)
                res_f.write(byte)

        return codes_filename, res_filename, zeroes

    # восстанавливем исходный файл
    def decompress(self, filename, compressed_filename, zeroes):
        res_filename = "decompressed_" + filename
        with open(compressed_filename, "rb") as f, open(res_filename, "wb") as res_f:
            code_str = ""
            while True:
                s = f.read(1024)
                if not len(s):
                    break
                else:
                    for byte in s:
                        code = bin(byte)[2:].zfill(8)
                        code_str += code

            if zeroes:
                code_str = code_str[:-zeroes]

            code = ""
            while len(code_str):
                code += code_str[0]
                code_str = code_str[1:]
                byte = self.find_byte(code)

                if byte != None:
                    res_f.write(struct.pack('B', byte))
                    code = ""

        return res_filename


def main():
    try:
        filename = sys.argv[1]
    except IndexError:
        print("Задайте файл с помощью аргументов командной строки")
        return

    if not os.path.exists(filename):
        print("Файл не найден!")
        return

    print("Исходный файл: '{}' ({} байт)".format(filename, os.path.getsize(filename)))

    huf = Huffman(filename)
    print(huf.codes_table, huf.table)
    codes_filename, res_filename, zeroes = huf.compress(filename)
    print("Сжатый файл: '{}'  ({} байт)".format(res_filename,  os.path.getsize(res_filename)))
    print("Размер таблицы кодов: {} байт".format(sys.getsizeof(huf.codes_table)))
    print("Нулей дописано в последний байт:", zeroes)

    dec_filename = huf.decompress(filename, res_filename, zeroes)
    print("Восстановленный файл: '{}'  ({} байт)".format(dec_filename,  os.path.getsize(dec_filename)))


if __name__ == '__main__':
    main()
