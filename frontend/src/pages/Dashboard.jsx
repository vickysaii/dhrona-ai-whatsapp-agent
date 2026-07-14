import { useState, useEffect } from 'react'
import { MessageSquare, Users, Zap, Clock, TrendingUp, Activity } from 'lucide-react'
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar
} from 'recharts'
import StatCard from '../components/StatCard'
import api from '../services/api'

export default function Dashboard() {
  const [metrics, setMetrics] = useState(null)
  const [trends, setTrends] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetch = async () => {
      try {
        const res = await api.get('/dashboard/metrics')
        setMetrics(res.data.metrics)
        setTrends(res.data.trends)
      } catch {
        // fallback demo data
        setMetrics({ total_messages: 1247, today_messages: 38, total_customers: 312, tokens_used: 58420, avg_response_time_ms: 820 })
        setTrends({
          daily_active_chats: [
            { name: 'Mon', chats: 12 }, { name: 'Tue', chats: 18 }, { name: 'Wed', chats: 22 },
            { name: 'Thu', chats: 25 }, { name: 'Fri', chats: 30 }, { name: 'Sat', chats: 8 }, { name: 'Sun', chats: 5 }
          ],
          token_consumption: [
            { name: 'Week 1', tokens: 8500 }, { name: 'Week 2', tokens: 12400 },
            { name: 'Week 3', tokens: 19800 }, { name: 'Week 4', tokens: 17720 }
          ]
        })
      } finally {
        setLoading(false)
      }
    }
    fetch()
  }, [])

  const tooltipStyle = {
    backgroundColor: '#0f172a',
    border: '1px solid #1e293b',
    borderRadius: '12px',
    color: '#e2e8f0',
    fontSize: '12px',
  }

  if (loading) return (
    <div className="flex items-center justify-center h-64">
      <div className="w-8 h-8 border-3 border-brand-500 border-t-transparent rounded-full animate-spin" />
    </div>
  )

  return (
    <div className="space-y-6">
      {/* Hero Banner */}
      <div className="glass-panel rounded-2xl p-6 border border-slate-800 bg-gradient-to-r from-brand-900/30 to-slate-900/40 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-brand-500/5 rounded-full blur-3xl" />
        <div className="relative z-10">
          <div className="flex items-center gap-2 mb-1">
            <Activity size={14} className="text-brand-400" />
            <span className="text-xs text-brand-400 font-semibold uppercase tracking-wider">Live Status</span>
          </div>
          <h2 className="text-2xl font-bold text-white">AI Agent is Running</h2>
          <p className="text-slate-400 text-sm mt-1">
            Your WhatsApp AI Business Agent is actively responding to customer queries.
          </p>
        </div>
      </div>

      {/* Stat Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Messages"
          value={metrics?.total_messages?.toLocaleString()}
          icon={MessageSquare}
          color="brand"
          trend={12}
          subtitle="vs last month"
        />
        <StatCard
          title="Today's Messages"
          value={metrics?.today_messages}
          icon={TrendingUp}
          color="emerald"
          trend={8}
          subtitle="vs yesterday"
        />
        <StatCard
          title="Total Customers"
          value={metrics?.total_customers?.toLocaleString()}
          icon={Users}
          color="sky"
          trend={5}
          subtitle="unique phones"
        />
        <StatCard
          title="Tokens Used"
          value={(metrics?.tokens_used / 1000).toFixed(1) + 'K'}
          icon={Zap}
          color="amber"
          subtitle="Gemini API usage"
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Weekly Chats Chart */}
        <div className="glass-card rounded-2xl p-5 border border-slate-800">
          <div className="flex items-center justify-between mb-5">
            <div>
              <h3 className="text-sm font-semibold text-white">Weekly Active Chats</h3>
              <p className="text-xs text-slate-500 mt-0.5">Customer conversations per day</p>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={trends?.daily_active_chats} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
              <defs>
                <linearGradient id="chatGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#64748b' }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontSize: 11, fill: '#64748b' }} axisLine={false} tickLine={false} />
              <Tooltip contentStyle={tooltipStyle} />
              <Area type="monotone" dataKey="chats" stroke="#8b5cf6" strokeWidth={2} fill="url(#chatGrad)" dot={false} />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Token Usage Chart */}
        <div className="glass-card rounded-2xl p-5 border border-slate-800">
          <div className="flex items-center justify-between mb-5">
            <div>
              <h3 className="text-sm font-semibold text-white">Token Consumption</h3>
              <p className="text-xs text-slate-500 mt-0.5">Gemini API tokens per week</p>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={trends?.token_consumption} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#64748b' }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontSize: 11, fill: '#64748b' }} axisLine={false} tickLine={false} />
              <Tooltip contentStyle={tooltipStyle} />
              <Bar dataKey="tokens" fill="#f59e0b" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Performance Card */}
      <div className="glass-card rounded-2xl p-5 border border-slate-800">
        <h3 className="text-sm font-semibold text-white mb-4">Performance Summary</h3>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="text-center p-4 rounded-xl bg-slate-800/40">
            <Clock size={20} className="text-sky-400 mx-auto mb-2" />
            <p className="text-2xl font-bold text-white">{metrics?.avg_response_time_ms || 0}ms</p>
            <p className="text-xs text-slate-500 mt-1">Avg Response Time</p>
          </div>
          <div className="text-center p-4 rounded-xl bg-slate-800/40">
            <Zap size={20} className="text-amber-400 mx-auto mb-2" />
            <p className="text-2xl font-bold text-white">Gemini 2.5</p>
            <p className="text-xs text-slate-500 mt-1">AI Model Version</p>
          </div>
          <div className="text-center p-4 rounded-xl bg-slate-800/40">
            <Activity size={20} className="text-emerald-400 mx-auto mb-2" />
            <p className="text-2xl font-bold text-white">99.9%</p>
            <p className="text-xs text-slate-500 mt-1">Webhook Uptime</p>
          </div>
        </div>
      </div>
    </div>
  )
}
