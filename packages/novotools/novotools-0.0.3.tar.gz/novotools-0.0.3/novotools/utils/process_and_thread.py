import subprocess as sp
from multiprocessing import Process,Pool

def multi_process(assignments):
    """
    assignments is a list of tuples which are
    composed by a function and its arguments(in tuple format)
    this function is synchronized by .join() method
    of Process 
    """
    for func,args,kwargs in assignments:
        p = Process(target=func,args=args,kwargs=kwargs)
        print('subprocess for %s is running...' % func)
        p.start()

    p.join() #block the main process to synchronize the subprocesses
    print('All assignments are completed!')

def process_pool(assignments,number_of_process):
    """
    run multiple processes by specifying number of processes
    each time
    """
    p = Pool(number_of_process)
    for func,args,kwargs in assignments:
        p.apply_async(func,args=args,kwds=kwargs)

    p.close() # no other procee will be added into pool
    p.join() # synchronization
    print('All assignments are completed!')

def run_cmd(cmd):
    """
    run command by using subprocess,
    raise exception when error has happened
    return standard output and standard error
    """
    cp = sp.run(cmd,shell=True,capture_output=True,encoding="utf-8")
    if cp.returncode != 0:
        error = f"""Something wrong has happened when running command [{cmd}]:
         {cp.stderr}"""
        raise Exception(error)
    
    return cp.stdout,cp.stderr
