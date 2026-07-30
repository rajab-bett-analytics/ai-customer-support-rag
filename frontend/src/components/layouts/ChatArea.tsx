import {
  useEffect,
  useRef,
  useState,
} from "react";

import { askQuestion } from "../../features/chat/services/chatService";

import type { ChatMessage } from "../../features/chat/types/ChatMessage";
import type { DocumentSource } from "../../features/documents/types/DocumentSource";

import MessageBubble from "../../features/chat/components/MessageBubble";

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

  onSourceSelect: (
    source: DocumentSource,
  ) => void;
}

function ChatArea({
  messages,
  setMessages,
  conversationId,
  setConversationId,
  refreshConversations,
  onSourceSelect,
}: ChatAreaProps) {
  const [question, setQuestion] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const messagesEndRef =
    useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  async function handleSend() {
    if (!question.trim() || loading) {
      return;
    }

    const currentQuestion = question;

    setMessages((previous) => [
      ...previous,
      {
        id: Date.now(),
        role: "user",
        content: currentQuestion,
        created_at:
          new Date().toISOString(),
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response =
        await askQuestion({
          question: currentQuestion,
          conversation_id:
            conversationId,
        });

      const isNewConversation =
        conversationId === null;

      setConversationId(
        response.conversation_id,
      );

      setMessages((previous) => [
        ...previous,
        {
          id: Date.now() + 1,
          role: "assistant",
          content: response.answer,
          created_at:
            new Date().toISOString(),
          sources:
            response.sources,
        },
      ]);

      if (isNewConversation) {
        await refreshConversations();
      }
    } catch {
      setMessages((previous) => [
        ...previous,
        {
          id: Date.now() + 2,
          role: "assistant",
          content:
            "Sorry, something went wrong while contacting the AI.",
          created_at:
            new Date().toISOString(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      className="
        flex
        h-full
        min-h-0
        min-w-0
        flex-1
        flex-col
        overflow-hidden
        bg-slate-50
      "
    >
      {/* Messages */}

      <div
        className="
          flex-1
          min-h-0
          overflow-y-auto
          overflow-x-hidden
        "
      >
        <div
          className="
            mx-auto
            w-full
            max-w-5xl
            px-4
            py-6
            lg:px-8
            xl:px-10
            space-y-5
          "
        >
          {messages.length === 0 ? (
            <div
              className="
                flex
                min-h-[420px]
                flex-col
                items-center
                justify-center
                rounded-2xl
                border
                border-slate-200
                bg-white
                px-8
                py-12
                text-center
                shadow-sm
              "
            >
              <div
                className="
                  mb-5
                  flex
                  h-16
                  w-16
                  items-center
                  justify-center
                  rounded-full
                  bg-blue-100
                  text-3xl
                "
              >
                🤖
              </div>

              <h1 className="text-2xl font-bold text-slate-900">
                AI Customer Support
              </h1>

              <p
                className="
                  mt-4
                  max-w-xl
                  text-sm
                  leading-7
                  text-slate-500
                "
              >
                Ask questions about your
                uploaded documents and receive
                AI-powered answers from your
                knowledge base.
              </p>
            </div>
          ) : (
            messages.map((message) => (
              <MessageBubble
                key={message.id}
                message={message}
                onSourceSelect={
                  onSourceSelect
                }
              />
            ))
          )}

          {loading && (
            <div
              className="
                rounded-xl
                border
                border-slate-200
                bg-white
                p-4
                shadow-sm
              "
            >
              <p className="font-medium">
                AI Assistant
              </p>

              <p className="mt-1 animate-pulse text-sm text-slate-500">
                Thinking...
              </p>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input */}

      <div
        className="
          shrink-0
          border-t
          border-slate-200
          bg-white
        "
      >
        <div
          className="
            mx-auto
            w-full
            max-w-5xl
            px-4
            py-4
            lg:px-8
            xl:px-10
          "
        >
          <div
            className="
              flex
              items-center
              gap-3
              rounded-xl
              border
              border-slate-300
              bg-white
              p-2
              shadow-sm
            "
          >
            <input
              value={question}
              onChange={(e) =>
                setQuestion(
                  e.target.value,
                )
              }
              onKeyDown={(e) => {
                if (
                  e.key === "Enter"
                ) {
                  handleSend();
                }
              }}
              placeholder="Ask about your documents..."
              className="
                flex-1
                bg-transparent
                px-3
                py-2
                text-sm
                focus:outline-none
              "
            />

            <button
              onClick={handleSend}
              disabled={
                loading ||
                !question.trim()
              }
              className="
                rounded-lg
                bg-blue-600
                px-5
                py-2.5
                text-sm
                font-medium
                text-white
                transition
                hover:bg-blue-700
                disabled:bg-slate-400
              "
            >
              {loading
                ? "..."
                : "Send"}
            </button>
          </div>

          <p className="mt-2 text-center text-xs text-slate-500">
            AI responses are generated from your uploaded knowledge base.
          </p>
        </div>
      </div>
    </div>
  );
}

export default ChatArea;