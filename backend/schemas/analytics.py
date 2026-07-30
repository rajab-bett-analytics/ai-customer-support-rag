from pydantic import BaseModel


class AnalyticsSummary(BaseModel):
    conversations: int
    documents: int
    ai_responses: int
    average_response_time: float