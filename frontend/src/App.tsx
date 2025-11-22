import { useEffect, useMemo, useState } from 'react'
import axios from 'axios'
import './App.css'

type Theme = 'light' | 'dark'

const THEME_KEY = 'simplelinker-theme'

const getInitialTheme = (): Theme => {
  if (typeof window === 'undefined') {
    return 'light'
  }

  const stored = window.localStorage.getItem(THEME_KEY)
  return stored === 'dark' ? 'dark' : 'light'
}

const isValidUrl = (value: string) =>
  /^(http|https):\/\//i.test(value) || /^www\./i.test(value)

function App() {
  const [theme, setTheme] = useState<Theme>(getInitialTheme)
  const [url, setUrl] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [shortSlug, setShortSlug] = useState<string | null>(null)
  const [copied, setCopied] = useState(false)
  const [originalLink, setOriginalLink] = useState('')

  useEffect(() => {
    document.body.classList.remove('light', 'dark')
    document.body.classList.add(theme)
    window.localStorage.setItem(THEME_KEY, theme)
  }, [theme])

  useEffect(() => {
    if (!copied) {
      return
    }

    const timer = setTimeout(() => setCopied(false), 2000)
    return () => clearTimeout(timer)
  }, [copied])

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'))
  }

  const handleShorten = async () => {
    setError('')
    setShortSlug(null)

    if (!url.trim()) {
      setError('Please enter a link.')
      return
    }
    if (!isValidUrl(url.trim())) {
      setError('Link should start with http://, https://, or www.')
      return
    }

    setLoading(true)
    setOriginalLink(url.trim())

    try {
      let linkToSend = url.trim()
      if (linkToSend.startsWith('www.')) {
        linkToSend = `https://${linkToSend}`
      }
      const response = await axios.post('/api/', {
        link: linkToSend,
      })
      setShortSlug(response.data.link_with_slug)
    } catch (error) {
      setError('Something went wrong. Please try again.')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleCopy = async () => {
    if (!shortSlug) {
      return
    }

    try {
      await navigator.clipboard.writeText(shortSlug)
      setCopied(true)
    } catch (err) {
      console.error('Copy error', err)
    }
  }

  const resultVisible = useMemo(() => Boolean(shortSlug), [shortSlug])

  return (
    <div className="min-h-screen w-full flex flex-col items-center justify-center p-4">
      <button
        id="themeToggle"
        aria-label="Toggle theme"
        onClick={toggleTheme}
        className="absolute top-4 right-4 p-2 rounded-full bg-gray-200 dark:bg-gray-800 text-gray-700 dark:text-gray-300 shadow-md hover:scale-105 transition-transform duration-200"
      >
        {theme === 'light' ? (
          <svg
            className="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 3v1m0 16v1m9-9h1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
            />
          </svg>
        ) : (
          <svg
            className="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
            />
          </svg>
        )}
      </button>

      <div className="max-w-xl w-full p-8 md:p-10 main-card rounded-2xl text-center">
        <div className="flex items-center justify-center mb-4">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-10 w-10 logo-icon"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"
            />
          </svg>
          <span className="text-3xl font-extrabold ml-2 logo-text tracking-tight">
            SimpleLinker
          </span>
        </div>

        <h1 className="text-2xl md:text-3xl font-extrabold mb-3 text-main leading-tight">
          Shorten Any Link
        </h1>
        <p className="text-base font-medium text-primary-accent mb-8 max-w-sm mx-auto">
          Free. No Ads. Always Available.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 w-full">
          <input
            type="url"
            id="urlInput"
            placeholder="Paste your link just here..."
            className="flex-grow p-4 border-2 input-field rounded-xl focus:ring-4 focus-ring-primary outline-none placeholder:text-subtle text-base transition-all duration-200 shadow-inner"
            value={url}
            disabled={loading}
            onChange={(e) => setUrl(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                handleShorten()
              }
            }}
          />
          <button
            onClick={handleShorten}
            id="shortenBtn"
            disabled={loading}
            className="btn-primary-gradient font-bold py-4 px-8 rounded-xl flex items-center justify-center min-w-[150px] uppercase tracking-wider text-white transition-transform hover:scale-[1.02] active:scale-[0.98] disabled:opacity-70"
          >
            <span style={{ display: loading ? 'none' : 'inline' }}>Shorten</span>
            <div
              className="loader"
              style={{ display: loading ? 'block' : 'none' }}
            />
          </button>
        </div>

        {error && (
          <div className="mt-4 text-error text-sm font-semibold animate-pulse">
            {error}
          </div>
        )}

        {resultVisible && shortSlug && (
          <div className="mt-8 p-5 result-box border rounded-xl text-left fade-in shadow-lg">
            <p className="text-sm text-primary-accent uppercase tracking-wider font-bold mb-2">
              Your Short Link:
            </p>
            <div className="flex items-center justify-between">
              <a
                id="shortUrlText"
                href={originalLink}
                target="_blank"
                rel="noopener noreferrer"
                className="result-link-text font-extrabold text-xl md:text-2xl truncate max-w-[calc(100%-60px)] transition-colors duration-150"
              >
                {shortSlug}
              </a>
              <button
                onClick={handleCopy}
                className="ml-auto copy-btn p-2 rounded-lg relative group"
                title="Copy"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
                  />
                </svg>
                <span
                  className={`copy-tooltip absolute -top-10 left-1/2 -translate-x-1/2 bg-gray-800 text-white text-xs py-1 px-2 rounded pointer-events-none whitespace-nowrap ${
                    copied ? 'visible' : ''
                  }`}
                >
                  Copied!
                </span>
              </button>
            </div>
          </div>
        )}
      </div>

      <div className="mt-16 text-center flex flex-col items-center space-y-4">
        <a
          href="https://t.me/SimpleLinkerBot"
          target="_blank"
          rel="noopener noreferrer"
          className="telegram-link p-2 -m-2 rounded-full flex items-center group hover:scale-[1.05] transition-transform duration-200"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6 inline-block telegram-icon transition-colors duration-150"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <path d="M2.01 21L23 12 2.01 3v7l15 2-15 2z" />
          </svg>
          <span className="ml-2 align-middle text-base font-medium text-secondary group-hover:text-primary-accent transition-colors duration-150">
            SimpleLinker Bot
          </span>
        </a>

        <a
          href="https://github.com/DmDogger/SimpleLinker"
          target="_blank"
          rel="noopener noreferrer"
          className="github-link p-2 -m-2 rounded-full flex items-center group hover:scale-[1.05] transition-transform duration-200"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6 inline-block github-icon transition-colors duration-150"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              fillRule="evenodd"
              clipRule="evenodd"
              d="M12 0C5.373 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.6.11.82-.26.82-.577 0-.285-.01-1.04-.015-2.04-3.338.725-4.04-1.61-4.04-1.61-.546-1.385-1.332-1.75-1.332-1.75-1.087-.745.083-.73.083-.73 1.205.085 1.838 1.238 1.838 1.238 1.07 1.835 2.809 1.305 3.493.998.108-.777.418-1.305.762-1.605-2.665-.3-5.466-1.33-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.125-.3-.535-1.527.117-3.185 0 0 1-.32 3.3.125 1-.277 2.075-.415 3.15-.415.75 0 1.48.138 2.19.415 2.296-.445 3.296-.125 3.296-.125.65 1.658.24 2.885.118 3.185.77.84 1.235 1.91 1.235 3.22 0 4.61-2.8 5.63-5.476 5.92.42.36.81 1.096.81 2.21 0 1.6-.015 2.896-.015 3.29 0 .32.22.69.825.57C20.565 21.8 24 17.3 24 12c0-6.627-5.373-12-12-12z"
            />
          </svg>
          <span className="ml-2 align-middle text-base font-medium text-secondary group-hover:text-primary-accent transition-colors duration-150">
            SimpleLinker on GitHub
          </span>
        </a>
      </div>
    </div>
  )
}

export default App
