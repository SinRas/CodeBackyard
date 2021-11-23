# Modules
import multiprocessing as mp

# Parameters

# Methods

# Classes
class Master(mp.Process):
    # Constructor
    def __init__(self, name, queue_tasks, queue_logger):
        super().__init__()
        self.name = name
        self.queue_tasks = queue_tasks
        self.queue_logger = queue_logger
        self.initialize()
        return
    # Initializations
    def initialize(self):
        self.n = 2
        return
    # Generate Task
    def generate_task(self):
        n = self.n
        if( n >= 10 ):
            return None
        self.n += 1
        return n
    # Run
    def run(self):
        # Broadcast Tasks
        while True:
            # Task
            task = self.generate_task()
            # Tasks Finished
            if( task is None ):
                self.log(
                    "task generation finished, master shutting down",
                    0
                )
                break
            # Add Task to Queue for Workers
            self.queue_tasks.put(task)
            self.log( f"task {str(task)} created", 0 )
        # Return
        return
    # STR
    def __str__(self):
        return f"<Master@{self.name}>"
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
    # Create Master
    master = Master("main", queue_tasks, queue_logger)
    # Start Master
    master.start()
    master.join()
    # Report
    print( f"Queue Size of Tasks : {queue_tasks.qsize()}" )
    print( f"Queue Size of Logs  : {queue_logger.qsize()}" )