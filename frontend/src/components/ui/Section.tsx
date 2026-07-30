import type { ReactNode } from "react";

interface SectionProps {
  children: ReactNode;
  className?: string;
}

export default function Section({
  children,
  className = "",
}: SectionProps) {
  return (
    <section
      className={`
        flex
        min-h-0
        flex-col
        space-y-6
        ${className}
      `}
    >
      {children}
    </section>
  );
}