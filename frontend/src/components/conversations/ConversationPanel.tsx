import type { Dispatch, SetStateAction } from "react";

import ConversationList from "./ConversationList";

import type { ChatMessage } from "../../features/chat/types/ChatMessage";
import type { ConversationSummary } from "../../features/conversations/services/conversationService";

interface ConversationPanelProps {
  conversations: ConversationSummary[];
  conversationId: number | null;
  setConversationId: Dispatch<
    SetStateAction<number | null>
  >;
  setMessages: Dispatch<
    SetStateAction<ChatMessage[]>
  >;
}

function ConversationPanel({
  conversations,
  conversationId,
  setConversationId,
  setMessages,
}: ConversationPanelProps) {
  function handleNewConversation() {
    setConversationId(null);
    setMessages([]);
  }

  return (
    <aside className="flex h-full w-80 flex-col border-r border-gray-200 bg-slate-100">
      {/* Header */}
      <div className="m-4 rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
        <h2 className="text-lg font-semibold text-gray-900">
          Conversations
        </h2>

        <p className="mt-1 text-sm text-gray-500">
          Continue previous chats or start a new one.
        </p>

        <button
          onClick={handleNewConversation}
          className="mt-5 flex w-full items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-3 font-medium text-white shadow-sm transition duration-200 hover:bg-blue-700"
        >
          <span className="text-lg">＋</span>
          New Conversation
        </button>
      </div>

      {/* Conversation List */}
      <div className="flex-1 overflow-y-auto px-4 pb-4">
        {conversations.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-gray-300 bg-white p-10 text-center shadow-sm">
            <div className="mb-4 text-5xl">
              💬
            </div>

            <h3 className="text-lg font-semibold text-gray-900">
              No conversations
            </h3>

            <p className="mt-2 text-sm text-gray-500">
              Your previous conversations will
              appear here.
            </p>
          </div>
        ) : (
          <div className="rounded-2xl border border-gray-200 bg-white p-3 shadow-sm">
            <ConversationList
              conversations={conversations}
              conversationId={conversationId}
              setConversationId={setConversationId}
              setMessages={setMessages}
            />
          </div>
        )}
      </div>
    </aside>
  );
}

export default ConversationPanel;