# name = := expretion
print(x := 2 + 3)
print(f'x is {x}')

date = input('Enter your name:')
if len(date) > 0:
    print(f'Your name has {len(date)} characters')
else:
    print('your name can not be empty')


# Rewrite the code using warlus operater

date = input('Enter your age: ')
if (age := int(date)) > 18:
    print(f'your age is {age}, you can vote: ')
else:
    print(f'you are not old enough to vote')


price = input("Enter the price: ")
discount = 0.1
if (p := float(price)) >= 50:
    print(f"price is {p} discount {discount}")
elif (p := float(price)) >= 60:
    print(f"price is {p} discount {discount}")
else:
    print(f"price is {p} no discount: ")
