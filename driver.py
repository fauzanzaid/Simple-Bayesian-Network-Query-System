#! /usr/bin/python2


import Queue

from gui import GUI
from main import Main


qu_usr_ip = Queue.Queue()
qu_cmd = Queue.Queue()


main = Main(qu_usr_ip, qu_cmd)
gui = GUI(qu_usr_ip, qu_cmd, len(main.node_names))

main.start()
gui.run()

main.join()
