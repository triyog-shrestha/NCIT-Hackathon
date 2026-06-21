import { useCallback, useEffect, useState } from 'react'
import CharacterGrid from './components/CharacterGrid.jsx'
import ChatScreen from './components/ChatScreen.jsx'
import { fetchCharacters } from './api.js'
import './app.css'

export default function App() {
  const [characters, setCharacters] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [activeCharacter, setActiveCharacter] = useState(null)

  const loadCharacters = useCallback(() => {
    setLoading(true)
    setError(null)
    fetchCharacters()
      .then((list) => setCharacters(list))
      .catch((err) => setError(err.message || 'Unknown error'))
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    loadCharacters()
  }, [loadCharacters])

  const active = activeCharacter
    ? characters.find((c) => c.id === activeCharacter)
    : null

  return (
    <div className="app-shell">
      {active ? (
        <ChatScreen character={active} onBack={() => setActiveCharacter(null)} />
      ) : (
        <CharacterGrid
          characters={characters}
          loading={loading}
          error={error}
          onSelect={setActiveCharacter}
          onRetry={loadCharacters}
        />
      )}
    </div>
  )
}
