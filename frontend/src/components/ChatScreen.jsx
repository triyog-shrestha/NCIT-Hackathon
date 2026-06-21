import { useEffect, useRef, useState } from 'react'
import { CHARACTER_ART } from '../characterArt.js'
import { sendChatMessage } from '../api.js'

function MessageBubble({ role, content, avatarSrc, avatarInitial }) {
  const isUser = role === 'user'
  return (
    <div className={`msg-row ${isUser ? 'msg-row--user' : 'msg-row--assistant'}`}>
      {!isUser && (
        <div className="msg-avatar">
          {avatarSrc ? <img src={avatarSrc} alt="" /> : avatarInitial}
        </div>
      )}
      <div className={`msg-bubble ${isUser ? 'msg-bubble--user' : 'msg-bubble--assistant'}`}>
        {content}
      </div>
    </div>
  )
}

function ThinkingIndicator({ avatarSrc, avatarInitial }) {
  // A quiet "thinking" pulse — no artificial delay, no fake character-by-
  // character typing theater. It just reflects that a real request is in
  // flight, and disappears the moment the reply arrives.
  return (
    <div className="msg-row msg-row--assistant">
      <div className="msg-avatar msg-avatar--thinking">
        {avatarSrc ? <img src={avatarSrc} alt="" /> : avatarInitial}
      </div>
      <div className="msg-bubble msg-bubble--assistant msg-bubble--thinking">
        <span className="dot" />
        <span className="dot" />
        <span className="dot" />
      </div>
    </div>
  )
}

export default function ChatScreen({ character, onBack }) {
  const art = CHARACTER_ART[character.id] || {}
  const avatarSrc = art.avatar || art.image
  const avatarInitial = (character.name?.[0] || '?').toUpperCase()

  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [sending, setSending] = useState(false)
  const [error, setError] = useState(null)
  const scrollRef = useRef(null)

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' })
  }, [messages, sending])

  async function handleSend(e) {
    e.preventDefault()
    const text = input.trim()
    if (!text || sending) return

    setMessages((prev) => [...prev, { role: 'user', content: text }])
    setInput('')
    setSending(true)
    setError(null)

    try {
      const data = await sendChatMessage(character.id, text)
      setMessages((prev) => [...prev, { role: 'assistant', content: data.reply }])
    } catch (err) {
      setError(err.message || 'Something went wrong reaching the model.')
    } finally {
      setSending(false)
    }
  }

  return (
    <div className="chat-screen">
      <header className="chat-header">
        <button className="btn-back" onClick={onBack} aria-label="Back to character list">
          ← back
        </button>
        <h2 className="chat-header__name">{character.name}</h2>
      </header>

      <p className="ai-disclosure">
        You're chatting with an AI character, not a real person. It can't remember you between
        sessions and isn't a substitute for a friend, therapist, or professional support.
      </p>

      <div className="chat-log" ref={scrollRef}>
        {messages.length === 0 && (
          <div className="chat-log__empty">
            <p>Say hello to start the conversation.</p>
          </div>
        )}
        {messages.map((m, i) => (
          <MessageBubble
            key={i}
            role={m.role}
            content={m.content}
            avatarSrc={avatarSrc}
            avatarInitial={avatarInitial}
          />
        ))}
        {sending && <ThinkingIndicator avatarSrc={avatarSrc} avatarInitial={avatarInitial} />}
        {error && (
          <div className="chat-error">
            Couldn't reach the model: {error}
            <div className="chat-error__hint">
              Check that Ollama is running and the model has been pulled.
            </div>
          </div>
        )}
      </div>

      <form className="chat-input-row" onSubmit={handleSend}>
        <input
          className="chat-input"
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={`Message ${character.name}...`}
          disabled={sending}
        />
        <button className="btn-pill chat-send" type="submit" disabled={sending || !input.trim()}>
          Send
        </button>
      </form>
    </div>
  )
}
