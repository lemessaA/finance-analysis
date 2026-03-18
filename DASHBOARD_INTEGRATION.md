# Real Data Integration Guide

## Overview
The dashboard has been updated to use real API data instead of mock data. Here's how the integration works:

## Backend API Endpoints

### Main Dashboard Endpoint
- **GET** `/api/dashboard/dashboard` - Returns all dashboard data
- **GET** `/api/dashboard/dashboard/score` - Returns startup validation score
- **GET** `/api/dashboard/dashboard/market-analysis` - Returns market analysis summary
- **GET** `/api/dashboard/dashboard/competitors` - Returns competitor analysis
- **GET** `/api/dashboard/dashboard/revenue-forecast` - Returns revenue forecast data
- **GET** `/api/dashboard/dashboard/financial-comparison` - Returns financial comparison data

## Frontend Integration

### API Service
- **File**: `src/frontend/services/api.ts`
- **Function**: `getDashboardData()` - Fetches all dashboard data
- **Fallback**: Uses mock data if API is unavailable

### Dashboard Component
- **File**: `src/frontend/app/dashboard/page.tsx`
- **Features**:
  - Real-time data fetching
  - Error handling with fallback data
  - Loading states
  - Retry functionality

## Data Flow

1. **Dashboard loads** → Calls `getDashboardData()`
2. **API request** → Fetches data from backend
3. **Success** → Updates UI with real data
4. **Error** → Shows error message + uses fallback data
5. **Retry** → User can manually retry fetching

## Backend Services Required

The dashboard API expects these services to be implemented:

### 1. Startup Validator Service
```python
class StartupValidator:
    async def validate_startup(self, db: Session) -> Dict[str, Any]:
        # Returns overall score and breakdown
```

### 2. Market Intelligence Service
```python
class MarketIntelligenceService:
    async def get_market_analysis(self, db: Session) -> Dict[str, Any]:
        # Returns market size, growth, competition, opportunity
    
    async def get_competitors(self, db: Session) -> Dict[str, Any]:
        # Returns competitor data with strengths/weaknesses
```

### 3. Financial Reports Service
```python
class FinancialReportsService:
    async def get_financial_comparison(self, db: Session) -> Dict[str, Any]:
        # Returns financial metrics vs industry benchmarks
```

### 4. Forecasting Service
```python
class ForecastingService:
    async def get_revenue_forecast(self, db: Session) -> Dict[str, Any]:
        # Returns revenue forecast with actual vs projected
```

## Environment Setup

### Backend
1. Install dependencies: `pip install -r requirements.txt`
2. Set up virtual environment: `python3 -m venv venv`
3. Activate: `source venv/bin/activate`
4. Run: `uvicorn app.main:app --reload`

### Frontend
1. Install dependencies: `npm install`
2. Set environment variable: `NEXT_PUBLIC_API_URL=http://localhost:8000`
3. Run: `npm run dev`

## Data Schema

### Dashboard Response
```json
{
  "score": 78,
  "marketAnalysis": {
    "marketSize": "$2.4B",
    "growthRate": "18.5%",
    "competitionLevel": "Medium",
    "opportunityScore": 82
  },
  "competitors": [
    {
      "name": "TechCorp Inc.",
      "marketShare": "32%",
      "revenue": "$450M",
      "strengths": ["Brand recognition"],
      "weaknesses": ["Slow innovation"]
    }
  ],
  "revenueForecast": [
    {
      "month": "Jan",
      "actual": 120000,
      "forecast": 120000
    }
  ],
  "financialComparison": [
    {
      "category": "Revenue",
      "yourCompany": 189000,
      "industryAvg": 165000,
      "topPerformer": 245000
    }
  ],
  "marketSegments": [
    {
      "name": "Enterprise",
      "value": 45,
      "color": "#4f62ff"
    }
  ]
}
```

## Testing

### With Mock Data
- Remove `NEXT_PUBLIC_API_URL` environment variable
- Dashboard will use fallback data

### With Real API
- Set `NEXT_PUBLIC_API_URL=http://localhost:8000`
- Start backend server
- Dashboard will fetch real data

## Error Handling

- **Network errors**: Shows error message with retry button
- **API errors**: Falls back to mock data
- **Loading states**: Shows spinner during data fetch
- **Real-time updates**: Can be refreshed manually

## Next Steps

1. Implement the backend services
2. Connect to real database
3. Add authentication
4. Implement real-time updates with WebSockets
5. Add data caching for performance
