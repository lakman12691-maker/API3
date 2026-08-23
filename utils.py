import math
from typing import List

def calculate_mean(values: List[float]) -> float:
    """Calculates the mathematical mean of a list of numbers."""
    if not values:
        return 0.0
    return sum(values) / len(values)

def calculate_std_dev(values: List[float], mean: float) -> float:
    """Calculates the population standard deviation."""
    if not values or len(values) == 1:
        return 0.0
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return math.sqrt(variance)

def calculate_cv(std_dev: float, mean: float) -> float:
    """
    Calculates the Coefficient of Variation.
    Adds a small epsilon to the denominator to prevent division by zero
    in cases where a player averages 0 (e.g., 0 wickets over 3 matches).
    """
    epsilon = 1e-5
    return std_dev / (mean + epsilon)
