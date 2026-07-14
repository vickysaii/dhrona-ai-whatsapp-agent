import { useLocation } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth.jsx'
import { LogOut, User, Bell } from 'lucide-react'

const pageTitles = {
  '/dashboard':     { title: 'Dashboard',      subtitle: 'Overview of your AI agent activity' },
  '/analytics':     { title: 'Analytics',      subtitle: 'Message trends and performance metrics' },
  '/knowledge-base':{ title: 'Knowledge Base', subtitle: 'Manage documents and vector embeddings' },
  '/conversations': { title: 'Conversations',  subtitle: 'View and manage customer chat sessions' },
  '/settings':      { title: 'Settings',       subtitle: 'Configure your AI agent and business profile' },
}

export default function Header() {
  const { logout } = useAuth()
  const { pathname } = useLocation()
  const page = pageTitles[pathname] || { title: 'Admin', subtitle: '' }

  return (
    <header className="px-6 py-4 border-b border-slate-800 glass-panel flex items-center justify-between flex-shrink-0">
      <div>
        <h2 className="text-lg font-semibold text-white">{page.title}</h2>
        <p className="text-xs text-slate-500 mt-0.5">{page.subtitle}</p>
      </div>
      <div className="flex items-center gap-3">
        <button className="w-9 h-9 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-400 hover:text-white hover:border-slate-600 transition-all">
          <Bell size={16} />
        </button>
        <div className="flex items-center gap-2 pl-3 border-l border-slate-800">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center">
            <User size={14} className="text-white" />
          </div>
          <span className="text-sm text-slate-300 font-medium hidden sm:block">Admin</span>
        </div>
        <button
          onClick={logout}
          className="flex items-center gap-2 px-3 py-2 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm font-medium hover:bg-red-500/20 transition-all"
        >
          <LogOut size={14} />
          <span className="hidden sm:block">Logout</span>
        </button>
      </div>
    </header>
  )
}
