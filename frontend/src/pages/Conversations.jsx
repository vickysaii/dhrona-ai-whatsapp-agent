import { useState, useEffect, useRef } from 'react'
import {
  MessageSquare, Phone, Search, User, Bot, Users,
  UserCheck, UserX, ChevronRight, ArrowLeft, ToggleLeft, ToggleRight
} from 'lucide-react'
import api from '../services/api'

export default function Conversations() {
  const [sessions, setSessions] = useState([])
  const [selected, setSelected] = useState(null)
  const [messages, setMessages] = useState([])
  const [searchQuery, setSearchQuery] = useState('')
  const [loading, setLoading] = useState(true)
  const [msgLoading, setMsgLoading] = useState(false)
  const [togglingTakeover, setTogglingTakeover] = useState(false)
  const msgEndRef = useRef(null)

  const fetchSessions = async () => {
    try {
      const res = await api.get('/conversations')
      setSessions(res.data || [])
    } catch {
      setSessions([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchSessions() }, [])

  const selectSession = async (session) => {
    setSelected(session)
    setMsgLoading(true)
    try {
      const res = await api.get(`/conversations/${session.id}/messages`)
      setMessages(res.data || [])
    } catch {
      setMessages([])
    } finally {
      setMsgLoading(false)
    }
  }

  useEffect(() => {
    msgEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const toggleTakeover = async () => {
    if (!selected) return
    setTogglingTakeover(true)
    const newState = !selected.human_takeover
    try {
      await api.post(`/conversations/${selected.id}/takeover?human_takeover=${newState}`)
      const updated = { ...selected, human_takeover: newState }
      setSelected(updated)
      setSessions(prev => prev.map(s => s.id === selected.id ? updated : s))
    } catch { }
    finally { setTogglingTakeover(false) }
  }

  const filtered = sessions.filter(s =>
    s.customer_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    s.customer_phone?.includes(searchQuery)
  )

  const formatTime = (ts) => {
    const d = new Date(ts)
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }

  const formatDate = (ts) => {
    const d = new Date(ts)
    const today = new Date()
    if (d.toDateString() === today.toDateString()) return 'Today'
    return d.toLocaleDateString([], { month: 'short', day: 'numeric' })
  }

  return (
    <div className="h-[calc(100vh-130px)] flex gap-5">
      {/* Sidebar: Session List */}
      <div className={`w-full sm:w-80 flex-shrink-0 glass-card rounded-2xl border border-slate-800 flex flex-col ${selected ? 'hidden sm:flex' : 'flex'}`}>
        {/* Search */}
        <div className="p-4 border-b border-slate-800">
          <div className="relative">
            <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
            <input
              type="text"
              placeholder="Search customers…"
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              className="w-full bg-slate-900/60 border border-slate-700 rounded-xl pl-9 pr-4 py-2.5 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-brand-500 transition-all"
            />
          </div>
        </div>

        {/* Sessions */}
        <div className="flex-1 overflow-y-auto divide-y divide-slate-800/60">
          {loading ? (
            <div className="flex items-center justify-center h-32">
              <div className="w-6 h-6 border-2 border-brand-500 border-t-transparent rounded-full animate-spin" />
            </div>
          ) : filtered.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-32 text-center px-4">
              <Users size={28} className="text-slate-700 mb-2" />
              <p className="text-sm text-slate-500">No conversations yet</p>
            </div>
          ) : (
            filtered.map(session => (
              <button
                key={session.id}
                onClick={() => selectSession(session)}
                className={`w-full text-left px-4 py-3.5 hover:bg-slate-800/40 transition-colors flex items-start gap-3 ${
                  selected?.id === session.id ? 'bg-brand-600/10 border-l-2 border-brand-500' : ''
                }`}
              >
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-slate-700 to-slate-800 flex items-center justify-center flex-shrink-0 text-sm font-semibold text-white">
                  {(session.customer_name || '?').charAt(0).toUpperCase()}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between gap-2">
                    <p className="text-sm font-medium text-white truncate">{session.customer_name || 'Unknown'}</p>
                    <span className="text-[10px] text-slate-500 flex-shrink-0">{formatDate(session.updated_at)}</span>
                  </div>
                  <div className="flex items-center gap-2 mt-0.5">
                    <Phone size={10} className="text-slate-600" />
                    <p className="text-xs text-slate-500">{session.customer_phone}</p>
                  </div>
                  {session.human_takeover && (
                    <span className="inline-block mt-1 text-[10px] px-1.5 py-0.5 rounded-md bg-amber-500/10 border border-amber-500/20 text-amber-400 font-medium">
                      Human Mode
                    </span>
                  )}
                </div>
              </button>
            ))
          )}
        </div>
      </div>

      {/* Chat Window */}
      <div className={`flex-1 glass-card rounded-2xl border border-slate-800 flex flex-col ${!selected ? 'hidden sm:flex' : 'flex'}`}>
        {!selected ? (
          <div className="flex-1 flex flex-col items-center justify-center text-center p-8">
            <div className="w-16 h-16 rounded-2xl bg-slate-800/60 flex items-center justify-center mb-4">
              <MessageSquare size={28} className="text-slate-600" />
            </div>
            <p className="text-white font-semibold">Select a Conversation</p>
            <p className="text-slate-500 text-sm mt-1">Choose a customer from the list to view their chat history</p>
          </div>
        ) : (
          <>
            {/* Chat Header */}
            <div className="px-5 py-4 border-b border-slate-800 flex items-center gap-4">
              <button
                onClick={() => setSelected(null)}
                className="sm:hidden p-1.5 rounded-lg hover:bg-slate-800 text-slate-400"
              >
                <ArrowLeft size={16} />
              </button>
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-600 to-brand-800 flex items-center justify-center text-white font-semibold">
                {(selected.customer_name || '?').charAt(0).toUpperCase()}
              </div>
              <div className="flex-1">
                <p className="font-semibold text-white text-sm">{selected.customer_name || 'Unknown'}</p>
                <p className="text-xs text-slate-500">{selected.customer_phone}</p>
              </div>
              <button
                onClick={toggleTakeover}
                disabled={togglingTakeover}
                className={`flex items-center gap-2 px-3 py-2 rounded-xl text-xs font-medium border transition-all ${
                  selected.human_takeover
                    ? 'bg-amber-500/10 border-amber-500/30 text-amber-400 hover:bg-amber-500/20'
                    : 'bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:border-slate-600'
                }`}
              >
                {selected.human_takeover ? <ToggleRight size={14} /> : <ToggleLeft size={14} />}
                {selected.human_takeover ? 'Human Mode ON' : 'Human Mode'}
              </button>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-5 space-y-4">
              {msgLoading ? (
                <div className="flex items-center justify-center h-32">
                  <div className="w-6 h-6 border-2 border-brand-500 border-t-transparent rounded-full animate-spin" />
                </div>
              ) : messages.length === 0 ? (
                <div className="text-center text-slate-600 text-sm mt-8">No messages in this session yet.</div>
              ) : (
                messages.map(msg => (
                  <div key={msg.id} className={`flex gap-3 ${msg.sender === 'agent' ? 'justify-end' : 'justify-start'}`}>
                    {msg.sender === 'customer' && (
                      <div className="w-8 h-8 rounded-xl bg-slate-700 flex items-center justify-center flex-shrink-0">
                        <User size={14} className="text-slate-400" />
                      </div>
                    )}
                    <div className={`max-w-[70%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                      msg.sender === 'agent'
                        ? 'bg-brand-600/20 border border-brand-500/20 text-brand-100 rounded-tr-sm'
                        : 'bg-slate-800 border border-slate-700 text-slate-200 rounded-tl-sm'
                    }`}>
                      <p>{msg.content}</p>
                      <p className="text-[10px] mt-1.5 opacity-50">{formatTime(msg.created_at)}</p>
                    </div>
                    {msg.sender === 'agent' && (
                      <div className="w-8 h-8 rounded-xl bg-brand-600/20 flex items-center justify-center flex-shrink-0">
                        <Bot size={14} className="text-brand-400" />
                      </div>
                    )}
                  </div>
                ))
              )}
              <div ref={msgEndRef} />
            </div>
          </>
        )}
      </div>
    </div>
  )
}
