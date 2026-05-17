import json
from backend.evaluation.ragas_eval import evaluate_rag_pipeline

# Test data
question = "Does this policy share user data with third parties?"
answer = "Yes, the policy explicitly shares data with marketing and analytics partners for targeted advertising and behavioral tracking."
contexts = [
    "Our service shares user data with third-party marketing partners to deliver personalized advertising.",
    "Analytics data including browsing history is transmitted to external vendors for analysis.",
    "User consent is required before sharing personal information, but defaults to opt-in."
]

print("🔍 Running RAGAS Evaluation...")
print(f"Question: {question}")
print(f"Answer: {answer}")
print(f"Contexts: {len(contexts)}")

try:
    result = evaluate_rag_pipeline(question, answer, contexts)
    print("\n✅ Evaluation Results:")
    print(json.dumps(result, indent=2))
    
    # Extract individual metrics
    if isinstance(result, dict):
        for metric_name, metric_value in result.items():
            print(f"  {metric_name}: {metric_value}")
except Exception as e:
    print(f"❌ Evaluation failed: {e}")