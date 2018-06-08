import subprocess
import datetime
import time
from threading import Thread
import json
# :)
try:
    usage = json.load(open('usage.json'))
except:
    json.dump([], open('usage.json', 'w'))

_FINISH = False


def now():
    return datetime.datetime.now().strftime("%m-%d-%Y %H:%M")

def main():
    global _FINISH, usage
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
            try:
                usage.remove('CHARGING')
                usage.append(now())
            except:
                pass
            break
        else:
            print('unknown command')



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
            now = datetime.datetime.now()
            usage.append(now.strftime("%m-%d-%Y %H:%M"))
            charging = False
        

        

    

if __name__ == "__main__":
    pilot = Thread(target=updateList)
    pilot.start()
    main()
    pilot.join()
    json.dump(usage, open('usage.json', 'w'))

