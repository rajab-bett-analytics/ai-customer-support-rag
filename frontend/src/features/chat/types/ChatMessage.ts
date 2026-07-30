import type { ChatSource } from "./ChatSource";


export interface ChatMessage {
  id: number;
  role: "user" | "assistant";
  content: string;
  created_at: string;
  sources?: ChatSource[];
}