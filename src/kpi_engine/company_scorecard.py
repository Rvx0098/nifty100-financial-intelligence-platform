"""
Company Scorecard module for aggregating KPIs and generating overall company scores.

This module integrates revenue growth, profitability, liquidity, and leverage
metrics to create comprehensive company scorecards and performance rankings.
"""

from typing import Dict, Any, Optional


class CompanyScorecard:
    """
    Aggregates KPI metrics and generates company performance scores.
    """
    
    def __init__(self, company_id: str, company_name: str):
        """
        Initialize company scorecard.
        
        Args:
            company_id: Unique company identifier
            company_name: Company name
        """
        self.company_id = company_id
        self.company_name = company_name
        self.kpis = {}
        self.scores = {}
    
    def add_kpi(self, category: str, metric_name: str, value: Any) -> None:
        """
        Add a KPI to the scorecard.
        
        Args:
            category: KPI category (e.g., 'revenue_growth', 'profitability')
            metric_name: Name of the metric
            value: Metric value
        """
        if category not in self.kpis:
            self.kpis[category] = {}
        self.kpis[category][metric_name] = value
    
    def calculate_category_score(self, category: str, weights: Optional[Dict[str, float]] = None) -> Optional[float]:
        """
        Calculate weighted score for a KPI category.
        
        Args:
            category: KPI category
            weights: Optional dictionary of metric weights
            
        Returns:
            float: Weighted category score or None if category not found
        """
        if category not in self.kpis:
            return None
        
        metrics = self.kpis[category]
        if not metrics:
            return None
        
        if weights is None:
            # Equal weighting if not specified
            weights = {metric: 1.0 / len(metrics) for metric in metrics}
        
        score = 0.0
        for metric, value in metrics.items():
            if value is not None and metric in weights:
                score += value * weights[metric]
        
        return score
    
    def calculate_overall_score(self, category_weights: Optional[Dict[str, float]] = None) -> float:
        """
        Calculate overall company score across all categories.
        
        Args:
            category_weights: Optional weights for each category
            
        Returns:
            float: Overall company score (0-100)
        """
        if not self.kpis:
            return 0.0
        
        if category_weights is None:
            category_weights = {cat: 1.0 / len(self.kpis) for cat in self.kpis}
        
        overall_score = 0.0
        for category, weight in category_weights.items():
            cat_score = self.calculate_category_score(category)
            if cat_score is not None:
                overall_score += cat_score * weight
        
        return min(100.0, max(0.0, overall_score))
    
    def get_scorecard_summary(self) -> Dict[str, Any]:
        """
        Generate a summary of the company scorecard.
        
        Returns:
            dict: Scorecard summary with company info, KPIs, and scores
        """
        return {
            "company_id": self.company_id,
            "company_name": self.company_name,
            "kpis": self.kpis,
            "category_scores": {
                category: self.calculate_category_score(category)
                for category in self.kpis
            },
            "overall_score": self.calculate_overall_score()
        }
