import type {
  Dispatch,
  SetStateAction,
} from "react";

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

  loading: boolean;

  refreshing: boolean;

  onRefresh: () => Promise<void>;
}


function ConversationPanel({
  conversations,
  conversationId,
  setConversationId,
  setMessages,
  loading,
  refreshing,
  onRefresh,
}: ConversationPanelProps) {


  function handleNewConversation() {
    setConversationId(null);
    setMessages([]);
  }


  return (
    <aside
      className="
        flex
        h-full
        min-w-0
        flex-col
        overflow-hidden
        border-r
        border-slate-200
        bg-slate-50
      "
    >


      {/* Compact Header */}

      <div
        className="
          shrink-0
          border-b
          border-slate-200
          bg-white
          px-3
          py-3
        "
      >

        <div
          className="
            flex
            items-center
            justify-between
            gap-2
          "
        >

          <h2
            className="
              truncate
              text-sm
              font-semibold
              text-slate-900
            "
          >
            Conversations
          </h2>


          <button
            onClick={() => void onRefresh()}
            disabled={refreshing}
            title="Refresh conversations"
            className="
              rounded-lg
              border
              border-slate-200
              p-1.5
              text-sm
              transition
              hover:bg-slate-100
              disabled:opacity-50
            "
          >
            {refreshing ? "⏳" : "↻"}
          </button>

        </div>


        <button
          onClick={handleNewConversation}
          className="
            mt-3
            flex
            w-full
            items-center
            justify-center
            gap-1.5
            rounded-lg
            bg-blue-600
            px-3
            py-2
            text-sm
            font-medium
            text-white
            transition
            hover:bg-blue-700
          "
        >
          <span>
            ＋
          </span>

          New Chat
        </button>

      </div>



      {/* Conversation List */}

      <div
        className="
          min-h-0
          flex-1
          overflow-y-auto
          px-2
          py-2
        "
      >

        {loading ? (

          <div className="space-y-2">

            {Array.from({
              length: 8,
            }).map((_, index) => (

              <div
                key={index}
                className="
                  h-12
                  animate-pulse
                  rounded-lg
                  border
                  border-slate-200
                  bg-white
                "
              />

            ))}

          </div>


        ) : conversations.length === 0 ? (

          <div
            className="
              rounded-lg
              border
              border-dashed
              border-slate-300
              bg-white
              p-4
              text-center
            "
          >

            <div className="mb-2 text-2xl">
              💬
            </div>


            <h3
              className="
                text-sm
                font-semibold
                text-slate-900
              "
            >
              No conversations
            </h3>


            <p
              className="
                mt-1
                text-xs
                text-slate-500
              "
            >
              Previous chats appear here.
            </p>

          </div>


        ) : (

          <div
            className="
              rounded-lg
              border
              border-slate-200
              bg-white
              p-1
            "
          >

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