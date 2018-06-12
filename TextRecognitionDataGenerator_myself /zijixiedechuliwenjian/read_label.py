def readfile(filename):
    res = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        #print("lines", lines)
        for i in lines:
            res.append(i.strip())
            #print("i", i)
    dic = {}
    for i in res:
        p = i.split(' ')
        dic[p[0]] = p[1:]
        #print("dic", dic)
    return dic

image_label = readfile("../out/chinese_dataset_test_5990.txt")   #这一步貌似没有错
#print("image_label", image_label)
_imagefile = [i for i, j in image_label.items()]
print(_imagefile)
