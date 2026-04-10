#!/usr/bin/env python3
import json, os

Q = [
    {"id":"primary_role","q":"What best describes what you do?","sub":"This helps us show you the most relevant tools","type":"cards","opts":[
        {"v":"content_creator","l":"Content Creator","i":"🎬","d":"YouTube, TikTok, blogs, social media"},
        {"v":"business_pro","l":"Business Professional","i":"💼","d":"Marketing, sales, ops, management"},
        {"v":"developer","l":"Developer / Engineer","i":"💻","d":"Code, build, ship software"},
        {"v":"entrepreneur","l":"Entrepreneur / Founder","i":"🚀","d":"Starting or running a business"},
        {"v":"student","l":"Student / Learner","i":"📚","d":"Learning new skills"},
        {"v":"other","l":"Something Else","i":"✨","d":"None of the above"},
    ]},
    {"id":"primary_goal","q":"What's your primary goal with AI tools?","sub":"Be honest — there's no wrong answer","type":"cards","opts":[
        {"v":"save_time","l":"Save Time","i":"⚡","d":"Automate tasks, work faster"},
        {"v":"make_money","l":"Make Money","i":"💰","d":"Grow income, build a business"},
        {"v":"scale_content","l":"Scale Content","i":"📈","d":"Produce more, reach more people"},
        {"v":"learn","l":"Learn Skills","i":"🧠","d":"Study, practice, improve"},
        {"v":"automate","l":"Automate Work","i":"🤖","d":"Replace manual repetitive work"},
        {"v":"create","l":"Create Better","i":"✨","d":"Improve quality of my work"},
    ]},
    {"id":"biggest_challenge","q":"What's your biggest challenge right now?","sub":"Select the one that resonates most","type":"cards","opts":[
        {"v":"dont_know_where_to_start","l":"I Don't Know Where to Start","i":"🧭","d":"Overwhelmed by all the options"},
        {"v":"quality","l":"Quality Isn't Good Enough","i":"📉","d":"AI output needs too much editing"},
        {"v":"speed","l":"It's Too Slow","i":"🐢","d":"Takes longer than doing it manually"},
        {"v":"cost","l":"Too Expensive","i":"💸","d":"Can't afford all the tools I need"},
        {"v":"finding_right_tools","l":"Finding the Right Tools","i":"🔍","d":"Don't know what actually works"},
    ]},
    {"id":"how_solving","q":"How are you solving this today?","sub":"Don't overthink it","type":"cards","opts":[
        {"v":"not_yet","l":"I'm Not Solving It Yet","i":"🚫","d":"Just living with the problem"},
        {"v":"manual","l":"Doing It Manually","i":"✋","d":"Slow but it gets done"},
        {"v":"free_tools","l":"Free AI Tools","i":"🆓","d":"ChatGPT free, Bing AI, etc."},
        {"v":"paid_tools","l":"Paid AI Tools","i":"💎","d":"Already paying for some tools"},
    ]},
    {"id":"budget","q":"What's your monthly budget for AI tools?","sub":"This helps us recommend the right tier","type":"cards","opts":[
        {"v":"free_only","l":"Free Only","i":"🆓","d":"I'll pay $0/month"},
        {"v":"under_50","l":"Under $50/mo","i":"💵","d":"Starter budget"},
        {"v":"50_to_200","l":"$50-$200/mo","i":"💳","d":"Professional tier"},
        {"v":"200_to_500","l":"$200-$500/mo","i":"💼","d":"Business tier"},
        {"v":"over_500","l":"$500+/mo","i":"🏦","d":"Enterprise budget"},
    ]},
    {"id":"tools_interested","q":"Which AI tools are you most interested in?","sub":"Select all that apply — or skip this","type":"multi","opts":[
        {"v":"text_writing","l":"✍️ Text & Writing","d":"AI writing, copywriting, editing"},
        {"v":"image_generation","l":"🖼️ Image Generation","d":"AI art, photos, design"},
        {"v":"video_animation","l":"🎬 Video & Animation","d":"AI video, shorts, reels"},
        {"v":"voice_audio","l":"🎙️ Voice & Audio","d":"Voice cloning, TTS, music"},
        {"v":"coding_dev","l":"💻 Coding & Dev","d":"AI code, debugging, APIs"},
        {"v":"marketing_sales","l":"📈 Marketing & Sales","d":"SEO, ads, lead gen, CRM"},
        {"v":"productivity","l":"⚡ Productivity","d":"Slides, docs, notes, tasks"},
        {"v":"ai_agents","l":"🤖 AI Agents","d":"Automation, bots, workflows"},
        {"v":"research","l":"🔬 Research","d":"Data, analysis, reports"},
    ]},
    {"id":"how_often","q":"How often do you create content or use AI tools?","sub":"Rough estimate is fine","type":"cards","opts":[
        {"v":"rarely","l":"Rarely","i":"🌙","d":"Just exploring"},
        {"v":"weekly","l":"Weekly","i":"📅","d":"A few times a week"},
        {"v":"daily","l":"Daily","i":"☀️","d":"Part of my regular routine"},
        {"v":"professionally","l":"Professionally","i":"🏆","d":"It's my job or business"},
    ]},
]

TM = {
    "text_writing":["ChatGPT","Claude","Jasper","Copy.ai","Rytr"],
    "image_generation":["Midjourney","DALL-E 3","Leonardo.ai","Ideogram","Canva AI"],
    "video_animation":["Runway ML","Sora","HeyGen","Synthesia","Pika"],
    "voice_audio":["ElevenLabs","Murf AI","Suno","Play.ht","Otter.ai"],
    "coding_dev":["Cursor","GitHub Copilot","Claude Code","Replit Agent","v0"],
    "marketing_sales":["Jasper","AdCreative.ai","Surfer SEO","MarketMuse","Lavender"],
    "productivity":["Notion AI","Beautiful.ai","Gamma","Fireflies.ai","Tome"],
    "ai_agents":["Zapier","n8n","Make","Dify","Coze"],
    "research":["Perplexity","Consensus","Elicit","scite","Semantic Scholar"],
}

SEG = {
    "content_creator":{"l":"Content Creator","t":["Runway ML","Midjourney","ElevenLabs","ChatGPT","Suno"],"b":"Faceless YouTube, content repurposing, AI avatars"},
    "business_pro":{"l":"Business Professional","t":["ChatGPT","Notion AI","Jasper","Surfer SEO","Zapier"],"b":"Automating workflows, content marketing, lead gen"},
    "developer":{"l":"Developer","t":["Cursor","GitHub Copilot","Claude Code","Replit Agent","v0"],"b":"Ship faster, code review, debugging"},
    "entrepreneur":{"l":"Entrepreneur","t":["ChatGPT","Jasper","Zapier","Figma AI","Beautiful.ai"],"b":"Validating ideas, building MVPs, marketing"},
    "student":{"l":"Student","t":["ChatGPT","Notion AI","Perplexity","Gamma","Consensus"],"b":"Research, writing, learning faster"},
    "other":{"l":"General User","t":["ChatGPT","Notion AI","Perplexity","Gamma","Beautiful.ai"],"b":"General productivity and AI tools"},
}

n = len(Q)

def make_qblock(qi, idx):
    pct = int((idx/float(n))*100)
    opts = ""
    for o in qi["opts"]:
        ic = o.get("i","")
        cls = "opt-multi" if qi["type"]=="multi" else "opt-card"
        fn = 'toggleMulti(this,&quot;'+qi["id"]+'&quot;)' if qi["type"]=="multi" else 'selectOption(this,&quot;'+qi["id"]+'&quot;)'
        opts += '<button class="opt-card '+cls+'" data-value="'+o["v"]+'" onclick="'+fn+'"><div class="opt-icon">'+ic+'</div><div class="opt-body"><div class="opt-label">'+o["l"]+'</div><div class="opt-desc">'+o["d"]+'</div></div><div class="opt-check">✓</div></button>'
    mh = '<p class="multi-hint">Select all that apply — or <span onclick="nextQuestion(true)">skip this</span></p>' if qi["type"]=="multi" else ""
    disabled = "" if qi["type"]=="multi" else "disabled"
    bs = "display:none" if idx==0 else ""
    return '<div class="q-block" id="q-'+qi["id"]+'"><div class="q-progress"><div class="q-progress-bar" style="width:'+str(pct)+'%"></div></div><div class="q-step">Question '+str(idx+1)+' of '+str(n)+'</div><h2 class="q-title">'+qi["q"]+'</h2><p class="q-subtitle">'+qi["sub"]+'</p>'+mh+'<div class="q-options">'+opts+'</div><div class="q-footer"><button class="q-back" onclick="prevQuestion()" style="'+bs+'">← Back</button><button class="q-next" onclick="nextQuestion(false)" '+disabled+'>Continue →</button></div></div>'

qblocks = [make_qblock(Q[i],i) for i in range(n)]
ALLQ = "\n".join(qblocks)
QJ = json.dumps(Q, ensure_ascii=False)
TMJ = json.dumps(TM, ensure_ascii=False)
SEJ = json.dumps(SEG, ensure_ascii=False)

CSS = """*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"Inter",system-ui,sans-serif;background:#09090f;color:#f0f0f0;min-height:100vh;line-height:1.6}
a{text-decoration:none;color:inherit}
.badge{display:inline-flex;align-items:center;gap:8px;padding:8px 16px;border-radius:99px;background:rgba(212,175,55,0.1);border:1px solid rgba(212,175,55,0.2);font-size:12px;color:#D4AF37;margin-bottom:20px}
.btn-gold{background:linear-gradient(135deg,#D4AF37,#b8962e);color:#09090f;font-weight:700;font-size:15px;padding:13px 24px;border-radius:10px;border:none;cursor:pointer;transition:all 0.2s;display:inline-flex;align-items:center;gap:8px;width:100%;justify-content:center;box-sizing:border-box}
.btn-gold:hover{filter:brightness(1.05)}
.btn-gold:disabled{opacity:0.35;cursor:not-allowed}
.h1{font-size:clamp(24px,3.5vw,44px);font-weight:900;color:#fff;line-height:1.1;margin-bottom:14px}
.h1 span{background:linear-gradient(135deg,#D4AF37,#f5d76e);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.sub{font-size:15px;color:#9ca3af;line-height:1.7;margin-bottom:28px}
#landing{display:none;grid-template-columns:1fr 1fr;min-height:100vh}
#landing.active{display:grid}
#onboarding,#completion,.mobile-landing{display:none;min-height:100vh}
#onboarding.active,#completion.active,.mobile-landing.active{display:block}
.mobile-landing{display:none;padding:60px 24px;flex-direction:column;justify-content:center}
.left-col{padding:60px 56px 60px 0;display:flex;flex-direction:column;justify-content:center;background:radial-gradient(ellipse at 0% 50%,rgba(212,175,55,0.06) 0%,transparent 60%)}
.right-col{padding:60px 0 60px 56px;display:flex;flex-direction:column;justify-content:center;border-left:1px solid rgba(255,255,255,0.06);background:#0d0d18}
.features{list-style:none;display:flex;flex-direction:column;gap:12px;margin-bottom:32px}
.features li{display:flex;align-items:center;gap:10px;font-size:14px;color:#e5e7eb}
.features li span{font-size:18px}
.proof-item{display:flex;align-items:center;gap:14px;padding:12px 0;border-bottom:1px solid rgba(255,255,255,0.05)}
.proof-avatar{width:38px;height:38px;border-radius:50%;background:linear-gradient(135deg,#D4AF37,#b8962e);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:12px;color:#09090f;flex-shrink:0}
.proof-text{font-size:13px;color:#9ca3af}
.proof-text strong{color:#fff}
.q-wrap{max-width:600px;margin:0 auto;padding:48px 20px}
.q-block{animation:fadeUp 0.4s ease}
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
.opt-multi.selected .opt-check{background:#D4AF37;color:#09090f}
.q-footer{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-top:2px}
.q-back{background:none;border:none;color:#6b7280;font-size:14px;cursor:pointer;padding:8px 0;font-family:inherit;transition:color 0.2s}
.q-back:hover{color:#9ca3af}
.q-next{flex:1;background:linear-gradient(135deg,#D4AF37,#b8962e);color:#09090f;font-weight:700;font-size:15px;padding:13px;border-radius:10px;border:none;cursor:pointer;transition:all 0.2s;font-family:inherit}
.q-next:disabled{opacity:0.35;cursor:not-allowed}
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
#landing{display:none!important}
.mobile-landing.active{display:flex!important}
#onboarding.active,#completion.active{display:block!important}
.complete-wrap{padding:40px 16px}
.complete-card{padding:36px 20px}
.why-grid{grid-template-columns:1fr}
.complete-card h2{font-size:22px}
}"""

JS = """const QUESTIONS=%s;
const TOOL_MAP=%s;
const SEGMENTS=%s;
const STORED_EMAIL=localStorage.getItem("vault_email")||"";
const STORED_LEAD=JSON.parse(localStorage.getItem("vault_lead")||"{}");
let currentQ=parseInt(STORED_LEAD.currentQ||"0");
let answers=STORED_LEAD.answers||{};
let multi=STORED_LEAD.multi||{};
function $id(id){return document.getElementById(id);}
function show(id){
  ["landing","mobileLanding","onboarding","completion"].forEach(x=>{const e=$id(x);if(e){e.style.display="none";e.classList.remove("active");}});
  const e=$id(id);if(!e)return;
  if(id==="mobileLanding"&&window.innerWidth>768){$id("landing").style.display="grid";$id("landing").classList.add("active");}
  else if(id==="landing"&&window.innerWidth<=768){$id("mobileLanding").style.display="flex";$id("mobileLanding").classList.add("active");}
  else{e.style.display="block";e.classList.add("active");}
}
function startOnboarding(){if(!STORED_EMAIL){window.location.href="index.html";return;}show("onboarding");renderQuestion();}
function renderQuestion(){
  document.querySelectorAll(".q-block").forEach(e=>e.classList.remove("active"));
  const q=QUESTIONS[currentQ];const e=$id("q-"+q.id);if(e)e.classList.add("active");
  if(q.type==="multi"){
    const sel=multi[q.id]||[];document.querySelectorAll(".opt-multi").forEach(b=>b.classList.toggle("selected",sel.includes(b.dataset.value)));
    const nb=$id("next-btn-"+q.id);if(nb)nb.disabled=false;
  }else{
    const saved=answers[q.id];document.querySelectorAll(".opt-card:not(.opt-multi)").forEach(b=>b.classList.toggle("selected",b.dataset.value===saved));
    const nb=$id("next-btn-"+q.id);if(nb)nb.disabled=!saved;
  }
  const bb=$id("back-"+q.id);if(bb)bb.style.display=currentQ>0?"inline-block":"none";
  saveProgress();
}
function selectOption(btn,qId){
  const p=btn.closest(".q-options");if(p)p.querySelectorAll(".opt-card").forEach(b=>b.classList.remove("selected"));
  btn.classList.add("selected");answers[qId]=btn.dataset.value;
  const nb=$id("next-btn-"+qId);if(nb)nb.disabled=false;saveProgress();setTimeout(()=>nextQuestion(true),350);
}
function toggleMulti(btn,qId){btn.classList.toggle("selected");if(!multi[qId])multi[qId]=[];const v=btn.dataset.value;if(multi[qId].includes(v))multi[qId]=multi[qId].filter(x=>x!==v);else multi[qId].push(v);saveProgress();}
function nextQuestion(auto){
  const q=QUESTIONS[currentQ];if(!auto&&q.type!=="multi"&&!answers[q.id])return;
  if(currentQ<QUESTIONS.length-1){currentQ++;renderQuestion();}else{finishQuestionnaire();}
}
function prevQuestion(){if(currentQ>0){currentQ--;renderQuestion();}}
function finishQuestionnaire(){
  show("completion");
  const seg=answers.primary_role||"other";
  const segData=SEGMENTS[seg]||SEGMENTS.other;
  const badge=$id("segBadge");if(badge)badge.textContent="🎯 "+segData.l;
  const interested=multi.tools_interested||[];
  let tools=new Set();
  if(interested.length>0){interested.forEach(cat=>{const ct=TOOL_MAP[cat]||[];ct.slice(0,3).forEach(t=>tools.add(t));});}
  else{(segData.t||[]).slice(0,5).forEach(t=>tools.add(t));}
  const matchDiv=$id("matchTools");if(matchDiv){matchDiv.innerHTML=Array.from(tools).slice(0,6).map(t=>'<span class="match-tool">'+t+"</span>").join("");}
  const goalMap={save_time:"Save Time",make_money:"Make Money",scale_content:"Scale Content",learn:"Learn Skills",automate:"Automate Work",create:"Create Better"};
  const chalMap={dont_know_where_to_start:"Where to Start",quality:"Quality Issues",speed:"Speed",cost:"Cost",finding_right_tools:"Finding Tools"};
  const budgMap={free_only:"Free Only",under_50:"Under $50/mo",50_to_200:"$50-200/mo",200_to_500:"$200-500/mo",over_500:"$500+/mo"};
  if($id("whyGoal"))$id("whyGoal").textContent=goalMap[answers.primary_goal]||"Your Goal";
  if($id("whyGoalText"))$id("whyGoalText").textContent="Focus on tools that automate: "+(goalMap[answers.primary_goal]||"your goals");
  if($id("whyChallenge"))$id("whyChallenge").textContent=chalMap[answers.biggest_challenge]||"Your Challenge";
  if($id("whyChallengeText"))$id("whyChallengeText").textContent="We'll recommend tools that directly fix: "+(chalMap[answers.biggest_challenge]||"your challenge");
  if($id("whyBudget"))$id("whyBudget").textContent=budgMap[answers.budget]||answers.budget||"Budget";
  if($id("whyBudgetText"))$id("whyBudgetText").textContent="Best tools within your "+(budgMap[answers.budget]||"budget")+" range";
  if($id("whyBest"))$id("whyBest").textContent=segData.l;
  if($id("whyBestText"))$id("whyBestText").textContent=segData.b;
  if($id("emailConfirmed"))$id("emailConfirmed").textContent="✅ "+STORED_EMAIL+" — You are on the list!";
  const lead={email:STORED_EMAIL,segment:seg,answers,multi,recommendedTools:Array.from(tools).slice(0,6),budget:answers.budget,primaryGoal:answers.primary_goal,biggestChallenge:answers.biggest_challenge,howSolving:answers.how_solving,howOften:answers.how_often,toolsInterested:interested,timestamp:new Date().toISOString()};
  try{const key="vault_lead_"+STORED_EMAIL.replace(/[^a-z0-9]/gi,"_");localStorage.setItem(key,JSON.stringify(lead));const all=JSON.parse(localStorage.getItem("vault_all_leads")||"[]");all.push(lead);localStorage.setItem("vault_all_leads",JSON.stringify(all));}catch(e){console.error(e);}
}
function saveProgress(){try{localStorage.setItem("vault_lead",JSON.stringify({currentQ,answers,multi}));}catch(e){}}
if(window.innerWidth<=768){$id("mobileLanding").style.display="flex";$id("mobileLanding").classList.add("active");}else{$id("landing").style.display="grid";$id("landing").classList.add("active");}
if(STORED_LEAD.currentQ>0){show("onboarding");renderQuestion();}"""

html = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>Get Matched With the Right AI Tools — AI Tools Vault</title>\n<meta name="description" content="Answer 7 quick questions and get personalized AI tool recommendations. Get notified when new matching tools are added.">\n<link rel="preconnect" href="https://fonts.googleapis.com">\n<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">\n<style>'+CSS+'</style>\n</head>\n<body>\n<div id="landing">\n<div class="left-col">\n<div class="badge">🧠 AI Tools Vault — Personalized Matching</div>\n<h1 class="h1">Find Your Perfect <span>AI Tools</span> in 2 Minutes</h1>\n<p class="sub">Answer 7 quick questions and we will show you the exact AI tools that match your goals, budget, and workflow. Then we email you when new matching tools are added.</p>\n<ul class="features">\n<li><span>🎯</span> Personalized tool recommendations for your specific goals</li>\n<li><span>🔔</span> Email alerts when new tools matching your profile are added</li>\n<li><span>💰</span> Find tools that match your exact budget</li>\n<li><span>⚡</span> Takes under 2 minutes — then you are set for life</li>\n</ul>\n<button class="btn-gold" onclick="startOnboarding()">Start My Personalized List →</button>\n</div>\n<div class="right-col">\n<div class="badge" style="margin-bottom:14px">276+ People Already Matched</div>\n<div class="proof-item"><div class="proof-avatar">MK</div><div class="proof-text"><strong>Maya K. — Content Creator</strong><br>Found 5 tools that now save her 3 hours a day</div></div>\n<div class="proof-item"><div class="proof-avatar">CD</div><div class="proof-text"><strong>Chris D. — Developer</strong><br>Cut his coding time in half using AI pair programming</div></div>\n<div class="proof-item"><div class="proof-avatar">SM</div><div class="proof-text"><strong>Sarah M. — Entrepreneur</strong><br>Ditched 3 tools for 1 that does everything better</div></div>\n<div class="proof-item"><div class="proof-avatar">JR</div><div class="proof-text"><strong>James R. — Marketer</strong><br>Gets email alerts when new tools match his niche</div></div>\n</div>\n</div>\n<div class="mobile-landing" id="mobileLanding">\n<div class="badge">🧠 AI Tools Vault</div>\n<h1 class="h1">Find Your Perfect <span>AI Tools</span></h1>\n<p class="sub" style="font-size:14px;margin-bottom:24px">Answer 7 questions and get matched with the right AI tools for your goals. Get email alerts when new tools are added.</p>\n<button class="btn-gold" onclick="startOnboarding()">Start My Personalized List →</button>\n</div>\n<div id="onboarding" class="q-wrap">\n'+ALLQ+'\n</div>\n<div id="completion" class="complete-wrap">\n<div class="complete-card">\n<div class="check-circle">✅</div>\n<div class="seg-badge" id="segBadge">🎯 Your Profile Is Ready</div>\n<h2>You Are All Set!</h2>\n<p>We have matched you with the best AI tools based on your answers. When new tools are added that match your profile, we will email you automatically.</p>\n<div class="match-label">Your personalized AI tool picks:</div>\n<div class="match-tools" id="matchTools"></div>\n<div class="why-section">\n<div class="why-title">Based on your answers, here is what we recommend:</div>\n<div class="why-grid">\n<div class="why-item"><strong id="whyGoal">-</strong><p id="whyGoalText">-</p></div>\n<div class="why-item"><strong id="whyChallenge">-</strong><p id="whyChallengeText">-</p></div>\n<div class="why-item"><strong id="whyBudget">-</strong><p id="whyBudgetText">-</p></div>\n<div class="why-item"><strong id="whyBest">-</strong><p id="whyBestText">-</p></div>\n</div>\n</div>\n<div class="email-ok"><p id="emailConfirmed"></p></div>\n<button class="btn-gold" style="margin-bottom:12px" onclick="window.location.href=\'index.html\'">Browse All 276+ Tools →</button>\n<p class="complete-note">📬 You will receive emails when new tools matching your profile are added. No spam. Unsubscribe anytime.</p>\n</div>\n</div>\n<script>\n'+JS%(QJ,TMJ,SEJ)+'\n</script>\n</body>\n</html>'

with open("/workspace/ai-tools-directory/dist/onboarding.html","w",encoding="utf-8") as f:
    f.write(html)
sz = os.path.getsize("/workspace/ai-tools-directory/dist/onboarding.html")
print("DONE: %d bytes (%dKB)"%(sz,sz//1024))
print("Questions: %d"%n)
