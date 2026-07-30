import type { ReactNode } from "react";

interface Props {
  children: ReactNode;
}

export default function Workspace({
  children,
}: Props) {
  return (
    <main
      className="
        flex
        h-full
        w-full
        flex-1
        min-h-0
        min-w-0
        overflow-y-auto
        overflow-x-hidden
        bg-slate-50
      "
    >
      {children}
    </main>
  );
}