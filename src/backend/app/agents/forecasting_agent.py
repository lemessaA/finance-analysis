from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.agents.base_agent import BaseAgent


FORECASTING_INTERPRETATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert financial analyst and forecasting specialist. "
            "Interpret the following ML-generated financial forecast and provide:\n"
            "1. Executive summary of the forecast trend\n"
            "2. Key growth drivers and assumptions\n"
            "3. Risk factors that could impact the forecast\n"
            "4. Confidence assessment (High/Medium/Low) with reasoning\n"
            "5. Strategic recommendations based on the forecast\n\n"
            "Be clear, concise, and actionable.",
        ),
        (
            "human",
            "Metric: {metric}\n"
            "Historical Data: {historical_data}\n"
            "Forecasted Values: {forecast_data}\n"
            "Model Used: {model_type}\n"
            "Growth Rate (avg): {growth_rate:.1f}%\n\n"
            "Provide a professional forecast interpretation.",
        ),
    ]
)


class ForecastingAgent(BaseAgent):
    """Interprets ML-generated forecasts with LLM narrative."""

    def __init__(self):
        super().__init__(name="ForecastingAgent", temperature=0.2)
        self.chain = FORECASTING_INTERPRETATION_PROMPT | self.llm | StrOutputParser()

    async def run(
        self,
        metric: str,
        historical_data: list,
        forecast_data: list,
        model_type: str,
        growth_rate: float,
    ) -> str:
        self._log_start(f"forecast interpretation for {metric}")

        result = await self.chain.ainvoke(
            {
                "metric": metric,
                "historical_data": str(historical_data),
                "forecast_data": str(forecast_data),
                "model_type": model_type,
                "growth_rate": growth_rate,
            }
        )
        self._log_done("forecast interpretation")
        return result
