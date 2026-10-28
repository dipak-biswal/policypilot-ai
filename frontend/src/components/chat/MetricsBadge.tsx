import type { Metrics } from "@/types";

export function MetricsBadge({ metrics }: { metrics: Metrics }) {
  const secs = (metrics.latency_ms / 1000).toFixed(1);
  const tokens = metrics.input_tokens + metrics.output_tokens;
  return (
    <div className="mt-2 flex gap-3 text-xs text-gray-400 dark:text-gray-500">
      <span>⏱ {secs}s</span>
      <span>🔤 {tokens.toLocaleString()} tokens</span>
      <span>💲 {metrics.cost_usd.toFixed(4)}</span>
    </div>
  );
}
