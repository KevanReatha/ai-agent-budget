import os
import pandas as pd
from openai import OpenAI
from prompts import build_categorization_prompt
from io import StringIO
from dotenv import load_dotenv

def call_openai_to_categorize(df):
    # Load the key fresh
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OpenAI API key not found. Check your .env file.")

    # Create OpenAI client inside function
    client = OpenAI(api_key=api_key)

    sample_csv = df.head(10).to_csv(index=False)
    prompt = build_categorization_prompt(sample_csv)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a personal finance assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    output_csv = response.choices[0].message.content
    df_result = pd.read_csv(StringIO(output_csv))
    return df_result