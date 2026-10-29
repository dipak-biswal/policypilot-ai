import { useEffect } from "react";
import { Toaster } from "@/components/ui/sonner";
import { toast } from "sonner";
import { LoginPage } from "@/components/auth/LoginPage";
import { useAuth } from "@/context/useAuth";
import Workspace from "./Workspace";

export default function App() {
  const { auth, logout } = useAuth();

  useEffect(() => {
    const onExpired = () => {
      logout();
      toast.error("Session expired", { description: "Please log in again." });
    };
    window.addEventListener("auth:expired", onExpired);
    return () => window.removeEventListener("auth:expired", onExpired);
  }, [logout]);

  if (!auth) {
    return (
      <>
        <Toaster position="top-right" richColors closeButton />
        <LoginPage />
      </>
    );
  }
  // key = email: switching user remounts everything, so no state leaks between users
  return <Workspace key={auth.email} onLogout={logout} />;
}
