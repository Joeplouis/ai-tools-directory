#!/usr/bin/env python3
"""Build Mailchimp-style popup for AI Tools Vault"""
import json, os

INDUSTRIES = [
    {"v":"content_media","l":"Content & Media","d":"YouTube, blogging, podcasts, social media"},
    {"v":"marketing","l":"Marketing & Advertising","d":"Digital marketing, SEO, paid ads, email"},
    {"v":"software_tech","l":"Software & Technology","d":"Apps, SaaS, developer tools, AI platforms"},
    {"v":"ecommerce","l":"E-Commerce & Retail","d":"Online stores, dropshipping, product businesses"},
    {"v":"education","l":"Education & Learning","d":"Courses, tutoring, training, edtech"},
    {"v":"healthcare","l":"Healthcare & Wellness","d":"Medical, fitness, mental health, nutrition"},
    {"v":"finance","l":"Finance & Business","d":"Accounting, investing, business consulting"},
    {"v":"creative","l":"Creative & Design","d":"Graphic design, video production, arts"},
    {"v":"real_estate","l":"Real Estate","d":"Property, agents, investments, rentals"},
    {"v":"other","l":"Other","d":"Something else not listed here"},
]

GOALS = [
    {"v":"drive_sales","l":"Drive Sales Revenue","i":"💰"},
    {"v":"save_time","l":"Save Time with Automation","i":"⚡"},
    {"v":"attract_customers","l":"Attract More Customers","i":"📣"},
    {"v":"optimize_marketing","l":"Optimize Marketing Performance","i":"📊"},
    {"v":"send_sms","l":"Send SMS Campaigns","i":"📱"},
    {"v":"crm","l":"Manage Customer Relationships","i":"🤝"},
    {"v":"design_emails","l":"Design Effective Emails","i":"✉️"},
    {"v":"switch_tools","l":"Switch from Another Tool","i":"🔄"},
]

STEP1_HTML = ""
for ind in INDUSTRIES:
    STEP1_HTML += '<button class="mp-opt" data-v="'+ind["v"]+'" onclick="selectInd(this,&quot;'+ind["v"]+'&quot;)"><div class="mp-opt-main"><div class="mp-opt-label">'+ind["l"]+'</div><div class="mp-opt-sub">'+ind["d"]+'</div></div><div class="mp-check">✓</div></button>'

STEP2_HTML = ""
for g in GOALS:
    STEP2_HTML += '<button class="mp-goal" data-v="'+g["v"]+'" onclick="toggleGoal(this,&quot;'+g["v"]+'&quot;)"><div class="mp-goal-icon">'+g["i"]+'</div><div class="mp-goal-label">'+g["l"]+'</div><div class="mp-goal-check">✓</div></button>'

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"Inter",system-ui,sans-serif}
.mp-overlay{display:none;position:fixed;inset:0;background:rgba(9,9,15,0.92);backdrop-filter:blur(6px);z-index:9999;align-items:center;justify-content:center;padding:20px}
.mp-overlay.active{display:flex;align-items:center;justify-content:center}
.mp-modal{background:#13131f;border:1px solid rgba(255,255,255,0.1);border-radius:22px;max-width:560px;width:100%;max-height:90vh;overflow-y:auto;position:relative;animation:mpIn 0.35s cubic-bezier(0.16,1,0.3,1)}
@keyframes mpIn{from{opacity:0;transform:scale(0.93) translateY(10px)}to{opacity:1;transform:scale(1) translateY(0)}}
.mp-head{padding:28px 32px 0}
.mp-badge{display:inline-flex;align-items:center;gap:6px;padding:5px 12px;background:rgba(212,175,55,0.1);border:1px solid rgba(212,175,55,0.25);border-radius:99px;font-size:11px;color:#D4AF37;font-weight:600;letter-spacing:0.5px;margin-bottom:12px}
.mp-title{font-size:clamp(18px,3vw,22px);font-weight:800;color:#fff;line-height:1.2;margin-bottom:6px}
.mp-sub{font-size:13px;color:#9ca3af;line-height:1.5;margin-bottom:20px}
.mp-body{padding:0 32px 28px;display:none}
.mp-body.active{display:block}
.mp-hint{font-size:11px;color:#6b7280;margin-bottom:12px;font-weight:600;letter-spacing:0.5px;text-transform:uppercase}
.mp-opt{display:flex;align-items:center;width:100%;padding:12px 14px;background:#0d0d18;border:1.5px solid rgba(255,255,255,0.07);border-radius:12px;cursor:pointer;transition:all 0.2s;margin-bottom:7px;text-align:left;font-family:inherit}
.mp-opt:hover{border-color:rgba(212,175,55,0.3)}
.mp-opt.selected{border-color:#D4AF37;background:rgba(212,175,55,0.06)}
.mp-opt.selected .mp-check{background:#D4AF37;color:#09090f}
.mp-opt-main{flex:1}
.mp-opt-label{font-size:13px;font-weight:700;color:#f0f0f0}
.mp-opt-sub{font-size:11px;color:#9ca3af}
.mp-check{width:20px;height:20px;border-radius:50%;border:1.5px solid rgba(255,255,255,0.2);display:flex;align-items:center;justify-content:center;font-size:10px;color:transparent;transition:all 0.2s;flex-shrink:0}
.mp-goal{display:flex;align-items:center;gap:12px;width:100%;padding:11px 14px;background:#0d0d18;border:1.5px solid rgba(255,255,255,0.07);border-radius:12px;cursor:pointer;transition:all 0.2s;margin-bottom:7px;text-align:left;font-family:inherit}
.mp-goal:hover{border-color:rgba(212,175,55,0.3)}
.mp-goal.selected{border-color:#D4AF37;background:rgba(212,175,55,0.06)}
.mp-goal.selected .mp-goal-check{background:#D4AF37;color:#09090f}
.mp-goal-icon{font-size:18px;width:32px;height:32px;background:rgba(255,255,255,0.04);border-radius:8px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.mp-goal-label{font-size:13px;font-weight:600;color:#f0f0f0;flex:1}
.mp-goal-check{width:20px;height:20px;border-radius:50%;border:1.5px solid rgba(255,255,255,0.2);display:flex;align-items:center;justify-content:center;font-size:10px;color:transparent;transition:all 0.2s;flex-shrink:0}
.mp-selected-bar{background:rgba(212,175,55,0.08);border:1px solid rgba(212,175,55,0.2);border-radius:10px;padding:10px 14px;margin-bottom:14px;font-size:12px;color:#D4AF37;font-weight:600;text-align:center;display:none}
.mp-selected-bar.show{display:block}
.mp-foot{padding:0 32px 28px;display:none}
.mp-foot.active{display:block}
.mp-skip{background:none;border:none;color:#6b7280;font-size:12px;cursor:pointer;padding:10px 0;font-family:inherit;transition:color 0.2s;text-decoration:underline}
.mp-skip:hover{color:#9ca3af}
.mp-next{flex:1;background:linear-gradient(135deg,#D4AF37,#b8962e);color:#09090f;font-weight:700;font-size:14px;padding:12px;border-radius:10px;border:none;cursor:pointer;transition:all 0.2s;font-family:inherit}
.mp-next:disabled{opacity:0.35;cursor:not-allowed}
.mp-next:hover:not(:disabled){filter:brightness(1.05)}
.mp-foot-row{display:flex;gap:12px;align-items:center;justify-content:space-between}
.mp-logo-row{padding:16px 32px 24px;border-top:1px solid rgba(255,255,255,0.05);display:flex;align-items:center;justify-content:space-between}
.mp-logo{font-size:12px;color:#6b7280;font-weight:600;letter-spacing:0.5px}
.mp-powered{font-size:11px;color:#6b7280}
.mp-powered span{color:#D4AF37}
.mp-close{position:absolute;top:16px;right:16px;width:30px;height:30px;border-radius:50%;background:rgba(255,255,255,0.06);border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:14px;color:#9ca3af;transition:all 0.2s}
.mp-close:hover{background:rgba(255,255,255,0.1);color:#fff}
.mp-step-dots{display:flex;gap:6px;margin-bottom:18px}
.mp-dot{width:6px;height:6px;border-radius:50%;background:#2a2a3e;transition:all 0.3s}
.mp-dot.active{background:#D4AF37;width:20px;border-radius:3px}
.mp-dot.done{background:rgba(212,175,55,0.4)}
"""

JS = """
var selectedIndustry="";
var selectedGoals=[];
var step=0;
var totalSteps=2;

function $(id){return document.getElementById(id);}
function showStep(s){
  document.querySelectorAll('.mp-body').forEach(function(e){e.classList.remove('active');});
  document.querySelectorAll('.mp-foot').forEach(function(e){e.classList.remove('active');});
  var bodies=document.querySelectorAll('.mp-body');
  var foots=document.querySelectorAll('.mp-foot');
  if(bodies[s])bodies[s].classList.add('active');
  if(foots[s])foots[s].classList.add('active');
  document.querySelectorAll('.mp-dot').forEach(function(d,i){
    d.className='mp-dot'+(i<s?' done':i===s?' active':'');
  });
}
function selectInd(btn,v){
  document.querySelectorAll('.mp-opt').forEach(function(b){b.classList.remove('selected');});
  btn.classList.add('selected');
  selectedIndustry=v;
  $('indNext').disabled=false;
}
function toggleGoal(btn,v){
  btn.classList.toggle('selected');
  if(selectedGoals.includes(v)){selectedGoals=selectedGoals.filter(function(g){return g!==v;});}
  else{
    if(selectedGoals.length>=3){btn.classList.remove('selected');return;}
    selectedGoals.push(v);
  }
  var n=selectedGoals.length;
  var bar=$('selBar');
  if(bar){bar.textContent=n>0?'Selected: '+n+'/3 — you can add more or continue':'Select up to 3 (or skip)';bar.classList.add('show');}
  $('goalNext').disabled=n===0;
}
function skipGoals(){
  selectedGoals=[];
  finishSurvey();
}
function finishSurvey(){
  var lead={industry:selectedIndustry,goals:selectedGoals,timestamp:new Date().toISOString(),source:'popup'};
  try{
    var existing=JSON.parse(localStorage.getItem('vault_popup_leads')||'[]');
    existing.push(lead);
    localStorage.setItem('vault_popup_lead',JSON.stringify(lead));
    localStorage.setItem('vault_popup_leads',JSON.stringify(existing));
    localStorage.setItem('vault_saw_onboarding','true');
  }catch(e){}
  closePopup();
  setTimeout(function(){window.location.href='onboarding.html';},300);
}
function closePopup(){
  var overlay=$('mpOverlay');
  if(overlay)overlay.classList.remove('active');
  try{localStorage.setItem('vault_saw_onboarding','true');}catch(e){}
}
function initPopup(){
  try{
    if(localStorage.getItem('vault_saw_onboarding')==='true')return;
  }catch(e){}
  setTimeout(function(){
    var overlay=$('mpOverlay');
    if(overlay)overlay.classList.add('active');
  },1200);
}
document.addEventListener('DOMContentLoaded',initPopup);
"""

html='<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>AI Tools Vault</title>\n<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">\n<style>'+CSS+'</style>\n</head>\n<body>\n<div class="mp-overlay" id="mpOverlay">\n<div class="mp-modal">\n<button class="mp-close" onclick="closePopup()">✕</button>\n<div class="mp-head">\n<div class="mp-badge">🧠 AI Tools Vault</div>\n<div class="mp-step-dots"><div class="mp-dot active" id="dot0"></div><div class="mp-dot" id="dot1"></div></div>\n<div class="mp-title" id="mpTitle">Make AI Tools Vault work for you</div>\n<div class="mp-sub" id="mpSub">Answer a couple quick questions so we can show you the tools and strategies most relevant to your industry.</div>\n</div>\n\n<div class="mp-body active" id="body0">\n<div class="mp-hint">Which best describes your industry?</div>\n'+STEP1_HTML+'\n</div>\n<div class="mp-body" id="body1">\n<div class="mp-hint">What are the top 3 things you want to achieve? (Select up to 3)</div>\n<div class="mp-selected-bar" id="selBar">Select up to 3 — or skip this</div>\n'+STEP2_HTML+'\n</div>\n\n<div class="mp-foot active" id="foot0">\n<div class="mp-foot-row">\n<button class="mp-skip" onclick="closePopup()">Skip</button>\n<button class="mp-next" id="indNext" disabled onclick="document.querySelectorAll(\'.mp-body\')[1].classList.add(\'active\');document.querySelectorAll(\'.mp-foot\')[1].classList.add(\'active\');document.querySelectorAll(\'.mp-foot\')[0].classList.remove(\'active\');document.querySelectorAll(\'.mp-dot\')[0].classList.add(\'done\');document.querySelectorAll(\'.mp-dot\')[0].classList.remove(\'active\');document.querySelectorAll(\'.mp-dot\')[1].classList.add(\'active\');">Continue →</button>\n</div>\n</div>\n<div class="mp-foot" id="foot1">\n<div class="mp-foot-row">\n<button class="mp-skip" onclick="skipGoals()">Skip this</button>\n<button class="mp-next" id="goalNext" onclick="finishSurvey()">See My Results →</button>\n</div>\n</div>\n\n<div class="mp-logo-row">\n<div class="mp-logo">AI TOOLS VAULT</div>\n<div class="mp-powered">Powered by <span>AI Tools Vault</span></div>\n</div>\n</div>\n</div>\n<script>\n'+JS+'\n</script>\n</body>\n</html>'

os.makedirs('/workspace/ai-tools-directory/dist', exist_ok=True)
with open('/workspace/ai-tools-directory/dist/popup.html','w',encoding='utf-8') as f:
    f.write(html)
sz=os.path.getsize('/workspace/ai-tools-directory/dist/popup.html')
print('DONE: %d bytes (%dKB)'%(sz,sz//1024))
print('Industries: %d | Goals: %d'%(len(INDUSTRIES),len(GOALS)))
