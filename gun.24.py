import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk

cart = {} # เก็บรายการในตะกร้า
order_counter = 1 # นับออเดอร์

# --- การกำหนดฟอนต์และธีมสี Modern Vibrant Pastel POS ---
FONT_MAIN = ("Leelawadee UI", 11)
FONT_BOLD = ("Leelawadee UI", 11, "bold")
FONT_TITLE = ("Leelawadee UI", 12, "bold")
FONT_HEADER = ("Leelawadee UI", 16, "bold")

# สีพื้นหลังแต่ละโซน (Colorful Pastel Theme)
BG_MAIN = "#EBF2F7"      # สีพื้นหลังหลัก (ฟ้าอมเทาพาสเทล)
BG_MENU_CARD = "#FFF4ED" # สีพื้นหลังโซนเมนู (ส้มพีชอ่อน)
BG_CART_CARD = "#E6F7F5" # สีพื้นหลังโซนตะกร้า (ฟ้ามินต์อ่อน)
BG_STATUS_CARD = "#F3E8FF" # สีพื้นหลังโซนติดตามครัว (ม่วงพาสเทลอ่อน)

# สีเน้นและสถานะ
PRIMARY_COLOR = "#FF6B6B"  # สีส้มแดงพาสเทล
ACCENT_BLUE = "#00CEC9"   # สีฟ้าอมเขียวสดใส
ACCENT_GREEN = "#2ECC71"  # สีเขียวสดใส
ACCENT_ORANGE = "#E67E22" # สีส้มอบอุ่น
TEXT_DARK = "#2D3436"     # สีตัวอักษรเข้ม
TEXT_MUTED = "#636E72"    # สีตัวอักษรจาง

# --- ระบบแจ้งเตือน Toast Notification ---
def show_toast(root_win, message, bg_color="#2ECC71"):
  toast = tk.Toplevel(root_win)
  toast.overrideredirect(True)
  toast.attributes("-topmost", True)
  label = tk.Label(
    toast,
    text=message,
    font=FONT_BOLD,
    bg=bg_color,
    fg="white",
    padx=20,
    pady=10,
  )
  label.pack()
  root_win.update_idletasks()
  x = root_win.winfo_x() + root_win.winfo_width() - 340
  y = root_win.winfo_y() + root_win.winfo_height() - 80
  toast.geometry(f"+{x}+{y}")

  def fade_out():
    time.sleep(2.0)
    for alpha in [i / 10 for i in range(10, -1, -1)]:
      toast.attributes("-alpha", alpha)
      time.sleep(0.03)
    toast.destroy()

  threading.Thread(target=fade_out, daemon=True).start()

# --- หน้าต่างเลือกออปชันอาหาร ---
def create_popup(title):
  win = tk.Toplevel(root)
  win.title(title)
  win.geometry("420x500")
  win.configure(bg=BG_MENU_CARD)
  win.grab_set()
  return win

def create_qty_spinbox(parent):
  tk.Label(
    parent, text="🔢 จำนวน (รายการ):", font=FONT_BOLD, bg=BG_MENU_CARD, fg=TEXT_DARK
  ).pack(anchor="w", padx=35, pady=(12, 2))
  spin = tk.Spinbox(
    parent,
    from_=1,
    to=20,
    font=FONT_MAIN,
    justify="center",
    width=10,
    bd=1,
    relief="solid",
  )
  spin.pack(anchor="w", padx=35, pady=5)
  return spin

def create_dropdown(parent, variable, options):
  option_menu = tk.OptionMenu(parent, variable, *options)
  option_menu.config(
    font=FONT_MAIN,
    bg="white",
    fg=TEXT_DARK,
    activebackground="#FFEAA7",
    bd=1,
    relief="solid",
    anchor="w",
    pady=5,
  )
  menu = option_menu.nametowidget(option_menu.menuname)
  menu.config(font=FONT_MAIN, bg="white", fg=TEXT_DARK)
  option_menu.pack(padx=35, pady=5, fill="x")
  return option_menu

def add_custom_kaprao():
  def confirm():
    meat, has_egg, qty = (
      meat_var.get(),
      egg_var.get(),
      int(spin_qty.get()),
    )
    price = 50 + (10 if has_egg else 0)
    full_name = (
      f"ผัดกะเพรา{meat}" + (" + ไข่ดาว" if has_egg else " (ไม่ใส่ไข่)")
    )
    add_to_cart_dict(full_name, price, qty)
    win.destroy()

  win = create_popup("🍳 ตัวเลือกผัดกะเพรา")
  tk.Label(
    win, text="1. เลือกเนื้อสัตว์:", font=FONT_BOLD, bg=BG_MENU_CARD, fg=TEXT_DARK
  ).pack(anchor="w", padx=35, pady=(20, 4))
  meat_var = tk.StringVar(value="หมูสับ")
  create_dropdown(
    win, meat_var, ["หมูสับ", "หมูกรอบ", "ไก่", "เนื้อ", "ทะเล"]
  )

  egg_var = tk.BooleanVar(value=True)
  tk.Checkbutton(
    win,
    text="🍳 เพิ่มไข่ดาว (+10 บาท)",
    variable=egg_var,
    font=FONT_MAIN,
    bg=BG_MENU_CARD,
    fg=TEXT_DARK,
    activebackground=BG_MENU_CARD,
  ).pack(anchor="w", padx=35, pady=10)

  spin_qty = create_qty_spinbox(win)
  tk.Button(
    win,
    text="✨ บันทึกรายการ",
    bg=PRIMARY_COLOR,
    fg="white",
    font=FONT_BOLD,
    command=confirm,
    pady=8,
    bd=0,
    cursor="hand2",
  ).pack(padx=35, pady=25, fill="x")

def add_custom_padthai():
  def confirm():
    meat, qty = meat_var.get(), int(spin_qty.get())
    price = 60 + (15 if "กุ้ง" in meat else 0)
    clean_meat = meat.split(" ")[0]
    full_name = f"ผัดไทย{clean_meat}"
    add_to_cart_dict(full_name, price, qty)
    win.destroy()

  win = create_popup("🍝 ตัวเลือกผัดไทย")
  tk.Label(
    win, text="1. เลือกเนื้อสัตว์:", font=FONT_BOLD, bg=BG_MENU_CARD, fg=TEXT_DARK
  ).pack(anchor="w", padx=35, pady=(20, 4))
  meat_var = tk.StringVar(value="กุ้ง (+15บ.)")
  create_dropdown(win, meat_var, ["หมู", "ไก่", "กุ้ง (+15บ.)"])

  spin_qty = create_qty_spinbox(win)
  tk.Button(
    win,
    text="✨ บันทึกรายการ",
    bg="#FF7675",
    fg="white",
    font=FONT_BOLD,
    command=confirm,
    pady=8,
    bd=0,
    cursor="hand2",
  ).pack(padx=35, pady=25, fill="x")

def add_custom_noodle():
  def confirm():
    noodle, soup, qty = (
      noodle_var.get(),
      soup_var.get(),
      int(spin_qty.get()),
    )
    full_name = f"ก๋วยเตี๋ยว ({noodle} / {soup})"
    add_to_cart_dict(full_name, 55, qty)
    win.destroy()

  win = create_popup("🍜 ตัวเลือกก๋วยเตี๋ยว")
  tk.Label(
    win, text="1. เลือกเส้น:", font=FONT_BOLD, bg=BG_MENU_CARD, fg=TEXT_DARK
  ).pack(anchor="w", padx=35, pady=(20, 4))
  noodle_var = tk.StringVar(value="เส้นเล็ก")
  create_dropdown(
    win,
    noodle_var,
    ["เส้นเล็ก", "เส้นใหญ่", "เส้นหมี่", "บะหมี่", "วุ้นเส้น", "เกาเหลา"],
  )

  tk.Label(
    win, text="2. เลือกรสน้ำซุป:", font=FONT_BOLD, bg=BG_MENU_CARD, fg=TEXT_DARK
  ).pack(anchor="w", padx=35, pady=(12, 4))
  soup_var = tk.StringVar(value="น้ำใส")
  create_dropdown(
    win, soup_var, ["น้ำใส", "ต้มยำ", "น้ำตก", "เย็นตาโฟ", "แห้ง"]
  )

  spin_qty = create_qty_spinbox(win)
  tk.Button(
    win,
    text="✨ บันทึกรายการ",
    bg=ACCENT_BLUE,
    fg="white",
    font=FONT_BOLD,
    command=confirm,
    pady=8,
    bd=0,
    cursor="hand2",
  ).pack(padx=35, pady=25, fill="x")

def add_custom_fried_rice():
  def confirm():
    meat, size, has_egg, qty = (
      meat_var.get(),
      size_var.get(),
      egg_var.get(),
      int(spin_qty.get()),
    )
    price = (
      (50 if size == "ธรรมดา" else 60)
      + (10 if meat in ["เนื้อ (+10บ.)", "กุ้ง (+10บ.)"] else 0)
      + (10 if has_egg else 0)
    )
    clean_meat = meat.split(" ")[0]
    full_name = (
      f"ข้าวผัด{clean_meat} ({size})" + (" + ไข่ดาว" if has_egg else "")
    )
    add_to_cart_dict(full_name, price, qty)
    win.destroy()

  win = create_popup("🍚 ตัวเลือกข้าวผัด")
  tk.Label(
    win, text="1. เลือกเนื้อสัตว์:", font=FONT_BOLD, bg=BG_MENU_CARD, fg=TEXT_DARK
  ).pack(anchor="w", padx=35, pady=(16, 2))
  meat_var = tk.StringVar(value="หมู")
  create_dropdown(
    win, meat_var, ["หมู", "ไก่", "เนื้อ (+10บ.)", "กุ้ง (+10บ.)"]
  )

  tk.Label(
    win, text="2. เลือกขนาด:", font=FONT_BOLD, bg=BG_MENU_CARD, fg=TEXT_DARK
  ).pack(anchor="w", padx=35, pady=(10, 2))
  size_var = tk.StringVar(value="ธรรมดา")
  create_dropdown(win, size_var, ["ธรรมดา", "พิเศษ (+10บ.)"])

  egg_var = tk.BooleanVar(value=False)
  tk.Checkbutton(
    win,
    text="🍳 เพิ่มไข่ดาว (+10 บาท)",
    variable=egg_var,
    font=FONT_MAIN,
    bg=BG_MENU_CARD,
    fg=TEXT_DARK,
    activebackground=BG_MENU_CARD,
  ).pack(anchor="w", padx=35, pady=6)

  spin_qty = create_qty_spinbox(win)
  tk.Button(
    win,
    text="✨ บันทึกรายการ",
    bg="#0984E3",
    fg="white",
    font=FONT_BOLD,
    command=confirm,
    pady=8,
    bd=0,
    cursor="hand2",
  ).pack(padx=35, pady=20, fill="x")

def add_custom_tomyum():
  def confirm():
    soup, spicy, qty = (
      soup_var.get(),
      spicy_var.get(),
      int(spin_qty.get()),
    )
    full_name = f"ต้มยำกุ้ง ({soup} / {spicy})"
    add_to_cart_dict(full_name, 120, qty)
    win.destroy()

  win = create_popup("🥘 ตัวเลือกต้มยำกุ้ง")
  tk.Label(
    win, text="1. เลือกประเภทน้ำซุป:", font=FONT_BOLD, bg=BG_MENU_CARD, fg=TEXT_DARK
  ).pack(anchor="w", padx=35, pady=(20, 4))
  soup_var = tk.StringVar(value="น้ำข้น")
  create_dropdown(win, soup_var, ["น้ำข้น", "น้ำใส"])

  tk.Label(
    win, text="2. เลือกระดับความเผ็ด:", font=FONT_BOLD, bg=BG_MENU_CARD, fg=TEXT_DARK
  ).pack(anchor="w", padx=35, pady=(12, 4))
  spicy_var = tk.StringVar(value="เผ็ดปกติ")
  create_dropdown(win, spicy_var, ["เผ็ดน้อย", "เผ็ดปกติ", "เผ็ดมาก"])

  spin_qty = create_qty_spinbox(win)
  tk.Button(
    win,
    text="✨ บันทึกรายการ",
    bg="#D63031",
    fg="white",
    font=FONT_BOLD,
    command=confirm,
    pady=8,
    bd=0,
    cursor="hand2",
  ).pack(padx=35, pady=25, fill="x")

def add_custom_tea():
  def confirm():
    sweet, ice, qty = (
      sweet_var.get(),
      ice_var.get(),
      int(spin_qty.get()),
    )
    full_name = f"ชาเย็น (หวาน {sweet} / {ice})"
    add_to_cart_dict(full_name, 25, qty)
    win.destroy()

  win = create_popup("🧋 ตัวเลือกชาเย็น")
  tk.Label(
    win, text="1. เลือกระดับความหวาน:", font=FONT_BOLD, bg=BG_MENU_CARD, fg=TEXT_DARK
  ).pack(anchor="w", padx=35, pady=(20, 4))
  sweet_var = tk.StringVar(value="100% (หวานปกติ)")
  create_dropdown(
    win,
    sweet_var,
    ["0% (ไม่หวาน)", "25%", "50%", "100% (หวานปกติ)"],
  )

  tk.Label(
    win, text="2. การใส่น้ำแข็ง:", font=FONT_BOLD, bg=BG_MENU_CARD, fg=TEXT_DARK
  ).pack(anchor="w", padx=35, pady=(12, 4))
  ice_var = tk.StringVar(value="ใส่น้ำแข็ง")
  create_dropdown(win, ice_var, ["ใส่น้ำแข็ง", "แยกน้ำแข็ง"])

  spin_qty = create_qty_spinbox(win)
  tk.Button(
    win,
    text="✨ บันทึกรายการ",
    bg="#E17055",
    fg="white",
    font=FONT_BOLD,
    command=confirm,
    pady=8,
    bd=0,
    cursor="hand2",
  ).pack(padx=35, pady=25, fill="x")

def add_custom_water():
  def confirm():
    temp, has_ice, qty = temp_var.get(), ice_var.get(), int(spin_qty.get())
    price = 10 + (2 if has_ice else 0)
    full_name = (
      f"น้ำเปล่า ({temp})" + (" + แก้วน้ำแข็ง (+2บ.)" if has_ice else "")
    )
    add_to_cart_dict(full_name, price, qty)
    win.destroy()

  win = create_popup("💧 ตัวเลือกน้ำดื่ม")
  tk.Label(
    win, text="1. เลือกประเภท:", font=FONT_BOLD, bg=BG_MENU_CARD, fg=TEXT_DARK
  ).pack(anchor="w", padx=35, pady=(20, 4))
  temp_var = tk.StringVar(value="น้ำเย็น")
  create_dropdown(win, temp_var, ["น้ำเย็น", "น้ำธรรมดา (ไม่เย็น)"])

  ice_var = tk.BooleanVar(value=False)
  tk.Checkbutton(
    win,
    text="🧊 เพิ่มแก้วน้ำแข็ง (+2 บาท)",
    variable=ice_var,
    font=FONT_MAIN,
    bg=BG_MENU_CARD,
    fg=TEXT_DARK,
    activebackground=BG_MENU_CARD,
  ).pack(anchor="w", padx=35, pady=10)

  spin_qty = create_qty_spinbox(win)
  tk.Button(
    win,
    text="✨ บันทึกรายการ",
    bg="#74B9FF",
    fg="white",
    font=FONT_BOLD,
    command=confirm,
    pady=8,
    bd=0,
    cursor="hand2",
  ).pack(padx=35, pady=25, fill="x")

# --- การจัดการตะกร้าสินค้า ---
def add_to_cart_dict(full_name, price, qty):
  if qty > 0:
    if full_name in cart:
      cart[full_name]["qty"] += qty
      cart[full_name]["total"] += price * qty
    else:
      cart[full_name] = {"price": price, "qty": qty, "total": price * qty}
    update_cart_display()
    show_toast(root, f"🛒 เพิ่ม '{full_name}' ลงตะกร้าแล้ว", ACCENT_GREEN)

def update_cart_display():
  for row in tree.get_children():
    tree.delete(row)
  subtotal = 0
  for name, data in cart.items():
    tree.insert(
      "",
      "end",
      values=(
        name,
        f"{data['price']} บ.",
        f"x{data['qty']}",
        f"{data['total']} บ.",
      ),
    )
    subtotal += data["total"]
  vat = subtotal * 0.07
  grand_total = subtotal + vat
  lbl_subtotal.config(text=f"รวมราคาอาหาร : {subtotal:,.2f} บาท")
  lbl_vat.config(text=f"ภาษี VAT (7%) : {vat:,.2f} บาท")
  lbl_grand_total.config(text=f"ยอดรวมสุทธิ : {grand_total:,.2f} บาท")

def reset_order():
  if messagebox.askyesno("ยืนยัน", "ต้องการล้างรายการทั้งหมดหรือไม่?"):
    cart.clear()
    update_cart_display()
    show_toast(root, "🗑️ ล้างรายการในตะกร้าเรียบร้อย", TEXT_MUTED)

# --- ระบบชำระเงิน (Payment System) ---
def open_payment_window():
  if not cart:
    messagebox.showwarning("เตือน", "กรุณาเลือกอาหารก่อนทำการชำระเงิน")
    return
  subtotal = sum(data["total"] for data in cart.values())
  vat = subtotal * 0.07
  grand_total = subtotal + vat

  pay_win = tk.Toplevel(root)
  pay_win.title("💳 ระบบรับชำระเงิน (Cashier)")
  pay_win.geometry("440x560")
  pay_win.configure(bg=BG_CART_CARD)
  pay_win.grab_set()

  tk.Label(
    pay_win, text="ยอดรวมที่ต้องชำระ", font=FONT_BOLD, bg=BG_CART_CARD, fg=TEXT_MUTED
  ).pack(pady=(20, 0))
  lbl_amount = tk.Label(
    pay_win, text=f"{grand_total:,.2f} ฿", font=("Leelawadee UI", 26, "bold"), bg=BG_CART_CARD, fg=PRIMARY_COLOR
  )
  lbl_amount.pack(pady=(0, 10))

  tk.Label(pay_win, text="เลือกวิธีชำระเงิน:", font=FONT_BOLD, bg=BG_CART_CARD, fg=TEXT_DARK).pack(
    anchor="w", padx=35, pady=2
  )

  method_var = tk.StringVar(value="เงินสด")
  frame_cash = tk.Frame(pay_win, bd=1, relief="solid", bg="white", padx=15, pady=15)
  frame_qr = tk.Frame(pay_win, bd=1, relief="solid", bg="white", padx=15, pady=15)

  def toggle_method():
    if method_var.get() == "เงินสด":
      frame_qr.pack_forget()
      frame_cash.pack(fill="x", padx=35, pady=8)
    else:
      frame_cash.pack_forget()
      frame_qr.pack(fill="x", padx=35, pady=8)

  rb_cash = tk.Radiobutton(
    pay_win,
    text="💵 เงินสด (Cash)",
    variable=method_var,
    value="เงินสด",
    font=FONT_BOLD,
    bg=BG_CART_CARD,
    fg=TEXT_DARK,
    activebackground=BG_CART_CARD,
    command=toggle_method,
  )
  rb_cash.pack(anchor="w", padx=35)

  rb_qr = tk.Radiobutton(
    pay_win,
    text="📱 สแกน QR Code (PromptPay)",
    variable=method_var,
    value="QR Code",
    font=FONT_BOLD,
    bg=BG_CART_CARD,
    fg=TEXT_DARK,
    activebackground=BG_CART_CARD,
    command=toggle_method,
  )
  rb_qr.pack(anchor="w", padx=35)

  tk.Label(frame_cash, text="รับเงินมา (บาท):", font=FONT_BOLD, bg="white", fg=TEXT_DARK).pack(anchor="w")
  entry_received = tk.Entry(frame_cash, font=("Leelawadee UI", 14), justify="right", bd=1, relief="solid")
  entry_received.pack(fill="x", pady=6)

  lbl_change = tk.Label(
    frame_cash, text="เงินทอน: 0.00 บาท", font=FONT_BOLD, bg="white", fg=ACCENT_GREEN
  )
  lbl_change.pack(anchor="e", pady=4)

  def calc_change(event=None):
    try:
      received = float(entry_received.get())
      change = received - grand_total
      if change >= 0:
        lbl_change.config(text=f"เงินทอน: {change:,.2f} บาท", fg=ACCENT_GREEN)
      else:
        lbl_change.config(text="เงินยังขาดอยู่!", fg=PRIMARY_COLOR)
    except ValueError:
      lbl_change.config(text="กรุณากรอกตัวเลข", fg=PRIMARY_COLOR)

  entry_received.bind("<KeyRelease>", calc_change)

  tk.Label(
    frame_qr,
    text="📲 [ QR PROMPTPAY ]\nสแกนชำระเงินตามยอดผ่านแอปธนาคาร",
    font=FONT_BOLD,
    bg="white",
    fg="#0984E3",
    justify="center",
  ).pack(pady=12)

  toggle_method()

  def confirm_payment():
    method = method_var.get()
    change_text = ""
    if method == "เงินสด":
      try:
        received = float(entry_received.get())
        if received < grand_total:
          messagebox.showerror("ข้อผิดพลาด", "จำนวนเงินที่รับมาไม่พอชำระ!")
          return
        change_text = f"\nรับเงินมา: {received:,.2f} บาท\nเงินทอน: {(received - grand_total):,.2f} บาท"
      except ValueError:
        messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกจำนวนเงินสดให้ถูกต้อง")
        return
    pay_win.destroy()
    process_successful_order(method, change_text, grand_total, vat, subtotal)

  tk.Button(
    pay_win,
    text="✅ ยืนยันการชำระเงิน & พิมพ์ใบเสร็จ",
    bg=ACCENT_GREEN,
    fg="white",
    font=FONT_BOLD,
    command=confirm_payment,
    pady=10,
    bd=0,
    cursor="hand2",
  ).pack(padx=35, pady=20, fill="x")

def process_successful_order(method, change_text, grand_total, vat, subtotal):
  global order_counter
  order_id = f"A-{order_counter:03d}"
  order_counter += 1

  receipt_text = f"🧾 ใบเสร็จรับเงิน ({order_id})\n" + "-" * 36 + "\n"
  summary_items = []
  for name, data in cart.items():
    receipt_text += (
      f"{name}\n x{data['qty']} @ {data['price']} = {data['total']} บาท\n"
    )
    summary_items.append(f"{name} (x{data['qty']})")

  receipt_text += "-" * 36 + "\n"
  receipt_text += f"ราคารวม : {subtotal:,.2f} บาท\n"
  receipt_text += f"VAT 7% : {vat:,.2f} บาท\n"
  receipt_text += f"ยอดสุทธิ : {grand_total:,.2f} บาท\n"
  receipt_text += f"ช่องทางชำระ : {method}{change_text}\n"
  receipt_text += "=" * 36 + "\nขอบคุณที่ใช้บริการครับ 🙏"

  messagebox.showinfo("ชำระเงินสำเร็จ", receipt_text)

  items_str = ", ".join(summary_items)
  item_id = tree_status.insert(
    "",
    0,
    values=(
      order_id,
      items_str,
      "⏳ รอกำลังทำ...",
      time.strftime("%H:%M:%S"),
    ),
    tags=("pending",)
  )

  cart.clear()
  update_cart_display()
  show_toast(root, f"🚀 ส่งออเดอร์ {order_id} เข้าห้องครัวแล้ว!", "#0984E3")

  def process_kitchen():
    time.sleep(5)
    root.after(
      0,
      lambda: [
        tree_status.set(item_id, "status", "🔥 กำลังปรุงอาหาร..."),
        tree_status.item(item_id, tags=("cooking",)),
        show_toast(root, f"🍳 ออเดอร์ {order_id} กำลังปรุงอยู่", ACCENT_ORANGE)
      ]
    )
    time.sleep(7)
    root.after(
      0,
      lambda: [
        tree_status.set(item_id, "status", "✨ พร้อมเสิร์ฟ"),
        tree_status.item(item_id, tags=("ready",)),
        show_toast(root, f"🔔 ออเดอร์ {order_id} อาหารเสร็จแล้ว!", ACCENT_GREEN)
      ]
    )

  threading.Thread(target=process_kitchen, daemon=True).start()

# --- GUI หน้าต่างหลัก ---
root = tk.Tk()
root.title("🍽️ POS Restaurant - ระบบสั่งอาหารและชำระเงิน")
root.geometry("1020x740")
root.configure(bg=BG_MAIN)
root.resizable(False, False)

# ตกแต่งสไตล์ Treeview (ตาราง)
style = ttk.Style()
style.theme_use("clam")
style.configure(
  "Treeview.Heading",
  font=FONT_BOLD,
  background="#B2EBF2", # สีหัวตารางฟ้าพาสเทล
  foreground=TEXT_DARK,
  borderwidth=0,
)
style.configure(
  "Treeview",
  font=FONT_MAIN,
  rowheight=30,
  background="white",
  fieldbackground="white",
  bd=0,
)
style.map("Treeview", background=[("selected", "#FFEAA7")], foreground=[("selected", TEXT_DARK)])

# ฝั่งซ้าย: รายการเมนู (ส้มพีชพาสเทล)
frame_menu = tk.LabelFrame(
  root, text=" 🍔 รายการเมนูอาหาร ", font=FONT_TITLE, bg=BG_MENU_CARD, fg="#D35400", padx=12, pady=6, bd=2, relief="groove"
)
frame_menu.place(x=15, y=10, width=480, height=450)

menu_items = [
  ("🍳 ผัดกะเพรา", "เลือกเนื้อสัตว์ + ใส่ / ไม่ใส่ไข่ดาว", PRIMARY_COLOR, add_custom_kaprao),
  ("🍝 ผัดไทย", "เลือกเนื้อสัตว์ หมู / ไก่ / กุ้ง", "#FF7675", add_custom_padthai),
  ("🍜 ก๋วยเตี๋ยว", "เลือกเส้น + เลือกรสน้ำซุป", ACCENT_BLUE, add_custom_noodle),
  ("🍚 ข้าวผัด", "เลือกเนื้อสัตว์ + ขนาด + ไข่ดาว", "#0984E3", add_custom_fried_rice),
  ("🥘 ต้มยำกุ้ง", "เลือกรสน้ำซุป + ระดับความเผ็ด", "#D63031", add_custom_tomyum),
  ("🧋 ชาเย็น", "เลือกระดับความหวาน + น้ำแข็ง", "#E17055", add_custom_tea),
  ("💧 น้ำเปล่า", "เลือกประเภทน้ำ + แก้วน้ำแข็ง", "#74B9FF", add_custom_water),
]

for name, desc, color, cmd in menu_items:
  row = tk.Frame(frame_menu, bd=1, relief="solid", bg="white", pady=3, padx=8)
  row.pack(fill="x", pady=2)

  tf = tk.Frame(row, bg="white")
  tf.pack(side="left", fill="x", expand=True)

  tk.Label(tf, text=name, font=FONT_BOLD, bg="white", fg=TEXT_DARK, anchor="w").pack(fill="x")
  tk.Label(
    tf,
    text=desc,
    font=("Leelawadee UI", 8),
    bg="white",
    fg=TEXT_MUTED,
    anchor="w",
  ).pack(fill="x")

  tk.Button(
    row,
    text="เลือกออปชัน ⚙️",
    bg=color,
    fg="white",
    font=FONT_BOLD,
    command=cmd,
    padx=10,
    pady=2,
    bd=0,
    cursor="hand2",
  ).pack(side="right")

# ฝั่งขวา: ตะกร้าสินค้า (ฟ้ามินต์พาสเทล)
frame_cart = tk.LabelFrame(
  root, text=" 🛒 ตะกร้าสินค้า ", font=FONT_TITLE, bg=BG_CART_CARD, fg="#00838F", padx=12, pady=10, bd=2, relief="groove"
)
frame_cart.place(x=510, y=10, width=495, height=450)

tree_columns = ("name", "price", "qty", "total")
tree = ttk.Treeview(
  frame_cart, columns=tree_columns, show="headings", height=8
)
tree.heading("name", text="รายการ")
tree.heading("price", text="ราคา")
tree.heading("qty", text="จำนวน")
tree.heading("total", text="รวม")

tree.column("name", width=230)
tree.column("price", width=65, anchor="center")
tree.column("qty", width=55, anchor="center")
tree.column("total", width=85, anchor="e")
tree.pack(fill="x", pady=(0, 6))

lbl_subtotal = tk.Label(
  frame_cart, text="รวมราคาอาหาร : 0.00 บาท", font=FONT_MAIN, bg=BG_CART_CARD, fg=TEXT_MUTED
)
lbl_subtotal.pack(anchor="e", padx=10)

lbl_vat = tk.Label(
  frame_cart, text="ภาษี VAT (7%) : 0.00 บาท", font=FONT_MAIN, bg=BG_CART_CARD, fg=TEXT_MUTED
)
lbl_vat.pack(anchor="e", padx=10)

lbl_grand_total = tk.Label(
  frame_cart, text="ยอดรวมสุทธิ : 0.00 บาท", font=FONT_HEADER, bg=BG_CART_CARD, fg=PRIMARY_COLOR
)
lbl_grand_total.pack(anchor="e", padx=10, pady=(4, 12))

btn_frame = tk.Frame(frame_cart, bg=BG_CART_CARD)
btn_frame.pack(fill="x")

tk.Button(
  btn_frame,
  text="🗑️ ล้างรายการ",
  bg="#636E72",
  fg="white",
  font=FONT_BOLD,
  command=reset_order,
  pady=8,
  bd=0,
  cursor="hand2",
).pack(side="left", fill="x", expand=True, padx=(0, 5))

tk.Button(
  btn_frame,
  text="💰 เช็กบิล / รับชำระเงิน",
  bg=ACCENT_GREEN,
  fg="white",
  font=FONT_BOLD,
  command=open_payment_window,
  pady=8,
  bd=0,
  cursor="hand2",
).pack(side="right", fill="x", expand=True, padx=(5, 0))

# ส่วนล่าง: ตารางติดตามสถานะอาหารในครัว (ม่วงพาสเทล)
frame_status = tk.LabelFrame(
  root,
  text=" 👨‍🍳 สถานะรายการอาหารในครัว (Live Tracking) ",
  font=FONT_TITLE,
  bg=BG_STATUS_CARD,
  fg="#6C5CE7",
  padx=12,
  pady=10,
  bd=2,
  relief="groove",
)
frame_status.place(x=15, y=475, width=990, height=245)

status_cols = ("order_id", "items", "status", "time")
tree_status = ttk.Treeview(
  frame_status, columns=status_cols, show="headings", height=5
)
tree_status.heading("order_id", text="เลขที่ออเดอร์")
tree_status.heading("items", text="รายการอาหาร")
tree_status.heading("status", text="สถานะปัจจุบัน")
tree_status.heading("time", text="เวลาสั่ง")

tree_status.column("order_id", width=110, anchor="center")
tree_status.column("items", width=520)
tree_status.column("status", width=200, anchor="center")
tree_status.column("time", width=110, anchor="center")
tree_status.pack(fill="both", expand=True)

# การใส่สีไฮไลต์สถานะของออเดอร์ในตาราง
tree_status.tag_configure("pending", background="#FFF3BF", foreground="#856404") # เหลืองพาสเทล
tree_status.tag_configure("cooking", background="#FFE3E3", foreground="#C92A2A") # ส้ม/แดงพาสเทล
tree_status.tag_configure("ready", background="#D3F9D8", foreground="#2B8A3E")  # เขียวพาสเทล

root.mainloop()