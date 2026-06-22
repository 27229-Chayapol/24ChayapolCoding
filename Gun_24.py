print("โปรเเกรมคำนวณคะเเนน\n")

science = int(input("กรุณาใส่คะเเนนรายวิชาวิทยาศาสตร์:"))
math = int(input("กรุณาใส่คะเเนนรายวิชาคณิตศาสตร์:"))
english = int(input("กรุณาใส่คะเเนนรายวิชาภาษาอังกฤษ:"))
total = science + math + english
average = total / 3 
print("\nคะเเนนรวมของคุณคือ:", total)
print(f"คะเเนนเฉลี่ยของคุณคือ: {average:.2f}")

if average >= 80:
    print("เกรดของคุณคือ: A+")
elif average >= 50:
    print("เกรดของคุณคือ: D-")

print("จัดทำโดย: Gun_24")