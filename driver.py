#! /usr/bin/python2


import Queue

from gui import GUI
from main import Main


qu_usr_ip = Queue.Queue()
qu_cmd = Queue.Queue()


gui = GUI(qu_usr_ip,qu_cmd)
main = Main(qu_usr_ip, qu_cmd)

main.start()
gui.run()

main.join()
