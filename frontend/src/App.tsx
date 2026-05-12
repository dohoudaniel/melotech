import { useState, useEffect } from 'react';
import { Loader2, UserPlus, Sparkles, AlertCircle, Moon, Sun } from 'lucide-react';
import { generateQuestions, type Question } from './api';

const LOADING_MESSAGES = [
  "Analyzing the role requirements...",
  "Identifying relevant interview angles...",
  "Balancing behavioral and situational prompts...",
  "Refining questions for clarity and relevance...",
  "Reviewing for thoughtful candidate evaluation...",
  "Structuring the final questions...",
  "Finalizing your interview questions..."
];

export default function App() {
  const [jobTitle, setJobTitle] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [error, setError] = useState<string | null>(null);
  
  const [isDark, setIsDark] = useState(() => {
    if (typeof window !== 'undefined') {
      return document.documentElement.classList.contains('dark') || 
             window.matchMedia('(prefers-color-scheme: dark)').matches;
    }
    return false;
  });

  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDark]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!jobTitle.trim()) return;

    setIsLoading(true);
    setError(null);
    setQuestions([]);

    try {
      const data = await generateQuestions(jobTitle);
      setQuestions(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white dark:bg-zinc-950 text-zinc-900 dark:text-zinc-100 font-sans selection:bg-mint-100 selection:text-mint-600 dark:selection:bg-mint-900/40 dark:selection:text-mint-400 px-4 sm:px-6 py-12 md:py-24 transition-colors duration-300">
      
      {/* Theme Toggle */}
      <div className="absolute top-4 right-4 sm:top-6 sm:right-6">
        <button
          onClick={() => setIsDark(!isDark)}
          className="p-2 rounded-full text-zinc-500 hover:bg-zinc-100 dark:text-zinc-400 dark:hover:bg-zinc-800 transition-colors focus:outline-none focus:ring-2 focus:ring-mint-accent"
          aria-label="Toggle theme"
        >
          {isDark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
        </button>
      </div>

      <div className="max-w-xl mx-auto w-full flex flex-col gap-8">
        
        {/* Header Section */}
        <header className="flex flex-col items-center text-center space-y-3">
          <div className="inline-flex items-center justify-center p-2 bg-zinc-50 dark:bg-zinc-900 border border-zinc-100 dark:border-zinc-800 rounded-xl mb-2 transition-colors">
            <Sparkles className="w-5 h-5 text-mint-500 dark:text-mint-400" />
          </div>
          <h1 className="text-2xl md:text-3xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-50">
            MeloTech
          </h1>
          <p className="text-zinc-500 dark:text-zinc-400 text-sm md:text-base max-w-sm transition-colors">
            Generate thoughtful interview questions from a job title.
          </p>
        </header>

        {/* Main Content Area */}
        <main className="w-full space-y-8">
          
          {/* Input Form */}
          <section className="bg-white dark:bg-zinc-900/50 border border-zinc-200 dark:border-zinc-800 rounded-2xl p-5 md:p-6 shadow-sm transition-colors">
            <form onSubmit={handleSubmit} className="flex flex-col space-y-4">
              <div className="space-y-2">
                <label htmlFor="jobTitle" className="text-sm font-medium text-zinc-700 dark:text-zinc-300 ml-1 transition-colors">
                  What role are you hiring / applying for?
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                    <UserPlus className="h-4 w-4 text-zinc-400 dark:text-zinc-500" />
                  </div>
                  <input
                    id="jobTitle"
                    type="text"
                    value={jobTitle}
                    onChange={(e) => setJobTitle(e.target.value)}
                    placeholder="Customer Success Manager"
                    className="block w-full pl-10 pr-4 py-3 bg-zinc-50 dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-800 rounded-xl text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 dark:placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-mint-accent focus:border-mint-accent focus:bg-white dark:focus:bg-zinc-900 transition-all disabled:opacity-50 disabled:cursor-not-allowed text-sm md:text-base"
                    disabled={isLoading}
                    autoFocus
                  />
                </div>
              </div>
              
              <button
                type="submit"
                disabled={isLoading || !jobTitle.trim()}
                className="w-fit self-center inline-flex items-center justify-center py-2.5 px-6 bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 rounded-xl text-sm font-medium hover:bg-zinc-800 dark:hover:bg-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-zinc-900 dark:focus:ring-offset-zinc-950 dark:focus:ring-white disabled:bg-zinc-300 disabled:text-zinc-500 dark:disabled:bg-zinc-800 dark:disabled:text-zinc-600 disabled:cursor-not-allowed transition-colors"
              >
                {isLoading ? 'Generating...' : 'Generate Questions'}
              </button>
            </form>
          </section>

          {/* Loading State */}
          {isLoading && <LoadingState />}

          {/* Error State */}
          {error && !isLoading && (
            <div className="bg-red-50 dark:bg-red-950/30 text-red-600 dark:text-red-400 border border-red-100 dark:border-red-900/50 p-4 rounded-xl flex items-start gap-3 text-sm transition-colors">
              <AlertCircle className="w-5 h-5 shrink-0 mt-0.5 text-red-500 dark:text-red-400" />
              <p>{error}</p>
            </div>
          )}

          {/* Results Area */}
          {!isLoading && questions.length > 0 && (
            <section className="space-y-4">
              <div className="flex items-center gap-2 mb-2 ml-1">
                <div className="h-1.5 w-1.5 rounded-full bg-mint-500 dark:bg-mint-400"></div>
                <h2 className="text-sm font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider transition-colors">
                  Generated Questions
                </h2>
              </div>
              
              <div className="flex flex-col gap-3">
                {questions.map((q, idx) => (
                  <div 
                    key={idx} 
                    className="bg-white dark:bg-zinc-900/50 border border-zinc-200 dark:border-zinc-800 rounded-xl p-5 hover:border-mint-accent/50 dark:hover:border-mint-accent/50 transition-colors"
                  >
                    {q.category && (
                      <span className="inline-block px-2.5 py-1 mb-3 text-xs font-medium bg-mint-50 dark:bg-mint-500/10 text-mint-600 dark:text-mint-400 rounded-md transition-colors">
                        {q.category}
                      </span>
                    )}
                    <p className="text-zinc-800 dark:text-zinc-200 text-[15px] leading-relaxed transition-colors">
                      {q.question}
                    </p>
                  </div>
                ))}
              </div>
            </section>
          )}

        </main>
      </div>
    </div>
  );
}

function LoadingState() {
  const [messageIndex, setMessageIndex] = useState(0);

  useEffect(() => {
    // 7 messages over a typical 5-7 second wait. 
    // We'll rotate every 1 second.
    const interval = setInterval(() => {
      setMessageIndex((prev) => (prev + 1) % LOADING_MESSAGES.length);
    }, 1200);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex flex-col items-center justify-center p-8 space-y-4">
      <div className="relative flex items-center justify-center">
        <div className="absolute inset-0 bg-mint-100 dark:bg-mint-900/20 rounded-full blur-xl opacity-50 animate-pulse transition-colors"></div>
        <Loader2 className="w-6 h-6 text-mint-500 dark:text-mint-400 animate-spin relative transition-colors" />
      </div>
      <p className="text-sm font-medium text-zinc-500 dark:text-zinc-400 text-center min-h-[1.5rem] transition-colors duration-300">
        {LOADING_MESSAGES[messageIndex]}
      </p>
    </div>
  );
}
