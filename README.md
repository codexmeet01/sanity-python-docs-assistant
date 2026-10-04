# Python Library Assistant with Sanity Content Lake

An AI-grounded technical documentation assistant that queries verified documentation stored directly in Sanity's Content Lake to eliminate hallucinations.

## Key Features
- **Grounded Knowledge Base:** Stores structured documentation, code references, and best practices as JSON documents inside Sanity.
- **GROQ Queries:** Performs fast and targeted GROQ queries directly against Sanity API endpoints.
- **Zero-Dependency Architecture:** Built with Python standard libraries (`urllib`, `json`) for seamless deployment.

## Verified Libraries Covered
- **Pandas:** Handling missing values and data cleaning operations.
- **Scikit-learn:** Best practices for ML pipelines and avoiding data leakage.

## How to Run
1. Set up your Sanity project and generate an Editor API token.
2. Set the `TOKEN` variable inside `assistant.py`.
3. Run the script:
   ```bash
   python assistant.py
