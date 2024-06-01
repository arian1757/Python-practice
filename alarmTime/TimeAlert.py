
def start():
    try:
        now = input('what time is it?\n')
        alarm = input('give the alarm\n')
        h1,m1,s1 = map(int,now.split(':'))
        h2,m2,s2 = map(int,alarm.split(':'))
        if 0<=h1<24 and 0<=m1<61 and 0<=s1<61:
            nowTime = h1 *3600 + m1 *60 + s1
        else:
            raise ValueError('wrong time')
        if 0<=h2<24 and 0<=m2<61 and 0<=s2<61:
            alarmTime = h2 *3600 + m2 *60 + s2
        else:
            raise ValueError('wrong time')
        return nowTime, alarmTime
    except ValueError:
        print('wrong format') 

def calculator(diff):
    
    if diff > 0 :
        
        hour = diff // 3600
        minutes = (diff % 3600) // 60
        second = diff % 60 
        return  f"{hour:02}:{minutes:02}:{second:02}"
    elif diff < 0 :
        newDiff = 86400 + diff
        return calculator(newDiff)
    else:
        return f"24:00:00"
    



if __name__== "__main__":
    nowTime, alarmTime = start()
    diff = alarmTime - nowTime
    print(calculator(diff))
