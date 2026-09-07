from app.schemas.fundamental_metrics import FundamentalMetrics

def calculate_pe_score(pe):
    upper_limit = 40
    lower_limit = 5

    score = 100*(upper_limit - pe) / (upper_limit - lower_limit)

    return score

pe = calculate_pe_score(35)
print(pe)

# def calculate_score(metrics: FundamentalMetrics) -> ScoreResponse:

