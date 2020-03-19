import signal, os
import time

def handler(signum, frame):
    print 'Signal handler called with signal', signum
    raise IOError("Couldn't open device!")

# Set the signal handler and a 5-second alarm
signal.signal(signal.SIGALRM, handler)
signal.alarm(5)

# This open() may hang indefinitely
print("start")
time.sleep(10)
#time.sleep(1)
print("end")
signal.alarm(0) 
