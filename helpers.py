import openai
import pandas as pd
from prompts import build_categorization_prompt
from io import StringIO

def call_openai_to_categorize(df):
    sample_csv = df.head(10).to_csv(index=False)
    prompt = build_categorization_prompt(sample_csv)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a personal finance assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    output_csv = response['choices'][0]['message']['content']
    df_result = pd.read_csv(StringIO(output_csv))
    return df_result