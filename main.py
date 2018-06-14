import subprocess
import datetime
import time
from threading import Thread
import json
usage = []
try:
    usage = json.load(open('usage.json'))
except:
    json.dump([], open('usage.json', 'w'))

try:
    usage.remove('CHARGING')
except:
    pass
_FINISH = False

_ALERTS = True

_START = time.time()

def now():
    return datetime.datetime.now().strftime("%m-%d-%Y %H:%M")

def main():
    global _FINISH, usage, _ALERTS
    while 1:
        i = input()
        if i == '-r':
            try:
                print(usage[-1])
            except:
                print('no recored usage.')
        elif i == '-l':
            print(usage)
        elif i == '-s':
            cmd = ['pmset', '-g', 'batt']
            result = subprocess.run(cmd, stdout=subprocess.PIPE)
            s = result.stdout.decode(encoding="utf-8", errors="strict")
            l = s.split("'")
            status = l[1]
            if status == 'AC Power':
                print('charging')
            else:
                print('using battery')
        elif i == '-q':
            _FINISH = True
            if 'CHARGING' in usage:
                c = 1
                usage.remove('CHARGING') 
            else:
                c = 0
            if c:
                usage.append(now())
            break
        elif i == '-a':
            _ALERTS = False if _ALERTS else True
            print('Alert Status: ' + str(_ALERTS))
        elif i == '-c':
            print('Are you sure? This will clear all data (Y/N)')
            if input().lower() == 'y':
                usage = []
        elif i == '-t':
            print('program has been running for ' + str(datetime.timedelta(seconds=666)))

        else:
            print('unknown command')
def lowBattery(percent):
    cmd = ['osascript', '-e', 'display dialog "Warning: Battery is below ' +str(percent) + ' percent. Find a charger" with title "Battery Low"']
    subprocess.Popen(cmd)


def updateList():
    global usage
    charging = False
    while 1:
        
        if _FINISH:
            break
        cmd = ['pmset', '-g', 'batt']
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        s = result.stdout.decode(encoding="utf-8", errors="strict")
        l = s.split("'")
        status = l[1]
        currentBattery = int(s.split('\t')[1].split(';')[0].replace('%', ''))
        if status == 'AC Power' and not charging:
            charging = True
            print('-------CHARGING--------')
        if status == 'AC Power':
            try:
                usage.remove('CHARGING')
            except:
                pass
            usage.append('CHARGING')
        if status == 'Battery Power' and charging:
            if currentBattery == 20 and _ALERTS:
                lowBattery(currentBattery)
            elif currentBattery == 10 and _ALERTS:
                lowBattery(currentBattery)
            elif currentBattery == 5 and _ALERTS:
                lowBattery(currentBattery)
            now = datetime.datetime.now()
            usage.append(now.strftime("%m-%d-%Y %H:%M"))
            charging = False
        time.sleep(2)
        

        

    

if __name__ == "__main__":
    pilot = Thread(target=updateList)
    pilot.start()
    main()
    pilot.join()
    json.dump(usage, open('usage.json', 'w'))
