import { useState, type ReactNode } from "react";
import { AUTH_KEY, AuthContext, type Auth } from "./auth-store";
import { API_URL } from "@/api/client";

export function AuthProvider({ children }: { children: ReactNode }) {
  const [auth, setAuth] = useState<Auth | null>(() => {
    const raw = localStorage.getItem(AUTH_KEY);
    return raw ? JSON.parse(raw) : null;
  });

  async function login(
    email: string,
    password: string,
    mode: "login" | "register",
  ) {
    const res = await fetch(`${API_URL}/auth/${mode}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    const data = await res.json();
    if (!res.ok) {
      const msg =
        typeof data.detail === "string"
          ? data.detail
          : "Password must be at least 8 characters";
      throw new Error(msg);
    }
    const next = { token: data.access_token, email: data.email };
    localStorage.setItem(AUTH_KEY, JSON.stringify(next));
    setAuth(next);
  }

  function logout() {
    localStorage.removeItem(AUTH_KEY);
    setAuth(null);
  }

  return (
    <AuthContext.Provider value={{ auth, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
