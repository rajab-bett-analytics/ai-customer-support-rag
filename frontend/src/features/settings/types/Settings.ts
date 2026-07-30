export interface Settings {
  id: number;
  user_id: number;

  ai_provider: string;
  chat_model: string;
  embedding_model: string;

  top_k: number;
  similarity_threshold: number;

  temperature: number;
  max_tokens: number;

  system_prompt: string;

  created_at: string;
  updated_at: string;
}