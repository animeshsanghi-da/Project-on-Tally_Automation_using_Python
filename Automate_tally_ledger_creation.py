import os
import time
import pandas as pd
import pyautogui

# --------------------------------------------------------
# Safety Settings for PyAutoGUI
# --------------------------------------------------------
pyautogui.FAILSAFE = True  # Move mouse to top-left corner of screen to abort
pyautogui.PAUSE = 0.6     # Time delay (seconds) between keypresses

# --------------------------------------------------------
# Load sheets from Excel
# --------------------------------------------------------

# Target Excel File Name
EXCEL_FILE = "Tally_Import_data.xlsx"

xls = pd.ExcelFile(EXCEL_FILE)

df_ledger = pd.read_excel(EXCEL_FILE, sheet_name="Ledger")
df_stock = pd.read_excel(EXCEL_FILE, sheet_name="Stock_Item")
df_trans = pd.read_excel(EXCEL_FILE, sheet_name="Transactions")

# --------------------------------------------------------
# Start countdown
# --------------------------------------------------------
# Gives you 5 seconds time to click into Tally Prime before automation starts.
for i in range(5, 0, -1):
    print(f"Starting in {i}...", end="\r", flush=True)
    time.sleep(1)

# --------------------------------------------------------
# Automates creation of Ledgers from the 'Ledger' sheet.
# --------------------------------------------------------
print("\n>>> Creating Ledgers...")

pyautogui.press("c")
time.sleep(0.4)
pyautogui.typewrite("ledger")
pyautogui.press("enter")
time.sleep(0.4)

for idx, row in df_ledger.iterrows():
    name = str(row["Name"]).strip()
    group = str(row["Parent Group"]).strip()
    print(f"   >>> Creating '{name}' Ledger...")
    pyautogui.typewrite(name)
    pyautogui.press("enter")
    pyautogui.press("enter")
    pyautogui.typewrite(group)
    pyautogui.press("enter")
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.4)

pyautogui.press("esc", presses=3, interval=0.3)

# --------------------------------------------------------
# Automates creation of stock items from the 'stock item' sheet.
# --------------------------------------------------------
print("\n>>> Creating stock items...")

pyautogui.press("c")  # 'Create' menu
time.sleep(0.4)
pyautogui.typewrite("stock item")
pyautogui.press("enter")
time.sleep(0.4)

for idx, row in df_stock.iterrows():
    name = str(row["Name"]).strip()
    group = str(row["Parent Group"]).strip()
    uom = str(row["UOM"]).strip()
    print(f"   >>> Creating '{name}' stock items...")
    pyautogui.typewrite(name)
    pyautogui.press("enter")
    pyautogui.press("enter")
    pyautogui.typewrite(group)
    pyautogui.press("enter")
    pyautogui.press("enter")
    pyautogui.hotkey("alt", "c")
    pyautogui.typewrite(uom)
    pyautogui.press("enter")
    pyautogui.press("enter")
    pyautogui.typewrite(uom)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.4)

pyautogui.press("esc", presses=3, interval=0.3)

# --------------------------------------------------------
# Automates Voucher entry from the 'Transactions' sheet.
# --------------------------------------------------------
print("\n>>> Creating Vouchers...")

pyautogui.press("v")
time.sleep(0.5)

for idx, row in df_trans.iterrows():
    vtype = str(row["Voucher Type"]).strip().lower()
    # date can only be 01 or 02 because we are using education mode.
    vdate = pd.to_datetime(row["Date"]).strftime("01-%m-%Y")
    dr_ledger = str(row["Debit Ledger"]).strip()
    cr_ledger = str(row["Credit Ledger"]).strip()
    amount = str(row["Amount"]).strip()
    narration = str(row["Narration"]).strip()
    print(f"   >>> Creating {vtype} voucher: '{narration}'...")


    if vtype == "contra" or vtype == "receipt":
        if vtype == "contra":
            pyautogui.press("f4")
        else:
            pyautogui.press("f6")
        time.sleep(0.4)
        pyautogui.press("f2")
        pyautogui.typewrite(vdate)
        pyautogui.press("enter")

        pyautogui.typewrite(cr_ledger)
        pyautogui.press("enter")
        pyautogui.typewrite(amount)
        pyautogui.press("enter")
        if cr_ledger.lower() == "hdfc bank":
            pyautogui.hotkey("ctrl", "a")
        pyautogui.press("enter")
        pyautogui.typewrite(dr_ledger)
        pyautogui.press("enter")
        pyautogui.press("enter")
        if dr_ledger.lower() == "hdfc bank":
            pyautogui.hotkey("ctrl", "a")
        pyautogui.typewrite(narration)
        pyautogui.press("enter")


    elif vtype == "payment" or vtype == "journal":
        if vtype == "payment":
            pyautogui.press("f5")
        else:
            pyautogui.press("f7")
        time.sleep(0.4)
        pyautogui.press("f2")
        pyautogui.typewrite(vdate)
        pyautogui.press("enter")

        pyautogui.typewrite(dr_ledger)
        pyautogui.press("enter")
        pyautogui.typewrite(amount)
        pyautogui.press("enter")
        if dr_ledger.lower() == "hdfc bank":
            pyautogui.hotkey("ctrl", "a")
        pyautogui.press("enter")
        pyautogui.typewrite(cr_ledger)
        pyautogui.press("enter")
        pyautogui.press("enter")
        if cr_ledger.lower() == "hdfc bank":
            pyautogui.hotkey("ctrl", "a")
        pyautogui.typewrite(narration)
        pyautogui.press("enter")
    

    elif vtype == "sales" or vtype == "purchase":
        if vtype == "sales":
            pyautogui.press("f9")
            pyautogui.press("f8")
        else:
            pyautogui.press("f8")
            pyautogui.press("f9")
        time.sleep(0.4)
        pyautogui.press("f2")
        pyautogui.typewrite(vdate)
        pyautogui.press("enter")

        pyautogui.hotkey("ctrl", "h")
        pyautogui.typewrite("As Voucher")
        pyautogui.press("enter")
        if vtype == "sales":
            pyautogui.typewrite(dr_ledger)
            pyautogui.hotkey("ctrl", "a")
            pyautogui.hotkey("ctrl", "a")
            pyautogui.typewrite(amount)
            pyautogui.press("enter")
            pyautogui.hotkey("ctrl", "a")
            pyautogui.typewrite(cr_ledger)
        else:
            pyautogui.typewrite(cr_ledger)
            pyautogui.hotkey("ctrl", "a")
            pyautogui.hotkey("ctrl", "a")
            pyautogui.typewrite(amount)
            pyautogui.press("enter")
            pyautogui.hotkey("ctrl", "a")
            pyautogui.typewrite(dr_ledger)
        pyautogui.hotkey("ctrl", "a")
        pyautogui.press("enter")
        pyautogui.typewrite(narration)
        pyautogui.press("enter")

    elif vtype == "debit note" or vtype == "credit note":
        if vtype == "debit note":
            pyautogui.hotkey("alt", "f5")
        else:
            pyautogui.hotkey("alt", "f6")
        time.sleep(0.4)
        pyautogui.press("f2")
        pyautogui.typewrite(vdate)
        pyautogui.press("enter")

        pyautogui.hotkey("ctrl", "h")
        pyautogui.typewrite("As Voucher")
        pyautogui.press("enter")
        if vtype == "debit note":
            pyautogui.typewrite(dr_ledger)
            pyautogui.hotkey("ctrl", "a")
            pyautogui.hotkey("ctrl", "a")
            pyautogui.typewrite(amount)
            pyautogui.press("enter")
            pyautogui.hotkey("ctrl", "a")
            pyautogui.typewrite(cr_ledger)
            pyautogui.press("enter")
            pyautogui.hotkey("ctrl", "a")
            pyautogui.press("enter")
            pyautogui.typewrite("No")
        else:
            pyautogui.typewrite(cr_ledger)
            pyautogui.hotkey("ctrl", "a")
            pyautogui.hotkey("ctrl", "a")
            pyautogui.typewrite(amount)
            pyautogui.press("enter")
            pyautogui.press("enter")
            pyautogui.press("enter")
            pyautogui.press("enter")
            pyautogui.typewrite(dr_ledger)
            pyautogui.press("enter")
            pyautogui.hotkey("ctrl", "a")
        pyautogui.press("enter")
        pyautogui.typewrite(narration)
        pyautogui.press("enter")
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.5)