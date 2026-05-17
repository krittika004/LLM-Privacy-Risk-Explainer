import requests
import json
from tabulate import tabulate as print_table
from datetime import datetime

def run_evaluation_tests():
    """Run multiple evaluation scenarios and display results in table format"""
    
    base_url = "http://127.0.0.1:8000/evaluate/"
    
    # Define test scenarios
    scenarios = [
        {
            "name": "✅ Perfect Alignment",
            "question": "Does this policy share user data?",
            "answer": "Yes, user data is shared with third-party marketing partners.",
            "contexts": [
                "Our policy shares user data with third-party marketing partners",
                "Data is used for targeted advertising"
            ],
            "expected": "High scores across all metrics"
        },
        {
            "name": "⚠️ Partial Hallucination",
            "question": "Who receives user data?",
            "answer": "User data is shared with marketing partners, analytics vendors, and government agencies.",
            "contexts": [
                "Our policy shares user data with third-party marketing partners",
                "Analytics data is transmitted to external vendors"
            ],
            "expected": "Lower faithfulness (hallucinated government mention)"
        },
        {
            "name": "❌ Complete Contradiction",
            "question": "Is user data shared with third parties?",
            "answer": "No, we never share user data with anyone.",
            "contexts": [
                "Our policy explicitly shares user data with third-party marketing partners",
                "Data is transmitted to analytics vendors daily"
            ],
            "expected": "Very low faithfulness and relevancy"
        },
        {
            "name": "🟡 Irrelevant Answer",
            "question": "What is the data retention policy?",
            "answer": "Our CEO was founded in 2020.",
            "contexts": [
                "User data is retained for 30 days after account deletion",
                "Archived data is stored for 7 years for compliance"
            ],
            "expected": "Low answer relevancy (off-topic)"
        },
        {
            "name": "🔵 Incomplete but Accurate",
            "question": "How is user data protected?",
            "answer": "Data is encrypted.",
            "contexts": [
                "User data is encrypted using AES-256 encryption",
                "Data is transmitted over HTTPS",
                "Regular security audits are performed",
                "Data centers are SOC 2 compliant"
            ],
            "expected": "Good faithfulness, lower recall (partial answer)"
        },
        {
            "name": "🟢 Well-Grounded Multi-Point",
            "question": "What are the privacy safeguards?",
            "answer": "We use AES-256 encryption for data storage and HTTPS for transmission. We perform regular security audits and maintain SOC 2 compliance.",
            "contexts": [
                "User data is encrypted using AES-256 encryption",
                "Data is transmitted over HTTPS",
                "Regular security audits are performed",
                "Data centers are SOC 2 compliant"
            ],
            "expected": "Excellent scores (comprehensive and grounded)"
        },
        {
            "name": "🟠 Missing Context",
            "question": "What is the data retention period?",
            "answer": "We retain data for 30 days after account deletion and archived data for 7 years.",
            "contexts": [
                "User data is retained for 30 days after account deletion"
            ],
            "expected": "Good faithfulness, lower recall (missing archive context)"
        }
    ]
    
    results = []
    
    print("\n" + "="*120)
    print("🔍 PrivAware - Evaluation Metrics Testing (Different Scenarios)")
    print("="*120)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"[{i}/{len(scenarios)}] Running: {scenario['name']}...")
        
        try:
            # Prepare form data
            form_data = {
                "question": scenario["question"],
                "answer": scenario["answer"],
                "contexts": json.dumps(scenario["contexts"])
            }
            
            # Call API
            response = requests.post(base_url, data=form_data)
            result = response.json()
            
            if "evaluation" in result:
                eval_data = result["evaluation"]
                
                # Calculate average score
                avg_score = (
                    eval_data.get("faithfulness", 0) +
                    eval_data.get("answer_relevancy", 0) +
                    eval_data.get("context_precision", 0) +
                    eval_data.get("context_recall", 0)
                ) / 4
                
                results.append({
                    "Scenario": scenario["name"],
                    "Question": scenario["question"][:40] + "..." if len(scenario["question"]) > 40 else scenario["question"],
                    "Faithfulness": f"{eval_data.get('faithfulness', 0):.3f}",
                    "Answer Relevancy": f"{eval_data.get('answer_relevancy', 0):.3f}",
                    "Context Precision": f"{eval_data.get('context_precision', 0):.3f}",
                    "Context Recall": f"{eval_data.get('context_recall', 0):.3f}",
                    "Average": f"{avg_score:.3f}"
                })
            else:
                results.append({
                    "Scenario": scenario["name"],
                    "Question": scenario["question"][:40],
                    "Faithfulness": "ERROR",
                    "Answer Relevancy": "ERROR",
                    "Context Precision": "ERROR",
                    "Context Recall": "ERROR",
                    "Average": "ERROR"
                })
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            results.append({
                "Scenario": scenario["name"],
                "Question": scenario["question"][:40],
                "Faithfulness": "FAIL",
                "Answer Relevancy": "FAIL",
                "Context Precision": "FAIL",
                "Context Recall": "FAIL",
                "Average": "FAIL"
            })
    
    # Display main results table
    print("\n" + "="*120)
    print("📊 EVALUATION METRICS TABLE")
    print("="*120)
    print(print_table(results, headers="keys", tablefmt="grid"))
    
    # Detailed breakdown by metric
    print("\n" + "="*120)
    print("📈 METRIC COMPARISON")
    print("="*120)
    
    metric_rows = []
    for result in results:
        metric_rows.append({
            "Scenario": result["Scenario"],
            "Faithfulness": result["Faithfulness"],
            "Answer Relevancy": result["Answer Relevancy"],
            "Context Precision": result["Context Precision"],
            "Context Recall": result["Context Recall"],
            "Average": result["Average"]
        })
    
    print(print_table(metric_rows, headers="keys", tablefmt="grid"))
    
    # Summary statistics
    print("\n" + "="*120)
    print("📌 SUMMARY STATISTICS")
    print("="*120)
    
    try:
        faithfulness_scores = [float(r["Faithfulness"]) for r in results if r["Faithfulness"] not in ["ERROR", "FAIL"]]
        relevancy_scores = [float(r["Answer Relevancy"]) for r in results if r["Answer Relevancy"] not in ["ERROR", "FAIL"]]
        precision_scores = [float(r["Context Precision"]) for r in results if r["Context Precision"] not in ["ERROR", "FAIL"]]
        recall_scores = [float(r["Context Recall"]) for r in results if r["Context Recall"] not in ["ERROR", "FAIL"]]
        
        if faithfulness_scores and relevancy_scores and precision_scores and recall_scores:
            summary = [
                {
                    "Metric": "Faithfulness",
                    "Min": f"{min(faithfulness_scores):.3f}",
                    "Max": f"{max(faithfulness_scores):.3f}",
                    "Average": f"{sum(faithfulness_scores)/len(faithfulness_scores):.3f}"
                },
                {
                    "Metric": "Answer Relevancy",
                    "Min": f"{min(relevancy_scores):.3f}",
                    "Max": f"{max(relevancy_scores):.3f}",
                    "Average": f"{sum(relevancy_scores)/len(relevancy_scores):.3f}"
                },
                {
                    "Metric": "Context Precision",
                    "Min": f"{min(precision_scores):.3f}",
                    "Max": f"{max(precision_scores):.3f}",
                    "Average": f"{sum(precision_scores)/len(precision_scores):.3f}"
                },
                {
                    "Metric": "Context Recall",
                    "Min": f"{min(recall_scores):.3f}",
                    "Max": f"{max(recall_scores):.3f}",
                    "Average": f"{sum(recall_scores)/len(recall_scores):.3f}"
                }
            ]
            
            print(print_table(summary, headers="keys", tablefmt="grid"))
    except Exception as e:
        print(f"Could not calculate summary: {e}")
    
    # Score interpretation guide
    print("\n" + "="*120)
    print("🎯 SCORE INTERPRETATION")
    print("="*120)
    
    guide = [
        {"Range": "0.90-1.00", "Quality": "✅ Excellent", "Description": "Perfect alignment"},
        {"Range": "0.70-0.89", "Quality": "✓ Good", "Description": "Mostly accurate"},
        {"Range": "0.50-0.69", "Quality": "⚠️ Fair", "Description": "Some issues"},
        {"Range": "0.30-0.49", "Quality": "❌ Poor", "Description": "Significant problems"},
        {"Range": "0.00-0.29", "Quality": "❌❌ Very Poor", "Description": "Unreliable"}
    ]
    
    print(print_table(guide, headers="keys", tablefmt="grid"))
    
    print("\n" + "="*120 + "\n")

if __name__ == "__main__":
    try:
        # Check if backend is running
        requests.get("http://127.0.0.1:8000/docs", timeout=2)
    except:
        print("❌ Backend not running! Start it first:")
        print("  uvicorn backend.main:app --reload --reload-dir backend")
        exit(1)
    
    run_evaluation_tests()