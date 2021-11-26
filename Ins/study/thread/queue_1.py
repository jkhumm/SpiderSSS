import queue

# 　　    Queue.Queue(maxsize=0)   FIFO， 如果maxsize小于1就表示队列长度无限
#        Queue.LifoQueue(maxsize=0)   LIFO， 如果maxsize小于1就表示队列长度无限
#        Queue.qsize()   返回队列的大小
#        Queue.empty()   如果队列为空，返回True,反之False
#        Queue.full()   如果队列满了，返回True,反之False
#        Queue.get([block[, timeout]])   读队列，timeout等待时间
#        Queue.put(item, [block[, timeout]])   写队列，timeout等待时间
#        Queue.queue.clear()   清空队列

if __name__ == '__main__':
    queue = queue.Queue()  # FIFO 如果maxsize小于1就表示队列长度无限
    for i in range(10):
        queue.put(i) # 写队列，timeout等待时间，满了会处于阻塞
    for i in range(10):
        print("--------" + str(i))
        print(queue.get_nowait())  # 读队列，timeout等待时间，没有会处于阻塞
        print(queue.qsize())

    # 如循环11次，最后一次由于结果为空，处于阻塞。如果使用get_nowait（）就能抛出异常 raise Empty