#-*- coding:utf-8 -*
import argparse
import os, errno
import random
import re
import requests
import numpy as np

from bs4 import BeautifulSoup
from PIL import Image, ImageFont
from data_generator import FakeTextDataGenerator
from multiprocessing import Pool

def parse_arguments():
    """
        Parse the command line arguments of the program.
    """

    parser = argparse.ArgumentParser(description='Generate synthetic text data for text recognition.')
    parser.add_argument(
        "output_dir",
        type=str,
        nargs="?",
        help="The output directory",
        #default="/home/wave/Pictures/自己做的汉字识别数据集/",
        #default="out/",
        default="/home/wave/Pictures/dataset_612/test",
        #default="/home/wave/Pictures/chinese_dataset_test/",
        #default="/home/wave/Pictures/chinese_dataset_test_528/",
        #default="/home/wave/Pictures/chinese_dataset_wubeijing/train/",
        #default="/home/wave/Pictures/chinese_dataset_606/chinese_dataset_train_606/"
    )
    parser.add_argument(
        "-i",
        "--input_file",
        type=str,
        nargs="?",
        help="When set, this argument uses a specified text file as source for the text",
        default=""
    )
    parser.add_argument(
        "-l",
        "--language",
        type=str,
        nargs="?",
        help="The language to use, should be fr (Français), en (English), es (Español), de (Deutsch), or cn (Chinese).",
        default="en"
    )
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        nargs="?",
        help="The number of images to be created.",
        default=15
    )
    parser.add_argument(
        "-n",
        "--include_numbers",
        action="store_true",
        help="Define if the text should contain numbers. (NOT IMPLEMENTED)",
        default=False
    )
    parser.add_argument(
        "-s",
        "--include_symbols",
        action="store_true",
        help="Define if the text should contain symbols. (NOT IMPLEMENTED)",
        default=False
    )
    parser.add_argument(
        "-w",
        "--length",
        type=int,
        nargs="?",
        help="Define how many words should be included in each generated sample. If the text source is Wikipedia, this is the MINIMUM length",
        default=1
    )
    parser.add_argument(
        "-r",
        "--random",
        action="store_true",
        help="Define if the produced string will have variable word count (with --length being the maximum)",
        default=False
    )
    parser.add_argument(
        "-f",
        "--format",
        type=int,
        nargs="?",
        help="Define the height of the produced images",
        default=32,
    )
    parser.add_argument(
        "-t",
        "--thread_count",
        type=int,
        nargs="?",
        help="Define the number of thread to use for image generation",
        default=1,
    )
    parser.add_argument(
        "-e",
        "--extension",
        type=str,
        nargs="?",
        help="Define the extension to save the image with",
        default="jpg",
    )
    parser.add_argument(
        "-k",
        "--skew_angle",
        type=int,
        nargs="?",
        help="Define skewing angle of the generated text. In positive degrees",
        default=0,
    )
    parser.add_argument(
        "-rk",
        "--random_skew",
        action="store_true",
        help="When set, the skew angle will be randomized between the value set with -k and it's opposite",
        default=False,
    )
    parser.add_argument(
        "-wk",
        "--use_wikipedia",
        action="store_true",
        help="Use Wikipedia as the source text for the generation, using this paremeter ignores -r, -n, -s",
        default=False,
    )
    parser.add_argument(
        "-bl",
        "--blur",
        type=int,
        nargs="?",
        help="Apply gaussian blur to the resulting sample. Should be an integer defining the blur radius",
        default=0,
    )
    parser.add_argument(
        "-rbl",
        "--random_blur",
        action="store_true",
        help="When set, the blur radius will be randomized between 0 and -bl.",
        default=False,
    )
    parser.add_argument(
        "-b",
        "--background",
        type=int,
        nargs="?",
        help="Define what kind of background to use. 0: Gaussian Noise, 1: Plain white, 2: Quasicrystal, 3: Pictures",
        default=0,
    )
    parser.add_argument(
        "-hw",
        "--handwritten",
        action="store_true",
        help="Define if the data will be \"handwritten\" by an RNN",
    )
    parser.add_argument(
        "-na",
        "--name_format",
        type=int,
        help="Define how the produced files will be named. 0: [TEXT]_[ID].[EXT], 1: [ID]_[TEXT].[EXT]",
        default=0,
    )
    parser.add_argument(
        "-d",
        "--distorsion",
        type=int,
        nargs="?",
        help="Define a distorsion applied to the resulting image. 0: None (Default), 1: Sine wave, 2: Cosine wave, 3: Random",
        default=0
    )
    parser.add_argument(
        "-do",
        "--distorsion_orientation",
        type=int,
        nargs="?",
        help="Define the distorsion's orientation. Only used if -d is specified. 0: Vertical (Up and down), 1: Horizontal (Left and Right), 2: Both",
        default=0
    )

    return parser.parse_args()

def load_dict(lang):
    """
        Read the dictionnary file and returns all words in it.
    """

    lang_dict = []
    with open(os.path.join('dicts', 'xingming_' + lang + '.txt'), 'r') as d:
    #with open(os.path.join('dicts', 'char_' + "std" + '_5990.txt'), 'r') as d:
        lang_dict = d.readlines()
    return lang_dict

def load_fonts(lang):
    """
        Load all fonts in the fonts directories
    """

    if lang == 'cn':
        return [os.path.join('fonts/cn', font) for font in os.listdir('fonts/cn')]
    else:
        return [os.path.join('fonts/latin', font) for font in os.listdir('fonts/latin')]

def create_strings_from_file(filename, count):
    """
        Create all strings by reading lines in specified files
    """

    strings = []

    with open(filename, 'r') as f:
        lines = [l.strip()[0:200] for l in f.readlines()]
        if len(lines) == 0:
            raise Exception("No lines could be read in file")
        while len(strings) < count:
            if len(lines) > count - len(strings):
                strings.extend(lines[0:count - len(strings)])
            else:
                strings.extend(lines)

    return strings
jishu = 0
def create_strings_from_dict(length, allow_variable, count, lang_dict):
    """
        Create all strings by picking X random word in the dictionnary
    """


    dict_len = len(lang_dict)
    strings = []
    strings_name = []
    for _ in range(0, count):
        current_string = ""
        for _ in range(0, random.randint(1, length) if allow_variable else length):
            current_string += lang_dict[random.randrange(dict_len)][:-1]
            #current_string += ' '
        #strings.append(string_new[:-1])

        #自己加的代码
        strings_name.append(current_string[:])
        string = current_string
        print("len(string)", len(string))
        #for i in range(5):
        weizhi = np.random.randint(len(string))
        string_new = string.replace(string[weizhi], string[weizhi] + " " * np.random.randint(5))
        #string_new = string

        print("string:", string)
        print("string_new:", string_new)
        print("len", len(string_new))
        strings.append(string_new[:])




    # global jishu
    # dict_len = len(lang_dict)
    # strings = []
    # for i in range(0, count):
    #     current_string = ""
    #     for j in range(0, random.randint(1, length) if allow_variable else length):
    #         current_string += lang_dict[jishu + j][:-1]
    #         # current_string += ' '
    #     strings.append(current_string[:-1])
    #     jishu = jishu + length - 1
    #     print(i,":", jishu)
    # print(jishu)

    #自己写的图片和标签同时生成的代码
    # dict_len = len(lang_dict)
    # strings = []
    # strings_name = []
    #
    # with open("label.txt", 'w') as f:
    #     f.write("")
    # for _ in range(0, count):
    #     current_string = ""
    #     label = ""
    #     label_name = ""
    #     for i in range(0, random.randint(1, length) if allow_variable else length):
    #         num = np.random.randint(1, dict_len)
    #         current_string += lang_dict[num][:-1]
    #         label = label + " " + str(num)
    #         label_name = label_name + str(lang_dict[num]).strip('\n')
    #         print("current_string", current_string)
    #
    #     strings_name.append(current_string[:])
    #     string = current_string
    #     weizhi = np.random.randint(len(string))
    #     print("len(string)", len(string))
    #     string_new = string.replace(string[weizhi], string[weizhi] + " " * np.random.randint(5))
    #     # print("string:", string)
    #     print("string_new:", string_new)
    #     print("len", len(string_new))
    #     #print("current_string", current_string)
    #     #print("label_name", label_name)
    #     strings.append(string_new[:])
    #
    #     label = label_name + ".jpg" + " " + label + "\n"
    #
    #     with open("label.txt", 'a') as f:
    #         f.write(label)

    #print("strings", strings)

    return strings, strings_name

def create_strings_from_wikipedia(minimum_length, count, lang):
    """
        Create all string by randomly picking Wikipedia articles and taking sentences from them.
    """
    sentences = []

    while len(sentences) < count:
        # We fetch a random page
        page = requests.get('https://{}.wikipedia.org/wiki/Special:Random'.format(lang))

        soup = BeautifulSoup(page.text, 'html.parser')

        for script in soup(["script", "style"]):
            script.extract()

        # Only take a certain length
        lines = list(filter(
            lambda s:
                len(s.split(' ')) > minimum_length
                and not "Wikipedia" in s
                and not "wikipedia" in s,
            [
                ' '.join(re.findall(r"[\w']+", s.strip()))[0:200] for s in soup.get_text().splitlines()
            ]
        ))

        # Remove the last lines that talks about contributing
        sentences.extend(lines[0:max([1, len(lines) - 5])])

    return sentences[0:count]

def main():
    """
        Description: Main function
    """

    # Argument parsing
    args = parse_arguments()

    # Create the directory if it does not exist.
    try:
        os.makedirs(args.output_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # Creating word list
    lang_dict = load_dict(args.language)

    # Create font (path) list
    fonts = load_fonts(args.language)
    print("len_fonts", len(fonts))

    # Creating synthetic sentences (or word)
    strings = []

    if args.use_wikipedia:
        strings = create_strings_from_wikipedia(args.length, args.count, args.language)
    elif args.input_file != '':
        strings = create_strings_from_file(args.input_file, args.count)
    else:
        strings, strings_name = create_strings_from_dict(args.length, args.random, args.count, lang_dict)


    string_count = len(strings)
    print("string_count:", string_count)
    #print("strings", strings)
    print("strings_name", strings_name)

    # 自己加的代码, 位置加错了
    # string = str(strings[:])
    # for i in range(5):
    #     weizhi = np.random.randint(len(string))
    #     string_new = string.replace(string[weizhi], string[weizhi] + " " * np.random.randint(5))
    # print("string:", string)
    # print("string_new:", string_new)
    #strings = strings[np.random.randint(len(strings))] + " " * np.random.randint(5)
    #print(strings)



    p = Pool(args.thread_count)
    p.starmap(
        FakeTextDataGenerator.generate,
        zip(
            [i for i in range(0, string_count)],
            strings, #strings
            strings_name,
            [fonts[random.randrange(0, len(fonts))] for _ in range(0, string_count)],
            #[fonts[0] for _ in range(0, string_count)],
            [args.output_dir] * string_count,
            [args.format] * string_count,
            [args.extension] * string_count,
            [args.skew_angle] * string_count,
            [args.random_skew] * string_count,
            [args.blur] * string_count,
            [args.random_blur] * string_count,
            [args.background] * string_count,
            [args.distorsion] * string_count,
            [args.distorsion_orientation] * string_count,
            [args.handwritten] * string_count,
            [args.name_format] * string_count,
        )
    )
    p.terminate()

if __name__ == '__main__':
    main()
