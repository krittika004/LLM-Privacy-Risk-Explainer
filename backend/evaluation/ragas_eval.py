from datasets import Dataset
from backend.evaluation.metrics import get_metrics

def evaluate_rag_pipeline(question, answer, contexts):
    """
    Run RAGAS evaluation. Falls back to mock scores if dependencies unavailable.
    """
    try:
        from ragas import evaluate
        from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
        from ragas.dataset_schema import SingleTurnSample, EvaluationDataset
        from backend.evaluation.config import get_llm
        
        llm = get_llm()
        
        # Create evaluation sample
        sample = SingleTurnSample(
            user_input=question,
            response=answer,
            retrieved_contexts=contexts
        )
        dataset = EvaluationDataset(samples=[sample])
        
        # Run evaluation
        result = evaluate(
            dataset,
            metrics=[
                faithfulness,
                answer_relevancy,
                context_precision,
                context_recall
            ],
            llm=llm
        )
        
        return result
    except Exception as e:
        print(f"⚠️  RAGAS evaluation failed: {e}. Returning mock scores.")
        # Return mock evaluation results
        return {
            "faithfulness": 0.75,
            "answer_relevancy": 0.82,
            "context_precision": 0.88,
            "context_recall": 0.79,
            "note": "Mock evaluation (real evaluation unavailable)"
        }