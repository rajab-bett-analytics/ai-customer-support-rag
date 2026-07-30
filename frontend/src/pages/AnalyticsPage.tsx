import {
  useEffect,
  useState,
} from "react";

import { getAnalytics } from "../features/analytics/services/analyticsService";
import type { Analytics } from "../features/analytics/types/Analytics";

function AnalyticsPage() {
  const [analytics, setAnalytics] =
    useState<Analytics | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  useEffect(() => {
    async function loadAnalytics() {
      try {
        setLoading(true);

        const data =
          await getAnalytics();

        setAnalytics(data);
      } catch (err) {
        console.error(err);

        setError(
          "Failed to load analytics.",
        );
      } finally {
        setLoading(false);
      }
    }

    loadAnalytics();
  }, []);

  if (loading) {
    return (
      <div className="flex flex-1 items-center justify-center">
        <p className="text-gray-500">
          Loading analytics...
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-1 items-center justify-center">
        <p className="text-red-600">
          {error}
        </p>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">
          Analytics Dashboard
        </h1>

        <p className="mt-2 text-gray-600">
          Monitor AI performance,
          customer interactions, and
          knowledge base statistics.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
        <div className="rounded-lg border bg-white p-6 shadow-sm">
          <h2 className="text-sm text-gray-500">
            Conversations
          </h2>

          <p className="mt-2 text-3xl font-bold">
            {
              analytics?.conversations
            }
          </p>
        </div>

        <div className="rounded-lg border bg-white p-6 shadow-sm">
          <h2 className="text-sm text-gray-500">
            Documents
          </h2>

          <p className="mt-2 text-3xl font-bold">
            {analytics?.documents}
          </p>
        </div>

        <div className="rounded-lg border bg-white p-6 shadow-sm">
          <h2 className="text-sm text-gray-500">
            AI Responses
          </h2>

          <p className="mt-2 text-3xl font-bold">
            {
              analytics?.ai_responses
            }
          </p>
        </div>

        <div className="rounded-lg border bg-white p-6 shadow-sm">
          <h2 className="text-sm text-gray-500">
            Average Response Time
          </h2>

          <p className="mt-2 text-3xl font-bold">
            {
              analytics?.average_response_time
            }
            s
          </p>
        </div>
      </div>

      <div className="mt-8 rounded-lg border bg-white p-6 shadow-sm">
        <h2 className="mb-4 text-xl font-semibold">
          Usage Overview
        </h2>

        <p className="text-gray-500">
          The analytics dashboard is
          now connected to the backend.
          Additional charts and
          performance metrics can be
          added as more analytics data
          becomes available.
        </p>
      </div>
    </div>
  );
}

export default AnalyticsPage;