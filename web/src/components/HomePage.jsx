import { useState } from 'react'

function HomePage() {
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Welcome to Tokyo-IA! How can I help you today?' }
  ])

  const handleSend = () => {
    if (!message.trim()) return
    
    const newMessages = [
      ...messages,
      { role: 'user', content: message },
      { role: 'assistant', content: 'This is a placeholder response. Real AI integration coming soon!' }
    ]
    
    setMessages(newMessages)
    setMessage('')
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="home-page">
      <div className="hero-section">
        <h2>Your Tokyo-Themed AI Companion</h2>
        <p>Experience the future of AI interaction</p>
      </div>
      
      <div className="chat-container">
        <div className="messages">
          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role}`}>
              <div className="message-content">{msg.content}</div>
            </div>
          ))}
        </div>
        
        <div className="input-area">
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            rows="3"
          />
          <button onClick={handleSend}>Send</button>
        </div>
      </div>
    </div>
  )
}

export default HomePage
