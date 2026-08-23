from schemas import VarianceRequest, VarianceResponse, RoleMetrics
from utils import calculate_mean, calculate_std_dev, calculate_cv

def determine_stability_category(score: float) -> str:
    """Maps the 0-100 stability score to an interpretable category."""
    if score >= 80:
        return "Highly Consistent"
    elif score >= 60:
        return "Moderately Consistent"
    elif score >= 40:
        return "Inconsistent"
    else:
        return "Highly Erratic"

def process_performance_variance(data: VarianceRequest) -> VarianceResponse:
    # 1. Extract raw variables into role-specific arrays
    runs = [float(m.runs_scored) for m in data.matches]
    wickets = [float(m.wickets_taken) for m in data.matches]
    fielding = [float(m.fielding_points) for m in data.matches]
    
    # 2. Derive statistical variables for Batting
    bat_mean = calculate_mean(runs)
    bat_std = calculate_std_dev(runs, bat_mean)
    bat_cv = calculate_cv(bat_std, bat_mean)
    
    # 3. Derive statistical variables for Bowling
    bowl_mean = calculate_mean(wickets)
    bowl_std = calculate_std_dev(wickets, bowl_mean)
    bowl_cv = calculate_cv(bowl_std, bowl_mean)
    
    # 4. Derive statistical variables for Fielding
    field_mean = calculate_mean(fielding)
    field_std = calculate_std_dev(fielding, field_mean)
    field_cv = calculate_cv(field_std, field_mean)
    
    # 5. Calculate Final Combined Metrics
    # Overall Variance Index is the average of the relative variances
    overall_variance_index = (bat_cv + bowl_cv + field_cv) / 3.0
    
    # Transform OVI into a 0-100 Stability Score
    # We multiply OVI by 50 to scale it (a CV of 2.0 would drop the score to 0)
    stability_score = max(0.0, 100.0 - (overall_variance_index * 50.0))
    stability_score = round(stability_score, 2)
    
    category = determine_stability_category(stability_score)
    
    # 6. Construct and return structured response
    return VarianceResponse(
        player_id=data.player_id,
        matches_analyzed=len(data.matches),
        batting_variance=RoleMetrics(
            mean=round(bat_mean, 2), 
            std_dev=round(bat_std, 2), 
            cv=round(bat_cv, 4)
        ),
        bowling_variance=RoleMetrics(
            mean=round(bowl_mean, 2), 
            std_dev=round(bowl_std, 2), 
            cv=round(bowl_cv, 4)
        ),
        fielding_variance=RoleMetrics(
            mean=round(field_mean, 2), 
            std_dev=round(field_std, 2), 
            cv=round(field_cv, 4)
        ),
        overall_variance_index=round(overall_variance_index, 4),
        stability_score=stability_score,
        stability_category=category
    )
