import {
  useCallback,
  useEffect,
  useState,
} from "react";

import ConversationPanel from "../components/conversations/ConversationPanel";
import ChatArea from "../components/layouts/ChatArea";

import SourceViewer from "../features/documents/components/SourceViewer";

import { useLayout } from "../components/layouts/AppShell/useLayout";

import type { ChatMessage } from "../features/chat/types/ChatMessage";
import type { DocumentSource } from "../features/documents/types/DocumentSource";

import {
  getConversations,
  type ConversationSummary,
} from "../features/conversations/services/conversationService";

function DashboardPage() {
  const {
    setPreviewVisible,
  } = useLayout();

  const [messages, setMessages] =
    useState<ChatMessage[]>([]);

  const [conversationId, setConversationId] =
    useState<number | null>(null);

  const [conversations, setConversations] =
    useState<ConversationSummary[]>([]);

  const [loadingConversations, setLoadingConversations] =
    useState(true);

  const [refreshing, setRefreshing] =
    useState(false);

  const [selectedSource, setSelectedSource] =
    useState<DocumentSource | null>(null);

  const refreshConversations =
    useCallback(async () => {
      try {
        setRefreshing(true);

        const data =
          await getConversations();

        setConversations(data);
      } catch (error) {
        console.error(
          "Failed to load conversations",
          error,
        );
      } finally {
        setRefreshing(false);
        setLoadingConversations(false);
      }
    }, []);

  useEffect(() => {
    void refreshConversations();
  }, [refreshConversations]);

  function handleSourceSelect(
    source: DocumentSource,
  ) {
    setSelectedSource(source);
    setPreviewVisible(true);
  }

  return (
    <>
      <div
        className="
          flex
          h-full
          min-h-0
          min-w-0
          gap-3
          bg-slate-100
          p-3
          xl:gap-4
          xl:p-4
        "
      >
        {/* Conversation Panel */}

        <aside
          className="
            hidden
            lg:flex
            w-[260px]
            xl:w-[280px]
            2xl:w-[320px]
            shrink-0
            rounded-2xl
            border
            border-slate-200
            bg-white
            shadow-sm
          "
        >
          <ConversationPanel
            conversations={conversations}
            conversationId={conversationId}
            setConversationId={setConversationId}
            setMessages={setMessages}
            loading={loadingConversations}
            refreshing={refreshing}
            onRefresh={refreshConversations}
          />
        </aside>

        {/* Chat Area */}

        <main
          className="
            flex
            flex-1
            basis-0
            min-h-0
            min-w-0
            rounded-2xl
            border
            border-slate-200
            bg-white
            shadow-sm
          "
        >
          <ChatArea
            messages={messages}
            setMessages={setMessages}
            conversationId={conversationId}
            setConversationId={setConversationId}
            refreshConversations={
              refreshConversations
            }
            onSourceSelect={
              handleSourceSelect
            }
          />
        </main>
      </div>

      <SourceViewer
        source={selectedSource}
      />
    </>
  );
}

export default DashboardPage;