import pandas as pd

# 1. Masters Dataset (Ledgers & Stock Items)
masters_data = [
    {"Master Type": "Ledger", "Name": "Director's Capital", "Parent Group": "Capital Account", "UOM": ""},
    {"Master Type": "Ledger", "Name": "HDFC Bank", "Parent Group": "Bank Accounts", "UOM": ""},
    {"Master Type": "Ledger", "Name": "ICICI Bank Loan", "Parent Group": "Loans (Liability)", "UOM": ""},
    {"Master Type": "Ledger", "Name": "Dell Computers", "Parent Group": "Sundry Creditors", "UOM": ""},
    {"Master Type": "Ledger", "Name": "Britannia Industries", "Parent Group": "Sundry Creditors", "UOM": ""},
    {"Master Type": "Ledger", "Name": "HUL", "Parent Group": "Sundry Creditors", "UOM": ""},
    {"Master Type": "Ledger", "Name": "Krishna Kirana Store", "Parent Group": "Sundry Debtors", "UOM": ""},
    {"Master Type": "Ledger", "Name": "Mega Supermarket", "Parent Group": "Sundry Debtors", "UOM": ""},
    {"Master Type": "Ledger", "Name": "Sales Account", "Parent Group": "Sales Accounts", "UOM": ""},
    {"Master Type": "Ledger", "Name": "Purchase Account", "Parent Group": "Purchase Accounts", "UOM": ""},
    {"Master Type": "Ledger", "Name": "Packing Material Expense", "Parent Group": "Direct Expenses", "UOM": ""},
    {"Master Type": "Ledger", "Name": "Freight Inward", "Parent Group": "Direct Expenses", "UOM": ""},
    {"Master Type": "Ledger", "Name": "Rent Expense", "Parent Group": "Indirect Expenses", "UOM": ""},
    {"Master Type": "Ledger", "Name": "Salary Expense", "Parent Group": "Indirect Expenses", "UOM": ""},
    {"Master Type": "Ledger", "Name": "Electricity Expense", "Parent Group": "Indirect Expenses", "UOM": ""},
    {"Master Type": "Ledger", "Name": "Printing & Stationery", "Parent Group": "Indirect Expenses", "UOM": ""},
    {"Master Type": "Ledger", "Name": "Staff Advance", "Parent Group": "Loans & Advances (Asset)", "UOM": ""},
    {"Master Type": "Ledger", "Name": "Discount Allowed", "Parent Group": "Indirect Expenses", "UOM": ""},
    {"Master Type": "Ledger", "Name": "Interest Income", "Parent Group": "Indirect Incomes", "UOM": ""},
    {"Master Type": "Ledger", "Name": "Computers", "Parent Group": "Fixed Assets", "UOM": ""},
    {"Master Type": "Ledger", "Name": "Depreciation", "Parent Group": "Indirect Expenses", "UOM": ""},
    {"Master Type": "Ledger", "Name": "Internet Expense", "Parent Group": "Indirect Expenses", "UOM": ""},
    {"Master Type": "Ledger", "Name": "Outstanding Expenses", "Parent Group": "Current Liabilities", "UOM": ""},
    {"Master Type": "Stock Item", "Name": "Biscuits (Boxes)", "Parent Group": "Primary", "UOM": "Box"},
    {"Master Type": "Stock Item", "Name": "Bathing Soap (Cases)", "Parent Group": "Primary", "UOM": "Case"}
]

# 2. Vouchers Dataset (All 25 Daily Transactions)
vouchers_data = [
    {"Date": "2026-04-01", "Voucher Type": "Receipt", "Voucher No": "RCP-001", "Debit Ledger": "Cash", "Credit Ledger": "Director's Capital", "Amount": 1000000, "Narration": "Capital infused by directors in cash"},
    {"Date": "2026-04-01", "Voucher Type": "Contra", "Voucher No": "CNT-001", "Debit Ledger": "HDFC Bank", "Credit Ledger": "Cash", "Amount": 500000, "Narration": "Cash deposited into HDFC Bank"},
    {"Date": "2026-04-02", "Voucher Type": "Receipt", "Voucher No": "RCP-002", "Debit Ledger": "HDFC Bank", "Credit Ledger": "ICICI Bank Loan", "Amount": 300000, "Narration": "Secured bank loan credited from ICICI Bank"},
    {"Date": "2026-04-03", "Voucher Type": "Journal", "Voucher No": "JRN-001", "Debit Ledger": "Computers", "Credit Ledger": "Dell Computers", "Amount": 45000, "Narration": "Purchased office computers on credit from Dell"},
    {"Date": "2026-04-03", "Voucher Type": "Payment", "Voucher No": "PAY-001", "Debit Ledger": "Packing Material Expense", "Credit Ledger": "Cash", "Amount": 1000000, "Narration": "Loose packing materials purchased in cash"},
    {"Date": "2026-04-04", "Voucher Type": "Purchase", "Voucher No": "PUR-001", "Debit Ledger": "Purchase Account", "Credit Ledger": "Britannia Industries", "Amount": 100000, "Narration": "Purchased 500 boxes biscuits @ 200/box"},
    {"Date": "2026-04-04", "Voucher Type": "Purchase", "Voucher No": "PUR-002", "Debit Ledger": "Purchase Account", "Credit Ledger": "HUL", "Amount": 300000, "Narration": "Purchased 200 cases bathing soap @ 1500/case"},
    {"Date": "2026-04-05", "Voucher Type": "Debit Note", "Voucher No": "DN-001", "Debit Ledger": "Britannia Industries", "Credit Ledger": "Purchase Account", "Amount": 4000, "Narration": "Returned 20 damaged boxes of biscuits"},
    {"Date": "2026-04-05", "Voucher Type": "Payment", "Voucher No": "PAY-002", "Debit Ledger": "Freight Inward", "Credit Ledger": "Cash", "Amount": 5000, "Narration": "Paid cash for freight charges on goods purchased"},
    {"Date": "2026-04-06", "Voucher Type": "Sales", "Voucher No": "SAL-001", "Debit Ledger": "Cash", "Credit Ledger": "Sales Account", "Amount": 15000, "Narration": "Cash sales of 50 boxes of biscuits"},
    {"Date": "2026-04-06", "Voucher Type": "Sales", "Voucher No": "SAL-002", "Debit Ledger": "Krishna Kirana Store", "Credit Ledger": "Sales Account", "Amount": 180000, "Narration": "Credit sales of 100 cases soap @ 1800/case"},
    {"Date": "2026-04-07", "Voucher Type": "Sales", "Voucher No": "SAL-003", "Debit Ledger": "Mega Supermarket", "Credit Ledger": "Sales Account", "Amount": 45000, "Narration": "Credit sales of 150 boxes biscuits @ 300/box"},
    {"Date": "2026-04-07", "Voucher Type": "Credit Note", "Voucher No": "CN-001", "Debit Ledger": "Sales Account", "Credit Ledger": "Krishna Kirana Store", "Amount": 9000, "Narration": "Sales return of 5 defective cases soap"},
    {"Date": "2026-04-08", "Voucher Type": "Journal", "Voucher No": "JRN-002", "Debit Ledger": "Discount Allowed", "Credit Ledger": "Mega Supermarket", "Amount": 200000, "Narration": "Cash discount allowed to Mega Supermarket on bulk order"},
    {"Date": "2026-04-10", "Voucher Type": "Payment", "Voucher No": "PAY-003", "Debit Ledger": "Britannia Industries", "Credit Ledger": "HDFC Bank", "Amount": 50000, "Narration": "Paid Britannia Industries via HDFC Bank cheque"},
    {"Date": "2026-04-10", "Voucher Type": "Payment", "Voucher No": "PAY-004", "Debit Ledger": "Rent Expense", "Credit Ledger": "HDFC Bank", "Amount": 2500000, "Narration": "Paid warehouse and office rent via bank transfer"},
    {"Date": "2026-04-11", "Voucher Type": "Payment", "Voucher No": "PAY-005", "Debit Ledger": "Salary Expense", "Credit Ledger": "Cash", "Amount": 120000, "Narration": "Paid monthly staff salaries in cash"},
    {"Date": "2026-04-11", "Voucher Type": "Payment", "Voucher No": "PAY-006", "Debit Ledger": "Electricity Expense", "Credit Ledger": "HDFC Bank", "Amount": 8500, "Narration": "Paid office electricity bill via debit card"},
    {"Date": "2026-04-12", "Voucher Type": "Payment", "Voucher No": "PAY-007", "Debit Ledger": "Printing & Stationery", "Credit Ledger": "Cash", "Amount": 2500, "Narration": "Purchased office stationery in cash"},
    {"Date": "2026-04-12", "Voucher Type": "Payment", "Voucher No": "PAY-008", "Debit Ledger": "Staff Advance", "Credit Ledger": "Cash", "Amount": 500000, "Narration": "Advanced cash to sales executive for travel"},
    {"Date": "2026-04-15", "Voucher Type": "Receipt", "Voucher No": "RCP-003", "Debit Ledger": "HDFC Bank", "Credit Ledger": "Krishna Kirana Store", "Amount": 150000, "Narration": "Received cheque from Krishna Kirana Store"},
    {"Date": "2026-04-15", "Voucher Type": "Receipt", "Voucher No": "RCP-004", "Debit Ledger": "HDFC Bank", "Credit Ledger": "Mega Supermarket", "Amount": 4000000, "Narration": "Received NEFT collection from Mega Supermarket"},
    {"Date": "2026-04-16", "Voucher Type": "Receipt", "Voucher No": "RCP-005", "Debit Ledger": "HDFC Bank", "Credit Ledger": "Interest Income", "Amount": 3200, "Narration": "Interest credited by bank"},
    {"Date": "2026-04-30", "Voucher Type": "Journal", "Voucher No": "JRN-003", "Debit Ledger": "Depreciation", "Credit Ledger": "Computers", "Amount": 4500, "Narration": "10% depreciation charged on computers"},
    {"Date": "2026-04-30", "Voucher Type": "Journal", "Voucher No": "JRN-004", "Debit Ledger": "Internet Expense", "Credit Ledger": "Outstanding Expenses", "Amount": 1500, "Narration": "Provision for outstanding internet bill"}
]

# Save to multi-sheet Excel file
with pd.ExcelWriter("Tally_Import_data.xlsx", engine="openpyxl") as writer:
    pd.DataFrame(masters_data).to_excel(writer, sheet_name="Masters", index=False)
    pd.DataFrame(vouchers_data).to_excel(writer, sheet_name="Transactions", index=False)

print("Excel import file generated successfully: Tally_Import_data.xlsx")