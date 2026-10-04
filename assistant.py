import json
import urllib.parse
import urllib.request

PROJECT_ID = "8b2bupco"
DATASET = "production"
API_VERSION = "2024-10-01"
TOKEN = "YOUR_SANITY_API_TOKEN"

BASE_URL = f"https://{PROJECT_ID}.api.sanity.io/v{API_VERSION}/data/mutate/{DATASET}"
QUERY_URL = f"https://{PROJECT_ID}.api.sanity.io/v{API_VERSION}/data/query/{DATASET}"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def seed_knowledge_base():
    """Seed structured Python documentation into Sanity Content Lake"""
    print("⏳ Seeding verified Python documentation into Sanity...")
    payload = {
        "mutations": [
            {
                "createOrReplace": {
                    "_id": "doc-pandas-missing-values",
                    "_type": "pythonDoc",
                    "library": "pandas",
                    "topic": "Handling Missing Values",
                    "content": "To detect missing values use df.isna() or df.isnull(). To fill missing values with a default value, use df.fillna(value). To drop rows with missing values, use df.dropna().",
                    "bestPractice": "Always check df.info() or df.isnull().sum() before dropping rows to assess missing data patterns."
                }
            },
            {
                "createOrReplace": {
                    "_id": "doc-sklearn-pipeline",
                    "_type": "pythonDoc",
                    "library": "scikit-learn",
                    "topic": "Machine Learning Pipelines",
                    "content": "Use sklearn.pipeline.Pipeline to sequentially apply a list of transforms and a final estimator. Prevents data leakage between training and testing sets.",
                    "bestPractice": "Only call fit() on the training data, and use transform() or predict() on the test split."
                }
            }
        ]
    }
    
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(BASE_URL, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req) as resp:
            if resp.status == 200:
                print("✅ Sanity Knowledge Base seeded successfully!")
            else:
                print(f"Error seeding data: {resp.status}")
    except Exception as e:
        print(f"Failed to connect to Sanity: {e}")

def query_agent(library_name):
    """Retrieve grounded context via GROQ query against Sanity Content Lake"""
    groq_query = f'*[_type == "pythonDoc" && library == "{library_name}"]'
    encoded_query = urllib.parse.urlencode({"query": groq_query})
    full_url = f"{QUERY_URL}?{encoded_query}"
    
    print(f"\n🔍 Querying Sanity Knowledge Base for: '{library_name}'...")
    try:
        req = urllib.request.Request(full_url, headers=headers, method="GET")
        with urllib.request.urlopen(req) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8")).get("result", [])
                print("🤖 Agent Response (Verified via Sanity Content Lake):")
                for doc in data:
                    print(f"\n  📌 Topic: {doc.get('topic')}")
                    print(f"  📖 Reference: {doc.get('content')}")
                    print(f"  💡 Best Practice: {doc.get('bestPractice')}")
            else:
                print(f"Error executing query: {resp.status}")
    except Exception as e:
        print(f"Failed to execute query: {e}")

if __name__ == "__main__":
    seed_knowledge_base()
    query_agent("pandas")
    query_agent("scikit-learn")
