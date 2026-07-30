import type { ButtonHTMLAttributes } from "react";

interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "danger";
}

export default function Button({
  variant = "primary",
  className = "",
  children,
  ...props
}: ButtonProps) {
  const styles = {
    primary:
      "bg-blue-600 text-white hover:bg-blue-700",

    secondary:
      "border border-slate-300 bg-white hover:bg-slate-50",

    danger:
      "bg-red-600 text-white hover:bg-red-700",
  };

  return (
    <button
      {...props}
      className={`
        inline-flex
        items-center
        justify-center
        gap-2
        rounded-xl
        px-4
        py-2.5
        text-sm
        font-medium
        transition
        ${styles[variant]}
        ${className}
      `}
    >
      {children}
    </button>
  );
}