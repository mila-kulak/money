from functools import wraps


transaction_rows = [
        "payment 30",
        "refund50",
        "transfer 90",
        "грошики",
        "payment 70",
        "refund 50",
        "transfer 130",
    ]

def shadow(limit: 200):
    def check_amount_decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            total_amount=0
            limit_exceeded = False

            for row in function(*args, **kwargs):
                operation, amount = row.split()
                amount = int(amount)
                total_amount+=amount

                if(total_amount>limit and limit_exceeded==False):
                    print("Тіньовий ліміт порушено. Активую схему")
                    limit_exceeded=True

                yield row
            print(f"Загальна сума: {total_amount}")
            return total_amount

        return wrapper
    return check_amount_decorator

def suspicious_counter(treshhold: int):
    def count_exceeding_amounts(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            total_amount=0
            for row in function(*args, **kwargs):
                operation, amount = row.split()
                amount = int(amount)
                total_amount+=amount

                if(total_amount>treshhold):
                    print(f"Попередження: сума {total_amount} перевищила поріг")
                yield row

        return wrapper
    return count_exceeding_amounts

@suspicious_counter(treshhold=200)
@shadow(limit=200)
def return_transaction():
    for row in transaction_rows:
        try:
            operation, amount = row.split()
            amount=int(amount)
        except ValueError:
            pass
        else:
            yield row


for transaction in return_transaction():
    print(transaction)
