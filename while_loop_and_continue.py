
    
a = 5
while a < 7:
    a += 5
    print(a)
    
x = 5
while x > 0:
    x -= 1
else:
    print("bye!")

while True:
    a = 1
    print(a)
    a += 2
    if a > 2:
        break
    

    
firs_name = 'Ahmed'
last_name = 'Abdullahi'
full_name = firs_name + ' ' + last_name
print(full_name)
    
a = 10
while a > 0:
    a -= 1
    if a % 2 == 0:
        continue
    print(a, end=' ')
    
x = 5
s = 0
while x:
    x -= 1
    s += x
    print(s)
    
my_sum = 0
x = 100
while x:
    if x % 2 != 0:
        my_sum += x
    x -= 1
print(my_sum)
