import { useState, useEffect } from 'react'
import {
  Building2, MessageSquareDashed, HelpCircle, Save, Plus,
  Trash2, Thermometer, Hash, Globe, Phone, Mail, MapPin,
  Clock, CheckCircle2
} from 'lucide-react'
import api from '../services/api'

const TABS = [
  { id: 'business', label: 'Business Profile', icon: Building2 },
  { id: 'prompt',   label: 'AI Prompt',        icon: MessageSquareDashed },
  { id: 'faq',      label: 'FAQ Manager',      icon: HelpCircle },
]

function InputField({ label, value, onChange, type = 'text', placeholder, icon: Icon, multi = false }) {
  const base = 'w-full bg-slate-900/60 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500/30 transition-all'
  return (
    <div>
      <label className="block text-xs font-semibold text-slate-400 mb-2 uppercase tracking-wider">{label}</label>
      {multi ? (
        <textarea
          value={value || ''}
          onChange={e => onChange(e.target.value)}
          rows={4}
          placeholder={placeholder}
          className={base + ' resize-none'}
        />
      ) : (
        <div className="relative">
          {Icon && <Icon size={14} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />}
          <input
            type={type}
            value={value || ''}
            onChange={e => onChange(e.target.value)}
            placeholder={placeholder}
            className={base + (Icon ? ' pl-9' : '')}
          />
        </div>
      )}
    </div>
  )
}

export default function Settings() {
  const [activeTab, setActiveTab] = useState('business')
  const [business, setBusiness] = useState({})
  const [prompt, setPrompt] = useState({})
  const [faqs, setFaqs] = useState([])
  const [newQ, setNewQ] = useState('')
  const [newA, setNewA] = useState('')
  const [saving, setSaving] = useState(false)
  const [toast, setToast] = useState(null)

  const showToast = (msg, type = 'success') => {
    setToast({ msg, type })
    setTimeout(() => setToast(null), 3000)
  }

  useEffect(() => {
    const fetchAll = async () => {
      try {
        const settingsRes = await api.get('/settings')
        setBusiness(settingsRes.data.business || {})
        setPrompt(settingsRes.data.prompt || {})
      } catch {}
      try {
        const faqRes = await api.get('/settings/faqs')
        setFaqs(faqRes.data || [])
      } catch {}
    }
    fetchAll()
  }, [])

  const saveBusiness = async () => {
    setSaving(true)
    try {
      await api.put('/settings/business', business)
      showToast('Business settings saved!')
    } catch { showToast('Failed to save settings.', 'error') }
    finally { setSaving(false) }
  }

  const savePrompt = async () => {
    setSaving(true)
    try {
      await api.put('/settings/prompt', prompt)
      showToast('Prompt settings saved!')
    } catch { showToast('Failed to save prompt settings.', 'error') }
    finally { setSaving(false) }
  }

  const addFaq = async () => {
    if (!newQ.trim() || !newA.trim()) return
    try {
      const res = await api.post(`/settings/faqs?question=${encodeURIComponent(newQ)}&answer=${encodeURIComponent(newA)}`)
      setFaqs(prev => [res.data, ...prev])
      setNewQ('')
      setNewA('')
      showToast('FAQ added!')
    } catch { showToast('Failed to add FAQ.', 'error') }
  }

  const deleteFaq = async (id) => {
    try {
      await api.delete(`/settings/faqs/${id}`)
      setFaqs(prev => prev.filter(f => f.id !== id))
      showToast('FAQ removed.')
    } catch { showToast('Failed to delete FAQ.', 'error') }
  }

  const setB = (key) => (val) => setBusiness(prev => ({ ...prev, [key]: val }))
  const setP = (key) => (val) => setPrompt(prev => ({ ...prev, [key]: val }))

  return (
    <div className="space-y-5 relative">
      {/* Toast */}
      {toast && (
        <div className={`fixed top-6 right-6 z-50 flex items-center gap-2 px-5 py-3 rounded-xl text-sm font-medium shadow-2xl border ${
          toast.type === 'error'
            ? 'bg-red-900/80 border-red-500/30 text-red-200'
            : 'bg-emerald-900/80 border-emerald-500/30 text-emerald-200'
        }`}>
          <CheckCircle2 size={14} />
          {toast.msg}
        </div>
      )}

      {/* Tabs */}
      <div className="flex gap-2 p-1 glass-card rounded-2xl border border-slate-800 w-fit">
        {TABS.map(tab => {
          const Icon = tab.icon
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium transition-all ${
                activeTab === tab.id
                  ? 'bg-brand-600/20 text-brand-300 border border-brand-500/30'
                  : 'text-slate-500 hover:text-slate-300'
              }`}
            >
              <Icon size={15} />
              {tab.label}
            </button>
          )
        })}
      </div>

      {/* ─── Business Tab ─── */}
      {activeTab === 'business' && (
        <div className="glass-card rounded-2xl border border-slate-800 p-6 space-y-5">
          <div className="flex items-center justify-between mb-2">
            <h3 className="font-semibold text-white">Business Information</h3>
            <button
              onClick={saveBusiness}
              disabled={saving}
              className="flex items-center gap-2 px-4 py-2 rounded-xl bg-brand-600 text-white text-sm font-medium hover:bg-brand-500 transition-all disabled:opacity-60"
            >
              <Save size={14} />
              {saving ? 'Saving…' : 'Save Changes'}
            </button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <InputField label="Business Name" value={business.business_name} onChange={setB('business_name')} placeholder="My AI Business" icon={Building2} />
            <InputField label="Email Address" value={business.email} onChange={setB('email')} placeholder="support@business.com" icon={Mail} type="email" />
            <InputField label="Phone Number" value={business.phone} onChange={setB('phone')} placeholder="+1 234 567 8900" icon={Phone} />
            <InputField label="Website URL" value={business.website} onChange={setB('website')} placeholder="https://yourbusiness.com" icon={Globe} />
            <InputField label="Address" value={business.address} onChange={setB('address')} placeholder="123 Main St, City" icon={MapPin} />
          </div>

          <InputField
            label="Business Description"
            value={business.business_description}
            onChange={setB('business_description')}
            placeholder="A brief description of what your business does…"
            multi
          />

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <InputField
              label="Greeting Message"
              value={business.greeting_message}
              onChange={setB('greeting_message')}
              placeholder="Hello! How can I help you today?"
              multi
            />
            <InputField
              label="Fallback Message"
              value={business.fallback_message}
              onChange={setB('fallback_message')}
              placeholder="I'm sorry, I don't have that information…"
              multi
            />
          </div>
        </div>
      )}

      {/* ─── Prompt Tab ─── */}
      {activeTab === 'prompt' && (
        <div className="glass-card rounded-2xl border border-slate-800 p-6 space-y-5">
          <div className="flex items-center justify-between mb-2">
            <h3 className="font-semibold text-white">AI Agent Prompt Configuration</h3>
            <button
              onClick={savePrompt}
              disabled={saving}
              className="flex items-center gap-2 px-4 py-2 rounded-xl bg-brand-600 text-white text-sm font-medium hover:bg-brand-500 transition-all disabled:opacity-60"
            >
              <Save size={14} />
              {saving ? 'Saving…' : 'Save Changes'}
            </button>
          </div>

          {/* System Prompt */}
          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-2 uppercase tracking-wider">System Prompt</label>
            <textarea
              value={prompt.system_prompt || ''}
              onChange={e => setP('system_prompt')(e.target.value)}
              rows={8}
              className="w-full bg-slate-900/60 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500/30 transition-all resize-none font-mono"
              placeholder="You are a professional AI assistant…"
            />
            <p className="text-xs text-slate-600 mt-1.5">
              This is the core instruction given to Gemini 2.5 Flash before every conversation.
            </p>
          </div>

          {/* Sliders */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            {/* Temperature */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                  <Thermometer size={12} /> Temperature
                </label>
                <span className="text-sm font-bold text-brand-400">{prompt.llm_temperature ?? 0.3}</span>
              </div>
              <input
                type="range"
                min={0} max={1} step={0.05}
                value={prompt.llm_temperature ?? 0.3}
                onChange={e => setP('llm_temperature')(parseFloat(e.target.value))}
                className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-brand-500"
              />
              <div className="flex justify-between text-[10px] text-slate-600 mt-1">
                <span>Precise (0.0)</span>
                <span>Creative (1.0)</span>
              </div>
            </div>

            {/* Max Tokens */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                  <Hash size={12} /> Max Output Tokens
                </label>
                <span className="text-sm font-bold text-brand-400">{prompt.max_tokens ?? 800}</span>
              </div>
              <input
                type="range"
                min={100} max={4096} step={50}
                value={prompt.max_tokens ?? 800}
                onChange={e => setP('max_tokens')(parseInt(e.target.value))}
                className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-brand-500"
              />
              <div className="flex justify-between text-[10px] text-slate-600 mt-1">
                <span>Short (100)</span>
                <span>Long (4096)</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ─── FAQ Tab ─── */}
      {activeTab === 'faq' && (
        <div className="space-y-4">
          {/* Add New FAQ */}
          <div className="glass-card rounded-2xl border border-slate-800 p-5 space-y-3">
            <h3 className="font-semibold text-white text-sm mb-1">Add New FAQ</h3>
            <input
              type="text"
              placeholder="Question — e.g. What are your business hours?"
              value={newQ}
              onChange={e => setNewQ(e.target.value)}
              className="w-full bg-slate-900/60 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-brand-500 transition-all"
            />
            <textarea
              placeholder="Answer — e.g. We are open Mon–Fri, 9am to 6pm."
              value={newA}
              onChange={e => setNewA(e.target.value)}
              rows={3}
              className="w-full bg-slate-900/60 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-brand-500 transition-all resize-none"
            />
            <button
              onClick={addFaq}
              disabled={!newQ.trim() || !newA.trim()}
              className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-brand-600 text-white text-sm font-medium hover:bg-brand-500 transition-all disabled:opacity-50"
            >
              <Plus size={15} />
              Add FAQ
            </button>
          </div>

          {/* FAQ List */}
          <div className="space-y-3">
            {faqs.length === 0 ? (
              <div className="glass-card rounded-2xl border border-slate-800 p-10 text-center">
                <HelpCircle size={32} className="text-slate-700 mx-auto mb-3" />
                <p className="text-slate-500 text-sm">No FAQs yet. Add your first one above.</p>
              </div>
            ) : (
              faqs.map(faq => (
                <div key={faq.id} className="glass-card rounded-xl border border-slate-800 p-4 flex items-start gap-4">
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-semibold text-white">{faq.question}</p>
                    <p className="text-sm text-slate-400 mt-1 leading-relaxed">{faq.answer}</p>
                  </div>
                  <button
                    onClick={() => deleteFaq(faq.id)}
                    className="p-2 rounded-lg text-slate-600 hover:text-red-400 hover:bg-red-500/10 transition-all flex-shrink-0"
                  >
                    <Trash2 size={15} />
                  </button>
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  )
}
