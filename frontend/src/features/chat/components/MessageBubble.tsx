import { useMemo, useState } from "react";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import type { ChatMessage } from "../types/ChatMessage";
import type { DocumentSource } from "../../documents/types/DocumentSource";

interface MessageBubbleProps {
  message: ChatMessage;

  onSourceSelect: (
    source: DocumentSource,
  ) => void;
}

function MessageBubble({
  message,
  onSourceSelect,
}: MessageBubbleProps) {
  const isUser =
    message.role === "user";

  const [copied, setCopied] =
    useState(false);

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(
        message.content,
      );

      setCopied(true);

      setTimeout(() => {
        setCopied(false);
      }, 2000);
    } catch (error) {
      console.error(error);
    }
  }

  // Remove duplicate sources
  const uniqueSources = useMemo(() => {
    if (!message.sources) {
      return [];
    }

    const map = new Map<
      string,
      DocumentSource
    >();

    message.sources.forEach((source) => {
      const key = `${source.document_id}-${source.page}`;

      if (!map.has(key)) {
        map.set(key, source);
      }
    });

    return [...map.values()];
  }, [message.sources]);

  return (
    <div
      className={`flex w-full ${
        isUser
          ? "justify-end"
          : "justify-start"
      }`}
    >
      <div
        className={`flex max-w-[92%] gap-3 lg:max-w-[78%] ${
          isUser
            ? "flex-row-reverse"
            : "flex-row"
        }`}
      >
        {/* Avatar */}

        <div
          className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-full text-xs font-semibold ${
            isUser
              ? "bg-blue-600 text-white"
              : "bg-slate-900 text-white"
          }`}
        >
          {isUser ? "U" : "AI"}
        </div>

        {/* Bubble */}

        <div
          className={`group rounded-2xl px-5 py-4 shadow-sm ${
            isUser
              ? "bg-blue-600 text-white"
              : "border border-slate-200 bg-white text-slate-900"
          }`}
        >
          {/* Header */}

          <div className="mb-3 flex items-center justify-between">
            <div>
              <p
                className={`text-[11px] font-semibold uppercase ${
                  isUser
                    ? "text-blue-100"
                    : "text-slate-500"
                }`}
              >
                {isUser
                  ? "You"
                  : "AI Assistant"}
              </p>

              {message.created_at && (
                <p
                  className={`text-[11px] ${
                    isUser
                      ? "text-blue-200"
                      : "text-slate-400"
                  }`}
                >
                  {new Date(
                    message.created_at,
                  ).toLocaleTimeString()}
                </p>
              )}
            </div>

            <button
              onClick={handleCopy}
              className={`rounded-md px-2 py-1 text-[11px] opacity-0 transition group-hover:opacity-100 ${
                isUser
                  ? "bg-blue-500 hover:bg-blue-400"
                  : "bg-slate-100 hover:bg-slate-200"
              }`}
            >
              {copied
                ? "Copied"
                : "Copy"}
            </button>
          </div>

          {/* Markdown */}

          <div
            className={`prose prose-sm max-w-none ${
              isUser
                ? "prose-invert"
                : "prose-slate"
            }`}
          >
            <ReactMarkdown
              remarkPlugins={[
                remarkGfm,
              ]}
            >
              {message.content}
            </ReactMarkdown>
          </div>

          {/* References */}

          {!isUser &&
            uniqueSources.length > 0 && (
              <div className="mt-4">
                <div className="mb-2 text-[11px] font-medium text-slate-500">
                  References
                </div>

                <div className="flex flex-wrap gap-2">
                  {uniqueSources.map(
                    (source) => (
                      <button
                        key={`${source.document_id}-${source.page}`}
                        onClick={() =>
                          onSourceSelect(
                            source,
                          )
                        }
                        className="
                          rounded-full
                          border
                          border-slate-200
                          bg-slate-50
                          px-3
                          py-1.5
                          text-xs
                          text-slate-700
                          transition
                          hover:border-blue-300
                          hover:bg-blue-50
                        "
                      >
                        📄{" "}
                        {source.document_name.replace(
                          ".pdf",
                          "",
                        )}
                        {" · "}
                        p.{source.page}
                      </button>
                    ),
                  )}
                </div>
              </div>
            )}
        </div>
      </div>
    </div>
  );
}

export default MessageBubble;