# Modules
import time, random
import multiprocessing as mp

# Parameters

# Methods

# Classes
class Worker(mp.Process):
    # Constructor
    def __init__(self, name, queue_tasks, queue_logger):
        super().__init__()
        self.name = name
        self.queue_tasks = queue_tasks
        self.queue_logger = queue_logger
        return
    # Do
    def do( self, task ):
        _start = time.time()
        # do fake task
        r = 2*random.random()
        time.sleep( r )
        _duration = time.time() - _start
        self.log(f"task process result is \"{r}\", process took: {1000*_duration:>3.1f} ms", 1)
        return
    # Generate Tasks
    def run(self):
        # Infinite Loop
        while True:
            # New Task
            task = self.queue_tasks.get()
            # Poison Pill
            if( task is None ):
                self.log( "poison pill taken", -1 )
                break
            # Do Task
            self.log( f"task {str(task)}  started", 2 )
            self.do( task )
            self.log( f"task {str(task)} finished", 2 )
        # Return
        return
    # STR
    def __str__(self):
        return f"<Worker@{self.name}>"
    # Log
    def log(self, msg, log_level):
        self.queue_logger.put((
            str(self),
            msg,
            log_level
        ))
        return

# Main
if __name__ == "__main__":
    # Parameters
    queue_tasks, queue_logger = mp.Queue(100), mp.Queue()
    # Create Workers
    workers = [
        Worker( f"Worker{i}", queue_tasks, queue_logger ) for i in range(4)
    ]
    # Start Workers
    [ worker.start() for worker in workers ]
    # Add Sample Tasks
    for i in range(12):
        queue_tasks.put(i)
    # Add Poison Pills
    [ queue_tasks.put(None) for worker in workers ]
    # Wait for Workers to Finishe
    [ worker.join() for worker in workers ]
    queue_logger.put(None)
    # Report
    print( f"Queue Size of Tasks : {queue_tasks.qsize()}" )
    print( f"Queue Size of Logs  : {queue_logger.qsize()}" )
    for _ in range(queue_logger.qsize()):
        print( queue_logger.get() )
