
print("โปรแกรมตารางสูตรคูณ\n")


input_start = int(input("แม่สูตรคูณเริ่มต้น: "))
input_end = int(input("แม่สูตรคูณสุดท้าย: "))


start = min(input_start, input_end)
end = max(input_start, input_end)

for i in range(start, end + 1):
    print(f"\nตารางสูตรคูณแม่ {i}")
    for j in range(1, 13):
        print(f"{i} x {j} = {i * j}")

print("\n------------------------------")
print("24 นาย ชยพล เดชทะสร 4/4")
print("------------------------------")