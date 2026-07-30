interface LoadingStateProps {
  message?: string;
}

export default function LoadingState({
  message = "Loading...",
}: LoadingStateProps) {
  return (
    <div className="flex h-64 items-center justify-center rounded-2xl border border-slate-200 bg-white">
      <p className="text-slate-500">
        {message}
      </p>
    </div>
  );
}