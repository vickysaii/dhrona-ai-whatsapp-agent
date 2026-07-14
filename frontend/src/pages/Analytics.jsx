import { useState, useEffect } from 'react'
import { MessageSquare, Users, Zap, Clock, BarChart3, TrendingUp } from 'lucide-react'
import {
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend
} from 'recharts'
import StatCard from '../components/StatCard'
import api from '../services/api'

const DEMO_WEEKLY = [
  { day: 'Mon', messages: 45, responses: 43 },
  { day: 'Tue', messages: 62, responses: 60 },
  { day: 'Wed', messages: 78, responses: 75 },
  { day: 'Thu', messages: 55, responses: 54 },
  { day: 'Fri', messages: 90, responses: 88 },
  { day: 'Sat', messages: 32, responses: 31 },
  { day: 'Sun', messages: 18, responses: 17 },
]

const DEMO_TOPICS = [
  { name: 'Product Info', value: 38, color: '#8b5cf6' },
  { name: 'Support',      value: 27, color: '#06b6d4' },
  { name: 'Pricing',      value: 20, color: '#f59e0b' },
  { name: 'Hours',        value: 10, color: '#10b981' },
  { name: 'Other',        value: 5,  color: '#6b7280' },
]

export default function Analytics() {
  const [metrics, setMetrics] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetch = async () => {
      try {
        const res = await api.get('/dashboard/metrics')
        setMetrics(res.data.metrics)
      } catch {
        setMetrics({ total_messages: 1247, today_messages: 38, total_customers: 312, tokens_used: 58420, avg_response_time_ms: 820 })
      } finally { setLoading(false) }
    }
    fetch()
  }, [])

  const tooltipStyle = {
    backgroundColor: '#0f172a', border: '1px solid #1e293b',
    borderRadius: '12px', color: '#e2e8f0', fontSize: '12px'
  }

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard title="Total Messages" value={metrics?.total_messages?.toLocaleString()} icon={MessageSquare} color="brand" trend={12} subtitle="all time" />
        <StatCard title="Active Customers" value={metrics?.total_customers?.toLocaleString()} icon={Users} color="sky" trend={5} subtitle="unique phones" />
        <StatCard title="Avg Response" value={`${metrics?.avg_response_time_ms || 0}ms`} icon={Clock} color="emerald" subtitle="response latency" />
        <StatCard title="Tokens Used" value={`${((metrics?.tokens_used || 0) / 1000).toFixed(1)}K`} icon={Zap} color="amber" subtitle="Gemini usage" />
      </div>

      {/* Weekly Message Trend */}
      <div className="glass-card rounded-2xl p-5 border border-slate-800">
        <h3 className="text-sm font-semibold text-white mb-1">Weekly Message Volume</h3>
        <p className="text-xs text-slate-500 mb-5">Customer messages vs AI responses this week</p>
        <ResponsiveContainer width="100%" height={240}>
          <LineChart data={DEMO_WEEKLY} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="day" tick={{ fontSize: 11, fill: '#64748b' }} axisLine={false} tickLine={false} />
            <YAxis tick={{ fontSize: 11, fill: '#64748b' }} axisLine={false} tickLine={false} />
            <Tooltip contentStyle={tooltipStyle} />
            <Line type="monotone" dataKey="messages" stroke="#8b5cf6" strokeWidth={2} dot={{ fill: '#8b5cf6', r: 4 }} name="Customer Messages" />
            <Line type="monotone" dataKey="responses" stroke="#10b981" strokeWidth={2} dot={{ fill: '#10b981', r: 4 }} name="AI Responses" />
            <Legend wrapperStyle={{ fontSize: '11px', color: '#64748b', paddingTop: '12px' }} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Bottom Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Topics Pie Chart */}
        <div className="glass-card rounded-2xl p-5 border border-slate-800">
          <h3 className="text-sm font-semibold text-white mb-1">Top Query Topics</h3>
          <p className="text-xs text-slate-500 mb-4">Distribution of customer question categories</p>
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie
                data={DEMO_TOPICS}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={90}
                paddingAngle={3}
                dataKey="value"
              >
                {DEMO_TOPICS.map((entry, i) => (
                  <Cell key={i} fill={entry.color} stroke="transparent" />
                ))}
              </Pie>
              <Tooltip contentStyle={tooltipStyle} />
              <Legend wrapperStyle={{ fontSize: '11px', color: '#94a3b8' }} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Response Time Bar */}
        <div className="glass-card rounded-2xl p-5 border border-slate-800">
          <h3 className="text-sm font-semibold text-white mb-1">Daily Response Time</h3>
          <p className="text-xs text-slate-500 mb-4">Average AI response latency in milliseconds</p>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart
              data={[
                { day: 'Mon', ms: 750 }, { day: 'Tue', ms: 820 }, { day: 'Wed', ms: 690 },
                { day: 'Thu', ms: 910 }, { day: 'Fri', ms: 780 }, { day: 'Sat', ms: 650 }, { day: 'Sun', ms: 720 }
              ]}
              margin={{ top: 0, right: 0, left: -20, bottom: 0 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="day" tick={{ fontSize: 11, fill: '#64748b' }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontSize: 11, fill: '#64748b' }} axisLine={false} tickLine={false} />
              <Tooltip contentStyle={tooltipStyle} />
              <Bar dataKey="ms" fill="#06b6d4" radius={[4, 4, 0, 0]} name="Response (ms)" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}
