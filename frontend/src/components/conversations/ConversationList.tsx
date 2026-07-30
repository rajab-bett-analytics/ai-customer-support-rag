import { MoreHorizontal, Trash2 } from "lucide-react";
import {
  useState,
  type Dispatch,
  type SetStateAction,
} from "react";

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

  const [menuOpen, setMenuOpen] =
    useState<number | null>(null);



  async function handleConversationClick(
    id: number,
  ) {

    try {

      const conversation =
        await getConversation(id);


      setConversationId(
        conversation.id,
      );


      setMessages(
        conversation.messages.map(
          (message) => ({
            id: message.id,
            role: message.role,
            content: message.content,
            created_at:
              message.created_at,
            sources: [],
          }),
        ),
      );

    } catch(error) {

      console.error(error);

    }

  }



  function handleDelete(id:number) {

    console.log(
      "Delete conversation:",
      id,
    );

  }



  if(conversations.length === 0){

    return (
      <p
        className="
          py-6
          text-center
          text-sm
          text-slate-500
        "
      >
        No conversations yet.
      </p>
    );

  }



  return (

    <div
      className="
        space-y-1
      "
    >

      {conversations.map(
        (conversation)=> (

        <div
          key={conversation.id}
          className="
            group
            relative
          "
        >

          <button
            onClick={() =>
              void handleConversationClick(
                conversation.id,
              )
            }
            className={`
              flex
              w-full
              items-center
              rounded-lg
              px-3
              py-2.5
              pr-10
              text-left
              text-sm
              transition

              ${
                conversationId === conversation.id

                ? 
                "bg-blue-50 text-blue-700"

                :

                "text-slate-700 hover:bg-slate-100"
              }
            `}
          >

            <span
              className="
                truncate
              "
            >
              {conversation.title}
            </span>

          </button>



          <button
            type="button"
            onClick={(e)=>{

              e.stopPropagation();

              setMenuOpen(
                menuOpen === conversation.id
                ? null
                : conversation.id,
              );

            }}

            className="
              absolute
              right-2
              top-1/2
              -translate-y-1/2
              rounded-md
              p-1
              text-slate-400
              opacity-0
              transition
              group-hover:opacity-100
              hover:bg-slate-200
              hover:text-slate-700
            "
          >

            <MoreHorizontal size={16}/>

          </button>



          {
            menuOpen === conversation.id && (

              <div
                className="
                  absolute
                  right-2
                  top-10
                  z-20
                  w-36
                  rounded-lg
                  border
                  border-slate-200
                  bg-white
                  shadow-lg
                "
              >

                <button
                  onClick={() =>
                    handleDelete(
                      conversation.id,
                    )
                  }

                  className="
                    flex
                    w-full
                    items-center
                    gap-2
                    px-3
                    py-2
                    text-sm
                    text-red-600
                    hover:bg-red-50
                  "
                >

                  <Trash2 size={15}/>

                  Delete

                </button>

              </div>

            )
          }


        </div>

      ))}

    </div>

  );

}


export default ConversationList;