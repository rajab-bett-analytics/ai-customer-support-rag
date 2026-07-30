import SidebarFooter from "./SidebarFooter";
import SidebarHeader from "./SidebarHeader";
import SidebarNavigation from "./SidebarNavigation";

import { useLayout } from "../useLayout";

export default function Sidebar() {
  const { sidebarCollapsed } = useLayout();

  return (
    <aside
      className={`
        flex
        h-screen
        shrink-0
        flex-col
        border-r
        border-slate-200
        bg-white
        transition-all
        duration-300
        ${
          sidebarCollapsed
            ? "w-16"
            : "w-52 xl:w-60"
        }
      `}
    >
      <SidebarHeader />

      <SidebarNavigation />

      <SidebarFooter />
    </aside>
  );
}