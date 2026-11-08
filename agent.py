
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load configuration from the .env file
load_dotenv()

# Example customer requirement
customer_requirement = """
A global manufacturing company uses SAP ERP
across 15 factories.

Procurement approvals are manual and take
an average of 12 days.

Leadership wants to automate procurement
using AI agents while retaining SAP.

Identify potential technology solutions
and expected business outcomes.
"""

# Instructions for our AI model
system_instructions = """
You are an enterprise technology consultant.

Analyze the customer's business problem.

Provide:
1. The main business challenges.
2. Potential AI and cloud solutions.
3. Expected business benefits.
4. Three discovery questions.

Clearly distinguish assumptions from known facts.
"""

def analyze_opportunity(requirement):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("OpenAI API key not configured yet.")
        return

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=system_instructions,
        input=requirement
    )

    print(response.output_text)


if __name__ == "__main__":
    print("Enterprise Opportunity Intelligence Agent")
    print("-----------------------------------------")
    analyze_opportunity(customer_requirement)