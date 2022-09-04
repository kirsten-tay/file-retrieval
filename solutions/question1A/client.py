from __future__ import print_function
import time
import threading
import sys
import Pyro4


if sys.version_info < (3, 0):
    input = raw_input


def regular_pyro(uri):
    start = time.time()
    name = threading.currentThread().name
    with Pyro4.core.Proxy(uri) as p:
        data=p.get_with_pyro()
        print(data)
    duration = time.time() - start
    print("thread {0} done, {1:.2f} Mb/sec.".format(name,duration))













if __name__ == "__main__":
    uri = input("Uri of filetransfer server? ").strip()
    print("\n\n**** regular pyro calls ****\n")
    t1 = threading.Thread(target=regular_pyro, args=(uri, ))
    t2 = threading.Thread(target=regular_pyro, args=(uri, ))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    input("enter to exit:")
