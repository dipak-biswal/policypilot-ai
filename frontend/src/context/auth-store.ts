import { createContext } from "react";

export const AUTH_KEY = "pp_auth";

export type Auth = { token: string; email: string };
export type AuthCtx = {
  auth: Auth | null;
  login: (
    email: string,
    password: string,
    mode: "login" | "register",
  ) => Promise<void>;
  logout: () => void;
};

export const AuthContext = createContext<AuthCtx | null>(null);

/** Use in api/* files that aren't React components */
export function authHeader(): Record<string, string> {
  const raw = localStorage.getItem(AUTH_KEY);
  return raw ? { Authorization: `Bearer ${JSON.parse(raw).token}` } : {};
}
