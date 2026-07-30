import { useRef } from "react";
import { Upload } from "lucide-react";

interface DocumentDropzoneProps {
  uploading: boolean;
  onUpload: (
    event: React.ChangeEvent<HTMLInputElement>,
  ) => void;
}

function DocumentDropzone({
  uploading,
  onUpload,
}: DocumentDropzoneProps) {
  const inputRef =
    useRef<HTMLInputElement | null>(null);

  return (
    <>
      <button
        type="button"
        disabled={uploading}
        onClick={() =>
          inputRef.current?.click()
        }
        className="
          inline-flex
          items-center
          gap-2
          rounded-xl
          border
          border-slate-300
          bg-white
          px-4
          py-2.5
          text-sm
          font-medium
          text-slate-700
          shadow-sm
          transition
          hover:border-blue-500
          hover:bg-blue-50
          hover:text-blue-600
          disabled:cursor-not-allowed
          disabled:opacity-60
        "
      >
        <Upload size={18} />

        {uploading
          ? "Uploading..."
          : "Upload PDF"}
      </button>

      <input
        ref={inputRef}
        type="file"
        hidden
        accept=".pdf"
        disabled={uploading}
        onChange={onUpload}
      />
    </>
  );
}

export default DocumentDropzone;