function AnalyticsPage() {
  return (
    <div className="flex-1 overflow-y-auto p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">
          Analytics Dashboard
        </h1>

        <p className="mt-2 text-gray-600">
          Monitor AI performance, customer interactions,
          and knowledge base statistics.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
        <div className="rounded-lg border bg-white p-6 shadow-sm">
          <h2 className="text-sm text-gray-500">
            Conversations
          </h2>

          <p className="mt-2 text-3xl font-bold">
            --
          </p>
        </div>

        <div className="rounded-lg border bg-white p-6 shadow-sm">
          <h2 className="text-sm text-gray-500">
            Documents
          </h2>

          <p className="mt-2 text-3xl font-bold">
            --
          </p>
        </div>

        <div className="rounded-lg border bg-white p-6 shadow-sm">
          <h2 className="text-sm text-gray-500">
            AI Responses
          </h2>

          <p className="mt-2 text-3xl font-bold">
            --
          </p>
        </div>

        <div className="rounded-lg border bg-white p-6 shadow-sm">
          <h2 className="text-sm text-gray-500">
            Average Response Time
          </h2>

          <p className="mt-2 text-3xl font-bold">
            --
          </p>
        </div>
      </div>

      <div className="mt-8 rounded-lg border bg-white p-6 shadow-sm">
        <h2 className="mb-4 text-xl font-semibold">
          Usage Overview
        </h2>

        <p className="text-gray-500">
          Analytics charts and performance metrics will
          appear here as the platform collects data.
        </p>
      </div>
    </div>
  );
}

export default AnalyticsPage;