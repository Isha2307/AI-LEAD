"use client";

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Terminal, ShieldAlert, Cpu, Sparkles, Send, Database, 
  BarChart, ArrowRight, User, Mail, Briefcase, Building2,
  CheckCircle2, XCircle
} from 'lucide-react';

export default function Home() {
  const [activeTab, setActiveTab] = useState<'pipeline' | 'directory' | 'integration'>('pipeline');
  const [emailText, setEmailText] = useState('');
  const [processing, setProcessing] = useState(false);
  const [results, setResults] = useState<any>(null);
  const [leads, setLeads] = useState<any[]>([]);

  // Fetch leads
  useEffect(() => {
    if (activeTab === 'directory') {
      fetchLeads();
    }
  }, [activeTab]);

  const fetchLeads = async () => {
    try {
      const res = await fetch('/api/v1/leads');
      if (res.ok) {
        const data = await res.json();
        setLeads(data);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const runPipeline = async () => {
    if (!emailText) return;
    setProcessing(true);
    setResults(null);
    try {
      // Step 1: Analyze Email
      const analyzeRes = await fetch('/api/v1/leads/analyze-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email_content: emailText })
      });
      if (!analyzeRes.ok) {
        const errData = await analyzeRes.json().catch(() => ({}));
        throw new Error(errData.detail || "Failed to analyze email");
      }
      const analyzeData = await analyzeRes.json();

      // Step 2: Score Lead
      const scoreRes = await fetch('/api/v1/leads/score', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: analyzeData.name,
          email: analyzeData.email,
          company: analyzeData.company,
          industry: analyzeData.industry,
          employee_count: analyzeData.employee_count,
          lead_message: analyzeData.lead_message,
          analysis: analyzeData.analysis
        })
      });
      if (!scoreRes.ok) {
        const errData = await scoreRes.json().catch(() => ({}));
        throw new Error(errData.detail || "Failed to score lead");
      }
      const scoreData = await scoreRes.json();

      // Step 3: Generate Outreach Email
      const generateRes = await fetch('/api/v1/leads/generate-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          company: analyzeData.company,
          requirement: analyzeData.lead_message,
          budget: "Unknown", // Can extract if needed
          timeline: "As soon as possible",
          priority: scoreData.scoring.priority
        })
      });
      let drafted_email_subject = null;
      let drafted_email_body = null;
      if (generateRes.ok) {
        const generateData = await generateRes.json();
        drafted_email_subject = generateData.email_content.subject;
        drafted_email_body = generateData.email_content.email;
      }

      // Combine results for UI
      setResults({
        name: analyzeData.name,
        company: analyzeData.company,
        industry: analyzeData.industry,
        company_research: analyzeData.analysis.company_research,
        analysis: analyzeData.analysis.analysis,
        lead_score: scoreData.scoring.lead_score,
        priority: scoreData.scoring.priority,
        confidence: scoreData.scoring.confidence,
        success_probability: scoreData.scoring.success_probability,
        scoring_reasoning: scoreData.scoring.reasoning,
        drafted_email_subject,
        drafted_email_body
      });

    } catch (e: any) {
      console.error("Pipeline Error:", e);
      alert(e.message || "Failed to execute pipeline. Check console logs.");
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-brand-dark bg-mesh-glow relative text-brand-text-main font-sans selection:bg-brand-primary/30">
      
      {/* Navbar */}
      <nav className="fixed top-0 w-full z-50 glass-card !rounded-none !border-x-0 !border-t-0 !bg-brand-dark/80 px-8 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-brand-primary to-brand-secondary flex items-center justify-center">
            <Sparkles className="w-4 h-4 text-white" />
          </div>
          <span className="text-xl font-bold tracking-wide">AI<span className="font-light">Lead</span></span>
        </div>
        
        <div className="hidden md:flex items-center gap-8 text-sm font-medium text-brand-text-muted">
          <button onClick={() => setActiveTab('pipeline')} className={`transition-colors ${activeTab === 'pipeline' ? 'text-white' : 'hover:text-white'}`}>Intelligence Pipeline</button>
          <button onClick={() => setActiveTab('directory')} className={`transition-colors ${activeTab === 'directory' ? 'text-white' : 'hover:text-white'}`}>Lead Directory</button>
          <button onClick={() => setActiveTab('integration')} className={`transition-colors ${activeTab === 'integration' ? 'text-white' : 'hover:text-white'}`}>Integration</button>
        </div>
        
        {/* Placeholder for alignment if needed, or remove completely */}
        <div className="w-20" />
      </nav>

      {/* Main Content */}
      <main className="pt-32 pb-24 px-8 max-w-7xl mx-auto relative z-10">
        
        {/* Hero Section */}
        <div className="text-center mb-16 space-y-6">
          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-5xl md:text-7xl font-bold tracking-tight text-gradient pb-2"
          >
            One go-to partner who<br/>orchestrates and delivers.
          </motion.h1>
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="text-lg md:text-xl text-brand-text-muted max-w-2xl mx-auto"
          >
            Automated intelligence routing, lead scoring, and automated outreach via Gemini models. 
          </motion.p>
        </div>

        {/* Dynamic Content */}
        <AnimatePresence mode="wait">
          {activeTab === 'pipeline' && (
            <motion.div 
              key="pipeline"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="space-y-8"
            >
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                
                {/* Input Section */}
                <div className="lg:col-span-1 glass-card p-6 flex flex-col h-[500px]">
                  <div className="flex items-center gap-3 mb-6">
                    <Terminal className="w-5 h-5 text-brand-primary" />
                    <h2 className="text-lg font-semibold">Raw Data Ingestion</h2>
                  </div>
                  <textarea 
                    value={emailText}
                    onChange={(e) => setEmailText(e.target.value)}
                    placeholder="Paste incoming raw email here..."
                    className="flex-1 w-full bg-brand-dark/50 border border-brand-border rounded-xl p-4 text-sm resize-none focus:outline-none focus:border-brand-primary transition-colors text-gray-300 placeholder-gray-600 font-mono"
                  />
                  <button 
                    onClick={runPipeline}
                    disabled={processing || !emailText}
                    className="mt-4 w-full py-3 rounded-xl bg-white text-black font-bold flex items-center justify-center gap-2 hover:bg-gray-200 transition-colors disabled:opacity-50 disabled:bg-gray-500 disabled:text-gray-900"
                  >
                    {processing ? (
                      <span className="flex items-center gap-2">
                        <Cpu className="w-4 h-4 animate-spin" /> Processing AI Models...
                      </span>
                    ) : (
                      <span className="flex items-center gap-2">
                        Execute Pipeline <ArrowRight className="w-4 h-4" />
                      </span>
                    )}
                  </button>
                </div>

                {/* Results Section */}
                <div className="lg:col-span-2 glass-card p-6 min-h-[500px] flex flex-col">
                  <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center gap-3">
                      <BarChart className="w-5 h-5 text-brand-secondary" />
                      <h2 className="text-lg font-semibold">Intelligence Output</h2>
                    </div>
                  </div>

                  {!results && !processing && (
                    <div className="flex-1 flex flex-col items-center justify-center text-brand-text-muted border-2 border-dashed border-brand-border rounded-xl">
                      <Database className="w-12 h-12 mb-4 opacity-50" />
                      <p>Awaiting data ingestion. Run pipeline to extract insights.</p>
                    </div>
                  )}

                  {processing && (
                    <div className="flex-1 flex flex-col items-center justify-center space-y-6">
                      <div className="w-24 h-24 rounded-full border-4 border-brand-border border-t-brand-primary animate-spin" />
                      <p className="text-brand-primary animate-pulse font-mono">Running neural network analysis...</p>
                    </div>
                  )}

                  {results && !processing && (
                    <motion.div 
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="space-y-6 flex-1 overflow-y-auto pr-2 custom-scrollbar"
                    >
                      {/* Metric Cards */}
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div className="bg-brand-dark/80 rounded-xl p-4 border border-brand-border">
                          <p className="text-xs text-brand-text-muted mb-1 uppercase tracking-wider">Lead Score</p>
                          <p className="text-3xl font-bold text-white">{results.lead_score}<span className="text-sm text-gray-500 font-normal">/100</span></p>
                        </div>
                        <div className="bg-brand-dark/80 rounded-xl p-4 border border-brand-border">
                          <p className="text-xs text-brand-text-muted mb-1 uppercase tracking-wider">Priority</p>
                          <p className={`text-xl font-bold mt-2 ${results.priority === 'Hot' ? 'text-orange-400' : results.priority === 'Warm' ? 'text-yellow-400' : 'text-blue-400'}`}>
                            {results.priority}
                          </p>
                        </div>
                        <div className="bg-brand-dark/80 rounded-xl p-4 border border-brand-border">
                          <p className="text-xs text-brand-text-muted mb-1 uppercase tracking-wider">Confidence</p>
                          <p className="text-3xl font-bold text-white">{results.confidence}%</p>
                        </div>
                        <div className="bg-brand-dark/80 rounded-xl p-4 border border-brand-border">
                          <p className="text-xs text-brand-text-muted mb-1 uppercase tracking-wider">Success Prob</p>
                          <p className="text-3xl font-bold text-brand-secondary">{results.success_probability || 0}%</p>
                        </div>
                      </div>

                      {/* Company Info */}
                      <div className="bg-brand-dark/80 rounded-xl p-5 border border-brand-border">
                        <h3 className="text-sm font-semibold text-brand-text-muted uppercase tracking-wider mb-4 flex items-center gap-2">
                          <Building2 className="w-4 h-4" /> Company Intelligence
                        </h3>
                        <div className="grid grid-cols-2 gap-y-4 text-sm">
                          <div>
                            <p className="text-gray-500">Contact</p>
                            <p className="font-medium text-white">{results.name}</p>
                          </div>
                          <div>
                            <p className="text-gray-500">Company</p>
                            <p className="font-medium text-white">{results.company}</p>
                          </div>
                          <div className="col-span-2">
                            <p className="text-gray-500">Industry</p>
                            <p className="font-medium text-white">{results.industry}</p>
                          </div>
                          <div className="col-span-2 mt-2">
                            <p className="text-gray-500 mb-1">Company Profile Research</p>
                            <p className="text-gray-300 leading-relaxed bg-[#0a0a14] p-4 rounded-lg border border-white/5">{results.company_research || "No external profile generated."}</p>
                          </div>
                        </div>
                      </div>

                      {/* AI Analysis */}
                      <div className="bg-brand-dark/80 rounded-xl p-5 border border-brand-border">
                        <h3 className="text-sm font-semibold text-brand-text-muted uppercase tracking-wider mb-4 flex items-center gap-2">
                          <Sparkles className="w-4 h-4" /> AI Analysis & Reasoning
                        </h3>
                        <p className="text-sm text-gray-300 leading-relaxed">
                          {results.analysis}
                        </p>
                        <div className="mt-4 flex flex-wrap gap-2">
                          {results.scoring_reasoning?.map((reason: string, i: number) => (
                            <span key={i} className="px-3 py-1 bg-brand-primary/10 text-brand-primary text-xs rounded-full border border-brand-primary/20">
                              {reason}
                            </span>
                          ))}
                        </div>
                      </div>

                      {/* Drafted Email */}
                      {results.drafted_email_subject && (
                        <div className="bg-brand-dark/80 rounded-xl p-5 border border-brand-border relative overflow-hidden">
                          <div className="absolute top-0 left-0 w-1 h-full bg-brand-secondary" />
                          <h3 className="text-sm font-semibold text-brand-text-muted uppercase tracking-wider mb-4 flex items-center gap-2">
                            <Send className="w-4 h-4" /> Auto-Drafted Outreach
                          </h3>
                          <div className="mb-3">
                            <span className="text-xs text-gray-500">Subject:</span>
                            <p className="font-medium text-white">{results.drafted_email_subject}</p>
                          </div>
                          <div className="bg-[#0a0a14] p-4 rounded-lg text-sm text-gray-300 whitespace-pre-wrap border border-white/5 font-mono">
                            {results.drafted_email_body}
                          </div>
                        </div>
                      )}

                    </motion.div>
                  )}
                </div>
              </div>
            </motion.div>
          )}
          {activeTab === 'directory' && (
            <motion.div 
              key="directory"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="glass-card p-8"
            >
              <div className="flex items-center justify-between mb-8">
                <div>
                  <h2 className="text-2xl font-bold text-white mb-1">Lead Directory</h2>
                  <p className="text-brand-text-muted text-sm">Historically processed records and AI intelligence</p>
                </div>
                <button onClick={fetchLeads} className="px-4 py-2 bg-brand-dark border border-brand-border rounded-lg text-sm hover:bg-gray-800 transition-colors">
                  Refresh Data
                </button>
              </div>

              {leads.length === 0 ? (
                <div className="text-center py-12 text-gray-500">
                  <Database className="w-12 h-12 mx-auto mb-4 opacity-50" />
                  <p>No leads found in database.</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {leads.map((lead) => (
                    <div key={lead.id} className="bg-brand-dark/60 rounded-xl border border-brand-border p-5 hover:border-brand-primary/50 transition-colors group">
                      <div className="flex justify-between items-start mb-4">
                        <div>
                          <h3 className="text-lg font-bold text-white group-hover:text-brand-primary transition-colors">{lead.name}</h3>
                          <p className="text-sm text-gray-400">{lead.company}</p>
                        </div>
                        <span className={`px-2 py-1 text-xs font-bold rounded-md ${lead.priority === 'Hot' ? 'bg-orange-500/20 text-orange-400' : lead.priority === 'Warm' ? 'bg-yellow-500/20 text-yellow-400' : 'bg-blue-500/20 text-blue-400'}`}>
                          {lead.priority}
                        </span>
                      </div>
                      
                      <div className="space-y-3 text-sm">
                        <div className="flex justify-between border-b border-white/5 pb-2">
                          <span className="text-gray-500">Lead Score</span>
                          <span className="font-semibold text-white">{lead.lead_score}/100</span>
                        </div>
                        <div className="flex justify-between border-b border-white/5 pb-2">
                          <span className="text-gray-500">Success Prob.</span>
                          <span className="font-semibold text-brand-secondary">{lead.success_probability || 0}%</span>
                        </div>
                        <div className="flex justify-between pb-2">
                          <span className="text-gray-500">Industry</span>
                          <span className="font-medium text-gray-300 truncate max-w-[120px]">{lead.industry}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </motion.div>
          )}
          {activeTab === 'integration' && (
            <motion.div 
              key="integration"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="glass-card p-8 min-h-[500px]"
            >
              <div className="text-center max-w-2xl mx-auto mb-12">
                <h2 className="text-3xl font-bold text-white mb-4">Connect Your Stack</h2>
                <p className="text-brand-text-muted">Seamlessly route AI-qualified leads and drafted outreach emails into your existing CRM and sales orchestration tools.</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {[
                  { name: 'Salesforce', desc: 'Sync leads and scores directly to Salesforce CRM objects.', status: 'Connected' },
                  { name: 'HubSpot', desc: 'Trigger HubSpot workflows and update deal stages.', status: 'Coming Soon' },
                  { name: 'Slack', desc: 'Get instant notifications for Hot priority leads.', status: 'Coming Soon' }
                ].map((intg, i) => (
                  <div key={i} className="bg-brand-dark/60 rounded-xl border border-brand-border p-6 hover:border-brand-primary/50 transition-colors flex flex-col justify-between">
                    <div>
                      <div className="w-12 h-12 bg-white/5 rounded-lg flex items-center justify-center mb-4">
                        <Database className="w-6 h-6 text-brand-primary" />
                      </div>
                      <h3 className="text-xl font-bold text-white mb-2">{intg.name}</h3>
                      <p className="text-sm text-gray-400 mb-6">{intg.desc}</p>
                    </div>
                    <button className={`w-full py-2 rounded-lg text-sm font-semibold border ${intg.status === 'Connected' ? 'border-white text-black bg-white hover:bg-gray-200' : 'border-gray-800 text-gray-500 bg-transparent hover:bg-white/5 hover:text-gray-300'} transition-colors`}>
                      {intg.status}
                    </button>
                  </div>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

      </main>

      {/* Decorative Background Elements */}
      <div className="fixed top-[20%] left-[10%] w-72 h-72 bg-brand-primary/20 rounded-full blur-[120px] pointer-events-none" />
      <div className="fixed bottom-[10%] right-[10%] w-96 h-96 bg-brand-secondary/20 rounded-full blur-[120px] pointer-events-none" />
    </div>
  );
}
