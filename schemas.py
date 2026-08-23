from pydantic import BaseModel, Field
from typing import List

class MatchPerformance(BaseModel):
    match_id: str = Field(..., description="Unique identifier for the match")
    runs_scored: int = Field(..., ge=0, description="Runs scored in the match")
    wickets_taken: int = Field(..., ge=0, description="Wickets taken in the match")
    fielding_points: int = Field(..., ge=0, description="Fielding points accumulated")

class VarianceRequest(BaseModel):
    player_id: str = Field(..., description="Unique identifier for the player")
    matches: List[MatchPerformance] = Field(
        ..., 
        min_length=3, 
        description="List of match performances. Minimum 3 required for variance calculation."
    )

class RoleMetrics(BaseModel):
    mean: float = Field(..., description="Average performance for the role")
    std_dev: float = Field(..., description="Standard deviation for the role")
    cv: float = Field(..., description="Coefficient of Variation (relative variance)")

class VarianceResponse(BaseModel):
    player_id: str
    matches_analyzed: int
    batting_variance: RoleMetrics
    bowling_variance: RoleMetrics
    fielding_variance: RoleMetrics
    overall_variance_index: float = Field(..., description="Combined CV across all roles")
    stability_score: float = Field(..., description="0-100 score indicating overall stability")
    stability_category: str = Field(..., description="Interpretable classification of stability")
