import csv
from datetime import datetime

# --- Hardcoded stock prices (USD per share) -----------------------------
STOCK_PRICES = {
    "AAPL":  180,
    "TSLA":  250,
    "GOOGL": 140,
    "MSFT":  410,
    "AMZN":  185,
}


def show_available_stocks():
    """Print the list of supported stocks and their prices."""
    print("\n" + "=" * 45)
    print(f"{'Available Stocks':^45}")
    print("=" * 45)
    print(f"{'Symbol':<10}{'Price (USD)':>20}")
    print("-" * 45)
    for symbol, price in STOCK_PRICES.items():
        print(f"{symbol:<10}{price:>20,.2f}")
    print("=" * 45 + "\n")


def get_portfolio_from_user():
    """Ask the user for stock symbols and quantities until they type 'done'."""
    portfolio = {}
    print("Enter your holdings one by one.")
    print("Type 'done' as the stock symbol when you are finished.\n")

    while True:
        symbol = input("Stock symbol : ").strip().upper()

        if symbol == "DONE":
            break

        if symbol not in STOCK_PRICES:
            print(f"  '{symbol}' is not in our price list. Try again.\n")
            continue

        qty_raw = input(f"Quantity of {symbol} : ").strip()
        if not qty_raw.isdigit() or int(qty_raw) <= 0:
            print("  Please enter a positive whole number.\n")
            continue

        quantity = int(qty_raw)
        portfolio[symbol] = portfolio.get(symbol, 0) + quantity
        print(f"  Added {quantity} share(s) of {symbol}.\n")

    return portfolio


def build_summary(portfolio):
    """Return a list of rows + the grand total investment."""
    rows = []
    total = 0
    for symbol, qty in portfolio.items():
        price = STOCK_PRICES[symbol]
        value = price * qty
        total += value
        rows.append({
            "symbol":   symbol,
            "quantity": qty,
            "price":    price,
            "value":    value,
        })
    return rows, total


def print_summary(rows, total):
    """Pretty-print the portfolio summary."""
    print("\n" + "=" * 55)
    print(f"{'Portfolio Summary':^55}")
    print("=" * 55)
    print(f"{'Symbol':<10}{'Qty':>8}{'Price':>14}{'Value':>20}")
    print("-" * 55)
    for r in rows:
        print(f"{r['symbol']:<10}{r['quantity']:>8}"
              f"{r['price']:>14,.2f}{r['value']:>20,.2f}")
    print("-" * 55)
    print(f"{'TOTAL INVESTMENT':<32}{total:>22,.2f} USD")
    print("=" * 55 + "\n")


def save_to_csv(rows, total, filename=None):
    """Save the portfolio summary to a .csv file."""
    if filename is None:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"portfolio_{stamp}.csv"

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Symbol", "Quantity", "Price (USD)", "Value (USD)"])
        for r in rows:
            writer.writerow([r["symbol"], r["quantity"],
                             r["price"], r["value"]])
        writer.writerow([])
        writer.writerow(["", "", "TOTAL", total])

    print(f"Saved portfolio to '{filename}'\n")


def main():
    print("\n" + "*" * 55)
    print(f"{'STOCK PORTFOLIO TRACKER':^55}")
    print("*" * 55)

    show_available_stocks()
    portfolio = get_portfolio_from_user()

    if not portfolio:
        print("No holdings entered. Goodbye!")
        return

    rows, total = build_summary(portfolio)
    print_summary(rows, total)

    choice = input("Save result to a CSV file? (y/n): ").strip().lower()
    if choice == "y":
        save_to_csv(rows, total)
    else:
        print("Result not saved.\n")

    print("Thanks for using the Stock Portfolio Tracker!\n")


if __name__ == "__main__":
    main()