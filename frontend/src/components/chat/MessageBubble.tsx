import type { ChatMessage } from "../../features/chat/types/ChatMessage";

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
        className={`max-w-3xl rounded-2xl px-5 py-3 shadow-sm ${
          isUser
            ? "bg-blue-600 text-white"
            : "border border-gray-200 bg-white text-gray-900"
        }`}
      >
        <p className="whitespace-pre-wrap">
          {message.content}
        </p>
      </div>
    </div>
  );
}

export default MessageBubble;