# Modules
from multiprocessing.queues import Queue
import time, math
import multiprocessing as mp
## Internal
from logger import Logger
from master import Master
from worker import Worker

# Parameters

# Methods

# Classes
## Master
class MasterNaturals(Master):
    # Initialization
    def initialize(self):
        self.n = 2
        return
    # Generate Task
    def generate_task(self):
        n = self.n
        if( n >= 1000 ):
            return
        self.n += 1
        return n
## Worker
class WorkerIsPrime(Worker):
    # Override Do
    def do( self, task ):
        _start = time.time()
        n = int(task)
        is_prime = True
        for i in range(2, int(math.sqrt(n))+1 ):
            if( n%i == 0 ):
                is_prime = False
                break
        _duration = time.time() - _start
        self.log(
            f"number {n} primality check result is {str(is_prime):<5}, process took {1000*_duration:>6.3}ms",
            1
        )
        return



# Main
if __name__ == "__main__":
    # Parameters
    N_WORKERS = 4
    # Queues
    queue_tasks = mp.Queue(100)
    queue_logger = mp.Queue()
    # Processes
    ## Logger
    logger = Logger(queue_logger, verbose=True, fp_base='.')
    logger.start()
    ## Master
    master = MasterNaturals("MasterOfNaturalNumbers", queue_tasks, queue_logger)
    master.start()
    ## Workers
    workers = [
        WorkerIsPrime(
            f"WorkerIsPrime{i}",
            queue_tasks,
            queue_logger
        ) for i in range(N_WORKERS)
    ]
    [ worker.start() for worker in workers ]
    # Join
    ## Master
    master.join()
    [ queue_tasks.put(None) for worker in workers ]
    ## Workers
    [ worker.join() for worker in workers ]
    ## Logger
    queue_logger.put(None)
    logger.join()