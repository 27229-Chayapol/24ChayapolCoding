print("โปรเเกรมทายจำนวณ By 24")
import random
number = random.randint(1, 100)
count = 1
while True:
    guess = int(input("กรุณาใส่ตัวเลขที่คุณทาย: "))
    count += 1
     
    if guess > number:
       print("มากเกินไป")
    elif guess < number:
       print("น้อยเกินไป")
    else:
       print(f"ถูกต้องเเล้ว คุณทายทั้งหมด {count} ครั้ง")
