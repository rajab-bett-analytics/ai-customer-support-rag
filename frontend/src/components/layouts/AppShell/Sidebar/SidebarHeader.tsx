import { ChevronLeft, ChevronRight, Bot } from "lucide-react";

import { useLayout } from "../useLayout";

export default function SidebarHeader() {
  const {
    sidebarCollapsed,
    setSidebarCollapsed,
  } = useLayout();

  return (
    <header className="flex h-16 items-center justify-between border-b border-slate-200 px-4">
      <div className="flex items-center gap-3 overflow-hidden">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600 text-white shadow-sm">
          <Bot size={20} />
        </div>

        {!sidebarCollapsed && (
          <div className="min-w-0">
            <h1 className="truncate text-sm font-semibold text-slate-900">
              AI Support
            </h1>

            <p className="truncate text-xs text-slate-500">
              Customer Platform
            </p>
          </div>
        )}
      </div>

      <button
        type="button"
        onClick={() =>
          setSidebarCollapsed(
            !sidebarCollapsed,
          )
        }
        className="rounded-lg p-2 text-slate-500 transition hover:bg-slate-100 hover:text-slate-800"
      >
        {sidebarCollapsed ? (
          <ChevronRight size={18} />
        ) : (
          <ChevronLeft size={18} />
        )}
      </button>
    </header>
  );
}