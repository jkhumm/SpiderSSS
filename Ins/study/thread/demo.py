import threading,time

class A(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        for i in range(10):
            time.sleep(0.1)
            print(str(i) + " 线程A:" + threading.Thread.getName(self))


class B(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        for i in range(10):
            time.sleep(0.1)
            print(str(i) + " 线程B:" + threading.Thread.getName(self))


def threadA(name):
    for i in range(10):
        time.sleep(0.1)
        print(str(i) + " 线程A:" + name)

def threadB(name):
    for i in range(10):
        time.sleep(0.1)
        print(str(i) + " 线程B:" + name)


if __name__ == '__main__':
    print("main thread begin")
    # a = A()
    # a.start()
    # b = B()
    # b.start()
    # threading.Thread(target=threadA,args=("Thread-1",)).start()
    # threading.Thread(target=threadB,args=("Thread-2",)).start()