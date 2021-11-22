import time


total_set = set([])

total_set.add("1")
total_set.add("2")
total_set.add("3")

print(total_set)



mailto = ['cc', 'bbbb', 'afa', 'sss', 'bbbb', 'cc', 'shafa']
addr_to = list(set(mailto))
addr_to.sort(key = mailto.index)
# print(addr_to)

l1 = ['b','c','d','b','c','a','a']
l2 = []
[l2.append(i) for i in l1 if not i in l2]
print(l2)

l1 = ['b','c','d','b','c','a','a']
l2 = []
for i in l1:
    if i not in l2:
        l2.append(i)

total_href_len_previous = 0
total_href_len_post = 0

def init():
    total_href_len_previous = 1
   # total_href_len_post = total_href_len_post + 1


def test():
    while True:
        print(time.time())
        print(time.localtime())

        t = [1, 2, 3]
        s = [3, 4, 5]

        a = set(t) | set(s)

        a = list(set(t) | set(s))  # t 和 s的并集

        b = list(set(t) & set(s))  # t 和 s的交集

        c = list(set(t) - set(s))  # 求差集（项在t中，但不在s中）

        d = list(set(t) ^ set(s))  # 对称差集（项在t或s中，但不会同时出现在二者中）




        print("init")
        init()
        print(total_href_len_previous)
        print(total_href_len_post)
        time.sleep(1)
        break


# 2021年1月15日
def dateStr_to_datetime(dateStr):
    ary1 = dateStr.split('年')
    ary2 = ary1[1].split('月')
    year,month,day = ary1[0], ary2[0], ary2[1].replace('日','')
    print(year)


# def init():
#     return total_href_len_previous + 1,total_href_len_post + 1
#
# def test():
#     while True:
#         print("init")
#         previous,post = init()
#         print(previous)
#         print(post)
#         time.sleep(1)

ary = []
def init2():
    ary.append(1)

tuple_demo = ((1,'www.instagram1'),(2,'www.instagram2'))

def test2():
    init2()
    for href in ary:
        print(href)
    for i in range(len(ary)):
        print(ary[i])
    for t in tuple_demo:
        print("元祖：" + t[1])

    a = 100 % 10
    b = int(111 / 10)
    print(a)
    print(b)

# Photo by Eddie Yuyan Peng on July 11, 2021. May be an image of coast, ocean and nature.

# 一月January
# 二月February
# 三月March
# 四月April
# 五月May
# 六月June
# 七月July
# 八月August
# 九月September
# 十月Octorber
# 十一月November
# 十二月December


month_ary = ["January","February","March","April","May","June","July","August","September","Octorber","November","December"]
def get_Publish_time(img_alt_str):
    year,month,day = 0,0,0
    s1 = img_alt_str.split(".")[0].split("on")[1][1:]
    data_array = s1.replace(",", "").split(" ")  # ['February', '01', '2021']
    year = int(data_array[2])
    day = int(data_array[1])
    for i in range(len(month_ary)):
        if month_ary[i].__eq__(data_array[0]):
            month = i+1
            break
    return year,month,day
task_ary = []
def map_func():
    task = {}
    task.setdefault("data","2012")
    task.setdefault("url", "xxxx")
    task.setdefault("data", "2013")
    task.setdefault("url", "yyyyy")
    print(task)
    print(task.get("url"))


if __name__ == '__main__':
   # str1 = "Photo by 张子枫 on February 01, 2021. May be a closeup of one or more people."
   # print(get_Publish_time(str2))
   # time.localtime()
   # map_func()
   # dateStr_to_datetime("2021年1月12日")
   # test2()
    print(1)
    print(time.localtime() > time.localtime())


