# Modules
import multiprocessing as mp

# Parameters

# Methods
def do_parallel( func, tasks, n_proc ):
    mp_pool = mp.Pool(n_proc)
    results = mp_pool.map( func, tasks )
    mp_pool.close()
    mp_pool.join()
    return results

# Classes

# Main
if __name__ == "__main__":
    # Function
    def is_divisible( task ):
        # Extract
        x, y = task
        # Do
        result = y%x == 0
        # Return
        return result
    # Tasks
    tasks = [ (i+1,i+9) for i in range(1000) ]
    # Do Parallel
    divisibilities = do_parallel(
        is_divisible,
        tasks,
        6
    )
    # Report
    print(divisibilities)