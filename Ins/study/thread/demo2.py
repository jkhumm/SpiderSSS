import queue,threading

import requests

baseUrl = 'https://www.pythontab.com/html/pythonjichu/'

urlQueue = queue.Queue(maxsize=8)
for i in range(2,10):
    urlQueue.put(baseUrl + str(i) + '.html')


def fetchUrl():
    while True:
        try:
            url = urlQueue.get_nowait()
            #print('目前队列大小：' + str(urlQueue.qsize()))
            res = requests.get(url, verify=False)
            print('当前线程名：' + threading.currentThread().name + '  Url：' + url + "结果：" + str(res.status_code))
        except Exception as e:
            print("已经没有任务可取，退出本线程！")
            break


if __name__ == '__main__':
    # 屏蔽warning信息
    requests.packages.urllib3.disable_warnings()
    # fetchUrl()
    for i in range(0, 3):
        t = threading.Thread(target=fetchUrl).start()

