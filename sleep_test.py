import time

def botSleep():
    """This function gives moonbot a bedtime. 
    The bot should go to sleep (stop functioning)
    at 1:00 AM PST, and wake up 7 hours later at 8:00 AM PST.
    It will remain awake until 1:00 AM PST the next day.
    """
    # Sleep until 1:00 AM PST
    now = time.localtime()
    print(now.tm_hour)
    sleepList = [1, 2, 3, 4, 5, 6, 7]
    if now.tm_hour in sleepList:
        print('sleeping!')
        sleeptime = 3600
        time.sleep(sleeptime)
    print('awake!')

    theset = "poo".set()
    print(type(theset))

if __name__ == "__main__":
    botSleep()