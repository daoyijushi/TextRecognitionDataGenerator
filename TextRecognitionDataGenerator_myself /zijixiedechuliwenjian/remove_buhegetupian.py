# import os
# from glob import glob
#
# jpg_files = glob("/home/wave/Pictures/自己做的汉字识别数据集/*.jpg")
#
# for jpg_file in sorted(jpg_files):
#     s = jpg_file.split("_")[0].split("/")[-1]
#     if len(s) < 10 or len(s) > 10:
#         os.remove(jpg_file)


import os
def del_files(path):
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.startswith("."):
                s = name.split("_")[0]
                if len(s) < 10 or len(s) > 10:
                    os.remove(os.path.join(root, name))
                print("Delete File: " + os.path.join(root, name))

del_files("/home/wave/Pictures/自己做的汉字识别数据集/")