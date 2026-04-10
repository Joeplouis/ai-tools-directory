#!/usr/bin/env python3
"""Build the AI Tools Vault adaptive onboarding questionnaire."""
import json, os

QUESTIONS = [
    {"id":"primary_role","question":"What best describes what you do?","subtitle":"This helps us show you the most relevant tools","type":"cards","options":[
        {"value":"content_creator","label":"Content Creator","icon":"🎬","desc":"YouTube, TikTok, blogs, social media"},
        {"value":"business_pro","label":"Business Professional","icon":"💼","desc":"Marketing, sales, ops, management"},
        {"value":"developer","label":"Developer / Engineer","icon":"💻","desc":"Code, build, ship software"},
        {"value":"entrepreneur","label":"Entrepreneur / Founder","icon":"🚀","desc":"Starting or running a business"},
        {"value":"student","label":"Student / Learner","icon":"📚","desc":"Learning new skills"},
        {"value":"other","label":"Something Else","icon":"✨","desc":"None of the above"},
    ]},
    {"id":"primary_goal","question":"What's your primary goal with AI tools?","subtitle":"Be honest — there's no wrong answer","type":"cards","options":[
        {"value":"save_time","label":"Save Time","icon":"⚡","desc":"Automate tasks, work faster"},
        {"value":"make_money","label":"Make Money","icon":"💰","desc":"Grow income, build a business"},
        {"value":"scale_content","label":"Scale Content","icon":"📈","desc":"Produce more, reach more people"},
        {"value":"learn","label":"Learn Skills","icon":"🧠","desc":"Study, practice, improve"},
        {"value":"automate","label":"Automate Work","icon":"🤖","desc":"Replace manual repetitive work"},
        {"value":"create","label":"Create Better","icon":"✨","desc":"Improve quality of my work"},
    ]},
    {"id":"biggest_challenge","question":"What's your biggest challenge right now?","subtitle":"Select the one that resonates most","type":"cards","options":[
        {"value":"dont_know_where_to_start","label":"I Don't Know Where to Start","icon":"🧭","desc":"Overwhelmed by all the options"},
        {"value":"quality","label":"Quality Isn't Good Enough","icon":"📉","desc":"AI output needs too much editing"},
        {"value":"speed","label":"It's Too Slow","icon":"🐢","desc":"Takes longer than doing it manually"},
        {"value":"cost","label":"Too Expensive","icon":"💸","desc":"Can't afford all the tools I need"},
        {"value":"finding_right_tools","label":"Finding the Right Tools","icon":"🔍","desc":"Don't know what actually works"},
    ]},
    {"id":"how_solving","question":"How are you solving this today?","subtitle":"Don't overthink it","type":"cards","options":[
        {"value":"not_yet","label":"I'm Not Solving It Yet","icon":"🚫","desc":"Just living with the problem"},
        {"value":"manual","label":"Doing It Manually","icon":"✋","desc":"Slow but it gets done"},
        {"value":"free_tools","label":"Free AI Tools","icon":"🆓","desc":"ChatGPT free, Bing AI, etc."},
        {"value":"paid_tools","label":"Paid AI Tools","icon":"💎","desc":"Already paying for some tools"},
    ]},
    {"id":"budget","question":"What's your monthly budget for AI tools?","subtitle":"This helps us recommend the right tier","type":"cards","options":[
        {"value":"free_only","label":"Free Only","icon":"🆓","desc":"I'll pay $0/month"},
        {"value":"under_50","label":"Under $50/mo","icon":"💵","desc":"Starter budget"},
        {"value":"50_to_200","label":"$50–$200/mo","icon":"💳","desc":"Professional tier"},
        {"value":"200_to_500","label":"$200–$500/mo","icon":"💼","desc":"Business tier"},
        {"value":"over_500","label":"$500+/mo","icon":"🏦","desc":"Enterprise budget"},
    ]},
    {"id":"tools_interested","question":"Which AI tools are you most interested in?","subtitle":"Select all that apply — or skip this","type":"multi","options":[
        {"value":"text_writing","label":"✍️ Text & Writing","desc":"AI writing, copywriting, editing"},
        {"value":"image_generation","label":"🖼️ Image Generation","desc":"AI art, photos, design"},
        {"value":"video_animation","label":"🎬 Video & Animation","desc":"AI video, shorts, reels"},
        {"value":"voice_audio","label":"🎙️ Voice & Audio","desc":"Voice cloning, TTS, music"},
        {"value":"coding_dev","label":"💻 Coding & Dev","desc":"AI code, debugging, APIs"},
        {"value":"marketing_sales","label":"📈 Marketing & Sales","desc":"SEO, ads, lead gen, CRM"},
        {"value":"productivity","label":"⚡ Productivity","desc":"Slides, docs, notes, tasks"},
        {"value":"ai_agents","label":"🤖 AI Agents","desc":"Automation, bots, workflows"},
        {"value":"research","label":"🔬 Research","desc":"Data, analysis, reports"},
    ]},
    {"id":"how_often","question":"How often do you create content or use AI tools?","subtitle":"Rough estimate is fine","type":"cards","options":[
        {"value":"rarely","label":"Rarely","icon":"🌙","desc":"Just exploring"},
        {"value":"weekly","label":"Weekly","icon":"📅","desc":"A few times a week"},
        {"value":"daily","label":"Daily","icon":"☀️","desc":"Part of my regular routine"},
        {"value":"professionally","label":"Professionally","icon":"🏆","desc":"It's my job or business"},
    ]},
]

TOOL_MAP = {
    "text_writing":["ChatGPT","Claude","Jasper","Copy.ai","QuillBot"],
    "image_generation":["Midjourney","DALL-E 3","Leonardo.ai","Ideogram","Canva AI"],
    "video_animation":["Runway ML","Sora","HeyGen","Synthesia","Pika"],
    "voice_audio":["ElevenLabs","Murf AI","Suno","Play.ht","Otter.ai"],
    "coding_dev":["Cursor","GitHub Copilot","Claude Code","Replit Agent","v0"],
    "marketing_sales":["Jasper","AdCreative.ai","Surfer SEO","MarketMuse","Lavender"],
    "productivity":["Notion AI","Beautiful.ai","Gamma","Fireflies.ai","Tome"],
    "ai_agents":["Zapier","n8n","Make","Dify","Coze"],
    "research":["Perplexity","Consensus","Elicit","scite","Semantic Scholar"],
}

SEGMENTS = {
    "content_creator":{"primary_tools":["Runway ML","Midjourney","ElevenLabs","ChatGPT","Suno"],"segment_label":"Content Creator","best_for":"Faceless YouTube, content repurposing, AI avatars"},
    "business_pro":{"primary_tools":["ChatGPT","Notion AI","Jasper","Surfer SEO","Zapier"],"segment_label":"Business Professional","best_for":"Automating workflows, content marketing, lead gen"},
    "developer":{"primary_tools":["Cursor","GitHub Copilot","Claude Code","Replit Agent","v0"],"segment_label":"Developer","best_for":"Ship faster, code review, debugging"},
    "entrepreneur":{"primary_tools":["ChatGPT","Jasper","Zapier","Figma AI","Beautiful.ai"],"segment_label":"Entrepreneur","best_for":"Validating ideas, building MVPs, marketing"},
    "student":{"primary_tools":["ChatGPT","Notion AI","Perplexity","Gamma","Consensus"],"segment_label":"Student","best_for":"Research, writing, learning faster"},
    "other":{"primary_tools":["ChatGPT","Notion AI","Perplexity","Gamma","Beautiful.ai"],"segment_label":"General User","best_for":"Productivity, writing, general tasks"},
}

def q_html(q, i):
    opts = []
    for opt in q["options"]:
        score = opt.get("score",0)
        if q["type"] == "multi":
            btn = '<button class="opt-card opt-multi" data-value="{v}" onclick="toggleMulti(this,&quot;{q}&quot;)"><div class="opt-icon">{ic}</div><div class="opt-body"><div class="opt-label">{l}</div><div class="opt-desc">{d}</div></div><div class="opt-check">✓</div></button>'
        else:
            btn = '<button class="opt-card" data-value="{v}" data-score="{s}" onclick="selectOption(this,&quot;{q}&quot;)"><div class="opt-icon">{ic}</div><div class="opt-body"><div class="opt-label">{l}</div><div class="opt-desc">{d}</div></div><div class="opt-check">✓</div></button>'
        btn = btn.format(v=opt["value"],s=score,ic=opt["icon"],l=opt["label"],d=opt["desc"],q=q["id"])
        opts.append(btn)
    opts_str = "\n".join(opts)
    multi_hint = '<p class="multi-hint">Select all that apply — or <span onclick="nextQuestion(true)">skip this</span></p>' if q["type"]=="multi" else ""
    pct = int((i/float(len(QUESTIONS)))*100)
    back_style = "display:none" if i==0 else ""
    block = '<div class="q-block" id="q-{id}"><div class="q-progress"><div class="q-progress-bar" id="progress-{id}" style="width:{pct}%"></div></div><div class="q-step">Question {n} of {total}</div><h2 class="q-title">{q}</h2><p class="q-subtitle">{sub}</p>{mh}<div class="q-options" id="opts-{id}">{opts}</div><div class="q-footer"><button class="q-back" id="back-{id}" onclick="prevQuestion()" style="{bs}">← Back</button><button class="q-next" id="next-btn-{id}" onclick="nextQuestion(false)" disabled>Continue →</button></div></div>'
    return block.format(id=q["id"],q=q["question"],sub=q["subtitle"],pct=pct,n=i+1,total=len(QUESTIONS),opts=opts_str,mh=multi_hint,bs=back_style)

q_blocks = [q_html(Q,i) for i,Q in enumerate(QUESTIONS)]
ALL_Q = "\n".join(q_blocks)
Q_JSON = json.dumps(QUESTIONS, ensure_ascii=False)
TM_JSON = json.dumps(TOOL_MAP, ensure_ascii=False)
SEG_JSON = json.dumps(SEGMENTS, ensure_ascii=False)

# Now write the complete HTML file
output_path = "/workspace/ai-tools-directory/dist/onboarding.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write('<!DOCTYPE html>\n')
    f.write('<html lang="en">\n<head>\n')
    f.write('<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n')
    f.write('<title>Get Matched With the Right AI Tools — AI Tools Vault</title>\n')
    f.write('<meta name="description" content="Answer 7 quick questions and get personalized AI tool recommendations. Get notified when new matching tools are added.">\n')
    f.write('<link rel="preconnect" href="https://fonts.googleapis.com">\n')
    f.write('<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">\n')
    f.write('<style>\n')
    css = """
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"Inter",system-ui,sans-serif;background:#09090f;color:#f0f0f0;min-height:100vh;line-height:1.6}
a{text-decoration:none;color:inherit}
.container{max-width:1100px;margin:0 auto;padding:0 24px}
.badge{display:inline-flex;align-items:center;gap:8px;padding:8px 16px;border-radius:99px;background:rgba(212,175,55,0.1);border:1px solid rgba(212,175,55,0.2);font-size:12px;color:#D4AF37;margin-bottom:20px}
.btn-gold{background:linear-gradient(135deg,#D4AF37,#b8962e);color:#09090f;font-weight:700;font-size:15px;padding:13px 24px;border-radius:10px;border:none;cursor:pointer;transition:all 0.2s;display:inline-flex;align-items:center;gap:8px;width:100%;justify-content:center}
.btn-gold:hover{filter:brightness(1.05)}
.btn-gold:disabled{opacity:0.35;cursor:not-allowed}
.h1{font-size:clamp(26px,3.5vw,44px);font-weight:900;color:#fff;line-height:1.1;margin-bottom:14px}
.h1 span{background:linear-gradient(135deg,#D4AF37,#f5d76e);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.sub{font-size:15px;color:#9ca3af;line-height:1.7;margin-bottom:28px}
#landing{display:grid;grid-template-columns:1fr 1fr;min-height:100vh}
#onboarding,.mobile-landing,#completion,.mobile-landing{display:none;min-height:100vh}
#landing.active{display:grid}
.mobile-landing.active{display:flex;flex-direction:column;justify-content:center;padding:60px 24px}
.left-col{padding:60px 56px 60px 0;display:flex;flex-direction:column;justify-content:center;background:radial-gradient(ellipse at 0% 50%,rgba(212,175,55,0.06) 0%,transparent 60%)}
.right-col{padding:60px 0 60px 56px;display:flex;flex-direction:column;justify-content:center;border-left:1px solid rgba(255,255,255,0.06);background:#0d0d18}
.features{list-style:none;display:flex;flex-direction:column;gap:12px;margin-bottom:32px}
.features li{display:flex;align-items:center;gap:10px;font-size:14px;color:#e5e7eb}
.features li span{font-size:18px}
.proof-item{display:flex;align-items:center;gap:14px;padding:12px 0;border-bottom:1px solid rgba(255,255,255,0.05)}
.proof-item:last-child{border-bottom:none}
.proof-avatar{width:38px;height:38px;border-radius:50%;background:linear-gradient(135deg,#D4AF37,#b8962e);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:12px;color:#09090f;flex-shrink:0}
.proof-text{font-size:13px;color:#9ca3af}
.proof-text strong{color:#fff}
.mobile-trigger{display:none;padding:60px 24px;flex-direction:column;justify-content:center;min-height:100vh}
.mobile-trigger.active{display:flex}
.mobile-trigger h1{margin-bottom:12px}
.mobile-trigger p{margin-bottom:24px;font-size:14px;color:#9ca3af}
.q-wrap{max-width:600px;margin:0 auto;padding:48px 20px}
.q-block{display:none;animation:fadeUp 0.4s ease}
.q-block.active{display:block}
@keyframes fadeUp{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}
.q-progress{height:3px;background:#1f2937;border-radius:99px;margin-bottom:8px}
.q-progress-bar{height:3px;background:linear-gradient(90deg,#D4AF37,#f5d76e);border-radius:99px;transition:width 0.5s ease}
.q-step{font-size:11px;color:#6b7280;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:10px}
.q-title{font-size:clamp(20px,4vw,26px);font-weight:800;color:#fff;margin-bottom:8px;line-height:1.2}
.q-subtitle{font-size:14px;color:#9ca3af;margin-bottom:22px}
.multi-hint{font-size:12px;color:#6b7280;margin-bottom:12px;display:flex;align-items:center;gap:6px}
.multi-hint span{color:#D4AF37;cursor:pointer;text-decoration:underline}
.q-options{display:flex;flex-direction:column;gap:9px;margin-bottom:22px}
.opt-card{display:flex;align-items:center;gap:14px;padding:13px 15px;background:#13131f;border:1.5px solid rgba(255,255,255,0.07);border-radius:12px;cursor:pointer;transition:all 0.2s;text-align:left;width:100%;font-family:inherit}
.opt-card:hover{border-color:rgba(212,175,55,0.3);transform:translateY(-1px)}
.opt-card.selected{border-color:#D4AF37;background:rgba(212,175,55,0.07)}
.opt-card.selected .opt-check{background:#D4AF37;color:#09090f}
.opt-icon{font-size:20px;width:40px;height:40px;background:rgba(255,255,255,0.04);border-radius:10px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.opt-body{flex:1;min-width:0}
.opt-label{font-size:14px;font-weight:700;color:#f0f0f0;margin-bottom:2px}
.opt-desc{font-size:12px;color:#9ca3af}
.opt-check{width:22px;height:22px;border-radius:50%;border:1.5px solid rgba(255,255,255,0.15);display:flex;align-items:center;justify-content:center;font-size:11px;flex-shrink:0;transition:all 0.2s;color:transparent}
.opt-multi.selected .opt-check{background:#D4AF37;color:#09090f;border-color:#D4AF37}
.q-footer{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-top:2px}
.q-back{background:none;border:none;color:#6b7280;font-size:14px;cursor:pointer;padding:8px 0;font-family:inherit;transition:color 0.2s}
.q-back:hover{color:#9ca3af}
.q-next{flex:1;background:linear-gradient(135deg,#D4AF37,#b8962e);color:#09090f;font-weight:700;font-size:15px;padding:13px;border-radius:10px;border:none;cursor:pointer;transition:all 0.2s;font-family:inherit}
.q-next:disabled{opacity:0.35;cursor:not-allowed}
/* completion */
.complete-wrap{max-width:560px;margin:0 auto;padding:60px 20px}
.complete-card{background:#13131f;border:1px solid rgba(255,255,255,0.08);border-radius:22px;padding:44px 36px;text-align:center}
.check-circle{width:68px;height:68px;background:rgba(16,185,129,0.12);border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 20px;font-size:34px}
.complete-card h2{font-size:24px;font-weight:900;color:#fff;margin-bottom:10px}
.complete-card > p{font-size:14px;color:#9ca3af;line-height:1.6;margin-bottom:26px}
.seg-badge{display:inline-flex;align-items:center;gap:8px;padding:7px 14px;background:rgba(212,175,55,0.1);border:1px solid rgba(212,175,55,0.2);border-radius:99px;font-size:13px;color:#D4AF37;margin-bottom:20px}
.match-label{font-size:13px;font-weight:700;color:#fff;text-align:left;margin-bottom:12px}
.match-tools{display:flex;flex-wrap:wrap;gap:7px;justify-content:center;margin-bottom:26px}
.match-tool{padding:5px 12px;background:rgba(212,175,55,0.08);border:1px solid rgba(212,175,55,0.2);border-radius:99px;font-size:12px;color:#D4AF37;font-weight:600}
.why-section{margin-top:26px;padding-top:26px;border-top:1px solid rgba(255,255,255,0.06);text-align:left}
.why-title{font-size:14px;font-weight:700;color:#fff;margin-bottom:14px}
.why-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.why-item{padding:12px;background:#0d0d18;border-radius:10px}
.why-item strong{display:block;font-size:12px;font-weight:700;color:#fff;margin-bottom:3px}
.why-item p{font-size:12px;color:#9ca3af;line-height:1.5}
.email-ok{background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);border-radius:10px;padding:13px 16px;margin-bottom:22px;text-align:left}
.email-ok p{font-size:13px;color:#10b981;font-weight:600}
.complete-note{font-size:12px;color:#6b7280;margin-top:14px;line-height:1.5}
@media(max-width:768px){
#landing{display:none}
.mobile-trigger.active{display:flex}
#onboarding.active{display:block}
#completion.active{display:block}
.complete-wrap{padding:40px 16px}
.complete-card{padding:36px 20px}
.why-grid{grid-template-columns:1fr}
.complete-card h2{font-size:22px}
}
@media(max-width:480px){
.right-col{display:none}
.left-col{padding:48px 24px 48px 0}
}
"""
    f.write(css)
    f.write('\n</style>\n</head>\n<body>\n')
    # LANDING
    f.write('<div id="landing">\n')
    f.write('  <div class="left-col">\n')
    f.write('    <div class="badge">🧠 AI Tools Vault — Personalized Matching</div>\n')
    f.write('    <h1 class="h1">Find Your Perfect <span>AI Tools</span> in 2 Minutes</h1>\n')
    f.write('    <p class="sub">Answer 7 quick questions and we will show you the exact AI tools that match your goals, budget, and workflow. Then we email you when new matching tools are added.</p>\n')
    f.write('    <ul class="features">\n')
    f.write('      <li><span>🎯</span> Personalized tool recommendations for your specific goals</li>\n')
    f.write('      <li><span>🔔</span> Email alerts when new tools matching your profile are added</li>\n')
    f.write('      <li><span>💰</span> Find tools that match your exact budget</li>\n')
    f.write('      <li><span>⚡</span> Takes under 2 minutes — then you are set for life</li>\n')
    f.write('    </ul>\n')
    f.write('    <button class="btn-gold" onclick="startOnboarding()">Start My Personalized List →</button>\n')
    f.write('  </div>\n')
    f.write('  <div class="right-col">\n')
    f.write('    <div class="badge" style="margin-bottom:14px">276+ People Matched</div>\n')
    f.write('    <div class="proof-item"><div class="proof-avatar">MK</div><div class="proof-text"><strong>Maya K. — Content Creator</strong><br>Found 5 tools that now save her 3 hours a day</div></div>\n')
    f.write('    <div class="proof-item"><div class="proof-avatar">CD</div><div class="proof-text"><strong>Chris D. — Developer</strong><br>Cut his coding time in half using AI pair programming</div></div>\n')
    f.write('    <div class="proof-item"><div class="proof-avatar">SM</div><div class="proof-text"><strong>Sarah M. — Entrepreneur</strong><br>Ditched 3 tools for 1 that does everything better</div></div>\n')
    f.write('    <div class="proof-item"><div class="proof-avatar">JR</div><div class="proof-text"><strong>James R. — Marketer</strong><br>Gets email alerts when new tools match his niche</div></div>\n')
    f.write('  </div>\n')
    f.write('</div>\n')
    # MOBILE LANDING
    f.write('<div class="mobile-landing" id="mobileLanding">\n')
    f.write('  <div class="badge">🧠 AI Tools Vault</div>\n')
    f.write('  <h1 class="h1" style="margin-bottom:12px">Find Your Perfect <span>AI Tools</span></h1>\n')
    f.write('  <p class="sub" style="font-size:14px;margin-bottom:24px">Answer 7 questions and get matched with the right AI tools for your goals. Then get email alerts when new tools are added.</p>\n')
    f.write('  <button class="btn-gold" onclick="startOnboarding()">Start My Personalized List →</button>\n')
    f.write('</div>\n')
    # QUESTIONNAIRE
    f.write('<div id="onboarding" class="q-wrap">\n')
    f.write(ALL_Q)
    f.write('\n</div>\n')
    # COMPLETION
    f.write('<div id="completion" class="complete-wrap">\n')
    f.write('  <div class="complete-card">\n')
    f.write('    <div class="check-circle">✅</div>\n')
    f.write('    <div class="seg-badge" id="segBadge">🎯 Your Profile Is Ready</div>\n')
    f.write('    <h2>You Are All Set!</h2>\n')
    f.write('    <p>We have matched you with the best AI tools based on your answers. When new tools are added that match your profile, we will email you automatically.</p>\n')
    f.write('    <div class="match-label">Your personalized AI tool picks:</div>\n')
    f.write('    <div class="match-tools" id="matchTools"></div>\n')
    f.write('    <div class="why-section">\n')
    f.write('      <div class="why-title">Based on your answers, here is what we recommend:</div>\n')
    f.write('      <div class="why-grid">\n')
    f.write('        <div class="why-item"><strong id="whyGoal">-</strong><p id="whyGoalText">-</p></div>\n')
    f.write('        <div class="why-item"><strong id="whyChallenge">-</strong><p id="whyChallengeText">-</p></div>\n')
    f.write('        <div class="why-item"><strong id="whyBudget">-</strong><p id="whyBudgetText">-</p></div>\n')
    f.write('        <div class="why-item"><strong id="whyBest">-</strong><p id="whyBestText">-</p></div>\n')
    f.write('      </div>\n')
    f.write('    </div>\n')
    f.write('    <div class="email-ok"><p id="emailConfirmed"></p></div>\n')
    f.write('    <button class="btn-gold" style="margin-bottom:12px" onclick="window.location.href=&quot;index.html&quot;">Browse All 276+ Tools →</button>\n')
    f.write('    <p class="complete-note">📬 You will receive emails when new tools matching your profile are added. No spam. Unsubscribe anytime.</p>\n')
    f.write('  </div>\n')
    f.write('</div>\n')
    # JAVASCRIPT
    js = """
<script>
const QUESTIONS = %(Q_JSON)s;
const TOOL_MAP = %(TM_JSON)s;
const SEGMENTS = %(SEG_JSON)s;

const STORED_EMAIL = localStorage.getItem("vault_email") || "";
const STORED_LEAD = JSON.parse(localStorage.getItem("vault_lead") || "{}");
let currentQ = parseInt(STORED_LEAD.currentQ || "0");
let answers = STORED_LEAD.answers || {};
let multi = STORED_LEAD.multi || {};

function $id(id) { return document.getElementById(id); }

function show(id) {
  ["landing","mobileLanding","onboarding","completion"].forEach(x => {
    const el = $id(x);
    if (el) { el.style.display = "none"; el.classList.remove("active"); }
  });
  const el = $id(id);
  if (el) {
    el.style.display = (id === "mobileLanding" && window.innerWidth > 768) ? "none" :
                       (id === "landing" && window.innerWidth <= 768) ? "none" : "block";
    el.classList.add("active");
  }
}

function startOnboarding() {
  if (!STORED_EMAIL) { window.location.href = "index.html"; return; }
  show("onboarding");
  renderQuestion();
}

function renderQuestion() {
  document.querySelectorAll(".q-block").forEach(e => e.classList.remove("active"));
  const q = QUESTIONS[currentQ];
  const el = $id("q-" + q.id);
  if (el) el.classList.add("active");
  // Restore
  if (q.type === "multi") {
    const sel = multi[q.id] || [];
    document.querySelectorAll(".opt-multi").forEach(b => b.classList.toggle("selected", sel.includes(b.dataset.value)));
    const nb = $id("next-btn-" + q.id);
    if (nb) nb.disabled = false;
  } else {
    const saved = answers[q.id];
    document.querySelectorAll(".opt-card:not(.opt-multi)").forEach(b => b.classList.toggle("selected", b.dataset.value === saved));
    const nb = $id("next-btn-" + q.id);
    if (nb) nb.disabled = !saved;
  }
  const bb = $id("back-" + q.id);
  if (bb) bb.style.display = currentQ > 0 ? "inline-block" : "none";
  saveProgress();
}

function selectOption(btn, qId) {
  const parent = btn.closest(".q-options");
  if (parent) parent.querySelectorAll(".opt-card").forEach(b => b.classList.remove("selected"));
  btn.classList.add("selected");
  answers[qId] = btn.dataset.value;
  const nb = $id("next-btn-" + qId);
  if (nb) nb.disabled = false;
  saveProgress();
  setTimeout(() => nextQuestion(true), 350);
}

function toggleMulti(btn, qId) {
  btn.classList.toggle("selected");
  if (!multi[qId]) multi[qId] = [];
  const val = btn.dataset.value;
  if (multi[qId].includes(val)) multi[qId] = multi[qId].filter(v => v !== val);
  else multi[qId].push(val);
  saveProgress();
}

function nextQuestion(auto) {
  const q = QUESTIONS[currentQ];
  if (!auto && q.type !== "multi" && !answers[q.id]) return;
  if (currentQ < QUESTIONS.length - 1) {
    currentQ++;
    renderQuestion();
  } else {
    finishQuestionnaire();
  }
}

function prevQuestion() {
  if (currentQ > 0) { currentQ--; renderQuestion(); }
}

function finishQuestionnaire() {
  show("completion");
  const seg = answers.primary_role || "other";
  const segData = SEGMENTS[seg] || SEGMENTS.other;
  // Show segment badge
  const badge = $id("segBadge");
  if (badge) badge.textContent = "🎯 " + segData.segment_label;
  // Show matched tools
  const toolsInterested = multi.tools_interested || [];
  let recommendedTools = new Set();
  if (toolsInterested.length > 0) {
    toolsInterested.forEach(cat => {
      const catTools = TOOL_MAP[cat] || [];
      catTools.slice(0, 3).forEach(t => recommendedTools.add(t));
    });
  } else {
    (segData.primary_tools || []).slice(0, 5).forEach(t => recommendedTools.add(t));
  }
  const matchDiv = $id("matchTools");
  if (matchDiv) {
    matchDiv.innerHTML = Array.from(recommendedTools).slice(0, 6).map(t =>
      '<span class="match-tool">' + t + '</span>'
    ).join("");
  }
  // Why section
  const goalMap = {save_time:"Save Time",make_money:"Make Money",scale_content:"Scale Content",learn:"Learn Skills",automate:"Automate Work",create:"Create Better"};
  const challengeMap = {dont_know_where_to_start:"Where to Start",quality:"Quality Issues",speed:"Speed",cost:"Cost",finding_right_tools:"Finding Tools"};
  const budgetMap = {free_only:"Free Only",under_50:"Under $50/mo",50_to_200:"$50-200/mo",200_to_500:"$200-500/mo",over_500:"$500+/mo"};
  const howMap = {not_yet:"Not solving it yet",manual:"Doing it manually",free_tools:"Using free tools",paid_tools:"Using paid tools"};
  if ($id("whyGoal")) $id("whyGoal").textContent = goalMap[answers.primary_goal] || "Multiple Goals";
  if ($id("whyGoalText")) $id("whyGoalText").textContent = "Focus on tools that automate or accelerate: " + (answers.primary_goal ? goalMap[answers.primary_goal] : "your goals");
  if ($id("whyChallenge")) $id("whyChallenge").textContent = challengeMap[answers.biggest_challenge] || "Getting started";
  if ($id("whyChallengeText")) $id("whyChallengeText").textContent = "We'll recommend tools that directly address: " + (answers.biggest_challenge ? challengeMap[answers.biggest_challenge] : "your challenge");
  if ($id("whyBudget")) $id("whyBudget").textContent = budgetMap[answers.budget] || answers.budget || "Budget";
  if ($id("whyBudgetText")) $id("whyBudgetText").textContent = "Best tools within your " + (budgetMap[answers.budget] || "budget") + " range";
  if ($id("whyBest")) $id("whyBest").textContent = segData.segment_label;
  if ($id("whyBestText")) $id("whyBestText").textContent = segData.best_for || "";
  // Email confirmed
  if ($id("emailConfirmed")) $id("emailConfirmed").textContent = "✅ " + STORED_EMAIL + " — You are on the list!";
  // Save full lead
  const lead = {
    email: STORED_EMAIL,
    segment: seg,
    answers: answers,
    multi: multi,
    recommendedTools: Array.from(recommendedTools).slice(0, 6),
    budget: answers.budget,
    primaryGoal: answers.primary_goal,
    biggestChallenge: answers.big