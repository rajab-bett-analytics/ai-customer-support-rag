import type { ReactNode } from "react";

interface PageHeaderProps {
  title: string;
  description?: string;
  action?: ReactNode;
}

function PageHeader({
  title,
  description,
  action,
}: PageHeaderProps) {
  return (
    <header
      className="
        flex
        flex-col
        gap-5

        lg:flex-row
        lg:items-start
        lg:justify-between
      "
    >
      {/* Title */}

      <div className="min-w-0">
        <h1
          className="
            text-3xl
            font-bold
            tracking-tight
            text-slate-900
          "
        >
          {title}
        </h1>

        {description && (
          <p
            className="
              mt-2
              max-w-3xl
              text-sm
              leading-6
              text-slate-500
            "
          >
            {description}
          </p>
        )}
      </div>

      {/* Search / Actions */}

      {action && (
        <div
          className="
            flex
            w-full
            flex-wrap
            items-center
            justify-end
            gap-3

            lg:w-auto
            lg:flex-nowrap
            lg:self-center
          "
        >
          {action}
        </div>
      )}
    </header>
  );
}

export default PageHeader;