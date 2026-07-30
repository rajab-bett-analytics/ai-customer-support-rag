import type { ReactNode } from "react";

interface CardHeaderProps {
  title: string;
  description?: string;
  action?: ReactNode;
}

export default function CardHeader({
  title,
  description,
  action,
}: CardHeaderProps) {
  return (
    <div className="flex items-start justify-between border-b border-slate-100 p-6">
      <div>
        <h2 className="text-lg font-semibold text-slate-900">
          {title}
        </h2>

        {description && (
          <p className="mt-1 text-sm text-slate-500">
            {description}
          </p>
        )}
      </div>

      {action}
    </div>
  );
}