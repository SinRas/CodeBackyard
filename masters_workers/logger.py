# Modules
import os
import time, datetime
import multiprocessing as mp

# Parameters

# Methods

# Classes
class Logger(mp.Process):
    # Constructor
    def __init__(self, queue_logger, verbose = False, fp_base = '.'):
        super().__init__()
        self.queue_logger = queue_logger
        self.fp_base = fp_base
        self.fp_logs = os.path.join( self.fp_base, f"logs_{str(int(time.time()))}.txt" )
        self.fp = open( self.fp_logs, 'a' )
        self.verbose = verbose
        return
    # Generate Tasks
    def run(self):
        # Intialization
        log_level = -1
        msg_log = f"{datetime.datetime.now()} {str(self)} {log_level:>2} logger started"
        self.fp.write(msg_log+"\n")
        self.fp.flush()
        # Infinite Loop
        while True:
            task = self.queue_logger.get()
            # Poison Pill
            if( task is None ):
                log_level = -1
                msg_log = f"{datetime.datetime.now()} {str(self)} {log_level:>2} Poison Pill Taking ... shutting down"
            else:
                name, msg, log_level = task
                msg_log = f"{datetime.datetime.now()} {name} {log_level:>2} {msg}"
            # Extract and Write
            self.fp.write(msg_log+"\n")
            self.fp.flush()
            if( self.verbose or task is None ):
                print(msg_log)
            # Break
            if( task is None ):
                break
        # Close File
        self.fp.flush()
        self.fp.close()
        # Return
        return
    # STR
    def __str__(self):
        return f"<Logger>"

# Main
if __name__ == "__main__":
    # Queues
    queue_logger = mp.Queue()
    # Logger
    logger = Logger( queue_logger, verbose=True )
    logger.start()
    # Put Messages
    for i in range(10):
        queue_logger.put(("PROCESS_NAME", f"hi@{i}", 0))
    queue_logger.put(None)
    # Join
    logger.join()