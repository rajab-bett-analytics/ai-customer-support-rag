import {
  FileText,
  CheckCircle2,
  FileStack,
  Brain,
} from "lucide-react";

import type { Document } from "../documentService";

interface DocumentStatsProps {
  documents: Document[];
}

function DocumentStats({
  documents,
}: DocumentStatsProps) {
  const totalDocuments = documents.length;

  const processedDocuments = documents.filter(
    (document) => document.status === "processed",
  ).length;

  const totalPages = documents.reduce(
    (sum, document) => sum + (document.page_count ?? 0),
    0,
  );

  const totalEmbeddings = documents.reduce(
    (sum, document) => sum + (document.embedding_count ?? 0),
    0,
  );

  const stats = [
    {
      label: "Documents",
      value: totalDocuments,
      icon: FileText,
      color: "text-blue-600",
    },
    {
      label: "Processed",
      value: processedDocuments,
      icon: CheckCircle2,
      color: "text-green-600",
    },
    {
      label: "Pages",
      value: totalPages,
      icon: FileStack,
      color: "text-violet-600",
    },
    {
      label: "Embeddings",
      value: totalEmbeddings,
      icon: Brain,
      color: "text-pink-600",
    },
  ];

  return (
    <div
      className="
        flex
        flex-wrap
        items-center
        gap-6
        rounded-xl
        border
        border-slate-200
        bg-white
        px-5
        py-3
        shadow-sm
      "
    >
      {stats.map((stat, index) => {
        const Icon = stat.icon;

        return (
          <div
            key={stat.label}
            className="flex items-center gap-2"
          >
            <Icon
              size={18}
              className={stat.color}
            />

            <span className="text-sm text-slate-500">
              {stat.label}
            </span>

            <span className="text-lg font-semibold text-slate-900">
              {stat.value}
            </span>

            {index < stats.length - 1 && (
              <span className="ml-4 text-slate-300">
                •
              </span>
            )}
          </div>
        );
      })}
    </div>
  );
}

export default DocumentStats;