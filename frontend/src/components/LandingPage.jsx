import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'

export default function LandingPage() {
  const { isAuthenticated } = useAuth()

  return (
    <div className="landing-page">
      <header className="landing-nav">
        <span className="landing-nav__brand">mindspace</span>
        <div className="landing-nav__actions">
          {isAuthenticated ? (
            <Link className="btn-pill" to="/characters">
              Open app
            </Link>
          ) : (
            <>
              <Link className="landing-nav__link" to="/login">
                Sign in
              </Link>
              <Link className="btn-pill" to="/login">
                Get started
              </Link>
            </>
          )}
        </div>
      </header>

      <main className="landing-hero">
        <p className="eyebrow">a quiet place to talk</p>
        <h1 className="landing-hero__title">
          Choose a voice.
          <br />
          Start a conversation.
        </h1>
        <p className="landing-hero__subtitle">
          Mindspace pairs you with AI characters for open-ended chats — playful, reflective, or
          just someone to listen. Pick who you want to talk to and say hello.
        </p>
        <div className="landing-hero__cta">
          <Link className="btn-pill btn-pill--accent" to={isAuthenticated ? '/characters' : '/login'}>
            {isAuthenticated ? 'Choose a character' : 'Get started'}
          </Link>
          {!isAuthenticated && (
            <Link className="landing-hero__secondary" to="/login">
              Already have an account? Sign in
            </Link>
          )}
        </div>
      </main>

      <section className="landing-features" aria-label="Features">
        <article className="landing-feature">
          <h2>Pick your companion</h2>
          <p>Browse characters with distinct personalities — from cheerful icons to calm listeners.</p>
        </article>
        <article className="landing-feature">
          <h2>Chat in the moment</h2>
          <p>Send a message and get a reply powered by a local language model through Ollama.</p>
        </article>
        <article className="landing-feature">
          <h2>Stay grounded</h2>
          <p>Every chat includes a clear reminder: you are talking with AI, not a real person.</p>
        </article>
      </section>

      <footer className="landing-footer">
        <p>Mindspace — Hackathon demo</p>
      </footer>
    </div>
  )
}
