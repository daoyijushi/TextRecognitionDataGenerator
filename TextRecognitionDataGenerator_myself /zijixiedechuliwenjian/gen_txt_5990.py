from glob import glob
jpg_files = glob("/home/wave/Pictures/dataset_612/test/*.jpg")

# with open("label.txt", "w") as f:
#     for jpg_file in sorted(jpg_files):
#         string = ""
#         s = jpg_file.split("_")[0]
#         #print(len(s))
#         for i in range(10):
#             string += str(s[i]) + " "
#
#         f.write(jpg_file + " " + string + '\n')

with open("../out/xingming_shuzi_test.txt", "w") as f:
    jishu = 1
    for jpg_file in sorted(jpg_files):
        string = ""
        s = jpg_file.split("_")[-2].split("/")[-1]
        s_name = jpg_file.split("/")[-1]
        length = len(s)
        if len(s) < 10 or len(s) > 10:
            continue
        #print(len(s))
        for i in range(len(s)):
            with open("/home/wave/Downloads/自然场景文字识别/TextRecognitionDataGenerator-master/TextRecognitionDataGenerator/dicts/char_cn_new.txt", "r") as fr:
            #with open("/home/wave/Downloads/自然场景文字识别/TextRecognitionDataGenerator-master/TextRecognitionDataGenerator/dicts/char_std_5990.txt", "r") as fr:
                lines = fr.readlines()
                for j, char in enumerate(lines):
                    if s[i] == char.replace("\n", ""):
                        string += str(j) + " "

        f.write(s_name + " " + string + '\n')

        print(jishu)
        jishu += 1
        # if jishu > 10000:
        #     break