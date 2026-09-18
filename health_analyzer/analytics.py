"""Analytics and visualization module."""
import json
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from storage_manager import get_user_history

def generate_severity_trend_chart(user_id: str) -> go.Figure:
    """Generate a Plotly line chart showing severity trend over time."""
    history = get_user_history(user_id)
    if not history:
        # Return empty chart
        fig = go.Figure()
        fig.update_layout(title="No history data available", height=400)
        return fig

    dates = [r["timestamp"][:10] for r in history]
    scores = [r.get("composite_score", 0) for r in history]
    user_severities = [r.get("user_severity", 0) for r in history]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=dates, y=scores, name="Composite Score", line=dict(color="red", width=3)),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=dates, y=user_severities, name="User Rating", line=dict(color="blue", width=2, dash="dash")),
        secondary_y=False,
    )

    fig.update_layout(
        title=f"Severity Trend for {user_id}",
        xaxis_title="Date",
        yaxis_title="Severity Score",
        height=400,
        template="plotly_white",
    )
    return fig

def generate_category_breakdown(user_id: str) -> go.Figure:
    """Generate a pie chart showing category distribution."""
    history = get_user_history(user_id)
    if not history:
        fig = go.Figure()
        fig.update_layout(title="No history data available", height=400)
        return fig

    categories = {}
    for r in history:
        cat = r.get("category", "Unknown")
        categories[cat] = categories.get(cat, 0) + 1

    fig = go.Figure(data=[go.Pie(labels=list(categories.keys()), values=list(categories.values()))])
    fig.update_layout(title="Symptom Category Distribution", height=400)
    return fig

def compute_composite_severity(
    symptoms: list[str],
    user_severity: int,
    duration_days: int,
    category: str,
) -> float:
    """Compute weighted composite severity score."""
    from symptom_data import CATEGORIES

    base_score = user_severity
    duration_factor = min(duration_days / 7, 2.0)
    category_multiplier = CATEGORIES.get(category, {}).get("risk_multiplier", 1.0)

    composite = base_score * duration_factor * category_multiplier
    return round(min(composite, 10.0), 1)
