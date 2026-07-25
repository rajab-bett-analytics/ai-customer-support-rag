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

      setConversationId(
        response.conversation_id,
      );

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
            "Sorry, something went wrong while contacting the AI.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex flex-1 flex-col bg-slate-100">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-8 py-8">
        <div className="mx-auto max-w-5xl space-y-8">
          {messages.length === 0 ? (
            <div className="flex min-h-[520px] flex-col items-center justify-center rounded-3xl border border-gray-200 bg-white p-12 text-center shadow-sm">
              <div className="mb-8 flex h-24 w-24 items-center justify-center rounded-full bg-blue-100 text-5xl">
                🤖
              </div>

              <h1 className="text-4xl font-bold text-gray-900">
                AI Customer Support
              </h1>

              <p className="mt-4 max-w-2xl text-lg leading-8 text-gray-500">
                Ask questions about your uploaded
                documents and receive accurate,
                AI-powered answers grounded in your
                knowledge base.
              </p>

              <div className="mt-8 rounded-xl bg-slate-100 px-6 py-4 text-sm text-gray-600">
                💡 Try asking:
                <br />
                <span className="italic">
                  "Summarize our refund policy."
                </span>
              </div>
            </div>
          ) : (
            messages.map((message, index) => (
              <MessageBubble
                key={index}
                message={message}
              />
            ))
          )}

          {loading && (
            <div className="max-w-4xl rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-200 font-semibold">
                  AI
                </div>

                <div>
                  <p className="font-medium text-gray-800">
                    AI Assistant
                  </p>

                  <p className="animate-pulse text-sm text-gray-500">
                    Thinking...
                  </p>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Chat Composer */}
      <div className="sticky bottom-0 border-t border-gray-200 bg-white/95 px-8 py-6 backdrop-blur">
        <div className="mx-auto max-w-5xl">
          <div className="flex items-end gap-4 rounded-2xl border border-gray-200 bg-white p-3 shadow-sm">
            <input
              className="flex-1 bg-transparent px-3 py-3 text-gray-900 placeholder:text-gray-400 focus:outline-none"
              placeholder="Ask a question about your documents..."
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
              disabled={
                loading || !question.trim()
              }
              className="rounded-xl bg-blue-600 px-6 py-3 font-medium text-white shadow transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-gray-400"
            >
              {loading ? "..." : "➤ Send"}
            </button>
          </div>

          <p className="mt-3 text-center text-xs text-gray-500">
            AI responses are generated from your uploaded knowledge base.
          </p>
        </div>
      </div>
    </main>
  );
}

export default ChatArea;