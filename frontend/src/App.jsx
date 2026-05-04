import React, { useState } from 'react';
import { Shield, AlertTriangle, TrendingUp, BarChart3, CheckCircle2, ChevronRight, Activity } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import ReactMarkdown from 'react-markdown';

const App = () => {
  const [auditData, setAuditData] = useState(null);
  const [loading, setLoading] = useState(false);

  const runAudit = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8001/audit');
      const data = await response.json();
      setAuditData(data);
    } catch (error) {
      console.error("Audit failed", error);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-[#050505] text-slate-200 font-sans selection:bg-indigo-500/30">
      {/* Sidebar Navigation */}
      <nav className="fixed left-0 top-0 h-full w-20 bg-slate-900/50 border-r border-slate-800 flex flex-col items-center py-8 space-y-8">
        <div className="w-12 h-12 bg-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-500/20">
          <Shield className="text-white" size={24} />
        </div>
        <div className="space-y-6">
          <BarChart3 className="text-slate-500 hover:text-indigo-400 cursor-pointer transition-colors" size={22} />
          <Activity className="text-slate-500 hover:text-indigo-400 cursor-pointer transition-colors" size={22} />
          <TrendingUp className="text-slate-500 hover:text-indigo-400 cursor-pointer transition-colors" size={22} />
        </div>
      </nav>

      {/* Main Content */}
      <main className="pl-32 pr-12 py-12 max-w-7xl mx-auto">
        <header className="flex justify-between items-end mb-12">
          <div>
            <h1 className="text-4xl font-extrabold tracking-tight text-white mb-2">Shadow COO</h1>
            <p className="text-slate-400 text-lg">Operational Intelligence & SOP Compliance Auditor</p>
          </div>
          <button 
            onClick={runAudit}
            disabled={loading}
            className="px-8 py-4 bg-indigo-600 hover:bg-indigo-500 text-white rounded-2xl font-bold transition-all shadow-xl shadow-indigo-900/20 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-3"
          >
            {loading ? "Analyzing Operations..." : "Run Full Audit"}
          </button>
        </header>

        {auditData ? (
          <div className="grid grid-cols-12 gap-8">
            {/* Health Overview */}
            <div className="col-span-12 lg:col-span-4 space-y-8">
              <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="p-8 bg-slate-900/40 border border-slate-800 rounded-3xl backdrop-blur-xl relative overflow-hidden"
              >
                <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-600/10 blur-3xl -mr-16 -mt-16" />
                <h3 className="text-slate-400 font-semibold mb-6 flex items-center gap-2">
                  <Activity size={18} className="text-indigo-400" />
                  Operational Health
                </h3>
                <div className="flex flex-col items-center py-4">
                  <div className="text-7xl font-black text-white mb-2">{auditData.health_score}%</div>
                  <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
                    <motion.div 
                      initial={{ width: 0 }}
                      animate={{ width: `${auditData.health_score}%` }}
                      className={`h-full ${auditData.health_score > 80 ? 'bg-emerald-500' : 'bg-orange-500'}`}
                    />
                  </div>
                </div>
              </motion.div>

              <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="p-8 bg-slate-900/40 border border-slate-800 rounded-3xl"
              >
                <h3 className="text-slate-400 font-semibold mb-4">Quick Stats</h3>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-slate-500">Violations Found</span>
                    <span className="text-orange-400 font-mono font-bold">{auditData.violations.length}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-500">Tasks Audited</span>
                    <span className="text-white font-mono font-bold">{auditData.parsed_logs.length}</span>
                  </div>
                </div>
              </motion.div>
            </div>

            {/* Detailed Report */}
            <div className="col-span-12 lg:col-span-8 space-y-8">
              <motion.div 
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="p-8 bg-slate-900/40 border border-slate-800 rounded-3xl min-h-[400px]"
              >
                <h3 className="text-white text-xl font-bold mb-6 flex items-center gap-2">
                  <BarChart3 className="text-indigo-400" size={20} />
                  Executive Intelligence Report
                </h3>
                <div className="prose prose-invert max-w-none text-slate-300 leading-relaxed prose-headings:text-white prose-strong:text-indigo-400 prose-headings:mb-4">
                  <ReactMarkdown>{auditData.report}</ReactMarkdown>
                </div>
              </motion.div>

              {auditData.violations.length > 0 && (
                <motion.div 
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="space-y-4"
                >
                  <h3 className="text-white text-xl font-bold px-2">Critical Violations</h3>
                  {auditData.violations.map((v, i) => (
                    <div key={i} className="p-5 bg-orange-500/5 border border-orange-500/20 rounded-2xl flex gap-4">
                      <AlertTriangle className="text-orange-500 shrink-0" size={20} />
                      <p className="text-orange-200/80 text-sm leading-relaxed">{v}</p>
                    </div>
                  ))}
                </motion.div>
              )}
            </div>
          </div>
        ) : (
          <div className="h-[60vh] flex flex-col items-center justify-center border-2 border-dashed border-slate-800 rounded-3xl">
            <div className="p-6 bg-slate-900/50 rounded-full mb-6">
              <Activity size={48} className="text-slate-700 animate-pulse" />
            </div>
            <p className="text-slate-500 font-medium text-lg">No audit data available. Run an audit to start snooping.</p>
          </div>
        )}
      </main>
    </div>
  );
};

export default App;
