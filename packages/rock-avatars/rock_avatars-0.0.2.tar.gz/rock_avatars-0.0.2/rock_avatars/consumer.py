import multiprocessing

from .log import logger


class Consumer(multiprocessing.Process):
    def __init__(self, task_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                logger.info(f'{proc_name}: Exiting')
                self.task_queue.task_done()
                break
            logger.info(f'{proc_name}: {next_task}')
            _ = next_task()
            self.task_queue.task_done()
