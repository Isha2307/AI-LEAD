import { useState, useEffect } from 'react'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [leads, setLeads] = useState([])
  const [stats, setStats] = useState({ total: 0, hot: 0, warm: 0, cold: 0 })
  const [loadingLeads, setLoadingLeads] = useState(false)
  const [backendOnline, setBackendOnline] = useState(false)

  // Form states
  const [pipelineInput, setPipelineInput] = useState({
    name: '',
    email: '',
    company: '',
    industry: '',
    employee_count: 50,
    lead_message: ''
  })
  
  const [emailInput, setEmailInput] = useState({
    company: '',
    requirement: '',
    budget: '',
    timeline: '',
    priority: 'Warm'
  })

  // Results states
  const [pipelineState, setPipelineState] = useState({
    loading: false,
    currentStep: 0, // 0 = idle, 1 = analyzing, 2 = scoring, 3 = writing email, 4 = finished
    error: null,
    analysis: null,
    scoring: null,
    emailContent: null
  })

  const [emailState, setEmailState] = useState({
    loading: false,
    error: null,
    result: null
  })

  const [expandedLead, setExpandedLead] = useState(null)

  // API Call helper
  const apiCall = async (url, options = {}) => {
    try {
      const response = await fetch(`/api/v1${url}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        },
        ...options
      })
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || response.statusText || 'API Call failed')
      }
      return await response.json()
    } catch (err) {
      console.error(`API Error (${url}):`, err)
      throw err
    }
  }

  // Health check
  const checkHealth = async () => {
    try {
      const res = await fetch('/api/v1/health')
      if (res.ok) {
        setBackendOnline(true)
      } else {
        setBackendOnline(false)
      }
    } catch (e) {
      setBackendOnline(false)
    }
  }

  // Fetch leads
  const fetchLeads = async () => {
    setLoadingLeads(true)
    try {
      const data = await apiCall('/leads')
      const leadsList = Array.isArray(data) ? data : (data.leads || [])
      setLeads(leadsList)
      
      // Calculate Stats
      const total = leadsList.length
      const hot = leadsList.filter(l => l.priority?.toLowerCase() === 'hot').length
      const warm = leadsList.filter(l => l.priority?.toLowerCase() === 'warm').length
      const cold = leadsList.filter(l => l.priority?.toLowerCase() === 'cold').length
      setStats({ total, hot, warm, cold })
    } catch (err) {
      console.error('Failed to fetch leads', err)
    } finally {
      setLoadingLeads(false)
    }
  }

  useEffect(() => {
    checkHealth()
    fetchLeads()
    
    // Refresh health status every 10 seconds
    const interval = setInterval(checkHealth, 10000)
    return () => clearInterval(interval)
  }, [])

  // Delete lead handler
  const handleDeleteLead = async (leadId) => {
    if (!window.confirm('Are you sure you want to delete this lead?')) return
    try {
      await apiCall(`/leads/${leadId}`, { method: 'DELETE' })
      fetchLeads()
    } catch (err) {
      alert(`Delete failed: ${err.message}`)
    }
  }

  // Run full pipeline
  const handleRunPipeline = async (e) => {
    e.preventDefault()
    setPipelineState({
      loading: true,
      currentStep: 1,
      error: null,
      analysis: null,
      scoring: null,
      emailContent: null
    })

    try {
      // Step 1: Analyze Lead
      const analysisData = await apiCall('/leads/analyze', {
        method: 'POST',
        body: JSON.stringify({
          name: pipelineInput.name,
          email: pipelineInput.email,
          company: pipelineInput.company,
          industry: pipelineInput.industry,
          employee_count: parseInt(pipelineInput.employee_count),
          lead_message: pipelineInput.lead_message
        })
      })
      
      const analysis = analysisData.analysis
      setPipelineState(prev => ({ ...prev, currentStep: 2, analysis }))

      // Step 2: Score Lead
      const analysisPayload = {
        ...analysis,
        company_name: analysis.company_name || pipelineInput.company,
        estimated_budget: analysis.estimated_budget || analysis.budget || '',
        decision_timeline: analysis.decision_timeline || analysis.timeline || '',
        engagement_level: analysis.engagement_level || analysis.urgency || '',
        technology_stack: analysis.technology_stack || [],
        key_decision_makers: analysis.key_decision_makers || [],
      }

      const scoringData = await apiCall('/leads/score', {
        method: 'POST',
        body: JSON.stringify({
          name: pipelineInput.name,
          email: pipelineInput.email,
          company: pipelineInput.company,
          industry: pipelineInput.industry,
          employee_count: parseInt(pipelineInput.employee_count),
          lead_message: pipelineInput.lead_message,
          analysis: analysisPayload
        })
      })

      const scoring = scoringData.scoring
      const priority = scoring.priority || 'Cold'
      setPipelineState(prev => ({ ...prev, currentStep: 3, scoring }))

      // Step 3: Generate outreach email
      const emailData = await apiCall('/leads/generate-email', {
        method: 'POST',
        body: JSON.stringify({
          company: pipelineInput.company,
          requirement: analysis.requirement || pipelineInput.lead_message.substring(0, 150),
          budget: analysis.budget || analysis.estimated_budget || 'TBD',
          timeline: analysis.timeline || analysis.decision_timeline || 'TBD',
          priority: priority
        })
      })

      setPipelineState(prev => ({
        ...prev,
        currentStep: 4,
        emailContent: emailData.email_content,
        loading: false
      }))
      
      // Refresh lead directory
      fetchLeads()

    } catch (err) {
      setPipelineState(prev => ({
        ...prev,
        error: err.message,
        loading: false,
        currentStep: 0
      }))
    }
  }

  // Generate Email Only
  const handleGenerateEmail = async (e) => {
    e.preventDefault()
    setEmailState({ loading: true, error: null, result: null })
    try {
      const emailData = await apiCall('/leads/generate-email', {
        method: 'POST',
        body: JSON.stringify({
          company: emailInput.company,
          requirement: emailInput.requirement,
          budget: emailInput.budget || 'TBD',
          timeline: emailInput.timeline || 'TBD',
          priority: emailInput.priority
        })
      })
      setEmailState({
        loading: false,
        error: null,
        result: emailData.email_content
      })
    } catch (err) {
      setEmailState({
        loading: false,
        error: err.message,
        result: null
      })
    }
  }

  // Render Priority Badge
  const renderPriorityBadge = (priority) => {
    const p = (priority || '').trim().toLowerCase()
    if (p === 'hot') return <span className="badge badge-hot">🔥 Hot</span>
    if (p === 'warm') return <span className="badge badge-warm">🔶 Warm</span>
    if (p === 'cold') return <span className="badge badge-cold">❄️ Cold</span>
    return <span className="badge badge-unknown">— Unknown</span>
  }

  // Download Email helper
  const downloadEmail = (subject, emailBody, company) => {
    const element = document.createElement("a")
    const file = new Blob([`Subject: ${subject}\n\n${emailBody}`], {type: 'text/plain'})
    element.href = URL.createObjectURL(file)
    element.download = `email_${(company || 'lead').toLowerCase().replace(/\s+/g, '_')}.txt`
    document.body.appendChild(element)
    element.click()
    document.body.removeChild(element)
  }

  return (
    <div className="app-container">
      {/* --- Sidebar Navigation --- */}
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-icon">🤖</span>
          <span className="brand-title">AI Lead Qualifier</span>
        </div>
        
        <ul className="nav-list">
          <li className="nav-item">
            <button 
              className={`nav-link ${activeTab === 'dashboard' ? 'active' : ''}`}
              onClick={() => setActiveTab('dashboard')}
            >
              🏠 Dashboard
            </button>
          </li>
          <li className="nav-item">
            <button 
              className={`nav-link ${activeTab === 'pipeline' ? 'active' : ''}`}
              onClick={() => setActiveTab('pipeline')}
            >
              🔄 Full Pipeline
            </button>
          </li>
          <li className="nav-item">
            <button 
              className={`nav-link ${activeTab === 'email' ? 'active' : ''}`}
              onClick={() => setActiveTab('email')}
            >
              ✉️ Generate Email
            </button>
          </li>
          <li className="nav-item">
            <button 
              className={`nav-link ${activeTab === 'leads' ? 'active' : ''}`}
              onClick={() => setActiveTab('leads')}
            >
              📂 All Leads
            </button>
          </li>
        </ul>

        <div className="sidebar-footer">
          <div style={{ marginBottom: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px' }}>
            <span style={{ height: '8px', width: '8px', borderRadius: '50%', backgroundColor: backendOnline ? '#10b981' : '#ef4444', display: 'inline-block' }}></span>
            <span>{backendOnline ? 'Backend Online' : 'Backend Offline'}</span>
          </div>
          <span>Powered by Gemini AI</span>
        </div>
      </aside>

      {/* --- Main Workspace --- */}
      <main className="main-content">
        
        {/* === TAB: Dashboard === */}
        {activeTab === 'dashboard' && (
          <div>
            <h1>Dashboard</h1>
            <p className="page-subtitle">Intelligent lead analysis, scoring, and automated outreach.</p>
            
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-value">{stats.total}</div>
                <div className="stat-label">Total Leads</div>
              </div>
              <div className="stat-card">
                <div className="stat-value" style={{ color: 'var(--color-hot)' }}>{stats.hot}</div>
                <div className="stat-label">🔥 Hot Leads</div>
              </div>
              <div className="stat-card">
                <div className="stat-value" style={{ color: 'var(--color-warm)' }}>{stats.warm}</div>
                <div className="stat-label">🔶 Warm Leads</div>
              </div>
              <div className="stat-card">
                <div className="stat-value" style={{ color: 'var(--color-cold)' }}>{stats.cold}</div>
                <div className="stat-label">❄️ Cold Leads</div>
              </div>
            </div>

            <div className="card">
              <h2 style={{ color: 'var(--color-text-white)', marginTop: 0 }}>Project Features</h2>
              <ul style={{ paddingLeft: '20px', lineHeight: '1.8' }}>
                <li><strong>🔍 Lead Analysis Agent:</strong> Extracts structured insights (budget, timeline, pain points) from text logs.</li>
                <li><strong>⭐ Lead Scoring Agent:</strong> Generates a rating between 0–100 and prioritizes followups.</li>
                <li><strong>✉️ B2B outreach copywriter:</strong> Drafts highly personalized business proposals.</li>
              </ul>
            </div>
          </div>
        )}

        {/* === TAB: Full Pipeline === */}
        {activeTab === 'pipeline' && (
          <div>
            <h1>Full Qualification Pipeline</h1>
            <p className="page-subtitle">Submit lead details to run the analysis, scoring, and outreach copywriter in sequence.</p>
            
            <div className="card">
              <form onSubmit={handleRunPipeline}>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                  <div className="form-group">
                    <label className="form-label">Contact Name</label>
                    <input 
                      type="text" 
                      required 
                      className="form-control" 
                      value={pipelineInput.name} 
                      onChange={e => setPipelineInput({ ...pipelineInput, name: e.target.value })} 
                      placeholder="e.g. Sarah Mitchell"
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Contact Email</label>
                    <input 
                      type="email" 
                      required 
                      className="form-control" 
                      value={pipelineInput.email} 
                      onChange={e => setPipelineInput({ ...pipelineInput, email: e.target.value })} 
                      placeholder="e.g. s.mitchell@nexasoft.io"
                    />
                  </div>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr', gap: '16px' }}>
                  <div className="form-group">
                    <label className="form-label">Company Name</label>
                    <input 
                      type="text" 
                      required 
                      className="form-control" 
                      value={pipelineInput.company} 
                      onChange={e => setPipelineInput({ ...pipelineInput, company: e.target.value })} 
                      placeholder="e.g. NexaSoft Technologies"
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Industry</label>
                    <input 
                      type="text" 
                      className="form-control" 
                      value={pipelineInput.industry} 
                      onChange={e => setPipelineInput({ ...pipelineInput, industry: e.target.value })} 
                      placeholder="e.g. SaaS"
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Employee Count</label>
                    <input 
                      type="number" 
                      className="form-control" 
                      value={pipelineInput.employee_count} 
                      onChange={e => setPipelineInput({ ...pipelineInput, employee_count: e.target.value })} 
                      placeholder="50"
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label className="form-label">Inbound Request / Pitch Message</label>
                  <textarea 
                    required 
                    className="form-control" 
                    value={pipelineInput.lead_message} 
                    onChange={e => setPipelineInput({ ...pipelineInput, lead_message: e.target.value })} 
                    placeholder="Describe their request, pain points, budget, timeline if mentioned..."
                  />
                </div>

                <button type="submit" className="btn" disabled={pipelineState.loading}>
                  {pipelineState.loading ? <div className="spinner"></div> : 'Launch AI Agents Pipeline'}
                </button>
              </form>
            </div>

            {/* Pipeline Step Progress tracker */}
            {pipelineState.loading && (
              <div className="card steps-container">
                <div className={`step-card ${pipelineState.currentStep >= 1 ? 'active' : ''}`}>
                  <div className="step-header">
                    <span className="step-title">Step 1: Extracting Lead Insights</span>
                    {pipelineState.currentStep === 1 && <div className="spinner"></div>}
                    {pipelineState.currentStep > 1 && <span style={{ color: '#10b981' }}>✓ Completed</span>}
                  </div>
                </div>
                <div className={`step-card ${pipelineState.currentStep >= 2 ? 'active' : ''}`}>
                  <div className="step-header">
                    <span className="step-title">Step 2: Scoring Lead Qualification</span>
                    {pipelineState.currentStep === 2 && <div className="spinner"></div>}
                    {pipelineState.currentStep > 2 && <span style={{ color: '#10b981' }}>✓ Completed</span>}
                  </div>
                </div>
                <div className={`step-card ${pipelineState.currentStep >= 3 ? 'active' : ''}`}>
                  <div className="step-header">
                    <span className="step-title">Step 3: Writing B2B Outreach Copy</span>
                    {pipelineState.currentStep === 3 && <div className="spinner"></div>}
                    {pipelineState.currentStep > 3 && <span style={{ color: '#10b981' }}>✓ Completed</span>}
                  </div>
                </div>
              </div>
            )}

            {pipelineState.error && (
              <div className="card" style={{ backgroundColor: 'rgba(239, 68, 68, 0.1)', borderColor: '#ef4444' }}>
                <strong style={{ color: '#ef4444' }}>Pipeline Failed:</strong> {pipelineState.error}
              </div>
            )}

            {/* Finished Pipeline Results Display */}
            {pipelineState.currentStep === 4 && pipelineState.scoring && (
              <div>
                <h2 style={{ color: 'var(--color-text-white)', marginTop: '32px' }}>🎯 Pipeline Evaluation Results</h2>
                
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '16px', marginBottom: '24px' }}>
                  <div className="stat-card">
                    <div className="stat-value">{pipelineState.scoring.lead_score}/100</div>
                    <div className="stat-label">Lead Score</div>
                  </div>
                  <div className="stat-card">
                    <div className="stat-value">{renderPriorityBadge(pipelineState.scoring.priority)}</div>
                    <div className="stat-label">Outreach Priority</div>
                  </div>
                  <div className="stat-card">
                    <div className="stat-value">{pipelineState.scoring.confidence}%</div>
                    <div className="stat-label">Model Confidence</div>
                  </div>
                </div>

                <div className="card">
                  <h3 style={{ color: 'var(--color-text-white)', marginTop: 0 }}>📋 Agent Reasoning</h3>
                  <ul style={{ paddingLeft: '20px', lineHeight: '1.8' }}>
                    {(pipelineState.scoring.reasoning || []).map((r, i) => <li key={i}>{r}</li>)}
                  </ul>
                </div>

                {pipelineState.emailContent && (
                  <div className="card">
                    <h3 style={{ color: 'var(--color-text-white)', marginTop: 0 }}>✉️ Suggested Proposal</h3>
                    <div className="email-box">
                      <div className="email-subject">Subject: {pipelineState.emailContent.subject}</div>
                      <div style={{ borderTop: '1px solid var(--color-border)', margin: '12px 0' }}></div>
                      {pipelineState.emailContent.email}
                    </div>
                    <button 
                      className="btn" 
                      onClick={() => downloadEmail(pipelineState.emailContent.subject, pipelineState.emailContent.email, pipelineInput.company)}
                    >
                      Download Pitch Email
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* === TAB: Email Writer === */}
        {activeTab === 'email' && (
          <div>
            <h1>Email Generator</h1>
            <p className="page-subtitle">Draft a highly-targeted sales email adapted for a specific prospect priority status.</p>

            <div className="card">
              <form onSubmit={handleGenerateEmail}>
                <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '16px' }}>
                  <div className="form-group">
                    <label className="form-label">Company Name</label>
                    <input 
                      type="text" 
                      required 
                      className="form-control" 
                      value={emailInput.company} 
                      onChange={e => setEmailInput({ ...emailInput, company: e.target.value })} 
                      placeholder="e.g. NexaSoft Technologies"
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Lead Priority</label>
                    <select 
                      className="form-control"
                      value={emailInput.priority}
                      onChange={e => setEmailInput({ ...emailInput, priority: e.target.value })}
                    >
                      <option value="Hot">🔥 Hot</option>
                      <option value="Warm">🔶 Warm</option>
                      <option value="Cold">❄️ Cold</option>
                    </select>
                  </div>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                  <div className="form-group">
                    <label className="form-label">Budget Details</label>
                    <input 
                      type="text" 
                      className="form-control" 
                      value={emailInput.budget} 
                      onChange={e => setEmailInput({ ...emailInput, budget: e.target.value })} 
                      placeholder="e.g. $150K"
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Timeline Details</label>
                    <input 
                      type="text" 
                      className="form-control" 
                      value={emailInput.timeline} 
                      onChange={e => setEmailInput({ ...emailInput, timeline: e.target.value })} 
                      placeholder="e.g. Q3 2025"
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label className="form-label">Core Requirement</label>
                  <textarea 
                    required 
                    className="form-control" 
                    value={emailInput.requirement} 
                    onChange={e => setEmailInput({ ...emailInput, requirement: e.target.value })} 
                    placeholder="What project scope or technology solution is the client looking for?"
                  />
                </div>

                <button type="submit" className="btn" disabled={emailState.loading}>
                  {emailState.loading ? <div className="spinner"></div> : 'Draft Proposal Copy'}
                </button>
              </form>
            </div>

            {emailState.error && (
              <div className="card" style={{ backgroundColor: 'rgba(239, 68, 68, 0.1)', borderColor: '#ef4444' }}>
                <strong style={{ color: '#ef4444' }}>Error:</strong> {emailState.error}
              </div>
            )}

            {emailState.result && (
              <div className="card">
                <h3 style={{ color: 'var(--color-text-white)', marginTop: 0 }}>✉️ Proposal Template</h3>
                <div className="email-box">
                  <div className="email-subject">Subject: {emailState.result.subject}</div>
                  <div style={{ borderTop: '1px solid var(--color-border)', margin: '12px 0' }}></div>
                  {emailState.result.email}
                </div>
                <button 
                  className="btn" 
                  onClick={() => downloadEmail(emailState.result.subject, emailState.result.email, emailInput.company)}
                >
                  Download Proposal Email
                </button>
              </div>
            )}
          </div>
        )}

        {/* === TAB: Leads Directory === */}
        {activeTab === 'leads' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
              <div>
                <h1 style={{ margin: 0 }}>Lead Directory</h1>
                <p className="page-subtitle" style={{ margin: 0 }}>Browse all qualification logs saved in the database.</p>
              </div>
              <button 
                className="btn" 
                style={{ width: 'auto', padding: '10px 20px' }} 
                onClick={fetchLeads}
                disabled={loadingLeads}
              >
                {loadingLeads ? 'Refreshing...' : '🔄 Refresh List'}
              </button>
            </div>

            {loadingLeads && leads.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '40px' }}>
                <div className="spinner" style={{ margin: '0 auto 16px', width: '28px', height: '28px' }}></div>
                <p>Loading database entries...</p>
              </div>
            ) : leads.length === 0 ? (
              <div className="card" style={{ textAlign: 'center', padding: '40px' }}>
                <p style={{ color: 'var(--color-text-muted)', marginBottom: '16px' }}>No leads saved in the database yet.</p>
                <button className="btn" style={{ width: 'auto' }} onClick={() => setActiveTab('pipeline')}>
                  Qualify your First Lead
                </button>
              </div>
            ) : (
              <div>
                {leads.map((lead) => {
                  const leadId = lead.id || lead._id;
                  const isExpanded = expandedLead === leadId;
                  
                  return (
                    <div key={leadId} className="lead-expander">
                      <div 
                        className="lead-header" 
                        onClick={() => setExpandedLead(isExpanded ? null : leadId)}
                      >
                        <div className="lead-title-area">
                          <strong style={{ color: 'var(--color-text-white)' }}>{lead.name}</strong>
                          <span style={{ color: 'var(--color-text-muted)' }}>@{lead.company}</span>
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                          <span>Score: <strong>{lead.lead_score ?? '—'}</strong></span>
                          {renderPriorityBadge(lead.priority)}
                          <span style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>
                            {isExpanded ? '▲' : '▼'}
                          </span>
                        </div>
                      </div>
                      
                      {isExpanded && (
                        <div className="lead-body">
                          <div className="lead-grid" style={{ marginBottom: '20px' }}>
                            <div>
                              <span className="form-label" style={{ marginBottom: '4px' }}>Email Address</span>
                              <span>{lead.email}</span>
                            </div>
                            <div>
                              <span className="form-label" style={{ marginBottom: '4px' }}>Status</span>
                              <span style={{ textTransform: 'capitalize' }}>{lead.status}</span>
                            </div>
                            <div>
                              <span className="form-label" style={{ marginBottom: '4px' }}>Industry</span>
                              <span>{lead.industry || '—'}</span>
                            </div>
                          </div>
                          
                          {lead.email_subject && (
                            <div style={{ marginBottom: '20px' }}>
                              <span className="form-label" style={{ marginBottom: '4px' }}>Outreach Pitch</span>
                              <div className="email-box" style={{ fontSize: '0.85rem' }}>
                                <div className="email-subject">Subject: {lead.email_subject}</div>
                                <div style={{ borderTop: '1px solid var(--color-border)', margin: '8px 0' }}></div>
                                {lead.email_body}
                              </div>
                              <button 
                                className="btn" 
                                style={{ width: 'auto', padding: '8px 16px', fontSize: '0.85rem' }}
                                onClick={() => downloadEmail(lead.email_subject, lead.email_body, lead.company)}
                              >
                                Download Copy
                              </button>
                            </div>
                          )}

                          <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '16px' }}>
                            <button 
                              className="btn" 
                              style={{ width: 'auto', backgroundColor: '#ef4444', backgroundImage: 'none', padding: '8px 16px', fontSize: '0.85rem' }}
                              onClick={() => handleDeleteLead(leadId)}
                            >
                              🗑 Delete Entry
                            </button>
                          </div>
                        </div>
                      )}
                    </div>
                  )
                })}
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  )
}

export default App

