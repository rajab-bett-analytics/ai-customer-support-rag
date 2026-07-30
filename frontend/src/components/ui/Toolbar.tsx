import type { ReactNode } from "react";

interface ToolbarProps {
  left?: ReactNode;
  right?: ReactNode;
}

function Toolbar({
  left,
  right,
}: ToolbarProps) {
  return (
    <div
      className="
        flex
        flex-col
        gap-4
        md:flex-row
        md:items-center
        md:justify-between
      "
    >
      <div className="min-w-0 flex-1">
        {left}
      </div>

      {right && (
        <div
          className="
            flex
            flex-shrink-0
            items-center
            gap-3
          "
        >
          {right}
        </div>
      )}
    </div>
  );
}

export default Toolbar;