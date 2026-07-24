import api from "../../../api/client";

export interface MessageResponse {
  id: number;
  role: "user" | "assistant";
  content: string;
  created_at: string;
}

export interface ConversationResponse {
  id: number;
  title: string;
  created_at: string;
  messages: MessageResponse[];
}

export async function getConversation(
  conversationId: number,
): Promise<ConversationResponse> {
  const response = await api.get(
    `/conversations/${conversationId}`,
  );

  return response.data;
}