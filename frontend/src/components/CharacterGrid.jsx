import { CHARACTER_ART } from '../characterArt.js'

function CharacterCard({ character, onSelect }) {
  const art = CHARACTER_ART[character.id] || {}
  const initial = (character.name?.[0] || character.id[0] || '?').toUpperCase()

  return (
    <button className="char-card" onClick={() => onSelect(character.id)}>
      <div
        className={`char-card__banner ${art.image ? '' : 'char-card__banner--flat'}`}
        style={art.image ? { backgroundImage: `url('${art.image}')` } : undefined}
      />
      <div className="char-card__body">
        <div className="char-card__avatar">
          {art.avatar || art.image ? (
            <img src={art.avatar || art.image} alt="" />
          ) : (
            initial
          )}
        </div>
        <p className="char-card__name">{character.name}</p>
        <p className="char-card__tagline">
          {art.tagline || character.tagline || 'Tap to start a conversation'}
        </p>
        <span className="char-card__cta">Start chat →</span>
      </div>
    </button>
  )
}

function ComingSoonCard() {
  return (
    <div className="char-card char-card--placeholder">
      <div className="char-card__placeholder-inner">
        <div className="char-card__placeholder-avatar">?</div>
        <p className="char-card__placeholder-label">Coming soon…</p>
      </div>
    </div>
  )
}

export default function CharacterGrid({ characters, loading, error, onSelect, onRetry }) {
  return (
    <div className="grid-screen">
      <p className="eyebrow">who do you want to talk to today?</p>
      <h1 className="grid-screen__title">Choose a voice</h1>

      {loading && (
        <div className="grid-screen__status">
          <div className="spinner" aria-hidden="true" />
          <span>Loading characters…</span>
        </div>
      )}

      {error && !loading && (
        <div className="grid-screen__status grid-screen__status--error">
          <p>Couldn't reach the character API: {error}</p>
          <button className="btn-pill" onClick={onRetry}>
            Try again
          </button>
        </div>
      )}

      {!loading && !error && characters.length === 0 && (
        <div className="grid-screen__status">
          <p>No characters defined yet. Add some to characters.py.</p>
        </div>
      )}

      {!loading && !error && characters.length > 0 && (
        <div className="char-grid">
          {characters.map((c) => (
            <CharacterCard key={c.id} character={c} onSelect={onSelect} />
          ))}
          <ComingSoonCard />
        </div>
      )}
    </div>
  )
}
