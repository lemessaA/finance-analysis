"""
Advanced financial analysis service with enhanced capabilities.
"""

from __future__ import annotations

import asyncio
import re
import statistics
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import logging

from app.agents.financial_analysis_agent import FinancialAnalysisAgent
from app.schemas.financial import FinancialReportResponse
from app.utils.performance import performance_timer

logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    """Risk level classification."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FinancialHealthScore(Enum):
    """Financial health score categories."""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    CRITICAL = "critical"


@dataclass
class TrendAnalysis:
    """Trend analysis results."""
    metric: str
    current_value: float
    previous_value: Optional[float]
    growth_rate: Optional[float]
    trend_direction: str  # "increasing", "decreasing", "stable"
    trend_strength: str  # "strong", "moderate", "weak"
    volatility: Optional[float]


@dataclass
class RiskAssessment:
    """Risk assessment results."""
    category: str
    level: RiskLevel
    score: float  # 0-100
    description: str
    mitigation_suggestions: List[str]


@dataclass
class IndustryBenchmark:
    """Industry benchmark data."""
    metric: str
    industry_average: float
    industry_median: float
    percentile_ranking: Optional[float]
    comparison: str  # "above_average", "below_average", "average"


@dataclass
class FinancialRatios:
    """Calculated financial ratios."""
    liquidity_ratios: Dict[str, float]
    profitability_ratios: Dict[str, float]
    leverage_ratios: Dict[str, float]
    efficiency_ratios: Dict[str, float]
    valuation_ratios: Dict[str, float]


@dataclass
class PredictiveInsights:
    """Predictive financial insights."""
    revenue_forecast: List[Tuple[str, float]]
    profit_forecast: List[Tuple[str, float]]
    confidence_level: float
    key_drivers: List[str]
    risk_factors: List[str]


class AdvancedFinancialAnalyzer:
    """Advanced financial analysis with enhanced capabilities."""
    
    def __init__(self):
        self.financial_agent = FinancialAnalysisAgent()
        
        # Industry benchmark data (simplified for demo)
        self.industry_benchmarks = {
            "technology": {
                "revenue_growth_yoy": {"avg": 0.15, "median": 0.12},
                "gross_margin": {"avg": 0.65, "median": 0.60},
                "net_margin": {"avg": 0.20, "median": 0.15},
                "current_ratio": {"avg": 2.5, "median": 2.0},
                "debt_to_equity": {"avg": 0.4, "median": 0.3},
            },
            "manufacturing": {
                "revenue_growth_yoy": {"avg": 0.08, "median": 0.06},
                "gross_margin": {"avg": 0.35, "median": 0.32},
                "net_margin": {"avg": 0.08, "median": 0.06},
                "current_ratio": {"avg": 1.8, "median": 1.5},
                "debt_to_equity": {"avg": 0.8, "median": 0.6},
            },
            "retail": {
                "revenue_growth_yoy": {"avg": 0.05, "median": 0.04},
                "gross_margin": {"avg": 0.40, "median": 0.38},
                "net_margin": {"avg": 0.03, "median": 0.02},
                "current_ratio": {"avg": 1.5, "median": 1.3},
                "debt_to_equity": {"avg": 1.2, "median": 0.9},
            }
        }
    
    @performance_timer("advanced_financial_analysis")
    async def analyze_comprehensive(
        self, 
        text: str, 
        filename: str,
        industry: Optional[str] = None,
        historical_data: Optional[List[FinancialReportResponse]] = None
    ) -> Dict[str, Any]:
        """Perform comprehensive financial analysis."""
        
        # Get base analysis
        base_analysis = await self.financial_agent.run(
            text=text,  # Actually use the passed text
            filename=filename
        )
        
        # Extract numeric values from metrics
        numeric_metrics = self._extract_numeric_values(base_analysis.metrics)
        
        # Calculate financial ratios
        ratios = self._calculate_financial_ratios(numeric_metrics)
        
        # Perform trend analysis if historical data available
        trend_analysis = None
        if historical_data:
            trend_analysis = self._analyze_trends(numeric_metrics, historical_data)
        
        # Risk assessment
        risk_assessment = self._assess_risks(numeric_metrics, ratios, base_analysis.key_risks)
        
        # Industry benchmarking
        benchmarking = None
        if industry:
            benchmarking = self._benchmark_against_industry(numeric_metrics, industry)
        
        # Financial health scoring
        health_score = self._calculate_financial_health_score(numeric_metrics, ratios, risk_assessment)
        
        # Predictive insights
        predictive_insights = self._generate_predictive_insights(
            numeric_metrics, 
            trend_analysis, 
            historical_data
        )
        
        # Enhanced recommendations
        recommendations = self._generate_recommendations(
            numeric_metrics, 
            ratios, 
            risk_assessment, 
            benchmarking, 
            health_score
        )
        
        return {
            "base_analysis": base_analysis,
            "financial_ratios": ratios,
            "trend_analysis": trend_analysis,
            "risk_assessment": risk_assessment,
            "industry_benchmarking": benchmarking,
            "financial_health_score": health_score,
            "predictive_insights": predictive_insights,
            "recommendations": recommendations,
            "analysis_metadata": {
                "industry": industry,
                "has_historical_data": bool(historical_data),
                "analysis_timestamp": asyncio.get_event_loop().time(),
                "data_quality_score": self._assess_data_quality(numeric_metrics)
            }
        }
    
    def _extract_numeric_values(self, metrics: Any) -> Dict[str, float]:
        """Extract numeric values from metrics strings or Pydantic model."""
        numeric_values = {}
        
        # Convert Pydantic model to dict if necessary
        if hasattr(metrics, 'model_dump'):
            metrics_dict = metrics.model_dump()
        elif hasattr(metrics, 'dict'):
            metrics_dict = metrics.dict()
        else:
            metrics_dict = metrics
            
        for key, value in metrics_dict.items():
            if value == "Not disclosed" or not value:
                continue
            
            # Remove common formatting and extract numbers
            cleaned_value = re.sub(r'[^\d.-]', '', str(value))
            
            try:
                # Handle percentage values
                if '%' in str(value):
                    numeric_values[key] = float(cleaned_value) / 100
                else:
                    numeric_values[key] = float(cleaned_value)
            except (ValueError, TypeError):
                logger.debug(f"Could not extract numeric value for {key}: {value}")
                continue
        
        return numeric_values
    
    def _calculate_financial_ratios(self, metrics: Dict[str, float]) -> FinancialRatios:
        """Calculate comprehensive financial ratios."""
        
        # Get key metrics
        revenue = metrics.get("revenue", 0)
        net_profit = metrics.get("net_profit", 0)
        operating_income = metrics.get("operating_income", 0)
        total_assets = metrics.get("total_assets", 0)
        total_liabilities = metrics.get("total_liabilities", 0)
        cash_flow = metrics.get("cash_flow", 0)
        current_assets = metrics.get("current_assets", total_assets * 0.5)  # Estimate
        current_liabilities = metrics.get("current_liabilities", total_liabilities * 0.5)  # Estimate
        
        # Liquidity Ratios
        liquidity_ratios = {}
        if current_liabilities > 0:
            liquidity_ratios["current_ratio"] = current_assets / current_liabilities
        if total_liabilities > 0:
            liquidity_ratios["debt_to_equity"] = total_liabilities / max(total_assets - total_liabilities, 1)
        
        # Profitability Ratios
        profitability_ratios = {}
        if revenue > 0:
            profitability_ratios["gross_margin"] = metrics.get("gross_profit", 0) / revenue
            profitability_ratios["net_margin"] = net_profit / revenue
            profitability_ratios["operating_margin"] = operating_income / revenue
        if total_assets > 0:
            profitability_ratios["return_on_assets"] = net_profit / total_assets
        if total_assets - total_liabilities > 0:
            profitability_ratios["return_on_equity"] = net_profit / (total_assets - total_liabilities)
        
        # Efficiency Ratios
        efficiency_ratios = {}
        if revenue > 0:
            efficiency_ratios["asset_turnover"] = revenue / total_assets
        if total_assets > 0:
            efficiency_ratios["cash_ratio"] = metrics.get("cash", 0) / total_assets
        
        # Valuation Ratios (would need market data)
        valuation_ratios = {}
        
        return FinancialRatios(
            liquidity_ratios=liquidity_ratios,
            profitability_ratios=profitability_ratios,
            leverage_ratios={"debt_to_equity": liquidity_ratios.get("debt_to_equity", 0)},
            efficiency_ratios=efficiency_ratios,
            valuation_ratios=valuation_ratios
        )
    
    def _analyze_trends(
        self, 
        current_metrics: Dict[str, float], 
        historical_data: List[FinancialReportResponse]
    ) -> List[TrendAnalysis]:
        """Analyze trends based on historical data."""
        
        trends = []
        
        if not historical_data:
            return trends
        
        # Get the most recent historical data
        latest_historical = historical_data[-1]
        historical_numeric = self._extract_numeric_values(latest_historical.metrics)
        
        for metric, current_value in current_metrics.items():
            if metric in historical_numeric:
                previous_value = historical_numeric[metric]
                
                # Calculate growth rate
                if previous_value != 0:
                    growth_rate = (current_value - previous_value) / abs(previous_value)
                else:
                    growth_rate = None
                
                # Determine trend direction
                if growth_rate is not None:
                    if abs(growth_rate) < 0.05:
                        trend_direction = "stable"
                    elif growth_rate > 0:
                        trend_direction = "increasing"
                    else:
                        trend_direction = "decreasing"
                    
                    # Determine trend strength
                    if abs(growth_rate) > 0.2:
                        trend_strength = "strong"
                    elif abs(growth_rate) > 0.1:
                        trend_strength = "moderate"
                    else:
                        trend_strength = "weak"
                else:
                    trend_direction = "unknown"
                    trend_strength = "weak"
                
                # Calculate volatility (simplified)
                if len(historical_data) > 1:
                    values = [self._extract_numeric_values(h.metrics).get(metric, 0) for h in historical_data[-4:]]
                    values = [v for v in values if v is not None]
                    if len(values) > 1:
                        volatility = statistics.stdev(values) / statistics.mean(values) if statistics.mean(values) != 0 else 0
                    else:
                        volatility = 0
                else:
                    volatility = 0
                
                trends.append(TrendAnalysis(
                    metric=metric,
                    current_value=current_value,
                    previous_value=previous_value,
                    growth_rate=growth_rate,
                    trend_direction=trend_direction,
                    trend_strength=trend_strength,
                    volatility=volatility
                ))
        
        return trends
    
    def _assess_risks(
        self, 
        metrics: Dict[str, float], 
        ratios: FinancialRatios, 
        base_risks: List[str]
    ) -> List[RiskAssessment]:
        """Comprehensive risk assessment."""
        
        risks = []
        
        # Liquidity Risk
        current_ratio = ratios.liquidity_ratios.get("current_ratio", 0)
        if current_ratio < 1:
            risks.append(RiskAssessment(
                category="Liquidity",
                level=RiskLevel.CRITICAL,
                score=20,
                description="Current ratio below 1 indicates potential liquidity issues",
                mitigation_suggestions=[
                    "Improve cash collection",
                    "Reduce inventory levels",
                    "Negotiate better payment terms with suppliers"
                ]
            ))
        elif current_ratio < 1.5:
            risks.append(RiskAssessment(
                category="Liquidity",
                level=RiskLevel.HIGH,
                score=40,
                description="Current ratio below 1.5 indicates liquidity concerns",
                mitigation_suggestions=[
                    "Monitor cash flow closely",
                    "Consider short-term financing options"
                ]
            ))
        
        # Leverage Risk
        debt_to_equity = ratios.leverage_ratios.get("debt_to_equity", 0)
        if debt_to_equity > 2:
            risks.append(RiskAssessment(
                category="Leverage",
                level=RiskLevel.HIGH,
                score=70,
                description="High debt-to-equity ratio indicates significant leverage risk",
                mitigation_suggestions=[
                    "Consider debt restructuring",
                    "Improve profitability to reduce reliance on debt",
                    "Explore equity financing options"
                ]
            ))
        
        # Profitability Risk
        net_margin = ratios.profitability_ratios.get("net_margin", 0)
        if net_margin < 0:
            risks.append(RiskAssessment(
                category="Profitability",
                level=RiskLevel.CRITICAL,
                score=10,
                description="Negative net margin indicates unprofitable operations",
                mitigation_suggestions=[
                    "Review cost structure",
                    "Implement cost reduction measures",
                    "Reassess pricing strategy"
                ]
            ))
        elif net_margin < 0.05:
            risks.append(RiskAssessment(
                category="Profitability",
                level=RiskLevel.HIGH,
                score=50,
                description="Low net margin indicates profitability concerns",
                mitigation_suggestions=[
                    "Focus on high-margin products/services",
                    "Improve operational efficiency"
                ]
            ))
        
        # Add base risks from analysis
        for risk_text in base_risks:
            risks.append(RiskAssessment(
                category="General",
                level=RiskLevel.MEDIUM,
                score=60,
                description=risk_text,
                mitigation_suggestions=["Monitor closely", "Develop mitigation plan"]
            ))
        
        return risks
    
    def _benchmark_against_industry(
        self, 
        metrics: Dict[str, float], 
        industry: str
    ) -> List[IndustryBenchmark]:
        """Benchmark metrics against industry standards."""
        
        benchmarks = []
        industry_data = self.industry_benchmarks.get(industry.lower(), {})
        
        for metric, value in metrics.items():
            if metric in industry_data:
                industry_stats = industry_data[metric]
                avg = industry_stats["avg"]
                median = industry_stats["median"]
                
                # Determine percentile ranking (simplified)
                if value > avg:
                    percentile_ranking = 75 + (value - avg) / avg * 25
                    comparison = "above_average"
                elif value < median:
                    percentile_ranking = 25 - (median - value) / median * 25
                    comparison = "below_average"
                else:
                    percentile_ranking = 50
                    comparison = "average"
                
                benchmarks.append(IndustryBenchmark(
                    metric=metric,
                    industry_average=avg,
                    industry_median=median,
                    percentile_ranking=max(0, min(100, percentile_ranking)),
                    comparison=comparison
                ))
        
        return benchmarks
    
    def _calculate_financial_health_score(
        self, 
        metrics: Dict[str, float], 
        ratios: FinancialRatios, 
        risks: List[RiskAssessment]
    ) -> Dict[str, Any]:
        """Calculate overall financial health score."""
        
        score_components = {}
        
        # Profitability Score (30% weight)
        net_margin = ratios.profitability_ratios.get("net_margin", 0)
        if net_margin > 0.15:
            profitability_score = 90
        elif net_margin > 0.10:
            profitability_score = 80
        elif net_margin > 0.05:
            profitability_score = 70
        elif net_margin > 0:
            profitability_score = 60
        else:
            profitability_score = 30
        
        score_components["profitability"] = profitability_score
        
        # Liquidity Score (25% weight)
        current_ratio = ratios.liquidity_ratios.get("current_ratio", 0)
        if current_ratio > 2.5:
            liquidity_score = 90
        elif current_ratio > 2.0:
            liquidity_score = 80
        elif current_ratio > 1.5:
            liquidity_score = 70
        elif current_ratio > 1.0:
            liquidity_score = 60
        else:
            liquidity_score = 30
        
        score_components["liquidity"] = liquidity_score
        
        # Leverage Score (20% weight)
        debt_to_equity = ratios.leverage_ratios.get("debt_to_equity", 0)
        if debt_to_equity < 0.5:
            leverage_score = 90
        elif debt_to_equity < 1.0:
            leverage_score = 80
        elif debt_to_equity < 1.5:
            leverage_score = 70
        elif debt_to_equity < 2.0:
            leverage_score = 60
        else:
            leverage_score = 30
        
        score_components["leverage"] = leverage_score
        
        # Risk Score (25% weight)
        high_risk_count = len([r for r in risks if r.level in [RiskLevel.HIGH, RiskLevel.CRITICAL]])
        if high_risk_count == 0:
            risk_score = 90
        elif high_risk_count == 1:
            risk_score = 75
        elif high_risk_count == 2:
            risk_score = 60
        else:
            risk_score = 40
        
        score_components["risk"] = risk_score
        
        # Calculate weighted average
        weights = {"profitability": 0.30, "liquidity": 0.25, "leverage": 0.20, "risk": 0.25}
        overall_score = sum(score_components[category] * weights[category] for category in weights)
        
        # Determine health category
        if overall_score >= 85:
            health_category = FinancialHealthScore.EXCELLENT
        elif overall_score >= 70:
            health_category = FinancialHealthScore.GOOD
        elif overall_score >= 55:
            health_category = FinancialHealthScore.FAIR
        elif overall_score >= 40:
            health_category = FinancialHealthScore.POOR
        else:
            health_category = FinancialHealthScore.CRITICAL
        
        return {
            "overall_score": round(overall_score, 1),
            "health_category": health_category.value,
            "score_components": score_components,
            "grade": self._get_letter_grade(overall_score)
        }
    
    def _get_letter_grade(self, score: float) -> str:
        """Convert numeric score to letter grade."""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"
    
    def _generate_predictive_insights(
        self, 
        metrics: Dict[str, float], 
        trend_analysis: Optional[List[TrendAnalysis]], 
        historical_data: Optional[List[FinancialReportResponse]]
    ) -> PredictiveInsights:
        """Generate predictive financial insights."""
        
        # Simple forecasting based on trends
        revenue_forecast = []
        profit_forecast = []
        
        current_revenue = metrics.get("revenue", 0)
        current_profit = metrics.get("net_profit", 0)
        
        # Get revenue growth trend
        revenue_trend = None
        if trend_analysis:
            revenue_trend = next((t for t in trend_analysis if t.metric == "revenue"), None)
        
        if revenue_trend and revenue_trend.growth_rate is not None:
            growth_rate = revenue_trend.growth_rate
            confidence = 0.8 if revenue_trend.trend_strength == "strong" else 0.6
        else:
            growth_rate = 0.05  # Default 5% growth
            confidence = 0.4
        
        # Generate simple forecasts
        for i in range(1, 4):  # 3-year forecast
            future_revenue = current_revenue * (1 + growth_rate) ** i
            future_profit = future_revenue * metrics.get("net_margin", 0.1)
            
            revenue_forecast.append((f"Year_{i}", future_revenue))
            profit_forecast.append((f"Year_{i}", future_profit))
        
        return PredictiveInsights(
            revenue_forecast=revenue_forecast,
            profit_forecast=profit_forecast,
            confidence_level=confidence,
            key_drivers=["Revenue growth", "Cost management", "Market conditions"],
            risk_factors=["Economic uncertainty", "Competition", "Regulatory changes"]
        )
    
    def _generate_recommendations(
        self, 
        metrics: Dict[str, float], 
        ratios: FinancialRatios, 
        risks: List[RiskAssessment], 
        benchmarking: Optional[List[IndustryBenchmark]], 
        health_score: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Generate actionable recommendations."""
        
        recommendations = {
            "immediate_actions": [],
            "short_term_goals": [],
            "long_term_strategy": [],
            "risk_mitigation": []
        }
        
        # Profitability recommendations
        net_margin = ratios.profitability_ratios.get("net_margin", 0)
        if net_margin < 0.05:
            recommendations["immediate_actions"].extend([
                "Conduct comprehensive cost review",
                "Eliminate non-profitable product lines",
                "Renegotiate supplier contracts"
            ])
        
        # Liquidity recommendations
        current_ratio = ratios.liquidity_ratios.get("current_ratio", 0)
        if current_ratio < 1.5:
            recommendations["immediate_actions"].extend([
                "Improve accounts receivable collection",
                "Reduce inventory holding periods",
                "Secure short-term financing if needed"
            ])
        
        # Leverage recommendations
        debt_to_equity = ratios.leverage_ratios.get("debt_to_equity", 0)
        if debt_to_equity > 1.5:
            recommendations["short_term_goals"].extend([
                "Develop debt reduction plan",
                "Improve profitability to reduce leverage ratio",
                "Consider equity financing options"
            ])
        
        # Growth recommendations
        revenue_growth = metrics.get("revenue_growth_yoy", 0)
        if revenue_growth < 0.1:
            recommendations["short_term_goals"].extend([
                "Explore new market opportunities",
                "Invest in product development",
                "Consider strategic partnerships"
            ])
        
        # Long-term strategic recommendations
        if health_score["overall_score"] < 70:
            recommendations["long_term_strategy"].extend([
                "Comprehensive business model review",
                "Strategic planning for sustainable growth",
                "Consider business restructuring options"
            ])
        
        # Risk mitigation
        high_risks = [r for r in risks if r.level in [RiskLevel.HIGH, RiskLevel.CRITICAL]]
        for risk in high_risks[:3]:  # Top 3 risks
            recommendations["risk_mitigation"].extend(risk.mitigation_suggestions[:2])
        
        return recommendations
    
    def _assess_data_quality(self, metrics: Dict[str, float]) -> float:
        """Assess the quality of extracted financial data."""
        
        total_metrics = len(metrics)
        if total_metrics == 0:
            return 0.0
        
        # Check for key metrics
        key_metrics = ["revenue", "net_profit", "total_assets", "total_liabilities"]
        available_key_metrics = len([m for m in key_metrics if m in metrics])
        
        # Calculate completeness score
        completeness_score = available_key_metrics / len(key_metrics)
        
        # Check data consistency (basic validation)
        consistency_score = 1.0
        if "total_assets" in metrics and "total_liabilities" in metrics:
            if metrics["total_liabilities"] > metrics["total_assets"] * 2:
                consistency_score -= 0.2
        
        if "revenue" in metrics and "net_profit" in metrics:
            if abs(metrics["net_profit"]) > metrics["revenue"]:
                consistency_score -= 0.3
        
        return round((completeness_score * 0.6 + consistency_score * 0.4) * 100, 1)


# Global analyzer instance
advanced_analyzer = AdvancedFinancialAnalyzer()
