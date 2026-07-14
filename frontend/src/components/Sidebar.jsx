import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard, BarChart3, BookOpen, MessageSquare,
  Settings, Bot, Zap
} from 'lucide-react'

const navItems = [
  { to: '/dashboard',     icon: LayoutDashboard, label: 'Dashboard'      },
  { to: '/analytics',     icon: BarChart3,        label: 'Analytics'      },
  { to: '/knowledge-base',icon: BookOpen,         label: 'Knowledge Base' },
  { to: '/conversations', icon: MessageSquare,    label: 'Conversations'  },
  { to: '/settings',      icon: Settings,         label: 'Settings'       },
]

export default function Sidebar() {
  return (
    <aside className="w-64 flex-shrink-0 glass-panel border-r border-slate-800 flex flex-col">
      {/* Brand */}
      <div className="px-6 py-5 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center shadow-lg shadow-brand-900/40">
            <Bot size={18} className="text-white" />
          </div>
          <div>
            <h1 className="font-bold text-sm text-white leading-tight">WhatsApp AI</h1>
            <p className="text-[10px] text-slate-500 font-medium tracking-wide uppercase">Business Agent</p>
          </div>
        </div>
      </div>

      {/* Nav Items */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        {navItems.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 group ${
                isActive
                  ? 'bg-brand-600/20 text-brand-300 border border-brand-500/30'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800/60'
              }`
            }
          >
            <Icon size={17} className="flex-shrink-0" />
            {label}
          </NavLink>
        ))}
      </nav>

      {/* Status Badge */}
      <div className="px-4 py-4 border-t border-slate-800">
        <div className="flex items-center gap-2 px-3 py-2 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
          <Zap size={13} className="text-emerald-400" />
          <span className="text-xs text-emerald-400 font-medium">Agent Active</span>
        </div>
      </div>
    </aside>
  )
}
