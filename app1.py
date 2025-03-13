from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

def get_news_data():
    try:
        df = pd.read_csv("news_summarized.csv")
        return df.to_dict(orient="records")  # Convert dataframe to a list of dictionaries
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []

@app.route("/")
def index():
    news_data = get_news_data()
    return render_template("index1.html", news=news_data)

if __name__ == "__main__":
    app.run(debug=True)
