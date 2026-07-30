import DocumentDropzone from "./DocumentDropzone";

interface DocumentUploaderProps {
  uploading: boolean;
  onUpload: (
    event: React.ChangeEvent<HTMLInputElement>,
  ) => void;
}

function DocumentUploader({
  uploading,
  onUpload,
}: DocumentUploaderProps) {
  return (
    <div className="mx-auto w-full max-w-2xl space-y-4">
      <DocumentDropzone
        uploading={uploading}
        onUpload={onUpload}
      />

      {uploading && (
        <div
          className="
            rounded-2xl
            border
            border-blue-200
            bg-blue-50
            px-5
            py-4
            shadow-sm
          "
        >
          <div className="flex items-start gap-3">
            <div className="mt-0.5 text-lg">
              📄
            </div>

            <div>
              <p className="font-semibold text-blue-900">
                Processing document...
              </p>

              <p className="mt-1 text-sm text-blue-700">
                Extracting text, splitting
                into chunks, and generating
                vector embeddings. This may
                take a few moments.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default DocumentUploader;