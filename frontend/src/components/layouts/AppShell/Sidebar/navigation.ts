import type { LucideIcon } from "lucide-react";

import {
  BarChart3,
  FileText,
  MessageSquare,
  Settings,
  User,
} from "lucide-react";

export interface NavigationItem {
  label: string;
  path: string;
  icon: LucideIcon;
}

export const sidebarNavigation: NavigationItem[] = [
  {
    label: "Chat",
    path: "/dashboard",
    icon: MessageSquare,
  },
  {
    label: "Documents",
    path: "/documents",
    icon: FileText,
  },
  {
    label: "Analytics",
    path: "/analytics",
    icon: BarChart3,
  },
  {
    label: "Profile",
    path: "/profile",
    icon: User,
  },
  {
    label: "Settings",
    path: "/settings",
    icon: Settings,
  },
];