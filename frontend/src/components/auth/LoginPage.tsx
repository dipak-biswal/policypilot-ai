import { useState, type FormEvent } from "react";
import { Eye, EyeOff, FileText, Sparkles, Zap, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useAuth } from "@/context/useAuth";

const FEATURES = [
  { icon: FileText, text: "Chat with any PDF — insurance, contracts, resumes" },
  { icon: Sparkles, text: "Cited answers, summaries and generative UI reports" },
  { icon: Zap, text: "Live agent steps: search, calculate, compare dates" },
];

export function LoginPage() {
  const { login } = useAuth();
  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setBusy(true);
    try {
      await login(email, password, mode);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="flex min-h-screen">
      {/* Brand panel — desktop only */}
      <aside className="hidden w-1/2 flex-col justify-between bg-slate-900 p-10 text-white lg:flex">
        <div>
          <p className="text-sm font-medium tracking-wide text-slate-300">PolicyPilot AI</p>
          <h1 className="mt-6 text-4xl font-semibold leading-tight tracking-tight">
            Your documents,
            <br />
            answered with citations.
          </h1>
          <p className="mt-4 max-w-md text-slate-300">
            Upload a PDF, ask anything, and get grounded answers with page links,
            AI reports and live agent steps.
          </p>
        </div>
        <ul className="space-y-4">
          {FEATURES.map(({ icon: Icon, text }) => (
            <li key={text} className="flex items-start gap-3 text-slate-100">
              <span className="mt-0.5 rounded-md bg-slate-700/60 p-1.5">
                <Icon className="h-4 w-4" />
              </span>
              <span className="text-sm leading-relaxed">{text}</span>
            </li>
          ))}
        </ul>
      </aside>

      {/* Form */}
      <main className="flex flex-1 items-center justify-center bg-background p-6">
        <div className="w-full max-w-sm space-y-6">
          <div className="lg:hidden">
            <p className="text-sm font-medium text-slate-700">PolicyPilot AI</p>
            <h1 className="mt-1 text-2xl font-semibold tracking-tight">Welcome back</h1>
          </div>

          <div className="hidden lg:block">
            <h2 className="text-2xl font-semibold tracking-tight">
              {mode === "login" ? "Log in" : "Create your account"}
            </h2>
            <p className="mt-1 text-sm text-muted-foreground">
              {mode === "login"
                ? "Enter your email and password to continue"
                : "A few details and you're ready to chat with your docs"}
            </p>
          </div>

          <Tabs
            value={mode}
            onValueChange={(v) => {
              setMode(v as "login" | "register");
              setError(null);
            }}
          >
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="login">Log in</TabsTrigger>
              <TabsTrigger value="register">Sign up</TabsTrigger>
            </TabsList>
          </Tabs>

          <form onSubmit={onSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                autoComplete="email"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <div className="relative">
                <Input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  placeholder="Min 8 characters"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  minLength={8}
                  autoComplete={mode === "login" ? "current-password" : "new-password"}
                  className="pr-10"
                />
                <button
                  type="button"
                  aria-label={showPassword ? "Hide password" : "Show password"}
                  className="absolute right-2 top-1/2 -translate-y-1/2 rounded p-1 text-muted-foreground hover:text-foreground"
                  onClick={() => setShowPassword((s) => !s)}
                >
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </div>

            {error && (
              <Alert variant="destructive">
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            <Button
              type="submit"
              className="w-full bg-slate-900 hover:bg-slate-800"
              disabled={busy}
            >
              {busy && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              {busy ? "Please wait..." : mode === "login" ? "Log in" : "Create account"}
            </Button>
          </form>
        </div>
      </main>
    </div>
  );
}