import {
  useEffect,
  useRef,
  useState,
} from "react";

import { askQuestion } from "../../features/chat/services/chatService";
import type { ChatMessage } from "../../features/chat/types/ChatMessage";

import MessageBubble from "../chat/MessageBubble";

interface ChatAreaProps {
  messages: ChatMessage[];
  setMessages: React.Dispatch<
    React.SetStateAction<ChatMessage[]>
  >;
  conversationId: number | null;
  setConversationId: React.Dispatch<
    React.SetStateAction<number | null>
  >;
  refreshConversations: () => Promise<void>;
}

function ChatArea({
  messages,
  setMessages,
  conversationId,
  setConversationId,
  refreshConversations,
}: ChatAreaProps) {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  const messagesEndRef =
    useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  async function handleSend() {
    if (!question.trim() || loading) {
      return;
    }

    const userMessage: ChatMessage = {
      role: "user",
      content: question,
    };

    setMessages((previous) => [
      ...previous,
      userMessage,
    ]);

    const currentQuestion = question;
    setQuestion("");
    setLoading(true);

    try {
      const response = await askQuestion({
        question: currentQuestion,
        conversation_id: conversationId,
      });

      const isNewConversation =
        conversationId === null;

      setConversationId(response.conversation_id);

      const assistantMessage: ChatMessage = {
        role: "assistant",
        content: response.answer,
      };

      setMessages((previous) => [
        ...previous,
        assistantMessage,
      ]);

      if (isNewConversation) {
        await refreshConversations();
      }
    } catch (error) {
      console.error(error);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            "Something went wrong while contacting the AI.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex flex-1 flex-col bg-gray-50">
      <div className="flex-1 space-y-4 overflow-y-auto p-6">
        {messages.length === 0 ? (
          <p className="text-gray-500">
            Start a conversation with your AI assistant.
          </p>
        ) : (
          messages.map((message, index) => (
            <MessageBubble
              key={index}
              message={message}
            />
          ))
        )}

        {loading && (
          <div className="max-w-3xl rounded-2xl border border-gray-200 bg-white p-4 text-gray-500 italic shadow-sm">
            AI is typing...
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="border-t bg-white p-4">
        <div className="flex gap-2">
          <input
            className="flex-1 rounded-lg border p-3 focus:border-blue-500 focus:outline-none"
            placeholder="Type your message..."
            value={question}
            onChange={(e) =>
              setQuestion(e.target.value)
            }
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleSend();
              }
            }}
          />

          <button
            onClick={handleSend}
            disabled={loading}
            className="rounded-lg bg-blue-600 px-6 text-white transition hover:bg-blue-700 disabled:bg-gray-400"
          >
            {loading ? "Sending..." : "Send"}
          </button>
        </div>
      </div>
    </main>
  );
}

export default ChatArea;