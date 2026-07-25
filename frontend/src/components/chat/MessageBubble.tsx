import type { ChatMessage } from "../../features/chat/types/ChatMessage";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface MessageBubbleProps {
  message: ChatMessage;
}

function MessageBubble({
  message,
}: MessageBubbleProps) {
  const isUser = message.role === "user";

  return (
    <div
      className={`flex ${
        isUser
          ? "justify-end"
          : "justify-start"
      }`}
    >
      <div
        className={`flex max-w-4xl gap-3 ${
          isUser
            ? "flex-row-reverse"
            : "flex-row"
        }`}
      >

        {/* Avatar */}
        <div
          className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-full font-semibold shadow-sm ${
            isUser
              ? "bg-blue-600 text-white"
              : "bg-slate-200 text-slate-700"
          }`}
        >
          {isUser ? "Y" : "AI"}
        </div>


        {/* Message */}
        <div
          className={`rounded-2xl px-5 py-4 shadow-sm ${
            isUser
              ? "bg-blue-600 text-white"
              : "border border-gray-200 bg-white text-gray-900"
          }`}
        >

          {/* Sender */}
          <p
            className={`mb-2 text-xs font-semibold uppercase tracking-wide ${
              isUser
                ? "text-blue-100"
                : "text-gray-500"
            }`}
          >
            {isUser
              ? "You"
              : "AI Assistant"}
          </p>


          {/* Markdown Message */}
          <div
            className={`prose prose-sm max-w-none leading-7 ${
              isUser
                ? "prose-invert"
                : ""
            }`}
          >
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
            >
              {message.content}
            </ReactMarkdown>
          </div>

        </div>
      </div>
    </div>
  );
}

export default MessageBubble;