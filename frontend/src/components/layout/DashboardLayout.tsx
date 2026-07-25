import { useEffect, useState } from "react";

import Header from "./Header";
import Sidebar from "./Sidebar";
import ChatArea from "./ChatArea";

import type { ChatMessage } from "../../features/chat/types/ChatMessage";
import {
  getConversations,
  type ConversationSummary,
} from "../../features/conversations/services/conversationService";

function DashboardLayout() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [conversations, setConversations] = useState<ConversationSummary[]>([]);

  async function refreshConversations() {
    try {
      const data = await getConversations();
      setConversations(data);
    } catch (error) {
      console.error(error);
    }
  }

  useEffect(() => {
    refreshConversations();
  }, []);

  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar
        conversations={conversations}
        conversationId={conversationId}
        setConversationId={setConversationId}
        setMessages={setMessages}
      />

      <div className="flex flex-1 flex-col">
        <Header />

        <ChatArea
          messages={messages}
          setMessages={setMessages}
          conversationId={conversationId}
          setConversationId={setConversationId}
          refreshConversations={refreshConversations}
        />
      </div>
    </div>
  );
}

export default DashboardLayout;