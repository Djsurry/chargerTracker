import subprocess
import datetime
import time
from threading import Thread
usage = []

def main():
    while 1:
        i = input()
        if i == '-r':
            print(usage[-1])
        if i == '-l':
            print(usage)
        if i == '-s':
            cmd = ['pmset', '-g', 'batt']
            result = subprocess.run(cmd, stdout=subprocess.PIPE)
            s = result.stdout.decode(encoding="utf-8", errors="strict")
            l = s.split("'")
            status = l[1]
            if status == 'AC Power':
                print('charging')
            else:
                print('using battery')
    

def updateList():
    global usage
    while 1:
        cmd = ['pmset', '-g', 'batt']
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        s = result.stdout.decode(encoding="utf-8", errors="strict")
        l = s.split("'")
        status = l[1]
        if status == 'AC Power':
            now = datetime.datetime.now()
            usage.append(now.strftime("%m-%d-%Y %H:%M"))
            print('-------CHARGING--------')
        time.sleep(10)

    

if __name__ == "__main__":
    pilot = Thread(target=updateList)
    pilot.start()
    main()
