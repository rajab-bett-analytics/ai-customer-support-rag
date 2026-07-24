import api from "../../../api/client";

export interface ChatRequest {
  question: string;
  conversation_id?: number | null;
}

export interface ChatResponse {
  conversation_id: number;
  question: string;
  answer: string;
}

export async function askQuestion(
  data: ChatRequest,
): Promise<ChatResponse> {
  const response = await api.post(
    "/chat",
    data,
  );

  return response.data;
}