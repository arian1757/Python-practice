def check_conditions(i):
    numbers = set()
    for number in range (3):
        digit = i%10
        numbers.add(digit)
        i = int(i/10)
    if 0 in numbers or len(numbers)!=2:
        return False
    else :
        return True
    
counter = 0
for i in range (110,999):
    
    if check_conditions(i):
        counter +=1
    
else :
    print (counter)