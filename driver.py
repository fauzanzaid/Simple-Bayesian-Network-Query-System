#! /usr/bin/python2


import Queue

from gui import GUI
from main import Main


qu_usr_ip = Queue.Queue()
qu_cmd = Queue.Queue()


input_filename = "input1.txt"


main = Main(qu_usr_ip, qu_cmd, input_filename)
gui = GUI(qu_usr_ip, qu_cmd, len(main.node_names))

main.start()
gui.run()

main.join()
