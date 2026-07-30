import type { ReactNode } from "react";

import Header from "./Header";
import Sidebar from "./Sidebar";
import Workspace from "./Workspace";

interface Props {
  children: ReactNode;
}

export default function AppShell({
  children,
}: Props) {
  return (
    <div
      className="
        flex
        h-screen
        w-full
        bg-slate-100
      "
    >
      <Sidebar />

      <div
        className="
          flex
          min-w-0
          flex-1
          flex-col
        "
      >
        <Header />

        <main
          className="
            flex
            flex-1
            min-h-0
            min-w-0
            bg-slate-100
          "
        >
          <Workspace>
            <div
              className="
                h-full
                w-full
                overflow-y-auto
                overflow-x-hidden
                p-3
                lg:p-4
                xl:p-5
                2xl:px-6
                2xl:py-5
              "
            >
              {children}
            </div>
          </Workspace>
        </main>
      </div>
    </div>
  );
}