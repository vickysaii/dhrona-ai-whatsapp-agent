import { useState, useEffect, useRef } from 'react'
import {
  Upload, FileText, Trash2, RefreshCw, CheckCircle2,
  Clock, AlertCircle, BookOpen, Database, Plus
} from 'lucide-react'
import api from '../services/api'

const STATUS_STYLES = {
  indexed:    { color: 'text-emerald-400', bg: 'bg-emerald-500/10 border-emerald-500/20', icon: CheckCircle2 },
  processing: { color: 'text-amber-400',   bg: 'bg-amber-500/10 border-amber-500/20',   icon: Clock         },
  uploaded:   { color: 'text-sky-400',     bg: 'bg-sky-500/10 border-sky-500/20',       icon: Clock         },
  failed:     { color: 'text-red-400',     bg: 'bg-red-500/10 border-red-500/20',       icon: AlertCircle   },
}

export default function KnowledgeBase() {
  const [files, setFiles] = useState([])
  const [uploading, setUploading] = useState(false)
  const [reindexing, setReindexing] = useState(false)
  const [dragOver, setDragOver] = useState(false)
  const [toastMsg, setToastMsg] = useState(null)
  const fileRef = useRef()

  const toast = (msg, type = 'success') => {
    setToastMsg({ msg, type })
    setTimeout(() => setToastMsg(null), 3500)
  }

  const fetchFiles = async () => {
    try {
      const res = await api.get('/kb/documents')
      setFiles(res.data || [])
    } catch {
      setFiles([])
    }
  }

  useEffect(() => { fetchFiles() }, [])

  const handleUpload = async (fileList) => {
    if (!fileList?.length) return
    setUploading(true)
    let successCount = 0
    for (const file of Array.from(fileList)) {
      const allowed = ['pdf', 'docx', 'doc', 'txt', 'md', 'csv']
      const ext = file.name.split('.').pop().toLowerCase()
      if (!allowed.includes(ext)) {
        toast(`Unsupported file type: .${ext}`, 'error')
        continue
      }
      const form = new FormData()
      form.append('file', file)
      try {
        await api.post('/kb/upload', form, { headers: { 'Content-Type': 'multipart/form-data' } })
        successCount++
      } catch (err) {
        toast(`Failed to upload ${file.name}: ${err.response?.data?.detail || 'Unknown error'}`, 'error')
      }
    }
    if (successCount > 0) toast(`${successCount} document(s) uploaded and indexed!`)
    await fetchFiles()
    setUploading(false)
    if (fileRef.current) fileRef.current.value = ''
  }

  const handleDelete = async (fileId, filename) => {
    if (!confirm(`Delete "${filename}" and all its embeddings?`)) return
    try {
      await api.delete(`/kb/documents/${fileId}`)
      toast(`"${filename}" deleted.`)
      await fetchFiles()
    } catch {
      toast('Failed to delete document.', 'error')
    }
  }

  const handleReindex = async () => {
    setReindexing(true)
    try {
      await api.post('/kb/reindex')
      toast('Knowledge base re-indexed successfully!')
    } catch {
      toast('Re-index failed.', 'error')
    } finally {
      setReindexing(false)
    }
  }

  const fileTypeIcon = (type) => {
    const icons = { pdf: '📄', docx: '📝', doc: '📝', txt: '📃', csv: '📊', md: '📋' }
    return icons[type] || '📁'
  }

  const formatSize = (bytes) => {
    if (!bytes) return '—'
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1048576) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / 1048576).toFixed(1)} MB`
  }

  return (
    <div className="space-y-6 relative">
      {/* Toast */}
      {toastMsg && (
        <div className={`fixed top-6 right-6 z-50 px-5 py-3 rounded-xl text-sm font-medium shadow-2xl border transition-all ${
          toastMsg.type === 'error'
            ? 'bg-red-900/80 border-red-500/30 text-red-200'
            : 'bg-emerald-900/80 border-emerald-500/30 text-emerald-200'
        }`}>
          {toastMsg.msg}
        </div>
      )}

      {/* Upload Zone */}
      <div
        onDragOver={e => { e.preventDefault(); setDragOver(true) }}
        onDragLeave={() => setDragOver(false)}
        onDrop={e => { e.preventDefault(); setDragOver(false); handleUpload(e.dataTransfer.files) }}
        onClick={() => fileRef.current?.click()}
        className={`glass-panel rounded-2xl border-2 border-dashed p-10 flex flex-col items-center justify-center cursor-pointer transition-all ${
          dragOver ? 'border-brand-500 bg-brand-500/5' : 'border-slate-700 hover:border-slate-600'
        }`}
      >
        <input
          ref={fileRef}
          type="file"
          className="hidden"
          multiple
          accept=".pdf,.docx,.doc,.txt,.md,.csv"
          onChange={e => handleUpload(e.target.files)}
        />
        {uploading ? (
          <div className="flex flex-col items-center gap-3">
            <div className="w-10 h-10 border-3 border-brand-500 border-t-transparent rounded-full animate-spin" />
            <p className="text-sm text-brand-400 font-medium">Processing & indexing documents…</p>
          </div>
        ) : (
          <>
            <div className="w-14 h-14 rounded-2xl bg-brand-500/10 border border-brand-500/20 flex items-center justify-center mb-4">
              <Upload size={24} className="text-brand-400" />
            </div>
            <p className="text-base font-semibold text-white">Drag & drop files here</p>
            <p className="text-sm text-slate-500 mt-1">or click to browse — PDF, DOCX, TXT, CSV, MD</p>
          </>
        )}
      </div>

      {/* Controls */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Database size={15} className="text-brand-400" />
          <span className="text-sm font-semibold text-white">{files.length} documents</span>
          <span className="text-xs text-slate-500">in vector store</span>
        </div>
        <button
          onClick={handleReindex}
          disabled={reindexing || files.length === 0}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-800 border border-slate-700 text-slate-300 text-sm hover:border-slate-600 hover:text-white transition-all disabled:opacity-50"
        >
          <RefreshCw size={14} className={reindexing ? 'animate-spin' : ''} />
          Re-index All
        </button>
      </div>

      {/* Documents Table */}
      <div className="glass-card rounded-2xl border border-slate-800 overflow-hidden">
        {files.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-16 text-center">
            <BookOpen size={36} className="text-slate-700 mb-4" />
            <p className="text-slate-500 font-medium">No documents uploaded yet</p>
            <p className="text-slate-600 text-sm mt-1">Upload your first document above to start building the knowledge base.</p>
          </div>
        ) : (
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-800 bg-slate-900/40">
                <th className="text-left px-5 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">Document</th>
                <th className="text-left px-5 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider hidden sm:table-cell">Type</th>
                <th className="text-left px-5 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider hidden md:table-cell">Size</th>
                <th className="text-left px-5 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">Status</th>
                <th className="text-right px-5 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {files.map(file => {
                const s = STATUS_STYLES[file.status] || STATUS_STYLES.uploaded
                const StatusIcon = s.icon
                return (
                  <tr key={file.id} className="hover:bg-slate-800/30 transition-colors">
                    <td className="px-5 py-4">
                      <div className="flex items-center gap-3">
                        <span className="text-xl">{fileTypeIcon(file.file_type)}</span>
                        <div>
                          <p className="font-medium text-white truncate max-w-[200px]">{file.filename}</p>
                          <p className="text-xs text-slate-500">{new Date(file.created_at).toLocaleDateString()}</p>
                        </div>
                      </div>
                    </td>
                    <td className="px-5 py-4 hidden sm:table-cell">
                      <span className="uppercase text-xs font-mono text-slate-400">{file.file_type}</span>
                    </td>
                    <td className="px-5 py-4 hidden md:table-cell text-slate-400">{formatSize(file.file_size)}</td>
                    <td className="px-5 py-4">
                      <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-medium border ${s.bg} ${s.color}`}>
                        <StatusIcon size={11} />
                        {file.status}
                      </span>
                    </td>
                    <td className="px-5 py-4 text-right">
                      <button
                        onClick={() => handleDelete(file.id, file.filename)}
                        className="p-2 rounded-lg text-slate-500 hover:text-red-400 hover:bg-red-500/10 transition-all"
                      >
                        <Trash2 size={15} />
                      </button>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
