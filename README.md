# 💸 AI Budget Assistant

An AI-powered tool to help you categorize your NAB (or other bank) statement CSV and visualize your spending trends over time. Built using Streamlit, OpenAI GPT-4, and Plotly.

---

## 🚀 Features

* Upload NAB transaction CSVs
* Automatically categorize transactions using GPT-4
* Handles partial or missing categories (e.g. "Uncategorised")
* Displays categorized table, category totals, and monthly spending trends
* Interactive filters by month

---

## 🧠 How It Works

If any transactions are marked "Uncategorised" (or no Category column is present), the app sends those rows to GPT-4 to generate meaningful spending categories. The model responds with a valid CSV, which gets merged back into your original data.

To reduce cost and avoid exceeding token limits, only uncategorized rows are sent to the OpenAI API, and results are processed in small chunks.

---

## 📦 Requirements

* Python 3.9+
* OpenAI API Key

You’ll need to create a `.env` file in the project root with the following content:

```bash
OPENAI_API_KEY="your-openai-key"
```

---

## 🛠️ Installation

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
pip install -r requirements.txt
streamlit run app.py
```

---

## 🧪 Sample CSV Format

Make sure your file looks like this:

| Date       | Description     | Amount | Category      |
| ---------- | --------------- | ------ | ------------- |
| 2024-05-02 | WOOLWORTHS 3163 | -35.20 | Supermarket   |
| 2024-05-04 | NETFLIX         | -22.99 | Uncategorised |

If no `Category` column exists, the app will generate one using AI.

---

## 📊 Tech Stack

* **Streamlit** – Web app interface
* **OpenAI GPT-4** – Categorization logic
* **Pandas** – Data handling
* **Plotly Express** – Interactive charts
* **Python-dotenv** – API key loading

---

## 🧠 Prompt Logic

The assistant uses a templated prompt like:

```
You are a personal finance assistant.
Below are banking transactions in CSV format. Add a new column called "Category" with one of the following values:
- Supermarket
- Transport
- Restaurants
- Subscriptions
- Leisure
- Health
- Other
Return a valid CSV with the new column.
```

---

## 🔒 Privacy

Your data never leaves your computer except for categorization requests to OpenAI. Nothing is stored or logged outside your session.

---

## 🧾 License

MIT License.
