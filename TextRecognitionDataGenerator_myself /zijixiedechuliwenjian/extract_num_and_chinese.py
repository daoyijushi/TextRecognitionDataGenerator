#  中文 :[\u4e00-\u9fa5]
#  数字 :[1-9]
#
# import re
# cn = []
# with open('char_cn.txt', 'r') as fp:
#
#     lines = fp.readlines()
#     for line in lines:
#         string = re.findall(r'[\u4e00-\u9fa5]|[1-9]', line)
#         if string :
#             print(string)
#             cn.extend(string)
# print(cn)
#
#
# with open(r'char_cn_new.txt', 'w') as f2:
# coding = -*-utf-*-
# import re
# new = ""
# with open(r'char_std_5990.txt') as fp:
#     fw = open("char_std_new.txt", "w")
#     lines = fp.readlines()
#     lines = set(lines)
#     for line in lines:
#         # print(line)
#         # string = re.findall(r'[\u4e00-\u9fa5]|[1-9]', line)
#         # if string:
#         #     #print(string)
#         #     fw.write(string[0]+'\n')
#         # #fw.writelines()
#         fw.write(line)
#
# with open(r'char_std_new.txt','r') as f2:
#     newlines = f2.readlines()
#     for line in newlines:
#         print(line)



# 找出文档中重复的字
d = {}
for line in open('../dicts/char_std_5990.txt'):
    d[line] = d.get(line, 0) + 1

for k, v in d.items():
    if v > 1:
        print(k)