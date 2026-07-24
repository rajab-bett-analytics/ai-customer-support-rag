import type { Dispatch, SetStateAction } from "react";

import ConversationList from "../conversations/ConversationList";

import type { ChatMessage } from "../../features/chat/types/ChatMessage";
import type { ConversationSummary } from "../../features/conversations/services/conversationService";

interface SidebarProps {
  conversations: ConversationSummary[];
  conversationId: number | null;
  setConversationId: Dispatch<
    SetStateAction<number | null>
  >;
  setMessages: Dispatch<
    SetStateAction<ChatMessage[]>
  >;
}

function Sidebar({
  conversations,
  conversationId,
  setConversationId,
  setMessages,
}: SidebarProps) {
  function handleNewConversation() {
    setConversationId(null);
    setMessages([]);
  }

  return (
    <aside className="flex h-full w-72 flex-col border-r bg-white">
      <div className="border-b p-4">
        <button
          onClick={handleNewConversation}
          className="w-full rounded bg-blue-600 p-2 text-white hover:bg-blue-700"
        >
          + New Conversation
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        <ConversationList
          conversations={conversations}
          conversationId={conversationId}
          setConversationId={setConversationId}
          setMessages={setMessages}
        />
      </div>
    </aside>
  );
}

export default Sidebar;