def build_categorization_prompt(transactions_csv):
    return f"""
You are a personal finance assistant.

Below is a CSV of banking transactions. Your task is to assign a category to each transaction based on the "Description".

➡️ Output a new CSV with the exact same data and an additional column called **Category**.

🎯 Category values (must be one of these):
- Supermarket
- Transport
- Restaurants
- Subscriptions
- Leisure
- Health
- Other

⚠️ Format rules:
- Keep all original column headers unchanged.
- Add only one new column called "Category".
- Do not include any commentary or explanation.
- Output **only valid CSV**, no Markdown, no code block.

📄 Transactions CSV:
{transactions_csv}

🔁 Return only this modified CSV (no headers, code fences, or explanations):
"""