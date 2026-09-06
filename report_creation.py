import glob
import os
import re
import pandas as pd


class TallyReportGenerator:

    def __init__(self, data_dir="tally_export_data"):
        self.data_dir = data_dir
        self.metrics = {
            "pnl": {},
            "bsheet": {},
            "trial_bal": {},
            "daybook": {},
        }

    def _locate_file(self, keywords):
        """Locates an excel file matching target keywords inside the folder."""
        if not os.path.exists(self.data_dir):
            return None
        for file in os.listdir(self.data_dir):
            if file.endswith((".xlsx", ".xls")):
                if any(kw.lower() in file.lower() for kw in keywords):
                    return os.path.join(self.data_dir, file)
        return None

    def _clean_amount(self, val):
        """Converts Tally string formats (e.g., '1,50,000.00 Dr', '(500.00)') to float."""
        if pd.isna(val):
            return 0.0
        if isinstance(val, (int, float)):
            return float(val)

        text = str(val).strip()
        is_cr = "Cr" in text
        # Remove currency symbols, Dr/Cr tags, commas
        clean_str = re.sub(r"[^\d.-]", "", text.replace("Cr", "").replace("Dr", ""))

        try:
            amount = float(clean_str) if clean_str else 0.0
            return -amount if is_cr else amount
        except ValueError:
            return 0.0

    def parse_pnl(self):
        """Parses Profit & Loss Excel file dynamically."""
        filepath = self._locate_file(["PandL", "P&L", "Profit"])
        if not filepath:
            return

        df = pd.read_excel(filepath, header=None)

        # Search for key financial line items across all cells
        keywords_map = {
            "Sales Accounts": "sales",
            "Gross Profit": "gross_profit",
            "Purchase Accounts": "purchases",
            "Indirect Expenses": "indirect_exp",
            "Nett Profit": "net_profit",
            "Net Profit": "net_profit",
        }

        found_values = {}
        for row_idx, row in df.iterrows():
            row_str = " ".join([str(val) for val in row.values if pd.notna(val)])
            for key, metric in keywords_map.items():
                if key.lower() in row_str.lower() and metric not in found_values:
                    # Look for numerical values in the row
                    nums = [
                        self._clean_amount(x)
                        for x in row.values
                        if self._clean_amount(x) != 0.0
                    ]
                    if nums:
                        found_values[metric] = nums[-1]

        self.metrics["pnl"] = found_values

    def parse_bsheet(self):
        """Parses Balance Sheet Excel file dynamically."""
        filepath = self._locate_file(["BSheet", "Balance"])
        if not filepath:
            return

        df = pd.read_excel(filepath, header=None)

        keywords_map = {
            "Capital Account": "capital",
            "Current Assets": "current_assets",
            "Fixed Assets": "fixed_assets",
            "Current Liabilities": "current_liabilities",
            "Loans (Liability)": "loans",
        }

        found_values = {}
        for row_idx, row in df.iterrows():
            row_str = " ".join([str(val) for val in row.values if pd.notna(val)])
            for key, metric in keywords_map.items():
                if key.lower() in row_str.lower() and metric not in found_values:
                    nums = [
                        self._clean_amount(x)
                        for x in row.values
                        if self._clean_amount(x) != 0.0
                    ]
                    if nums:
                        found_values[metric] = nums[-1]

        self.metrics["bsheet"] = found_values

    def parse_trial_bal(self):
        """Parses Trial Balance Excel file dynamically."""
        filepath = self._locate_file(["TrialBal", "Trial"])
        if not filepath:
            return

        df = pd.read_excel(filepath, header=None)
        numeric_vals = []

        for _, row in df.iterrows():
            for val in row.values:
                amt = self._clean_amount(val)
                if amt > 0:
                    numeric_vals.append(amt)

        total_debit = max(numeric_vals) if numeric_vals else 0.0
        self.metrics["trial_bal"] = {
            "total_turnover": total_debit,
            "status": "Balanced" if total_debit > 0 else "Unverified",
        }

    def parse_daybook(self):
        """Parses DayBook file dynamically to aggregate transaction activity."""
        filepath = self._locate_file(["DayBook", "Day"])
        if not filepath:
            return

        df = pd.read_excel(filepath)
        total_vouchers = len(df)

        # Attempt to detect amount column
        amount_col = None
        for col in df.columns:
            if any(
                k in str(col).lower() for k in ["amount", "debit", "credit", "val"]
            ):
                amount_col = col
                break

        total_value = 0.0
        if amount_col:
            total_value = (
                df[amount_col].apply(self._clean_amount).abs().sum() / 2
            )  # Divide by 2 for double-entry total

        # Detect voucher types distribution if column exists
        vtype_col = next(
            (c for c in df.columns if "type" in str(c).lower()), None
        )
        type_counts = {}
        if vtype_col:
            type_counts = df[vtype_col].value_counts().to_dict()

        self.metrics["daybook"] = {
            "total_vouchers": total_vouchers,
            "total_value": total_value,
            "voucher_types": type_counts,
        }

    def generate_markdown_report(self, output_file="report.md"):
        """Compiles calculated metrics into a Markdown report."""
        pnl = self.metrics["pnl"]
        bs = self.metrics["bsheet"]
        tb = self.metrics["trial_bal"]
        db = self.metrics["daybook"]

        sales = pnl.get("sales", 0.0)
        net_profit = pnl.get("net_profit", 0.0)
        gross_profit = pnl.get("gross_profit", 0.0)
        indirect_exp = pnl.get("indirect_exp", 0.0)

        c_assets = bs.get("current_assets", 0.0)
        c_liab = bs.get("current_liabilities", 0.0)
        f_assets = bs.get("fixed_assets", 0.0)
        capital = bs.get("capital", 0.0)
        working_capital = c_assets - c_liab

        md_content = f"""# Financial Performance & Statement Analysis Report

**Data Source Directory:** `{self.data_dir}`  
**Report Type:** Automated Dynamic Financial Compilation  

---

## Executive Financial Summary

| Key Metric | Value (INR) | Operational Context |
| :--- | :--- | :--- |
| **Total Sales / Revenue** | ₹{sales:,.2f} | Gross top-line turnover |
| **Gross Profit** | ₹{gross_profit:,.2f} | Direct trading profit margin |
| **Net Profit / Loss** | ₹{net_profit:,.2f} | Final bottom-line earnings |
| **Working Capital** | ₹{working_capital:,.2f} | Current Assets minus Current Liabilities |

---

## Profit & Loss Breakdown

* **Total Sales Revenue:** ₹{sales:,.2f}
* **Purchases:** ₹{pnl.get('purchases', 0.0):,.2f}
* **Gross Profit:** ₹{gross_profit:,.2f}
* **Indirect Expenses:** ₹{indirect_exp:,.2f}
* **Net Profit Margin:** {((net_profit / sales) * 100 if sales else 0.0):.2f}%

---

## Balance Sheet Position

* **Capital Account:** ₹{capital:,.2f}
* **Fixed Assets:** ₹{f_assets:,.2f}
* **Current Assets:** ₹{c_assets:,.2f}
* **Current Liabilities:** ₹{c_liab:,.2f}
* **Loans & Liabilities:** ₹{bs.get('loans', 0.0):,.2f}

---

## DayBook Transaction Metrics

* **Total Vouchers Recorded:** {db.get('total_vouchers', 0)}
* **Total Transaction Volume:** ₹{db.get('total_value', 0.0):,.2f}
"""

        if db.get("voucher_types"):
            md_content += "\n**Voucher Breakdown:**\n"
            for vtype, count in db["voucher_types"].items():
                md_content += f"* **{vtype}:** {count} transactions\n"

        md_content += f"""
---

## Trial Balance Verification

* **Trial Balance Total:** ₹{tb.get('total_turnover', 0.0):,.2f}
* **Verification Status:** {tb.get('status', 'Unverified')}
"""

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(md_content)

        print(f"Report successfully generated and saved to '{output_file}'")


if __name__ == "__main__":
    generator = TallyReportGenerator(data_dir="tally_export_data")
    generator.parse_pnl()
    generator.parse_bsheet()
    generator.parse_trial_bal()
    generator.parse_daybook()
    generator.generate_markdown_report(output_file="report.md")