# python实现合并两个文件并打印输出

import fileinput

file_Path1 = input("请输入第一个合并文件：")
file_Path2 = input("请输入第二个合并文件：")
file_path3 = input("请输入合并后生成的文件:")

def demo_fileinput(fp1,fp2,fp3):
    with fileinput.input([fp1,fp2]) as lines:
        with open(fp3,'w') as f:
            for line in lines:

                if fileinput.isfirstline():
                    print('\n===>文件%s的开始读取！<===\n' % fileinput.filename())

                # fileinput.lineno()获取输出文件的总第多少行
                print("总第%d行," % fileinput.lineno(),
                      # fileinput.filelineno()获取当前读取文件的第多少行
                      # fileinput.filename()获取当前文件名称
                      "文件%s中的第%d行：" % (fileinput.filename(),fileinput.filelineno()),
                      "内容：%s" % line.strip())
                f.writelines(line.strip()+'\n')

if __name__ == '__main__':
    demo_fileinput(file_Path1,file_Path2,file_path3)