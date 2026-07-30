import { Search } from "lucide-react";

interface DocumentToolbarProps {
  search: string;
  onSearch: (value: string) => void;
  uploading: boolean;
  onUpload: (
    event: React.ChangeEvent<HTMLInputElement>,
  ) => void;
}

function DocumentToolbar({
  search,
  onSearch,
}: DocumentToolbarProps) {
  return (
    <div className="flex items-center justify-between">
      <div className="relative w-full max-w-md">
        <Search
          size={18}
          className="
            absolute
            left-3
            top-1/2
            -translate-y-1/2
            text-slate-400
          "
        />

        <input
          value={search}
          onChange={(event) =>
            onSearch(event.target.value)
          }
          placeholder="Search documents..."
          className="
            h-11
            w-full
            rounded-xl
            border
            border-slate-300
            bg-white
            pl-10
            pr-4
            text-sm
            shadow-sm
            outline-none
            transition

            focus:border-blue-500
            focus:ring-4
            focus:ring-blue-100
          "
        />
      </div>
    </div>
  );
}

export default DocumentToolbar;