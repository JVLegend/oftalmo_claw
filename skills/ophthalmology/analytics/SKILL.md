---
name: ophthalmology-analytics
description: Natural language queries for ophthalmology analytics, trends, volumes, and performance metrics.
version: 1.0.0
author: GeekVision
license: MIT
metadata:
  hermes:
    tags: [ophthalmology, analytics, trends, dashboard]
    category: ophthalmology
---

# Ophthalmology Analytics

You can answer questions about clinical operations metrics using the analytics API.

## Available Metrics
- **Volume**: Total exams by period (day, week, month, quarter, year)
- **Quality Score**: Average quality score by period, exam type, or operator
- **Exam Types**: Breakdown by fundoscopy, OCT, campimetry, topography, biometry, retinography
- **Operator Rankings**: Performance by doctor (volume, quality, trend)
- **Second Opinions**: Pending, resolved, turnaround time
- **Report Metrics**: Pending reports, average time to sign

## Example Queries
- "Quantos exames de OCT fizemos este mes?" -> GET /api/v1/analytics/by-exam-type
- "Qual o ranking dos operadores?" -> GET /api/v1/analytics/rankings
- "Qual a tendencia de volume nos ultimos 6 meses?" -> GET /api/v1/analytics/trends?period=month
- "Exportar relatorio mensal" -> GET /api/v1/analytics/summary + format as report

## API Endpoints
- GET /api/v1/analytics/trends?period={week|month|quarter|year}
- GET /api/v1/analytics/by-exam-type
- GET /api/v1/analytics/rankings
- GET /api/v1/analytics/summary
