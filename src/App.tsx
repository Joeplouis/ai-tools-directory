import { useState, useEffect, useMemo } from 'react'

const CATEGORIES = [
  { id: 'All', name: 'All Tools', icon: '🧠', color: '#D4AF37', desc: 'Every AI tool in one place' },
  { id: 'Text & Writing', name: 'Text & Writing', icon: '✍️', color: '#06b6d4', desc: 'Copy, content, grammar, prompts' },
  { id: 'Image Generation', name: 'Image Generation', icon: '🖼️', color: '#ec4899', desc: 'AI art, photos, design' },
  { id: 'Video & Animation', name: 'Video & Animation', icon: '🎬', color: '#f97316', desc: 'Video generation & editing' },
  { id: 'Voice & Audio', name: 'Voice & Audio', icon: '🎙️', color: '#8b5cf6', desc: 'TTS, music, voice cloning' },
  { id: 'Coding & Dev', name: 'Coding & Dev', icon: '💻', color: '#10b981', desc: 'Code, APIs, dev tools' },
  { id: 'Marketing & Sales', name: 'Marketing & Sales', icon: '📈', color: '#f59e0b', desc: 'SEO, ads, lead gen, funnels' },
  { id: 'Productivity', name: 'Productivity', icon: '⚡', color: '#3b82f6', desc: 'Slides, docs, sheets, tasks' },
  { id: 'AI Agents & Automation', name: 'AI Agents', icon: '🤖', color: '#14b8a6', desc: 'Bots, workflows, automation' },
  { id: 'Research & Analytics', name: 'Research & Data', icon: '🔬', color: '#6366f1', desc: 'Analysis, data, research' },
  { id: 'Business & Finance', name: 'Business & Finance', icon: '💼', color: '#84cc16', desc: 'Investing, trading, business' },
  { id: 'Design & Art', name: 'Design & Art', icon: '🎨', color: '#e11d48', desc: '3D, logo, brand, UI design' },
  { id: 'Education & Learning', name: 'Education', icon: '📚', color: '#0ea5e9', desc: 'Courses, learning, tutoring' },
  { id: 'Other', name: 'Other', icon: '🔧', color: '#6b7280', desc: 'Miscellaneous AI tools' },
]

const SAMPLE_TOOLS = [
  { name: 'ChatGPT', category: 'Text & Writing', pricing: 'freemium', description: 'OpenAI\'s conversational AI — the most widely used AI assistant for writing, coding, analysis, and brainstorming.', website: 'https://chat.openai.com', views: 98000000, author: 'OpenAI' },
  { name: 'Claude', category: 'Text & Writing', pricing: 'freemium', description: 'Anthropic\'s AI assistant known for nuanced reasoning, long-form writing, and thoughtful analysis. Great for complex tasks.', website: 'https://claude.ai', views: 42000000, author: 'Anthropic' },
  { name: 'Midjourney', category: 'Image Generation', pricing: 'paid', description: 'AI image generator known for artistic, high-quality visuals. Creates stunning artwork from text descriptions.', website: 'https://midjourney.com', views: 28000000, author: 'Midjourney' },
  { name: 'DALL-E 3', category: 'Image Generation', pricing: 'freemium', description: 'OpenAI\'s image generation model — creates photorealistic and artistic images from natural language prompts.', website: 'https://openai.com/dall-e-3', views: 22000000, author: 'OpenAI' },
  { name: 'Runway ML', category: 'Video & Animation', pricing: 'freemium', description: 'AI-powered video editing and generation platform. Text-to-video, motion tracking, and film-quality effects.', website: 'https://runwayml.com', views: 14000000, author: 'Runway ML' },
  { name: 'ElevenLabs', category: 'Voice & Audio', pricing: 'freemium', description: 'AI voice synthesis and voice cloning. Creates natural speech in 29 languages. Used for voiceovers, audiobooks, and AI calling.', website: 'https://elevenlabs.io', views: 9800000, author: 'ElevenLabs' },
  { name: 'Cursor', category: 'Coding & Dev', pricing: 'freemium', description: 'AI-first code editor built on Claude. Write, edit, and understand code with full AI context awareness.', website: 'https://cursor.sh', views: 8500000, author: 'Cursor' },
  { name: 'GitHub Copilot', category: 'Coding & Dev', pricing: 'paid', description: 'Microsoft\'s AI pair programmer. Integrates into VS Code and GitHub. Autocomplete, refactoring, and full function generation.', website: 'https://github.com/features/copilot', views: 31000000, author: 'Microsoft' },
  { name: 'Jasper', category: 'Marketing & Sales', pricing: 'paid', description: 'Enterprise AI writing platform for marketing teams. Generates blog posts, ads, emails, and social media content at scale.', website: 'https://jasper.ai', views: 7400000, author: 'Jasper' },
  { name: 'Notion AI', category: 'Productivity', pricing: 'paid', description: 'AI writing assistant built into Notion. Summarize, write, brainstorm, and automate knowledge work inside your notes.', website: 'https://notion.so', views: 19000000, author: 'Notion' },
  { name: 'Zapier', category: 'AI Agents & Automation', pricing: 'freemium', description: 'Connect 6,000+ apps with AI-powered automation. No-code workflows that automate repetitive tasks across your entire stack.', website: 'https://zapier.com', views: 15000000, author: 'Zapier' },
  { name: 'Perplexity', category: 'Research & Analytics', pricing: 'freemium', description: 'AI search engine with real-time web access. Delivers cited, factual answers with sources listed for every claim.', website: 'https://perplexity.ai', views: 25000000, author: 'Perplexity' },
  { name: 'TradingAgents', category: 'Business & Finance', pricing: 'free', description: 'Multi-agent AI trading framework with fundamentals, sentiment, technical, and risk analysis agents working together.', website: 'https://github.com/TauricResearch/TradingAgents', views: 62000, author: 'Tauric Research' },
  { name: 'Beautiful.ai', category: 'Productivity', pricing: 'paid', description: 'AI-powered presentation software that automatically designs slides. Don\'t start from scratch — let AI format your ideas.', website: 'https://beautiful.ai', views: 4200000, author: 'Beautiful.ai' },
  { name: 'Figma AI', category: 'Design & Art', pricing: 'freemium', description: 'AI design tools built into Figma. Generate layouts, suggest components, and automate design tasks inside your workflow.', website: 'https://figma.com', views: 22000000, author: 'Figma' },
  { name: 'Gamma', category: 'Productivity', pricing: 'freemium', description: 'AI presentation and document generator.输入 prompt, get a complete slide deck or webpage in seconds.', website: 'https://gamma.app', views: 6800000, author: 'Gamma' },
  { name: 'Character.ai', category: 'AI Agents & Automation', pricing: 'freemium', description: 'Create and chat with AI characters, companions, and agents. Voice calling supported. 4M+ daily active users.', website: 'https://character.ai', views: 45000000, author: 'Character.AI' },
  { name: 'Synthesia', category: 'Video & Animation', pricing: 'paid', description: 'AI video generation with virtual avatars. Create professional videos with a script — no camera or crew needed.', website: 'https://synthesia.io', views: 8900000, author: 'Synthesia' },
  { name: 'Sunroom', category: 'Voice & Audio', pricing: 'paid', description: 'Voice-controlled ambient sound and music generator. Creates adaptive audio atmospheres for focus, relaxation, or creativity.', website: 'https://sunroom.com', views: 1200000, author: 'Sunroom' },
  { name: 'Otter.ai', category: 'Voice & Audio', pricing: 'freemium', description: 'AI meeting transcription and note-taking. Automatically records, transcribes, and generates actionable meeting notes.', website: 'https://otter.ai', views: 6500000, author: 'Otter.ai' },
  { name: 'Framer', category: 'Design & Art', pricing: 'freemium', description: 'AI-powered website builder with built-in prototyping. Push to publish beautiful sites with prompts alone.', website: 'https://framer.com', views: 8700000, author: 'Framer' },
  { name: 'AdCreative.ai', category: 'Marketing & Sales', pricing: 'paid', description: 'Generate 100+ ad variants in minutes. AI-optimized for conversion across Google, Meta, and display ad networks.', website: 'https://adcreative.ai', views: 5100000, author: 'AdCreative.ai' },
  { name: 'Surfer SEO', category: 'Marketing & Sales', pricing: 'paid', description: 'AI content optimization and keyword research. Analyze top-ranking pages and tell you exactly how to outrank them.', website: 'https://surferseo.com', views: 7300000, author: 'Surfer' },
  { name: 'Dify', category: 'AI Agents & Automation', pricing: 'free', description: 'Open-source LLM app development platform. Build and deploy AI workflows, agents, and chatbots without code.', website: 'https://dify.ai', views: 98000, author: 'Dify' },
  { name: 'n8n', category: 'AI Agents & Automation', pricing: 'free', description: 'Workflow automation tool with AI agent capabilities. Connect anything to anything — 400+ integrations included.', website: 'https://n8n.io', views: 3400000, author: 'n8n' },
]

const MINIMAX_TOOLS = [
  { name: 'PPTX Maker', category: 'Productivity', pricing: 'freemium', description: 'HTML Presentation Generator Expert — creates professional multi-page HTML-PPT presentations exportable to PDF.', website: 'https://agent.minimax.io', views: 104332, author: 'MiniMax' },
  { name: 'Landing Page Builder', category: 'Design & Art', pricing: 'freemium', description: 'Professional high-end landing page generation tool creating visually stunning, well-designed web pages.', website: 'https://agent.minimax.io', views: 72890, author: 'MiniMax' },
  { name: 'Multi-Agent Trading', category: 'Business & Finance', pricing: 'free', description: 'Multi-agent AI trading framework mirroring real-world trading firms — fundamentals, sentiment, technical analysis.', website: 'https://github.com/TauricResearch/TradingAgents', views: 62362, author: 'Max' },
  { name: 'Industry-Research-Expert', category: 'Research & Analytics', pricing: 'freemium', description: 'Professional industry research reports with credible financial sources. Produces polished Markdown, PDF, and DOCX reports.', website: 'https://agent.minimax.io', views: 45187, author: 'MiniMax' },
  { name: 'skill-creator', category: 'AI Agents & Automation', pricing: 'freemium', description: 'Create, refactor, and productionize Agent Skills with engineering-first workflow. Full .skill artifact packaging.', website: 'https://agent.minimax.io', views: 31861, author: 'MiniMax' },
  { name: 'Visual Lab', category: 'Design & Art', pricing: 'freemium', description: 'Professional visual content generation — presentations, infographics, charts, dashboards, timelines, flowcharts, mind maps.', website: 'https://agent.minimax.io', views: 22575, author: 'MiniMax' },
  { name: 'Video Story Generator', category: 'Video & Animation', pricing: 'freemium', description: 'Automatically generates complete video stories from images or text. Flexible input, selectable duration and style.', website: 'https://agent.minimax.io', views: 19746, author: 'MiniMax' },
  { name: 'Topic Tracker', category: 'Research & Analytics', pricing: 'freemium', description: 'Search latest sources, discover trending topics, generate long-form content for tracking events and industry trends.', website: 'https://agent.minimax.io', views: 19203, author: 'MiniMax' },
  { name: 'TrendIntel', category: 'Marketing & Sales', pricing: 'freemium', description: 'Cross-platform social media trend monitoring — Instagram, TikTok, Pinterest, Twitter. Tracks AI videos and pushes to Feishu.', website: 'https://agent.minimax.io', views: 16305, author: 'MiniMax' },
  { name: 'McKinsey PPT', category: 'Productivity', pricing: 'freemium', description: 'McKinsey-style consulting slide deck generator with charts, market analysis, and industry insights.', website: 'https://agent.minimax.io', views: 15067, author: 'MiniMax' },
  { name: 'Excel Processor', category: 'Productivity', pricing: 'freemium', description: 'Professional Excel/XLSX creation, editing, data analysis, and format conversion — full spreadsheet lifecycle.', website: 'https://agent.minimax.io', views: 14354, author: 'MiniMax' },
  { name: 'Doc Processor', category: 'Productivity', pricing: 'freemium', description: 'Professional PDF and DOCX creation, conversion, content refinement, and operations — full document lifecycle.', website: 'https://agent.minimax.io', views: 12480, author: 'MiniMax' },
  { name: 'LeadGen Autopilot', category: 'Marketing & Sales', pricing: 'freemium', description: 'B2B lead generation — identifies competitors, discovers customers, generates personalized BD materials.', website: 'https://agent.minimax.io', views: 11437, author: 'MiniMax' },
  { name: 'Icon Maker', category: 'Image Generation', pricing: 'freemium', description: 'AI icon generator for Apps, websites, software, games, brand logos, social avatars — 20+ style options.', website: 'https://agent.minimax.io', views: 8668, author: 'MiniMax' },
  { name: 'Image Craft', category: 'Image Generation', pricing: 'freemium', description: 'Curated AI image generation prompt collection — figures, scenes, products, and style transformations.', website: 'https://agent.minimax.io', views: 8321, author: 'MiniMax' },
  { name: 'SEO & GEO Optimization Expert', category: 'Marketing & Sales', pricing: 'freemium', description: 'SEO and GEO optimization expert agent for search engine visibility and geographic ranking improvements.', website: 'https://agent.minimax.io', views: 5896, author: 'MiniMax' },
  { name: 'PRD Assistant', category: 'Productivity', pricing: 'freemium', description: 'Product requirements analysis — from idea to complete product solutions including PRDs and specs.', website: 'https://agent.minimax.io', views: 5386, author: 'MiniMax' },
  { name: 'GIF Sticker Maker', category: 'Image Generation', pricing: 'freemium', description: 'Cute cartoon sticker generator — convert photos into adorable cartoon stickers for social media and messaging.', website: 'https://agent.minimax.io', views: 4105, author: 'MiniMax' },
  { name: 'Research Maestro', category: 'Research & Analytics', pricing: 'freemium', description: 'Doctorate-level academic research agent — topic analysis, literature review, citation, and full paper generation.', website: 'https://agent.minimax.io', views: 3554, author: 'Samuel Mwenda' },
  { name: 'app-builder', category: 'Coding & Dev', pricing: 'freemium', description: 'Full-stack application builder — creates web apps, APIs, mobile apps from natural language requests.', website: 'https://agent.minimax.io', views: 3511, author: 'Fernando Jimenez' },
  { name: 'AI Agents Architect', category: 'AI Agents & Automation', pricing: 'freemium', description: 'Expert in designing autonomous AI agents — agent architecture, tool integration, memory systems, and orchestration.', website: 'https://agent.minimax.io', views: 2697, author: 'Fernando Jimenez' },
  { name: 'Sales Power Map', category: 'Marketing & Sales', pricing: 'freemium', description: 'Enter product + target company — get visual decision chain, key stakeholders with contact info, and outreach path.', website: 'https://agent.minimax.io', views: 2896, author: 'MiniMax' },
  { name: 'job-hunter-agent', category: 'Education & Learning', pricing: 'freemium', description: 'Comprehensive job hunting and auto-application agent — finds jobs across all platforms, auto-applies at scale.', website: 'https://agent.minimax.io', views: 4259, author: 'Leoven Xenon' },
  { name: 'Mini Coder Max', category: 'Coding & Dev', pricing: 'freemium', description: 'Autonomous coding agent that spawns multiple subagents in parallel. Full-stack development from prompts.', website: 'https://agent.minimax.io', views: 4139, author: 'akunkuilang699' },
  { name: 'AI Trading Consortium', category: 'Business & Finance', pricing: 'free', description: 'AI-powered hedge fund agent combining multi-expert trading strategies with comprehensive information gathering.', website: 'https://agent.minimax.io', views: 3487, author: 'Max' },
  { name: 'ClickHouse Best Practices Expert', category: 'Coding & Dev', pricing: 'free', description: 'Expert guidance on ClickHouse database — query optimization, schema design, and performance best practices.', website: 'https://github.com/ClickHouse/agent-skills', views: 3123, author: 'MiniMax' },
  { name: 'job-finder', category: 'Education & Learning', pricing: 'freemium', description: 'Data-driven job search strategist — finds relevant high-quality job opportunities by searching live job boards.', website: 'https://agent.minimax.io', views: 2864, author: 'Fernando Jimenez' },
  { name: 'Principle Animator', category: 'Video & Animation', pricing: 'freemium', description: 'Transform concepts into interactive animations — 3D/2D web animations from physics, mechanics, and algorithms.', website: 'https://agent.minimax.io', views: 5165, author: 'MiniMax' },
]

const PRICING_LABELS: Record<string, string> = {
  free: '🆓 Free',
  freemium: '⚡ Free + Paid',
  paid: '💎 Paid',
  'contact for pricing': '📩 Contact',
}

function ToolCard({ tool, onTag }: { tool: typeof SAMPLE_TOOLS[0], onTag: (c: string) => void }) {
  const [expanded, setExpanded] = useState(false)
  const cat = CATEGORIES.find(c => c.id === tool.category) || CATEGORIES[13]
  const pricingColor = tool.pricing === 'free' ? '#10b981' : tool.pricing === 'freemium' ? '#f59e0b' : '#ec4899'

  return (
    <div
      className="tool-card"
      style={{ background: '#13132a', border: '1px solid #1f2937' }}
      onClick={() => setExpanded(!expanded)}
    >
      <div className="flex items-start gap-3">
        <div className="tool-icon" style={{ background: `${cat.color}15`, border: `1px solid ${cat.color}30` }}>
          <span style={{ fontSize: '18px' }}>{cat.icon}</span>
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-white font-semibold text-sm truncate">{tool.name}</span>
            <span className="text-xs px-2 py-0.5 rounded-full font-medium" style={{ background: `${pricingColor}20`, color: pricingColor }}>
              {PRICING_LABELS[tool.pricing] || tool.pricing}
            </span>
          </div>
          <div className="text-xs text-gray-500 mt-0.5">{cat.name} · {(tool.views || 0).toLocaleString()} views/mo</div>
          <p className="text-gray-400 text-xs mt-2 leading-relaxed line-clamp-2">{tool.description}</p>
          {expanded && tool.website && (
            <a
              href={tool.website}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block mt-3 text-xs px-3 py-1.5 rounded-lg font-medium"
              style={{ background: `${cat.color}20`, color: cat.color, border: `1px solid ${cat.color}40`, textDecoration: 'none' }}
              onClick={e => e.stopPropagation()}
            >
              🌐 Visit → Website
            </a>
          )}
        </div>
      </div>
    </div>
  )
}

function CategoryBar({ active, onSelect, counts }: { active: string, onSelect: (c: string) => void, counts: Record<string, number> }) {
  return (
    <div className="cat-bar">
      {CATEGORIES.map(cat => {
        const count = counts[cat.id] || 0
        const isActive = active === cat.id
        return (
          <button
            key={cat.id}
            onClick={() => onSelect(cat.id)}
            className={`cat-btn ${isActive ? 'active' : ''}`}
            style={isActive ? {
              background: `${cat.color}20`,
              borderColor: `${cat.color}60`,
              color: cat.color,
            } : {}}
          >
            <span>{cat.icon}</span>
            <span className="cat-name">{cat.name}</span>
            <span className="cat-count" style={isActive ? { background: cat.color, color: '#000' } : {}}>
              {count}
            </span>
          </button>
        )
      })}
    </div>
  )
}

export default function App() {
  const [activeCat, setActiveCat] = useState('All')
  const [search, setSearch] = useState('')
  const [sortBy, setSortBy] = useState<'views' | 'name'>('views')
  const [showFreeOnly, setShowFreeOnly] = useState(false)

  const allTools = useMemo(() => {
    try {
      const stored = localStorage.getItem('ai_tools_vault_data')
      if (stored) {
        const parsed = JSON.parse(stored)
        if (Array.isArray(parsed) && parsed.length > 0) return parsed
      }
    } catch {}
    try {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const modules = (import.meta as any).glob('./data/*.json', { eager: true })
      let best: any[] = [...SAMPLE_TOOLS, ...MINIMAX_TOOLS]
      for (const path in modules) {
        const mod = modules[path]
        if (mod && Array.isArray(mod.default) && mod.default.length > best.length) {
          best = mod.default
        }
      }
      return best
    } catch {}
    return [...SAMPLE_TOOLS, ...MINIMAX_TOOLS]
  }, [])

  const filtered = useMemo(() => {
    let list = allTools
    if (activeCat !== 'All') list = list.filter(t => t.category === activeCat)
    if (showFreeOnly) list = list.filter(t => t.pricing === 'free' || t.pricing === 'freemium')
    if (search.trim()) {
      const q = search.toLowerCase()
      list = list.filter(t =>
        t.name.toLowerCase().includes(q) ||
        t.description.toLowerCase().includes(q) ||
        t.category.toLowerCase().includes(q)
      )
    }
    list = [...list].sort((a, b) => sortBy === 'views' ? (b.views || 0) - (a.views || 0) : a.name.localeCompare(b.name))
    return list
  }, [allTools, activeCat, search, sortBy, showFreeOnly])

  const counts = useMemo(() => {
    const c: Record<string, number> = { All: allTools.length }
    for (const t of allTools) {
      c[t.category] = (c[t.category] || 0) + 1
    }
    return c
  }, [allTools])

  return (
    <div className="min-h-screen" style={{ background: '#0a0a0f', fontFamily: 'Inter, system-ui, sans-serif' }}>
      <style>{`
        .tool-card { border-radius: 14px; padding: 16px; cursor: pointer; transition: all 0.2s; }
        .tool-card:hover { border-color: rgba(212,175,55,0.3) !important; transform: translateY(-2px); }
        .tool-icon { width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
        .cat-bar { display: flex; gap: 6px; flex-wrap: wrap; padding: 6px; background: #0d0d14; border-radius: 14px; border: 1px solid #1f2937; }
        .cat-btn { display: flex; align-items: center; gap: 6px; padding: 6px 12px; border-radius: 8px; border: 1px solid transparent; background: none; color: #6b7280; font-size: 12px; cursor: pointer; transition: all 0.15s; white-space: nowrap; }
        .cat-btn:hover { background: #1a1a2e; color: #d1d5db; }
        .cat-count { background: #1f2937; color: #6b7280; font-size: 10px; font-weight: 700; padding: 1px 6px; border-radius: 99px; }
        .search-input { background: #13132a; border: 1px solid #1f2937; border-radius: 12px; padding: 10px 16px; color: #fff; font-size: 14px; outline: none; width: 100%; transition: border-color 0.2s; }
        .search-input:focus { border-color: rgba(212,175,55,0.5); }
        .search-input::placeholder { color: #4b5563; }
        .line-clamp-2 { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
      `}</style>

      {/* Header */}
      <header style={{ background: 'linear-gradient(180deg, rgba(212,175,55,0.06) 0%, transparent 100%)', borderBottom: '1px solid #1f2937' }}>
        <div className="max-w-6xl mx-auto px-5 py-10 text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full mb-5" style={{ background: 'rgba(212,175,55,0.1)', border: '1px solid rgba(212,175,55,0.2)' }}>
            <span style={{ fontSize: '14px' }}>🧠</span>
            <span className="text-gray-300 text-sm font-medium">1,000+ AI Tools · Updated Daily</span>
          </div>
          <h1 className="text-4xl md:text-6xl font-black text-white mb-4">
            The AI Tools<br />
            <span style={{ background: 'linear-gradient(135deg, #D4AF37, #f5d76e)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>Vault</span>
          </h1>
          <p className="text-gray-400 text-lg mb-8 max-w-xl mx-auto">Every AI tool you'll ever need. Search, filter, and discover — all in one place.</p>

          {/* Search */}
          <div className="max-w-2xl mx-auto">
            <input
              type="text"
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="Search 1,000+ AI tools..."
              className="search-input"
            />
            <div className="flex items-center gap-4 mt-4 justify-center flex-wrap">
              <label className="flex items-center gap-2 text-xs text-gray-400 cursor-pointer">
                <input type="checkbox" checked={showFreeOnly} onChange={e => setShowFreeOnly(e.target.checked)} className="accent-yellow-500" />
                Free / Freemium only
              </label>
              <button
                onClick={() => setSortBy(s => s === 'views' ? 'name' : 'views')}
                className="text-xs px-3 py-1.5 rounded-lg border"
                style={{ borderColor: '#1f2937', color: '#9ca3af', background: 'none', cursor: 'pointer' }}
              >
                Sort: {sortBy === 'views' ? '🔥 Most Popular' : '🔤 Alphabetical'}
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-5 py-8">
        {/* Stats bar */}
        <div className="grid grid-cols-4 gap-4 mb-8">
          {[['1,000+', 'Total Tools'], ['Free to Use', 'Tools Available'], ['12', 'Categories'], ['Updated', 'Daily']].map(([val, label]) => (
            <div key={label} className="text-center rounded-xl py-4" style={{ background: '#13132a', border: '1px solid #1f2937' }}>
              <div className="text-xl font-black" style={{ color: '#D4AF37' }}>{val}</div>
              <div className="text-gray-500 text-xs mt-0.5">{label}</div>
            </div>
          ))}
        </div>

        {/* Category bar */}
        <CategoryBar active={activeCat} onSelect={setActiveCat} counts={counts} />

        {/* Results count */}
        <div className="flex items-center justify-between mt-6 mb-4">
          <p className="text-gray-400 text-sm">
            Showing <span className="text-white font-semibold">{filtered.length}</span> tools
            {activeCat !== 'All' && <> in <span style={{ color: '#D4AF37' }}>{CATEGORIES.find(c => c.id === activeCat)?.name}</span></>}
            {search && <> matching "<span className="text-white">{search}</span>"</>}
          </p>
        </div>

        {/* Tools grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {filtered.map((tool, i) => (
            <ToolCard key={`${tool.name}-${i}`} tool={tool} onTag={setActiveCat} />
          ))}
        </div>

        {filtered.length === 0 && (
          <div className="text-center py-20">
            <div style={{ fontSize: '48px' }}>🔍</div>
            <p className="text-white font-semibold mt-4">No tools found</p>
            <p className="text-gray-500 text-sm mt-1">Try a different search or category</p>
          </div>
        )}
      </div>

      {/* Submit tool CTA */}
      <div className="max-w-6xl mx-auto px-5 pb-12">
        <div className="rounded-2xl p-8 text-center" style={{ background: 'linear-gradient(135deg, rgba(212,175,55,0.08), rgba(212,175,55,0.03))', border: '1px solid rgba(212,175,55,0.15)' }}>
          <h3 className="text-white text-xl font-bold mb-2">Know an AI tool we missed?</h3>
          <p className="text-gray-400 text-sm mb-5">Submit a tool and if it makes the directory, you'll be credited on the site.</p>
          <a
            href="mailto:submit@aitoolsvault.com?subject=Tool Submission"
            className="inline-block text-sm font-semibold px-6 py-3 rounded-full"
            style={{ background: 'linear-gradient(135deg, #D4AF37, #b8962e)', color: '#0a0a0f', textDecoration: 'none' }}
          >
            ✉️ Submit a Tool
          </a>
        </div>
      </div>

      <footer className="border-t" style={{ borderColor: '#1f2937', background: '#080810' }}>
        <div className="max-w-6xl mx-auto px-5 py-6 flex flex-col sm:flex-row justify-between items-center gap-3">
          <div className="text-gray-600 text-xs">© 2026 The AI Tools Vault · All rights reserved</div>
          <div className="flex gap-4">
            <a href="#" className="text-gray-600 text-xs" style={{ textDecoration: 'none' }}>About</a>
            <a href="#" className="text-gray-600 text-xs" style={{ textDecoration: 'none' }}>Submit Tool</a>
            <a href="#" className="text-gray-600 text-xs" style={{ textDecoration: 'none' }}>Advertise</a>
          </div>
        </div>
      </footer>
    </div>
  )
}
