import type { ElementType } from "react";
import { NavLink } from "react-router-dom";

import { useLayout } from "../useLayout";

interface Props {
  label: string;
  path: string;
  icon: ElementType;
}

export default function NavigationItem({
  label,
  path,
  icon: Icon,
}: Props) {
  const { sidebarCollapsed } = useLayout();

  return (
    <NavLink
      to={path}
      end={path === "/"}
      className={({ isActive }) =>
        `
          group
          flex
          items-center
          gap-3

          rounded-xl

          px-3
          py-3

          transition-all
          duration-200

          ${
            isActive
              ? "bg-blue-600 text-white shadow-sm"
              : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
          }
        `
      }
    >
      <Icon
        size={20}
        className="shrink-0"
      />

      {!sidebarCollapsed && (
        <span className="truncate font-medium">
          {label}
        </span>
      )}
    </NavLink>
  );
}