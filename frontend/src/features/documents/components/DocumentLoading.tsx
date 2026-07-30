function DocumentLoading() {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-16 text-center shadow-sm">
      <div className="mx-auto mb-4 h-10 w-10 animate-spin rounded-full border-4 border-blue-200 border-t-blue-600" />

      <h2 className="text-lg font-semibold text-slate-800">
        Loading documents...
      </h2>

      <p className="mt-2 text-slate-500">
        Please wait while we load your knowledge base.
      </p>
    </div>
  );
}

export default DocumentLoading;