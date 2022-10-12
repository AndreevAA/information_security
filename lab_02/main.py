import random
import base64
from os.path import basename, splitext
ASCII = 256


# заполнение ротора элементами ASCII-кода
def new_rotor():
    rotor = [None for _ in range(ASCII)]

    cur_num = 0
    while None in rotor:
        index = random.randint(0, ASCII - 1)
        if rotor[index] is None:
            rotor[index] = cur_num
            cur_num += 1

    return rotor


# заполнение рефлектора элементами ASCII-кода
def new_reflector():
    reflector = [None for _ in range(ASCII)]
    mas = [x for x in range(ASCII)]

    for i in range(ASCII):
        if reflector[i] is None:
            num = random.choice(mas)
            while num == i:
                num = random.choice(mas)
            mas.pop(mas.index(num))
            mas.pop(mas.index(i))
            reflector[i] = num
            reflector[num] = i

    return reflector


# шифрование символа
def encrypt(s, rotor1, rotor2, rotor3, reflector):
    s1 = rotor1.index(s)
    s2 = rotor2.index(s1)
    s3 = rotor3.index(s2)
    s4 = reflector.index(s3)
    s5 = rotor3[s4]
    s6 = rotor2[s5]
    s7 = rotor1[s6]

    return s7


# проворачиваем роторы и шифруем сообщение
def encrypt_message(msg, rotor1, rotor2, rotor3, reflector):
    nums = [ord(c) for c in msg]
    res_msg = []
    shift1 = 0
    shift2 = 0
    shift3 = 0
    for s in nums:
        res_msg.append(encrypt(s, rotor1, rotor2, rotor3, reflector))
        if shift1 < ASCII:
            rotor1 = rotor1[1:] + rotor1[:1]
            shift1 += 1
        elif shift2 < ASCII:
            rotor1 = rotor1[1:] + rotor1[:1]
            rotor2 = rotor2[1:] + rotor2[:1]
            shift1 = 0
            shift2 += 1
        elif shift3 < ASCII:
            rotor1 = rotor1[1:] + rotor1[:1]
            rotor2 = rotor2[1:] + rotor2[:1]
            rotor3 = rotor3[1:] + rotor3[:1]
            shift1 = 0
            shift2 = 0
            shift3 += 1
        else:
            rotor1 = rotor1[1:] + rotor1[:1]
            rotor2 = rotor2[1:] + rotor2[:1]
            rotor3 = rotor3[1:] + rotor3[:1]
            shift1 = 0
            shift2 = 0
            shift3 = 0

    return ''.join([chr(c) for c in res_msg])


def log(rotor1, rotor2, rotor3, reflector, file_path):
    with open("log.txt", 'a') as file:
        file.write(file_path + '\n' + str(rotor1) + '\n' + str(rotor2) + '\n'
                   + str(rotor3) + '\n' + str(reflector) + '\n')
        file.close()


def find_state(file_name):
    file = open("log.txt")
    data = file.read().split('\n')
    matches = []
    for i in range(len(data)):
        if data[i] == file_name:
            matches.append(data[i + 1])
            matches.append(data[i + 2])
            matches.append(data[i + 3])
            matches.append(data[i + 4])
    if len(matches) < 4:
        return [], [], [], []

    rotor1 = list(map(int, matches[-4][1:-1].split(', ')))
    rotor2 = list(map(int, matches[-3][1:-1].split(', ')))
    rotor3 = list(map(int, matches[-2][1:-1].split(', ')))
    reflector = list(map(int, matches[-1][1:-1].split(', ')))

    return rotor1, rotor2, rotor3, reflector


def main():

    choice = None
    while choice != '0':
        print("""
            Действие.
            1 - шифрация
            2 - дешифрация
            
            0 - выход 
        """)
        choice = input("Выбор: ")
        next_choice = None
        if choice == '1':
            while next_choice != '0':
                print("""
                    Что шифровать.
                    1 - строку
                    2 - файл
                    
                    0 - назад
                """)
                rotor1 = new_rotor()
                rotor2 = new_rotor()
                rotor3 = new_rotor()
                reflector = new_reflector()
                next_choice = input("Выбор: ")
                if next_choice == '1':
                    msg = input("Введите сообщение: ")
                    msg = base64.b64encode(msg.encode("UTF-8")).decode('ascii')
                    msg_enc = encrypt_message(msg, rotor1, rotor2, rotor3, reflector)
                    print("Зашифрованное сообщение: ", msg_enc)

                    flag = input("Хотите ли расшифровать сообщение? (1 - да, 0 - нет):  ")
                    if flag == '1':
                        msg_decr = encrypt_message(msg_enc, rotor1, rotor2, rotor3, reflector)
                        msg_decr = base64.b64decode(msg_decr).decode("UTF-8")
                        print("Расшифрованное сообщение: " + msg_decr)

                elif next_choice == '2':
                    file_path = input("Введите путь к файлу: ")
                    try:
                        with open(file_path, 'rb') as f:
                            msg = base64.b64encode(f.read()).decode('ascii')
                            msg_enc = encrypt_message(msg, rotor1, rotor2, rotor3, reflector)
                            f.close()

                        file_name = basename(file_path)
                        new_file_name = splitext(file_name)[0] + ".encrypt"
                        with open(new_file_name, 'wb') as file:
                            file.write(msg_enc.encode("UTF-8"))
                            file.close()
                        log(rotor1, rotor2, rotor3, reflector, new_file_name)

                    except FileNotFoundError:
                        print("file " + file_path + " not found")

                elif next_choice != '0':
                    print("Неверный ввод. Попробуйте снова.")

        elif choice == '2':
            file_path = input("Введите путь к зашифрованному файлу (расширение .encrypt): ")
            file_name = basename(file_path)
            ext = splitext(file_name)[-1]
            if ext == ".encrypt":
                try:
                    with open(file_path, 'rb') as f:
                        msg_enc = f.read().decode("UTF-8")
                        rotor1, rotor2, rotor3, reflector = find_state(file_name)
                        if len(rotor1) == 0:
                            print("Данный файл не был найден в списке зашифрованных. Невозможно найти конфигурацию.")
                        else:
                            msg_decr = encrypt_message(msg_enc, rotor1, rotor2, rotor3, reflector)
                            with open(splitext(file_name)[0] + ".decrypt", 'wb') as file:
                                file.write(base64.b64decode(msg_decr))
                                file.close()
                        f.close()
                except FileNotFoundError:
                    print("file " + file_path + " not found")
            else:
                print("Неверное расширение.")
        elif choice != '0':
            print("Неверный ввод. Попробуйте снова.")


if __name__ == '__main__':
    main()
