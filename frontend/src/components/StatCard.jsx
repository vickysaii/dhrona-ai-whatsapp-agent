export default function StatCard({ title, value, subtitle, icon: Icon, color = 'brand', trend }) {
  const colors = {
    brand:   { bg: 'bg-brand-500/10',   border: 'border-brand-500/20',   icon: 'text-brand-400',   glow: 'shadow-brand-900/20'  },
    emerald: { bg: 'bg-emerald-500/10', border: 'border-emerald-500/20', icon: 'text-emerald-400', glow: 'shadow-emerald-900/20'},
    amber:   { bg: 'bg-amber-500/10',   border: 'border-amber-500/20',   icon: 'text-amber-400',   glow: 'shadow-amber-900/20'  },
    rose:    { bg: 'bg-rose-500/10',    border: 'border-rose-500/20',    icon: 'text-rose-400',    glow: 'shadow-rose-900/20'   },
    sky:     { bg: 'bg-sky-500/10',     border: 'border-sky-500/20',     icon: 'text-sky-400',     glow: 'shadow-sky-900/20'    },
  }
  const c = colors[color] || colors.brand

  return (
    <div className={`glass-card rounded-2xl p-5 border ${c.border} shadow-xl ${c.glow} flex flex-col gap-3`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-medium text-slate-500 uppercase tracking-wider">{title}</p>
          <p className="text-3xl font-bold text-white mt-1">{value ?? '—'}</p>
        </div>
        <div className={`w-11 h-11 rounded-xl ${c.bg} border ${c.border} flex items-center justify-center`}>
          {Icon && <Icon size={20} className={c.icon} />}
        </div>
      </div>
      {(subtitle || trend !== undefined) && (
        <div className="flex items-center gap-2 pt-1 border-t border-slate-800">
          {trend !== undefined && (
            <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${trend >= 0 ? 'bg-emerald-500/10 text-emerald-400' : 'bg-red-500/10 text-red-400'}`}>
              {trend >= 0 ? '+' : ''}{trend}%
            </span>
          )}
          {subtitle && <p className="text-xs text-slate-500">{subtitle}</p>}
        </div>
      )}
    </div>
  )
}
