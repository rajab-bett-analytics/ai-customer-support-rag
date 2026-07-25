import { useEffect, useState } from "react";

import ConversationPanel from "../components/conversations/ConversationPanel";
import ChatArea from "../components/layout/ChatArea";

import type { ChatMessage } from "../features/chat/types/ChatMessage";

import {
  getConversations,
  type ConversationSummary,
} from "../features/conversations/services/conversationService";

function DashboardPage() {
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
    <div className="flex h-full">
      <ConversationPanel
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
        refreshConversations={refreshConversations}
      />
    </div>
  );
}

export default DashboardPage;