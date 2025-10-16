export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="text-center space-y-6">
        <h1 className="text-4xl font-bold tracking-tight sm:text-6xl">
          AI Job Application Assistant
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl">
          Automate your job search with AI-powered CV generation, personalized cover letters, and intelligent application tracking.
        </p>
        <div className="flex gap-4 justify-center mt-8">
          <a
            href="/signup"
            className="inline-flex items-center justify-center rounded-md bg-primary px-6 py-3 text-sm font-medium text-primary-foreground shadow hover:bg-primary/90 transition-colors"
          >
            Get Started
          </a>
          <a
            href="/login"
            className="inline-flex items-center justify-center rounded-md border border-input bg-background px-6 py-3 text-sm font-medium shadow-sm hover:bg-accent hover:text-accent-foreground transition-colors"
          >
            Sign In
          </a>
        </div>
      </div>
    </main>
  )
}
