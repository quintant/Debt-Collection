def settle_expenses(expenses):
    """Settle expenses between people.
    
    Given a dictionary of expenses where the keys are person identifiers (e.g. 'x1', 'x2', ...)
    and the values are the amounts each paid, this function computes how much each person owes
    to others so that all contributions are equal.
    
    Returns:
        A list of transactions in the format (debtor, creditor, amount).
    """
    n = len(expenses)
    total = sum(expenses.values())
    avg = total / n

    # A positive balance means the person overpaid (creditor).
    # A negative balance means the person underpaid (debtor).
    net_balances = {person: paid - avg for person, paid in expenses.items()}

    debtors = []
    creditors = []

    for person, balance in net_balances.items():
        if balance < -1e-9:
            debtors.append([person, -balance])  # store the amount they need to pay
        elif balance > 1e-9:
            creditors.append([person, balance])  # store the amount they are owed

    transactions = []

    # Use a greedy algorithm to settle debts between debtors and creditors.
    i, j = 0, 0
    while i < len(debtors) and j < len(creditors):
        debtor, debt_amount = debtors[i]
        creditor, credit_amount = creditors[j]
        
        settle_amount = min(debt_amount, credit_amount)
        transactions.append((debtor, creditor, settle_amount))
        
        debtors[i][1] -= settle_amount
        creditors[j][1] -= settle_amount
        
        if abs(debtors[i][1]) < 1e-9:
            i += 1
        if abs(creditors[j][1]) < 1e-9:
            j += 1

    return transactions

if __name__ == "__main__":
    # How much each person paid
    expenses = {
        "B": 63_272,
        "J": 13_000,
        "R": 5_450,
        "H": 31_700,
        "S": 7_500,
        "D": 7_750,
        "A": 0,
    }
    
    transactions = settle_expenses(expenses)
    
    print("Settlement transactions:")
    for debtor, creditor, amount in transactions:
        print(f"{debtor: <10} owes {creditor: >10}      ${amount:.2f}")
