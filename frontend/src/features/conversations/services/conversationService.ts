import api from "../../../api/client";

export interface ConversationSummary {
  id: number;
  title: string;
  created_at: string;
}

export async function getConversations(): Promise<
  ConversationSummary[]
> {
  const response = await api.get<ConversationSummary[]>(
    "/conversations",
  );

  return response.data;
}