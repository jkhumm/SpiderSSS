import re
################################### 原子 ###################################
# 普通字符
def demo1():
    exam = "qianfeng"
    str_1 = "qianfengedu"
    result = re.search(exam,str_1)
    print(result) #打印结果：<_sre.SRE_Match object; span=(0, 8), match='qianfeng'>

# 非打印字符串
def demo2():
    exam = "\n"
    str_1 = """http://www.1000phone.com
    http://codingke.com
    """
    result = re.search(exam, str_1)
    print(result) #打印结果：<_sre.SRE_Match object; span=(24, 25), match='\n'>

# 通用字符
def demo3():
    exam = "\w\dcodingke\w"
    str_1 = "abcd1234codingkeA_12ab"
    result = re.search(exam, str_1)
    print(result) #打印结果：<_sre.SRE_Match object; span=(6, 17), match='34codingkeA'>

# 原子表
def demo4():
    exam = "\w\dcodingke[xyz]\w"
    exam1 = "\w\dcodingke[^xyz]\w"
    exam2 = "\w\dcodingke[xyz]\W"
    str_1 = "a1codingkex_666"
    print(re.search(exam, str_1)) #打印结果：<_sre.SRE_Match object; span=(0, 12), match='a1codingkex_'>
    print(re.search(exam1, str_1)) #打印结果：None
    print(re.search(exam2, str_1)) #打印结果：None

################################### 元字符 ###################################

# 任意元字符
def demo5():
    exam = "codingke...."
    str_1 = "abcd1234codingke123456"
    result = re.search(exam, str_1)
    print(result) #打印结果：<_sre.SRE_Match object; span=(8, 20), match='codingke1234'>

# 边界限制元字符
def demo6():
    exam1 = "^codingke" # 以codingke开头
    exam2 = "^codingkee"
    exam3 = "ke$"  # 以ke结尾
    exam4 = "_jy$"  # 以_jy$结尾
    str_1 = "codeingke_jy"
    print(re.search(exam1, str_1))  # 打印结果：None
    print(re.search(exam2, str_1))  # 打印结果：None
    print(re.search(exam3, str_1))  # 打印结果：None
    print(re.search(exam4, str_1))  # 打印结果：<_sre.SRE_Match object; span=(9, 12), match='_jy'>

# 限定符 * ？ + {n} {n，} {n，m}
def demo7():
    exam1 = "py.*n" # py到n的之间任意字符（除换行符）且该结果出现0次 1次 或多次
    exam2 = "cd{2}" # cd中的d出现2次 也就是cdd
    exam3 = "cd{3}"  # cd中的d出现3次 也就是cddd
    exam4 = "cd{2,}"  # d出现2次以上
    str_1 = "abcdddpython_py"
    print(re.search(exam1, str_1))  # 打印结果：<_sre.SRE_Match object; span=(6, 12), match='python'>
    print(re.search(exam2, str_1))  # 打印结果：<_sre.SRE_Match object; span=(2, 5), match='cdd'>
    print(re.search(exam3, str_1))  # 打印结果：<_sre.SRE_Match object; span=(2, 6), match='cddd'>
    print(re.search(exam4, str_1))  # 打印结果：<_sre.SRE_Match object; span=(2, 6), match='cddd'>

def demo8():
    exam1 = "python|java"
    str_1 = "aaapython666java"
    result = re.search(exam1,str_1).group()
    print(result) # 打印结果： python

if __name__ == "__main__":
    demo8()