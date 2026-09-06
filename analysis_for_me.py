import pandas as pd
import os

def load_excel_safely(file_path):
    """Utility to load an Excel file and clean column names."""
    if not os.path.exists(file_path):
        print(f"Warning: File not found at {file_path}")
        return None
    
    # Read the first sheet by default
    df = pd.read_excel(file_path)
    # Clean whitespace in column headers
    df.columns = df.columns.astype(str).str.strip()
    return df

def analyze_financial_exports(files_dict):
    """Parses and computes summary analytics across financial statements."""
    summary = {}

    # 1. Day Book Analysis
    if 'daybook' in files_dict:
        df_db = load_excel_safely(files_dict['daybook'])
        if df_db is not None:
            # Find debit and credit columns dynamically
            dr_col = [c for c in df_db.columns if 'debit' in c.lower() or 'dr' in c.lower()]
            cr_col = [c for c in df_db.columns if 'credit' in c.lower() or 'cr' in c.lower()]
            
            tot_dr = df_db[dr_col[0]].sum() if dr_col else 0
            tot_cr = df_db[cr_col[0]].sum() if cr_col else 0
            
            summary['Day Book'] = {
                'Total Entries': len(df_db),
                'Total Debit Volume': round(tot_dr, 2),
                'Total Credit Volume': round(tot_cr, 2),
                'Net Flow Difference': round(tot_dr - tot_cr, 2)
            }

    # 2. Trial Balance Analysis
    if 'trial_bal' in files_dict:
        df_tb = load_excel_safely(files_dict['trial_bal'])
        if df_tb is not None:
            dr_col = [c for c in df_tb.columns if 'debit' in c.lower() or 'dr' in c.lower()]
            cr_col = [c for c in df_tb.columns if 'credit' in c.lower() or 'cr' in c.lower()]
            
            tb_dr = df_tb[dr_col[0]].sum() if dr_col else 0
            tb_cr = df_tb[cr_col[0]].sum() if cr_col else 0
            variance = abs(tb_dr - tb_cr)
            
            summary['Trial Balance'] = {
                'Total Debit': round(tb_dr, 2),
                'Total Credit': round(tb_cr, 2),
                'Balanced': variance < 0.01,
                'Out of Balance Amount': round(variance, 2)
            }

    # 3. Profit & Loss Analysis
    if 'pnl' in files_dict:
        df_pnl = load_excel_safely(files_dict['pnl'])
        if df_pnl is not None:
            summary['Profit & Loss'] = {
                'Total Line Items': len(df_pnl),
                'Columns Found': list(df_pnl.columns)
            }

    # 4. Balance Sheet Analysis
    if 'bsheet' in files_dict:
        df_bs = load_excel_safely(files_dict['bsheet'])
        if df_bs is not None:
            summary['Balance Sheet'] = {
                'Total Line Items': len(df_bs),
                'Columns Found': list(df_bs.columns)
            }

    return summary

if __name__ == "__main__":
    # Define file map for the uploaded files
    file_paths = {
        'daybook': 'tally_export_data/DayBook.xlsx',
        'trial_bal': 'tally_export_data/TrialBal.xlsx',
        'pnl': 'tally_export_data/PandL.xlsx',
        'bsheet': 'tally_export_data/BSheet.xlsx'
    }

    results = analyze_financial_exports(file_paths)
    
    # Display formatted results
    print("=" * 45)
    print("      FINANCIAL DATA ANALYSIS REPORT      ")
    print("=" * 45)
    
    for statement, metrics in results.items():
        print(f"\n[ {statement} Summary ]")
        for key, val in metrics.items():
            print(f"  • {key}: {val}")