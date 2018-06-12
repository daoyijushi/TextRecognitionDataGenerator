import numpy as np
import numpy.random as random


dict_len = len('../dicts/char_cn_new.txt')
strings = []
strings_name = []





# for _ in range(0, 10):
#     current_string = ""
#     for _ in range(0, random.randint(1, 10) if allow_variable else length):
#         current_string += lang_dict[random.randrange(dict_len)][:-1]
#         #current_string += ' '
#     #strings.append(string_new[:-1])
#
#     #自己加的代码
#     strings_name.append(current_string[:])
#     string = current_string
#     #for i in range(5):
#     weizhi = np.random.randint(len(string))
#     string_new = string.replace(string[weizhi], string[weizhi] + " " * np.random.randint(5))
#     #string_new = string
#
#     print("string:", string)
#     print("string_new:", string_new)
#     print("len", len(string_new))
#     strings.append(string_new[:])
# print(strings)
# print(strings_name)