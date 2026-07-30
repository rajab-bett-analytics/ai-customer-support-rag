import { UserCircle2 } from "lucide-react";

import { useLayout } from "../useLayout";

export default function SidebarFooter() {
  const { sidebarCollapsed } = useLayout();

  const user = JSON.parse(
    localStorage.getItem("user") || "null",
  );

  return (
    <footer className="border-t border-slate-200 p-4">
      <div className="flex items-center gap-3">
        <UserCircle2
          size={40}
          className="shrink-0 text-slate-500"
        />

        {!sidebarCollapsed && (
          <div className="min-w-0">
            <p className="truncate font-medium text-slate-800">
              {user?.fullName || "User"}
            </p>

            <p className="truncate text-xs text-slate-500">
              {user?.email || "Signed in"}
            </p>
          </div>
        )}
      </div>
    </footer>
  );
}