from telnetlib import Telnet
from time import sleep

keys = { '⇧':'w',
        '⇩': 's',
        '⇦':'a',
        '⇨':'d'

}

counter = 0

with Telnet("chal.2023.sunshinectf.games", 23200) as tn:
    tn.read_until(b'Start')
    s = tn.read_until(b'\r\n')
    tn.write(b'\n')
    s = tn.read_until(b'\r\n')
    while True:
        counter +=1
        
        s = tn.read_until(b'\r\n')
        print(f" counter {counter} data = {s}")
        try :
            data = s.decode("utf-8")
            
            data = data.replace('\r','')
            data = data.replace('\n','')
            
            ans = ''
            for char in data:
                ans += keys[char]
            print(f'my answer is {ans}')
            tn.write(ans.encode())
        except:
            pass
        tn.write(b'\n')

    

    