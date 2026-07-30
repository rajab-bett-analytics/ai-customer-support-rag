import type { ReactNode } from "react";

interface BadgeProps {
  color?: "green" | "red" | "yellow" | "blue";
  children: ReactNode;
}

export default function Badge({
  color = "blue",
  children,
}: BadgeProps) {
  const styles = {
    blue: "bg-blue-100 text-blue-700",
    green: "bg-green-100 text-green-700",
    yellow: "bg-yellow-100 text-yellow-700",
    red: "bg-red-100 text-red-700",
  };

  return (
    <span
      className={`
        inline-flex
        items-center
        rounded-full
        px-3
        py-1
        text-xs
        font-semibold
        ${styles[color]}
      `}
    >
      {children}
    </span>
  );
}