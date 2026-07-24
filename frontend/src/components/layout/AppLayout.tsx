import { useEffect, useState } from "react";

import Header from "./Header";
import Sidebar from "./Sidebar";
import ChatArea from "./ChatArea";

import {
  getConversations,
  type ConversationSummary,
} from "../../features/conversations/services/conversationService";

import type { ChatMessage } from "../../features/chat/types/ChatMessage";

function AppLayout() {
  const [messages, setMessages] =
    useState<ChatMessage[]>([]);

  const [conversationId, setConversationId] =
    useState<number | null>(null);

  const [conversations, setConversations] =
    useState<ConversationSummary[]>([]);

  async function loadConversations() {
    try {
      const data = await getConversations();
      setConversations(data);
    } catch (error) {
      console.error(error);
    }
  }

  useEffect(() => {
    void loadConversations();
  }, []);

  return (
    <div className="flex h-screen flex-col bg-gray-100">
      <Header />

      <main className="flex min-h-0 flex-1 overflow-hidden">
        <Sidebar
          conversations={conversations}
          conversationId={conversationId}
          setConversationId={setConversationId}
          setMessages={setMessages}
        />

        <ChatArea
          messages={messages}
          setMessages={setMessages}
          conversationId={conversationId}
          setConversationId={setConversationId}
          refreshConversations={loadConversations}
        />
      </main>
    </div>
  );
}

export default AppLayout;