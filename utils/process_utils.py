from multiprocessing import Process, Queue
import threading
import random

def fibonacci(n, result_queue):
    """
    计算斐波那契数列
    
    Args:
        n (int): 要计算的项数
        result_queue (Queue): 结果队列
    """
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    result_queue.put(b)

def print_numbers():
    """
    打印数字序列
    
    Returns:
        list: 数字列表
    """
    result = []
    for i in range(5):
        result.append(i)
    return result

def run_multiprocessing_task(num_processes=4, max_n=100):
    """
    运行多进程任务
    
    Args:
        num_processes (int): 进程数量
        max_n (int): 最大斐波那契项数
        
    Returns:
        list: 计算结果列表
    """
    result_queue = Queue()
    processes = []

    for _ in range(num_processes):
        p = Process(target=fibonacci, args=(random.randint(10, max_n), result_queue))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    results = [result_queue.get() for _ in range(num_processes)]
    return results

def run_multithreading_task(num_threads=3):
    """
    运行多线程任务
    
    Args:
        num_threads (int): 线程数量
        
    Returns:
        list: 计算结果列表
    """
    threads = []
    results = []

    for _ in range(num_threads):
        t = threading.Thread(target=lambda: results.extend(print_numbers()))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return results 