def build_categorization_prompt(transactions_csv):
    return f"""
You are a personal finance assistant.

Below are banking transactions in CSV format. For each line, add a new column called "Category" with one of the following values:
- Supermarket
- Transport
- Restaurants
- Subscriptions
- Leisure
- Health
- Other

Keep all existing columns, add only the "Category" column, and return the result as a valid CSV.

Transactions:
{transactions_csv}
"""