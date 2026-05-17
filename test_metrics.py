import requests
import json

def test_evaluation():
    """Test evaluation endpoint and display metrics"""
    
    test_cases = [
        {
            "question": "Does this policy share user data?",
            "answer": "Yes, it shares data with third-party marketing partners.",
            "contexts": [
                "Our policy shares user data with third-party marketing partners",
                "Data is used for analytics and targeted advertising",
                "User consent is required before sharing"
            ]
        },
        {
            "question": "What happens to my personal information?",
            "answer": "Your personal information is stored securely and not shared with anyone.",
            "contexts": [
                "Personal data is encrypted and stored locally",
                "We do not share data with third parties",
                "Data retention follows industry standards"
            ]
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"TEST CASE {i}")
        print(f"{'='*60}")
        print(f"Question: {test['question']}")
        print(f"Answer: {test['answer']}")
        print(f"Contexts: {len(test['contexts'])} documents\n")
        
        try:
            # Prepare form data
            form_data = {
                "question": test["question"],
                "answer": test["answer"],
                "contexts": json.dumps(test["contexts"])
            }
            
            # Call API
            response = requests.post(
                "http://127.0.0.1:8000/evaluate/",
                data=form_data
            )
            
            result = response.json()
            
            if "evaluation" in result:
                eval_data = result["evaluation"]
                print("📊 EVALUATION SCORES:")
                print(f"  ✓ Faithfulness:      {eval_data.get('faithfulness', 'N/A'):.2f}")
                print(f"  ✓ Answer Relevancy:  {eval_data.get('answer_relevancy', 'N/A'):.2f}")
                print(f"  ✓ Context Precision: {eval_data.get('context_precision', 'N/A'):.2f}")
                print(f"  ✓ Context Recall:    {eval_data.get('context_recall', 'N/A'):.2f}")
            else:
                print("Response:", json.dumps(result, indent=2))
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🔍 PrivAware Evaluation Metrics Test\n")
    test_evaluation()