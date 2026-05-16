"use client"

import { useState, useRef, useEffect } from "react"

type Message = { role: "user" | "assistant"; content: string }

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  async function send() {
    if (!input.trim() || loading) return
    const userMsg: Message = { role: "user", content: input }
    const next = [...messages, userMsg]
    setMessages(next)
    setInput("")
    setLoading(true)

    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/chat/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: next }),
    })
    const data = await res.json()
    setMessages([...next, { role: "assistant", content: data.reply }])
    setLoading(false)
  }

  return (
    <main className="flex flex-col h-screen bg-gray-950 text-white">
      <header className="px-6 py-4 border-b border-gray-800 flex items-center gap-3">
        <div className="w-8 h-8 rounded-full bg-violet-600 flex items-center justify-center font-bold text-sm">E</div>
        <div>
          <p className="font-semibold">Eli</p>
          <p className="text-xs text-gray-400">Vizio AI Virtual Employee</p>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4">
        {messages.length === 0 && (
          <p className="text-center text-gray-500 mt-20">Say hello to Eli</p>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
            <div className={`max-w-xl px-4 py-3 rounded-2xl text-sm whitespace-pre-wrap ${
              m.role === "user"
                ? "bg-violet-600 text-white rounded-br-sm"
                : "bg-gray-800 text-gray-100 rounded-bl-sm"
            }`}>
              {m.content}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-800 px-4 py-3 rounded-2xl rounded-bl-sm text-gray-400 text-sm animate-pulse">
              Eli is thinking...
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="px-4 py-4 border-t border-gray-800 flex gap-3">
        <input
          className="flex-1 bg-gray-800 rounded-xl px-4 py-3 text-sm outline-none focus:ring-2 focus:ring-violet-500 placeholder-gray-500"
          placeholder="Message Eli..."
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && send()}
        />
        <button
          onClick={send}
          disabled={loading}
          className="bg-violet-600 hover:bg-violet-500 disabled:opacity-50 px-5 py-3 rounded-xl text-sm font-medium transition-colors"
        >
          Send
        </button>
      </div>
    </main>
  )
}
