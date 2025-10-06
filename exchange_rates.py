# exchange_rates.py
# ---------------------------------------------
# FINE3300 - Assignment 1, Part 2
# Question: Exchange Rates
# ---------------------------------------------
# Author: <Your Name>
# GitHub Repo: https://github.com/<your-username>/FINE3300-2025-A1
#
# Reads a Bank of Canada CSV file and retrieves the most recent
# USD/CAD exchange rate (last row).  Converts between USD and CAD.
# ---------------------------------------------

import csv
from typing import Optional


class ExchangeRates:
    """
    Usage:
        ex = ExchangeRates("BankOfCanadaExchangeRates.csv")
        ex.get_latest_usd_to_cad()          # prints the latest USD→CAD rate
        ex.convert(100000, "USD", "CAD")    # convert amount
    """

    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.usd_col: Optional[str] = None
        self.latest_row: Optional[dict] = None
        self._load_csv()

    # --------------------------------------------------------------
    def _load_csv(self):
        """Read the CSV, find the USD column, and store the last row."""
        with open(self.csv_path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            rows = [r for r in reader if any(r.values())]  # remove blank rows
            if not rows:
                raise ValueError("CSV appears empty or invalid.")
            self.latest_row = rows[-1]  # last (most recent) row

            # Find the USD-related column automatically
            for col in reader.fieldnames:
                if not col:
                    continue
                if "usd" in col.lower() or "u.s." in col.lower():
                    self.usd_col = col
                    break

            if not self.usd_col:
                raise ValueError(
                    "Could not locate a USD column. "
                    "Please open the CSV and update the code with the exact header name."
                )

    # --------------------------------------------------------------
    def get_latest_usd_to_cad(self) -> float:
        """Return the most recent USD→CAD exchange rate."""
        if not self.usd_col or not self.latest_row:
            raise ValueError("USD column or data missing.")
        val = self.latest_row[self.usd_col].strip()
        if not val:
            raise ValueError("USD rate missing in latest row.")
        return float(val.replace(",", ""))  # remove commas just in case

    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """
        Convert between USD and CAD using the latest rate.
        """
        rate = self.get_latest_usd_to_cad()
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        if from_currency == to_currency:
            return round(amount, 2)
        elif from_currency == "USD" and to_currency == "CAD":
            return round(amount * rate, 2)
        elif from_currency == "CAD" and to_currency == "USD":
            return round(amount / rate, 2)
        else:
            raise ValueError("Supported currencies: USD and CAD only.")


def prompt_and_run():
    """Interactive prompt to perform conversions."""
    print("\n--- Exchange Rate Converter ---")
    csv_path = input("Enter CSV file name (e.g., BankOfCanadaExchangeRates.csv): ").strip()
    print(csv_path)
    ex = ExchangeRates(csv_path)
   

    amount = float(input("Amount: "))
    from_curr = input("From currency (USD or CAD): ").strip().upper()
    to_curr = input("To currency (USD or CAD): ").strip().upper()

    result = ex.convert(amount, from_curr, to_curr)

    print("\n--- Conversion Result ---")
    print(f"{amount:,.2f} {from_curr} → {result:,.2f} {to_curr}")
    print("-----------------------------")


# Run if executed directly
if __name__ == "__main__":
    prompt_and_run()

