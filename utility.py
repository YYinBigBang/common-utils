"""development tools

"""


from pathlib import Path
import logging
import sys
import os
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)
stdout_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)
# output Logger file
log_path = './log'
log_name = 'utility.log'
log_file = f'{log_path}/{log_name}'
os.makedirs(log_path, exist_ok=True)
file_handler = logging.FileHandler(log_file)
formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# logger.removeHandler(file_handler)

def timelog(callback):
    """calculate execution time
    """
    def wrapper(arg = None):
        try:
            # reocrd start time
            cpu_time_start = time.process_time() # Not include time.sleep()
            time_start = time.time() # Include sleep()
            # print START log
            logger.info('[phase:{}] --------------START'.format(callback.__name__))
            # call function
            callback(arg)

        finally:
            #record end time
            cpu_time = time.process_time() - cpu_time_start
            total_time = time.time() - time_start
            # print END log
            logger.info('[phase:{}] --------------END'.format(callback.__name__))
            logger.info(f'total time: {total_time} | cpu time: {cpu_time}')
    
    # let the decorator can be modified to function name
    wrapper.__name__ = callback.__name__
    return wrapper


