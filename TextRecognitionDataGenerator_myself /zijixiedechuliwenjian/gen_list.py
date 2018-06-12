with open("../dicts/char_cn_xiao.txt") as f:
    lines = f.readlines()
    print(lines)
    for i, char in enumerate(lines):
        print(i, ":", char)

print(char)