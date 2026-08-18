import datetime

def display_menu(menu, current_orders, menu_keys):
    """ฟังก์ชันสำหรับแสดงเมนูอาหาร ราคา และยอดสรุปปัจจุบัน"""
    print("\n" + "="*45)
    print("         🍴 เมนูอาหารเที่ยงวันนี้ 🍴")
    print("="*45)
    for index, (food, price) in enumerate(menu.items(), start=1):
        print(f"[{index}] {food:<25} {price:>5} บาท")
    print(" [0] 🛒 สิ้นสุดการเลือกอาหาร และไปหน้าโอนเงิน")
    print("="*45)
    
    # --- ส่วนที่เพิ่มเข้ามา: แสดงตระกร้าสินค้าและยอดชำระปัจจุบันทันที ---
    if current_orders:
        print("\n📥 ตะกร้าอาหารของคุณตอนนี้:")
        current_total = 0
        for food, qty in current_orders.items():
            price_per_unit = menu[food]
            subtotal = price_per_unit * qty
            current_total += subtotal
            print(f"  • {food} x{qty} ชิ้น ({subtotal} บาท)")
        print(f"💰 ยอดรวมที่ต้องชำระ ณ ตอนนี้: {current_total:,.2f} บาท")
        print("-" * 45)

def main():
    lunch_menu = {
        "ข้าวกะเพราไก่+ไข่ต้ม": 35,
        "ก๋วยเตี๋ยวหมูน้ำใส": 30,
        "ข้าวผัดหมู": 30,
        "ข้าวขาหมู": 50,
        "ส้มตำไทย+ไก่ย่าง": 60,
        "น้ำดื่มสะอาด (ขวด)": 10,
        "ชานมไข่มุก": 25
    }
    
    menu_keys = list(lunch_menu.keys())
    order_list = {}
    
    print("สวัสดีครับ! ยินดีต้อนรับสู่ระบบสั่งอาหารโรงอาหาร (ระบบสังคมไร้เงินสด)")
    
    while True:
        # ส่ง order_list เข้าไปด้วยเพื่อให้เมนูแสดงยอดเงินล่าสุดตลอดเวลา
        display_menu(lunch_menu, order_list, menu_keys)
        
        try:
            choice = int(input("กรุณาเลือกหมายเลขเมนูที่ต้องการ (0-7): "))
            
            if choice == 0:
                break
            elif 1 <= choice <= len(lunch_menu):
                selected_food = menu_keys[choice - 1]
                quantity = int(input(f"รับจำนวนกี่จาน/แก้ว สำหรับ '{selected_food}': "))
                
                if quantity <= 0:
                    print("❌ จำนวนต้องมากกว่า 0 รายการนี้จะไม่ถูกบันทึก")
                    continue
                
                if selected_food in order_list:
                    order_list[selected_food] += quantity
                else:
                    order_list[selected_food] = quantity
                    
                print(f"✔️ เพิ่ม '{selected_food}' จำนวน {quantity} เรียบร้อยแล้ว")
            else:
                print("❌ ไม่มีหมายเลขเมนูนี้ กรุณาเลือกใหม่")
        except ValueError:
            print("❌ กรุณากรอกเฉพาะตัวเลขเท่านั้น")

    # ตรวจสอบว่าสั่งอาหารหรือไม่
    if not order_list:
        print("\n👋 คุณไม่ได้เลือกสั่งอาหารรายการใดเลย ขอบคุณครับ")
        return

    # คิดเงินรวมสุทธิ
    total_price = sum(lunch_menu[food] * qty for food, qty in order_list.items())
    
    # หน้าจอจำลองการโอนเงิน
    print("\n--- 📲 หน้าจอชำระเงินผ่าน Mobile Banking ---")
    print(" [ รายละเอียดการโอนเงิน ]")
    print(" ธนาคาร: โรงอาหารโมบายแบงก์กิ้ง (Canteen Bank)")
    print(" เลขที่บัญชี: 123-4-56789-0")
    print(f" ยอดเงินสุทธิที่ต้องโอนชำระ: {total_price:,.2f} บาท")
    print("------------------------------------------")
    
    while True:
        try:
            transfer_amount = float(input(f"\nกรุณากรอกยอดเงินที่คุณกดโอนจริง (ยอดรวม {total_price:,.2f} บาท): "))
            
            if transfer_amount == total_price:
                current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                tx_id = f"TXN{current_time}"
                
                print("\n" + "🟢"*15)
                print("       🎉 ชำระเงินสำเร็จแล้ว 🎉")
                print("🟢"*15)
                print(f"📄 รหัสอ้างอิงสลิป: {tx_id}")
                print(f"💸 จำนวนเงินโอน: {transfer_amount:,.2f} บาท")
                print("------------------------------------------")
                break
            elif transfer_amount < total_price:
                shortage = total_price - transfer_amount
                print(f"❌ ยอดเงินโอนไม่ครบ! ขาดอีก {shortage:,.2f} บาท")
            else:
                overpaid = transfer_amount - total_price
                print(f"⚠️ ยอดเงินโอนเกินมา {overpaid:,.2f} บาท กรุณาติดต่อขอรับเงินคืน")
                break
        except ValueError:
            print("❌ กรุณากรอกจำนวนเงินเป็นตัวเลขที่ถูกต้อง")

if __name__ == "__main__":
    main()
