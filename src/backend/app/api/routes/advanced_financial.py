"""
Advanced financial analysis API endpoints.
"""

from __future__ import annotations

import uuid
from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, UploadFile, File, Query, BackgroundTasks
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from app.config import settings

from app.services.advanced_financial_analysis import advanced_analyzer
from app.services.pdf_service import _extract
from app.utils.performance import performance_timer
from app.utils.logger import setup_logger
import json

logger = setup_logger(__name__)
router = APIRouter()

# Enhanced request/response models
class AdvancedAnalysisRequest(BaseModel):
    """Request model for advanced financial analysis."""
    industry: Optional[str] = Field(None, description="Industry for benchmarking")
    include_forecasting: bool = Field(True, description="Include predictive insights")
    include_benchmarking: bool = Field(True, description="Include industry benchmarking")
    analysis_depth: str = Field("comprehensive", description="Analysis depth: basic, standard, comprehensive")

class ChatRequest(BaseModel):
    analysis_id: str = Field(..., description="The ID of the advanced analysis")
    message: str = Field(..., description="The user's question about the financials")

class ChatResponse(BaseModel):
    answer: str = Field(..., description="The AI's response")


class TrendAnalysisRequest(BaseModel):
    """Request model for trend analysis."""
    report_ids: List[str] = Field(..., description="List of report IDs for trend analysis")
    metrics: List[str] = Field(["revenue", "net_profit"], description="Metrics to analyze")


class ComparisonRequest(BaseModel):
    """Request model for advanced comparison."""
    primary_report_id: str = Field(..., description="Primary report ID")
    comparison_report_ids: List[str] = Field(..., description="Report IDs to compare against")
    comparison_type: str = Field("benchmark", description="Comparison type: benchmark, competitive, historical")


class ExportRequest(BaseModel):
    """Request model for exporting analysis."""
    report_id: str = Field(..., description="Report ID to export")
    export_format: str = Field("json", description="Export format: json, pdf, excel")
    include_charts: bool = Field(True, description="Include visualizations")


# In-memory storage for advanced analysis results (in production, use database)
_advanced_analysis_store: Dict[str, Dict[str, Any]] = {}
_historical_reports: Dict[str, List[Dict[str, Any]]] = {}


@router.post("/analyze-advanced")
async def analyze_financial_report_advanced(
    file: UploadFile = File(...),
    industry: Optional[str] = Query(None, description="Industry for benchmarking"),
    analysis_depth: str = Query("comprehensive", description="Analysis depth"),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Perform advanced financial analysis with enhanced capabilities.
    
    Features:
    - Comprehensive financial ratio analysis
    - Industry benchmarking
    - Risk assessment with scoring
    - Predictive insights and forecasting
    - Trend analysis (with historical data)
    - Actionable recommendations
    """
    
    if file.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(
            status_code=415,
            detail="Only PDF files are supported."
        )
    
    # Check file size (20MB limit)
    content = await file.read()
    if len(content) > 20 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="File exceeds 20 MB limit."
        )
    
    logger.info(f"Processing advanced analysis for: {file.filename}")
    
    try:
        # Extract text from PDF
        text, page_count = _extract(content)
        
        # Get historical data if available
        historical_data = []
        if file.filename in _historical_reports:
            historical_data = _historical_reports[file.filename]
        
        # Perform advanced analysis
        analysis_result = await advanced_analyzer.analyze_comprehensive(
            text=text,
            filename=file.filename or "report.pdf",
            industry=industry,
            historical_data=historical_data
        )
        
        # Store result
        analysis_id = str(uuid.uuid4())
        _advanced_analysis_store[analysis_id] = analysis_result
        
        # Store for future historical analysis
        if file.filename not in _historical_reports:
            _historical_reports[file.filename] = []
        _historical_reports[file.filename].append(analysis_result["base_analysis"])
        
        # Add metadata
        analysis_result["analysis_id"] = analysis_id
        analysis_result["filename"] = file.filename
        analysis_result["page_count"] = page_count
        analysis_result["analysis_depth"] = analysis_depth
        
        logger.info(f"Advanced analysis completed: {analysis_id}")
        
        return {
            "analysis_id": analysis_id,
            "status": "completed",
            "analysis_result": analysis_result,
            "next_steps": [
                "Review financial health score and recommendations",
                "Examine risk assessment and mitigation strategies",
                "Analyze industry benchmarking results",
                "Review predictive insights"
            ]
        }
        
    except Exception as exc:
        logger.error(f"Advanced analysis failed: {exc}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Advanced analysis error: {str(exc)}"
        )


@router.get("/analysis/{analysis_id}")
async def get_analysis_result(analysis_id: str):
    """Retrieve a previously completed advanced analysis."""
    
    if analysis_id not in _advanced_analysis_store:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found"
        )
    
    return {
        "analysis_id": analysis_id,
        "result": _advanced_analysis_store[analysis_id]
    }


@router.post("/trend-analysis")
@performance_timer("trend_analysis")
async def analyze_trends(request: TrendAnalysisRequest):
    """Perform trend analysis across multiple reports."""
    
    # Collect historical data
    all_reports = []
    for report_id in request.report_ids:
        if report_id in _advanced_analysis_store:
            analysis = _advanced_analysis_store[report_id]
            all_reports.append(analysis["base_analysis"])
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Report {report_id} not found"
            )
    
    if len(all_reports) < 2:
        raise HTTPException(
            status_code=400,
            detail="At least 2 reports required for trend analysis"
        )
    
    # Perform trend analysis
    trend_results = {}
    for metric in request.metrics:
        # Extract metric values over time
        metric_values = []
        for report in all_reports:
            numeric_metrics = advanced_analyzer._extract_numeric_values(report.metrics)
            if metric in numeric_metrics:
                metric_values.append(numeric_metrics[metric])
        
        if len(metric_values) > 1:
            # Calculate trend statistics
            growth_rates = []
            for i in range(1, len(metric_values)):
                if metric_values[i-1] != 0:
                    growth_rate = (metric_values[i] - metric_values[i-1]) / abs(metric_values[i-1])
                    growth_rates.append(growth_rate)
            
            trend_results[metric] = {
                "values": metric_values,
                "average_growth_rate": sum(growth_rates) / len(growth_rates) if growth_rates else 0,
                "volatility": max(growth_rates) - min(growth_rates) if growth_rates else 0,
                "trend_direction": "increasing" if growth_rates and sum(growth_rates) > 0 else "decreasing",
                "data_points": len(metric_values)
            }
    
    return {
        "trend_analysis": trend_results,
        "analysis_summary": {
            "reports_analyzed": len(all_reports),
            "metrics_analyzed": len(request.metrics),
            "time_period": f"{len(all_reports)} periods"
        }
    }


@router.post("/advanced-comparison")
async def advanced_comparison(request: ComparisonRequest):
    """Perform advanced comparison between reports."""
    
    # Get primary report
    if request.primary_report_id not in _advanced_analysis_store:
        raise HTTPException(
            status_code=404,
            detail="Primary report not found"
        )
    
    primary_analysis = _advanced_analysis_store[request.primary_report_id]
    
    # Get comparison reports
    comparison_analyses = []
    for comp_id in request.comparison_report_ids:
        if comp_id not in _advanced_analysis_store:
            raise HTTPException(
                status_code=404,
                detail=f"Comparison report {comp_id} not found"
            )
        comparison_analyses.append(_advanced_analysis_store[comp_id])
    
    # Perform detailed comparison
    comparison_results = {
        "primary_report": {
            "id": request.primary_report_id,
            "financial_health_score": primary_analysis["financial_health_score"],
            "key_metrics": primary_analysis["base_analysis"].metrics
        },
        "comparisons": [],
        "insights": []
    }
    
    for comp_analysis in comparison_analyses:
        comparison_data = {
            "report_id": request.comparison_report_ids[comparison_analyses.index(comp_analysis)],
            "financial_health_score": comp_analysis["financial_health_score"],
            "health_score_diff": (
                comp_analysis["financial_health_score"]["overall_score"] - 
                primary_analysis["financial_health_score"]["overall_score"]
            ),
            "key_metrics": comp_analysis["base_analysis"].metrics
        }
        comparison_results["comparisons"].append(comparison_data)
    
    # Generate insights
    primary_score = primary_analysis["financial_health_score"]["overall_score"]
    comparison_scores = [comp["financial_health_score"]["overall_score"] for comp in comparison_analyses]
    
    if primary_score > sum(comparison_scores) / len(comparison_scores):
        comparison_results["insights"].append("Primary report shows above-average financial health")
    else:
        comparison_results["insights"].append("Primary report shows below-average financial health")
    
    return comparison_results


@router.post("/export/{analysis_id}")
async def export_analysis(analysis_id: str, request: ExportRequest):
    """Export analysis results in various formats."""
    
    if analysis_id not in _advanced_analysis_store:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found"
        )
    
    analysis = _advanced_analysis_store[analysis_id]
    
    if request.export_format == "json":
        return {
            "export_data": analysis,
            "format": "json",
            "filename": f"financial_analysis_{analysis_id}.json"
        }
    elif request.export_format == "pdf":
        # Placeholder for PDF generation
        return {
            "message": "PDF export not yet implemented",
            "format": "pdf",
            "filename": f"financial_analysis_{analysis_id}.pdf"
        }
    elif request.export_format == "excel":
        # Placeholder for Excel generation
        return {
            "message": "Excel export not yet implemented",
            "format": "excel",
            "filename": f"financial_analysis_{analysis_id}.xlsx"
        }
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported export format: {request.export_format}"
        )


@router.get("/industries")
async def get_supported_industries():
    """Get list of supported industries for benchmarking."""
    
    industries = {
        "technology": {
            "name": "Technology",
            "description": "Software, hardware, and technology services",
            "benchmarks_available": True
        },
        "manufacturing": {
            "name": "Manufacturing",
            "description": "Industrial manufacturing and production",
            "benchmarks_available": True
        },
        "retail": {
            "name": "Retail",
            "description": "Retail and consumer goods",
            "benchmarks_available": True
        },
        "healthcare": {
            "name": "Healthcare",
            "description": "Healthcare services and pharmaceuticals",
            "benchmarks_available": False
        },
        "finance": {
            "name": "Finance",
            "description": "Banking and financial services",
            "benchmarks_available": False
        }
    }
    
    return {"industries": industries}


@router.delete("/analysis/{analysis_id}")
async def delete_analysis(analysis_id: str):
    """Delete an analysis result."""
    
    if analysis_id not in _advanced_analysis_store:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found"
        )
    
    del _advanced_analysis_store[analysis_id]
    
    return {"message": "Analysis deleted successfully"}


@router.get("/analytics/overview")
async def get_analytics_overview():
    """Get overview of all performed analyses."""
    
    total_analyses = len(_advanced_analysis_store)
    
    if total_analyses == 0:
        return {
            "total_analyses": 0,
            "average_health_score": 0,
            "industry_distribution": {},
            "analysis_depth_distribution": {}
        }
    
    # Calculate statistics
    health_scores = [
        analysis["financial_health_score"]["overall_score"] 
        for analysis in _advanced_analysis_store.values()
    ]
    
    avg_health_score = sum(health_scores) / len(health_scores)
    
    # Industry distribution
    industry_dist = {}
    for analysis in _advanced_analysis_store.values():
        industry = analysis["analysis_metadata"].get("industry", "unknown")
        industry_dist[industry] = industry_dist.get(industry, 0) + 1
    
    # Analysis depth distribution
    depth_dist = {}
    for analysis in _advanced_analysis_store.values():
        depth = analysis["analysis_metadata"].get("analysis_depth", "comprehensive")
        depth_dist[depth] = depth_dist.get(depth, 0) + 1
    
    return {
        "total_analyses": total_analyses,
        "average_health_score": round(avg_health_score, 1),
        "industry_distribution": industry_dist,
        "analysis_depth_distribution": depth_dist,
        "health_score_distribution": {
            "excellent": len([s for s in health_scores if s >= 85]),
            "good": len([s for s in health_scores if 70 <= s < 85]),
            "fair": len([s for s in health_scores if 55 <= s < 70]),
            "poor": len([s for s in health_scores if 40 <= s < 55]),
            "critical": len([s for s in health_scores if s < 40])
        }
    }

@router.post("/chat", response_model=ChatResponse)
async def chat_with_financials(request: ChatRequest):
    """
    Chat directly with your extracted financial data.
    """
    analysis_id = request.analysis_id
    if analysis_id not in _advanced_analysis_store:
        raise HTTPException(status_code=404, detail="Analysis not found")
        
    analysis_data = _advanced_analysis_store[analysis_id]
    
    # We serialize most of the metrics into a prompt context
    context = json.dumps({
        "metrics": analysis_data.get("base_analysis", {}).get("metrics", {}),
        "health_score": analysis_data.get("financial_health_score", {}),
        "ratios": analysis_data.get("financial_ratios", {}),
        "risks": analysis_data.get("risk_assessment", []),
        "recommendations": analysis_data.get("recommendations", {})
    }, default=str)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert CFO and financial advisor. You are helping a startup founder understand their financial report. Be highly professional, actionable, and reference the specific numbers provided in the context. Context: {context}"),
        ("user", "{message}")
    ])
    
    llm = ChatGroq(
        model=settings.GROQ_MODEL,
        temperature=0.3,
        api_key=settings.GROQ_API_KEY
    )
    
    chain = prompt | llm
    
    try:
        response = await chain.ainvoke({
            "context": context,
            "message": request.message
        })
        return {"answer": response.content}
    except Exception as exc:
        logger.error(f"Chat failed: {exc}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate response: {str(exc)}"
        )
