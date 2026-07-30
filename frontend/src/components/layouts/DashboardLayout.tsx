import { Outlet } from "react-router-dom";

import {
  AppShell,
  LayoutProvider,
} from "../layouts/AppShell";

export default function DashboardLayout() {
  return (
    <LayoutProvider>
      <AppShell>
        <Outlet />
      </AppShell>
    </LayoutProvider>
  );
}