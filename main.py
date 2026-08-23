from fastapi import FastAPI, HTTPException
from schemas import VarianceRequest, VarianceResponse
from services import process_performance_variance

app = FastAPI(
    title="Player Analytics - Performance Variance Model API",
    description="API to measure dimensional stability of an all-rounder across multiple roles.",
    version="1.0.0"
)

@app.post("/api/v1/analytics/performance-variance", response_model=VarianceResponse)
async def get_performance_variance(request: VarianceRequest):
    """
    Analyzes raw match data to generate stability metrics for an all-rounder.
    Applies the Coefficient of Variation (CV) principle to normalize and compare 
    performance consistency across batting, bowling, and fielding dimensions.
    """
    try:
        response_data = process_performance_variance(request)
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
