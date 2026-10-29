import { authHeader } from "@/context/auth-store";

export const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: { ...authHeader(), ...init?.headers },
  });
  if (res.status === 401 && !path.startsWith("/auth")) {
    window.dispatchEvent(new Event("auth:expired"));
    throw new Error("Your session has expired. Please log in again.");
  }
  if (res.status === 429) {
    throw new Error("Too many requests. Please wait a bit and try again.");
  }
  if (!res.ok) throw new Error(`${res.status}: ${await res.text()}`);
  return res.json() as Promise<T>;
}
