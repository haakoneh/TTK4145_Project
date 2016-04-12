#watchdogtest

from watchdog import Watchdog


def main():
    ''' This function is used to unit test the watchdog module. '''
    
    w = Watchdog(5.0)
    w.StartWatchdog()

    for i in range(0, 11):
        print 'Testing %d...' % i
        
        try:
            if (i % 3) == 0:
                sleep(1.5)
            else:
                sleep(0.5)
        except:
            print 'MAIN THREAD KNOWS ABOUT WATCHDOG'
                
        w.PetWatchdog()

    w.StopWatchdog()  # Not strictly necessary
    
    return

if __name__ == '__main__':
    main()
