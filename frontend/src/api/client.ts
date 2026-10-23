export const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, init);
  if (!res.ok) throw new Error(`${res.status}: ${await res.text()}`);
  if (res.status === 429) {
    throw new Error("Too many requests. Please wait a bit and try again.");
  }
  return res.json() as Promise<T>;
}
