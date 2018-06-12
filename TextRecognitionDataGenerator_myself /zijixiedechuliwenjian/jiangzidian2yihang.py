string = ""
with open("../dicts/char_cn_xiao.txt") as f:
    lines = f.readlines()
    #string = string + lines

    #print(lines)
    for i, char in enumerate(lines):
        char = char.replace("\n", "")
        print(char)
        string = string + str(char)
print(string)