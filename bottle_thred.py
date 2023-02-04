from bottle import Bottle, run
import threading
import os
import time
from queue import Queue

app = Bottle()
threads = Queue()
status = "Idle"

@app.route('/task')
def task():
    t = threading.Thread(target=long_running_task)
    t.start()
    yield "Task started: "
    status = "Your mama"
    threads.put(t)
    print("Number of threads in the queue: ", threads.qsize())
    yield "Task started in a new thread"

@app.route('/listthreads')
def listthreads():
    yield "Task status: {}".format(status)
    yield "Number of threads in the queue: {}".format(threads.qsize())

def long_running_task():
    # Do some time-consuming work
    print("Task started")
    for i in range(10):
        print(i)
        time.sleep(1)
    print("Task finished")

def check_queue():
    while not threads.empty():
        t_act = threads.get()
        if t_act.is_alive():
            t_act.join()
            threads.task_done()
        print("Check of threads in the queue: ", threads.qsize())

def thread_monitor():
    while True:
        check_queue()
        time.sleep(5) # the number of seconds to wait before calling the function again
    again

threading.Thread(target=run(app, host='localhost', port=8080, debug=True))
