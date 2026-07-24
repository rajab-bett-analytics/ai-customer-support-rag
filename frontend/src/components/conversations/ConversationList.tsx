import type { Dispatch, SetStateAction } from "react";

import type { ChatMessage } from "../../features/chat/types/ChatMessage";

import type { ConversationSummary } from "../../features/conversations/services/conversationService";

import {
  getConversation,
} from "../../features/conversations/services/conversationDetailsService";

interface ConversationListProps {
  conversations: ConversationSummary[];
  conversationId: number | null;
  setConversationId: Dispatch<
    SetStateAction<number | null>
  >;
  setMessages: Dispatch<
    SetStateAction<ChatMessage[]>
  >;
}

function ConversationList({
  conversations,
  conversationId,
  setConversationId,
  setMessages,
}: ConversationListProps) {
  async function handleConversationClick(
    conversationId: number,
  ) {
    try {
      const conversation =
        await getConversation(conversationId);

      setConversationId(conversation.id);

      setMessages(
        conversation.messages.map((message) => ({
          role: message.role,
          content: message.content,
        })),
      );
    } catch (error) {
      console.error(error);
    }
  }

  if (conversations.length === 0) {
    return (
      <p className="text-gray-500">
        No conversations yet.
      </p>
    );
  }

  return (
    <div className="space-y-2">
      {conversations.map((conversation) => (
        <button
          key={conversation.id}
          onClick={() =>
            handleConversationClick(
              conversation.id,
            )
          }
          className={`w-full rounded border p-3 text-left transition hover:bg-gray-100 ${
            conversationId === conversation.id
              ? "border-blue-600 bg-blue-50"
              : ""
          }`}
        >
          <p className="font-medium">
            {conversation.title}
          </p>

          <p className="text-xs text-gray-500">
            {new Date(
              conversation.created_at,
            ).toLocaleString()}
          </p>
        </button>
      ))}
    </div>
  );
}

export default ConversationList;