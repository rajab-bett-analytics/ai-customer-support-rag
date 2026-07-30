import { FolderOpen } from "lucide-react";

function DocumentEmptyState() {
  return (
    <div className="rounded-xl border-2 border-dashed border-slate-300 bg-white py-20 text-center">
      <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-slate-100">
        <FolderOpen
          size={30}
          className="text-slate-500"
        />
      </div>

      <h2 className="mt-6 text-2xl font-semibold text-slate-900">
        No documents found
      </h2>

      <p className="mt-2 text-slate-500">
        Upload your first PDF or try another search term.
      </p>
    </div>
  );
}

export default DocumentEmptyState;