import numpy as np

# simple formula: base from LLM (if LLM returns numeric), plus adjustments from retrieved labels
LABEL_WEIGHTS = {
    "HighRisk": -30,
    "RiskyClause": -25,
    "SensitiveData": -20,
    "LowRisk": +10,
    "UserRight": +15,
    "DataSharing": -10
}

def calibrate_trust(llm_score, retrieved_meta):
    # llm_score may be None -> default 50
    base = llm_score if isinstance(llm_score, (int,float)) else 50
    adjust = 0
    for r in retrieved_meta:
        labels = r.get("meta", {}).get("label", [])
        if isinstance(labels, str): labels = [labels]
        for lab in labels:
            adjust += LABEL_WEIGHTS.get(lab, 0)
    # scale adjust down
    adj = np.tanh(adjust/50.0) * 30
    final = int(np.clip(base + adj, 0, 100))
    return final

def consent_from_score(score, threshold_yes=70, threshold_maybe=45):
    if score >= threshold_yes: return "Yes"
    if score >= threshold_maybe: return "Maybe"
    return "No"
