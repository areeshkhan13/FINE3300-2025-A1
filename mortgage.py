# FINE3300 - Assignment 1, Part 1
# Mortgage Payments

from typing import Tuple

class MortgagePayment:
    """
    MortgagePayment(quoted_rate_percent, amortization_years)
    Example:
        mp = MortgagePayment(5.5, 25)
        payments = mp.payments(500000)
        print(payments)
    """

    def __init__(self, quoted_rate_percent: float, amortization_years: int):
        self.r_nom = quoted_rate_percent / 100.0
        self.amort_years = amortization_years

    def _effective_annual_rate(self) -> float:
        """
        Convert nominal rate (semi-annually compounded)
        to the effective annual rate (EAR).
        Formula: (1 + r_nom/2)^2 - 1
        """
        return (1 + self.r_nom / 2) ** 2 - 1

    def _periodic_rate(self, payments_per_year: int) -> float:
        """
        Convert the effective annual rate to a rate per payment period.
        Formula: (1 + EAR)^(1/m) - 1
        """
        EAR = self._effective_annual_rate()
        return (1 + EAR) ** (1 / payments_per_year) - 1

    def _pva(self, r: float, n: int) -> float:
        """
        Present Value of an Annuity (PVA) Factor:
        PVA = (1 - (1 + r)^(-n)) / r
        """
        if r == 0:
            return n
        return (1 - (1 + r) ** (-n)) / r

    def payments(self, principal: float) -> Tuple[float, float, float, float, float, float]:
        """
        Compute payments for all six payment frequencies.
        Returns a tuple:
        (monthly, semi-monthly, bi-weekly, weekly, rapid-bi-weekly, rapid-weekly)
        """
        # Payment frequencies
        freq = {"monthly": 12, "semi-monthly": 24, "bi-weekly": 26, "weekly": 52}
        total_periods = {k: self.amort_years * v for k, v in freq.items()}

        # Monthly payment
        r_month = self._periodic_rate(freq["monthly"])
        monthly = principal / self._pva(r_month, total_periods["monthly"])

        # Semi-monthly
        r_semi = self._periodic_rate(freq["semi-monthly"])
        semi_monthly = principal / self._pva(r_semi, total_periods["semi-monthly"])

        # Bi-weekly
        r_bi = self._periodic_rate(freq["bi-weekly"])
        bi_weekly = principal / self._pva(r_bi, total_periods["bi-weekly"])

        # Weekly
        r_week = self._periodic_rate(freq["weekly"])
        weekly = principal / self._pva(r_week, total_periods["weekly"])

        # Rapid (accelerated) payments
        rapid_bi_weekly = monthly / 2
        rapid_weekly = monthly / 4

        return (
            round(monthly, 2),
            round(semi_monthly, 2),
            round(bi_weekly, 2),
            round(weekly, 2),
            round(rapid_bi_weekly, 2),
            round(rapid_weekly, 2),
        )


def prompt_and_run():
    """
    Prompts the user for input and displays all mortgage payments.
    """
    print("\n--- Mortgage Payment Calculator ---")
    principal = float(input("Principal amount ($): "))
    quoted_rate = float(input("Quoted interest rate (%): "))
    amort = int(input("Amortization period (years): "))

    mp = MortgagePayment(quoted_rate, amort)
    (
        monthly,
        semi_monthly,
        bi_weekly,
        weekly,
        rapid_bi_weekly,
        rapid_weekly,
    ) = mp.payments(principal)

    print("\n--- Payment Summary ---")
    print(f"Monthly Payment: ${monthly:,.2f}")
    print(f"Semi-monthly Payment: ${semi_monthly:,.2f}")
    print(f"Bi-weekly Payment: ${bi_weekly:,.2f}")
    print(f"Weekly Payment: ${weekly:,.2f}")
    print(f"Rapid Bi-weekly Payment: ${rapid_bi_weekly:,.2f}")
    print(f"Rapid Weekly Payment: ${rapid_weekly:,.2f}")
    print("-----------------------------")


# Run if executed directly
if __name__ == "__main__":
    prompt_and_run()

