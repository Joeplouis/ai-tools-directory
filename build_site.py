import json, os, re

with open('/workspace/ai-tools-directory/src/data/tools.json') as f:
    tools = json.load(f)

with open('/tmp/cat_data.json') as f:
    data = json.load(f)

cats_str = data['cats_str']
icons_str = data['icons_str']
colors_str = data['colors_str']
n = data['n']
ncat = data['ncat']

cat_icon_list = {'Text & Writing':'✍️','Image Generation':'🖼️','Video & Animation':'🎬','Voice & Audio':'🎙️','Coding & Dev':'💻','Marketing & Sales':'📈','Productivity':'⚡','AI Agents & Automation':'🤖','Research & Analytics':'🔬','Business & Finance':'💼','Design & Art':'🎨','Education & Learning':'📚','Other':'🔧'}
cat_color_list = {'Text & Writing':'#06b6d4','Image Generation':'#ec4899','Video & Animation':'#f97316','Voice & Audio':'#8b5cf6','Coding & Dev':'#10b981','Marketing & Sales':'#f59e0b','Productivity':'#3b82f6','AI Agents & Automation':'#14b8a6','Research & Analytics':'#6366f1','Business & Finance':'#84cc16','Design & Art':'#e11d48','Education & Learning':'#0ea5e9','Other':'#6b7280'}

cat_counts = {}
for t in tools:
    cat_counts[t['category']] = cat_counts.get(t['category'], 0) + 1

cat_tiles = '<button class="cat-btn active" id="cat-All" onclick="filterCat(&apos;All&apos;)"><div class="cat-icon" style="background:rgba(212,175,55,0.12)"><span style="font-size:22px">🧠</span></div><div class="cat-name">All Tools</div><span class="n">%d tools</span></button>' % n
for cat, cnt in sorted(cat_counts.items(), key=lambda x:-x[1]):
    ic = cat_icon_list.get(cat,'🔧')
    col = cat_color_list.get(cat,'#6b7280')
    cat_tiles += '\n<button class="cat-btn" id="cat-%s" onclick="filterCat(&apos;%s&apos;)"><div class="cat-icon" style="background:%s18"><span style="font-size:22px">%s</span></div><div class="cat-name">%s</div><span class="n">%d tools</span></button>' % (cat,cat,col,ic,cat,cnt)

cats_opts = ''.join(['<option value="%s">%s</option>' % (c,c) for c in sorted(cat_counts.keys())])

pcols = {'free':'#10b981','freemium':'#f59e0b','paid':'#ec4899'}
featured = sorted(tools, key=lambda x: -x.get('views',0))[:50]
cards = ''
for t in featured:
    col = cat_color_list.get(t['category'],'#6b7280')
    pc = pcols.get(t['pricing'],'#6b7280')
    vk = str(int(t.get('views',0)//1000))+'K' if t.get('views',0)>=1000 else str(t.get('views',0))
    ic = cat_icon_list.get(t['category'],'🔧')
    d = t.get('description','')[:130].replace('"','&quot;').replace("'",'&#39;').replace('<','&lt;').replace('>','&gt;')
    nm = t['name'].replace('"','&quot;')
    catn = t['category'].replace('"','&quot;')
    ws = t.get('website','#').replace('"','&quot;')
    cards += '<div class="card"><div class="card-top"><div class="card-icon" style="background:%s18;border:1px solid %s30"><span style="font-size:20px">%s</span></div><div class="card-body"><div class="card-name">%s</div><div class="card-cat" style="color:%s">%s</div></div><div class="card-price" style="background:%s18;color:%s">%s</div></div><p class="card-desc">%s...</p><div class="card-foot"><span class="card-views">👁 %s/mo</span><a href="%s" target="_blank" class="card-link">🌐 Visit →</a></div></div>' % (col,col,ic,nm,col,catn,pc,pc,t['pricing'],d,vk,ws)

# Build tools JS array
def e(s):
    s = str(s)
    for old, new in [('\\','\\\\'),('"','\\"'),("\n"," "),("\r","")]:
        s = s.replace(old, new)
    return s

tools_js = ',\\\n  '.join([
    '{id:%d,name:"%s",desc:"%s",cat:"%s",pricing:"%s",website:"%s",views:%d}' % (
        i+1, e(t['name']), e(t.get('description','')), e(t['category']),
        t.get('pricing','freemium'), e(t.get('website','#')), t.get('views',0)
    ) for i,t in enumerate(tools)
])

# Escape % in CSS gradient values for Python %
def fix_pct(s):
    return re.sub(r'(\d+)%', r'\1%%', s)

html = fix_pct('''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI Tools Vault — 1,000+ AI Tools Directory | Search by Category</title>
<meta name="description" content="Search 1,000+ AI tools by category. Find any AI tool for your business — image generators, video AI, writing tools, voice cloning and more. Updated daily.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"Inter",system-ui,sans-serif;background:#09090f;color:#f0f0f0;line-height:1.6}
a{text-decoration:none;color:inherit}
.container{max-width:1200px;margin:0 auto;padding:0 24px}
nav{position:sticky;top:0;z-index:100;background:rgba(9,9,15,0.97);backdrop-filter:blur(16px);border-bottom:1px solid rgba(255,255,255,0.06)}
.nav-inner{display:flex;align-items:center;justify-content:space-between;height:64px}
.logo{font-size:20px;font-weight:900;color:#fff}
.logo span{color:#D4AF37}
.nav-a{font-size:14px;color:#9ca3af;font-weight:500;transition:color .2s}
.nav-a:hover{color:#fff}
.nav-cta{background:linear-gradient(135deg,#D4AF37,#b8962e);color:#09090f;font-weight:700;font-size:13px;padding:9px 20px;border-radius:8px;border:none;cursor:pointer}
.hero{padding:80px 0 60px;text-align:center;background:radial-gradient(ellipse at 50%% 0%%,rgba(212,175,55,0.09) 0%%,transparent 65%%)}
.hero-badge{display:inline-flex;align-items:center;gap:8px;padding:8px 16px;border-radius:99px;background:rgba(212,175,55,0.1);border:1px solid rgba(212,175,55,0.2);font-size:13px;color:#D4AF37;margin-bottom:28px}
.hero h1{font-size:clamp(36px,6vw,68px);font-weight:900;line-height:1.08;color:#fff;margin-bottom:16px}
.hero h1 span{background:linear-gradient(135deg,#D4AF37,#f5d76e);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero-sub{font-size:17px;color:#9ca3af;max-width:520px;margin:0 auto}
.search-wrap{max-width:660px;margin:0 auto}
.search-bar{display:flex;background:#13131f;border:2px solid rgba(255,255,255,0.1);border-radius:14px;overflow:hidden;transition:border-color .2s}
.search-bar:focus-within{border-color:rgba(212,175,55,0.5)}
.search-bar input{flex:1;background:none;border:none;outline:none;padding:16px 20px;font-size:16px;color:#fff;font-family:inherit}
.search-bar input::placeholder{color:#4b5563}
.search-bar button{background:linear-gradient(135deg,#D4AF37,#b8962e);color:#09090f;border:none;padding:16px 28px;font-weight:700;font-size:15px;cursor:pointer;white-space:nowrap}
.pop-tags{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:14px}
.pop-tag{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:#9ca3af;padding:5px 12px;border-radius:99px;font-size:12px;cursor:pointer;transition:all .2s}
.pop-tag:hover{border-color:rgba(212,175,55,0.4);color:#D4AF37}
.stats{display:flex;justify-content:center;gap:48px;margin-top:48px;padding-top:40px;border-top:1px solid rgba(255,255,255,0.05)}
.stat{text-align:center}
.stat .num{font-size:28px;font-weight:900;color:#D4AF37}
.stat .lbl{font-size:12px;color:#6b7280;margin-top:4px}
.section{padding:64px 0}
.section-label{font-size:11px;font-weight:700;color:#D4AF37;letter-spacing:2.5px;text-transform:uppercase;margin-bottom:8px}
.section-title{font-size:30px;font-weight:800;color:#fff;margin-bottom:32px}
.cat-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}
.cat-btn{display:flex;flex-direction:column;align-items:center;padding:20px 12px;background:#13131f;border:1px solid rgba(255,255,255,0.06);border-radius:14px;cursor:pointer;transition:all .2s;text-align:center}
.cat-btn:hover{border-color:rgba(212,175,55,0.3);transform:translateY(-2px)}
.cat-btn.active{border-color:rgba(212,175,55,0.5);background:rgba(212,175,55,0.08)}
.cat-icon{width:48px;height:48px;border-radius:12px;display:flex;align-items:center;justify-content:center;margin-bottom:10px;font-size:22px}
.cat-name{font-size:12px;font-weight:600;color:#e5e7eb;margin-bottom:4px;line-height:1.3}
.cat-btn .n{font-size:11px;color:#6b7280}
.tool-count{font-size:14px;color:#9ca3af;margin-bottom:20px}
.tool-count strong{color:#fff}
.tool-count span{color:#D4AF37;font-weight:700}
.filters{display:flex;gap:8px;margin-bottom:24px;flex-wrap:wrap}
.fil-btn{padding:7px 14px;border-radius:8px;border:1px solid rgba(255,255,255,0.08);background:#13131f;color:#9ca3af;font-size:13px;cursor:pointer;transition:all .2s;font-family:inherit}
.fil-btn:hover{border-color:rgba(212,175,55,0.3);color:#fff}
.fil-btn.active{background:rgba(212,175,55,0.12);border-color:rgba(212,175,55,0.5);color:#D4AF37}
.tool-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:16px}
.card{background:#13131f;border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:20px;transition:all .2s;display:flex;flex-direction:column}
.card:hover{border-color:rgba(212,175,55,0.2);transform:translateY(-1px)}
.card-top{display:flex;align-items:flex-start;gap:14px;margin-bottom:12px}
.card-icon{width:44px;height:44px;border-radius:11px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.card-body{flex:1;min-width:0}
.card-name{font-size:15px;font-weight:700;color:#f0f0f0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.card-cat{font-size:12px;color:#9ca3af;margin-top:2px}
.card-price{padding:4px 10px;border-radius:99px;font-size:11px;font-weight:700;flex-shrink:0;align-self:flex-start}
.card-desc{font-size:13px;color:#9ca3af;line-height:1.6;flex:1;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;margin-bottom:14px}
.card-foot{display:flex;align-items:center;justify-content:space-between;padding-top:12px;border-top:1px solid rgba(255,255,255,0.04)}
.card-views{font-size:12px;color:#6b7280}
.card-link{font-size:13px;font-weight:600;color:#D4AF37;padding:5px 12px;border-radius:7px;background:rgba(212,175,55,0.1);transition:background .2s}
.card-link:hover{background:rgba(212,175,55,0.18)}
#modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.88);backdrop-filter:blur(8px);z-index:1000;align-items:center;justify-content:center;padding:20px}
.modal-box{background:#13131f;border:1px solid rgba(255,255,255,0.1);border-radius:22px;max-width:500px;width:100%;padding:40px;text-align:center}
.m-emoji{font-size:52px;margin-bottom:16px}
.m-title{font-size:24px;font-weight:800;color:#fff;margin-bottom:10px}
.m-sub{font-size:14px;color:#9ca3af;line-height:1.6;margin-bottom:24px}
.m-email{width:100%;padding:14px 16px;border-radius:10px;border:1px solid rgba(255,255,255,0.1);background:#09090f;color:#fff;font-size:15px;outline:none;font-family:inherit;margin-bottom:10px;box-sizing:border-box}
.m-email:focus{border-color:rgba(212,175,55,0.5)}
.m-btn{width:100%;padding:14px;border-radius:10px;background:linear-gradient(135deg,#D4AF37,#b8962e);color:#09090f;font-weight:800;font-size:15px;border:none;cursor:pointer;margin-bottom:10px}
.m-close{background:none;border:none;color:#6b7280;font-size:13px;cursor:pointer}
.m-ok{color:#10b981;font-size:15px;font-weight:600;margin-top:10px}
.submit-page{padding:60px 0 100px}
.submit-card{max-width:580px;margin:0 auto;background:#13131f;border:1px solid rgba(255,255,255,0.07);border-radius:20px;padding:40px}
.fg{margin-bottom:18px}
.fg label{display:block;font-size:13px;font-weight:600;color:#e5e7eb;margin-bottom:7px}
.fg input,.fg select,.fg textarea{width:100%;padding:12px 14px;border-radius:10px;border:1px solid rgba(255,255,255,0.1);background:#09090f;color:#fff;font-size:14px;outline:none;font-family:inherit;transition:border-color .2s;box-sizing:border-box}
.fg input:focus,.fg textarea:focus{border-color:rgba(212,175,55,0.5)}
.fg textarea{resize:vertical;min-height:96px}
footer{border-top:1px solid rgba(255,255,255,0.05);padding:36px 0;margin-top:40px}
.footer-inner{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px}
footer .copy{font-size:13px;color:#6b7280}
footer .links{display:flex;gap:24px}
footer .links a{font-size:13px;color:#6b7280;transition:color .2s}
footer .links a:hover{color:#fff}
.no-results{text-align:center;padding:80px 0}
.no-results .e{font-size:56px;margin-bottom:16px}
.no-results p{font-size:16px;color:#9ca3af}
.tools-page{padding-top:0}
.submit-success{text-align:center;padding:16px;background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);border-radius:12px;color:#10b981;font-weight:600;margin-bottom:16px;display:none}
@media(max-width:768px){
.hero{padding:48px 0 40px}
.stats{gap:24px;flex-wrap:wrap}
.tool-grid{grid-template-columns:1fr}
.cat-grid{grid-template-columns:repeat(auto-fill,minmax(120px,1fr))}
}
</style>
</head>
<body>

<nav>
  <div class="container">
    <div class="nav-inner">
      <div class="logo">🧠 AI Tools <span>Vault</span></div>
      <div style="display:flex;gap:28px;align-items:center">
        <a href="#" class="nav-a" onclick="resetAll()">All Tools</a>
        <a href="#submit" class="nav-a">Submit Tool</a>
        <button class="nav-cta" onclick="document.getElementById('submit').scrollIntoView({behavior:'smooth'})">List Free →</button>
      </div>
    </div>
  </div>
</nav>

<section class="hero">
  <div class="container">
    <div class="hero-badge">🧠 ''' + str(n) + ''' AI Tools · Updated Daily</div>
    <h1>Find Any <span>AI Tool</span><br>You Need</h1>
    <p class="hero-sub">Search by category, feature, or use case. Discover the perfect AI solution for your business in seconds.</p>
    <div class="search-wrap">
      <div class="search-bar">
        <input type="text" id="searchInput" placeholder="Search AI tools (e.g. image generator, video editing, voice cloning)..." onkeydown="if(event.key==='Enter')doSearch()">
        <button onclick="doSearch()">Search</button>
      </div>
      <div class="pop-tags">
        <span style="font-size:12px;color:#6b7280;align-self:center">Popular:</span>
        <button class="pop-tag" onclick="quickSearch('image generator')">🖼️ Image</button>
        <button class="pop-tag" onclick="quickSearch('video AI')">🎬 Video</button>
        <button class="pop-tag" onclick="quickSearch('voice cloning')">🎙️ Voice</button>
        <button class="pop-tag" onclick="quickSearch('coding')">💻 Coding</button>
        <button class="pop-tag" onclick="quickSearch('SEO')">📈 Marketing</button>
        <button class="pop-tag" onclick="quickSearch('writing')">✍️ Writing</button>
      </div>
    </div>
    <div class="stats">
      <div class="stat"><div class="num">''' + str(n) + '''</div><div class="lbl">AI Tools</div></div>
      <div class="stat"><div class="num">''' + str(ncat) + '''</div><div class="lbl">Categories</div></div>
      <div class="stat"><div class="num">Free</div><div class="lbl">To Search</div></div>
      <div class="stat"><div class="num">Daily</div><div class="lbl">Updates</div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-label">Browse</div>
    <h2 class="section-title">Explore ''' + str(ncat) + ''' Categories</h2>
    <div class="cat-grid">
      ''' + cat_tiles + '''
    </div>
  </div>
</section>

<section class="section tools-page">
  <div class="container">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;flex-wrap:wrap;gap:12px">
      <h2 class="section-title" id="toolsTitle" style="margin-bottom:0">Featured Tools</h2>
      <div class="filters">
        <button class="fil-btn active" id="prc-All" onclick="filterPrice('All')">All Types</button>
        <button class="fil-btn" id="prc-free" onclick="filterPrice('free')">Free</button>
        <button class="fil-btn" id="prc-freemium" onclick="filterPrice('freemium')">Freemium</button>
        <button class="fil-btn" id="prc-paid" onclick="filterPrice('paid')">Paid</button>
      </div>
    </div>
    <p class="tool-count" id="toolCount">Showing <strong>''' + str(min(50,len(tools))) + '''</strong> tools</p>
    <div class="tool-grid" id="toolGrid">
      ''' + cards + '''
    </div>
    <div id="noResults" class="no-results" style="display:none">
      <div class="e">🔍</div>
      <p>No tools found. Try a different search or category.</p>
    </div>
  </div>
</section>

<section class="submit-page" id="submit">
  <div class="container">
    <div style="text-align:center;margin-bottom:40px">
      <div class="section-label">For Tool Makers</div>
      <h2 class="section-title">Submit Your AI Tool</h2>
      <p style="color:#9ca3af;font-size:15px;max-width:440px;margin:0 auto">Reach thousands of users searching for AI solutions every day. Free listing — no credit card needed.</p>
    </div>
    <div class="submit-card">
      <div id="submitSuccess" class="submit-success">✅ Tool submitted! We'll review and add it within 24 hours.</div>
      <div class="fg"><label>Tool Name *</label><input type="text" id="s-name" placeholder="e.g. ChatGPT, Midjourney, Cursor"></div>
      <div class="fg"><label>Website URL *</label><input type="url" id="s-url" placeholder="https://yourtool.com"></div>
      <div class="fg"><label>Category *</label>
        <select id="s-cat"><option value="">Select category</option>''' + cats_opts + '''</select>
      </div>
      <div class="fg"><label>Pricing Model</label>
        <select id="s-price"><option value="freemium">Freemium</option><option value="free">Free</option><option value="paid">Paid</option></select>
      </div>
      <div class="fg"><label>Your Email (for listing confirmation) *</label><input type="email" id="s-email" placeholder="you@company.com"></div>
      <div class="fg"><label>Short Description (1-2 sentences) *</label><textarea id="s-desc" placeholder="What does your tool do? Who is it for?"></textarea></div>
      <button class="nav-cta" style="width:100%;padding:14px;font-size:15px" onclick="submitTool()">Submit Tool for Free →</button>
    </div>
  </div>
</section>

<div id="modal">
  <div class="modal-box">
    <div class="m-emoji" id="mEmoji">📬</div>
    <div class="m-title" id="mTitle">Get Notified First</div>
    <p class="m-sub" id="mSub">Enter your email — we'll alert you when new tools matching your search are added to the directory.</p>
    <input type="email" class="m-email" id="mEmail" placeholder="your@email.com">
    <button class="m-btn" id="mBtn" onclick="saveLead()">Notify Me →</button>
    <button class="m-close" id="mClose" onclick="closeModal()">No thanks, I'll search later</button>
    <div class="m-ok" id="mOk" style="display:none"></div>
  </div>
</div>

<footer>
  <div class="container">
    <div class="footer-inner">
      <div class="copy">© 2026 AI Tools Vault — Built by BrightSpan Holdings LLC · The world's largest AI directory.</div>
      <div class="links">
        <a href="#">About</a>
        <a href="#submit">Submit Tool</a>
        <a href="#">Advertise</a>
        <a href="mailto:hello@aitoolsvault.com">Contact</a>
      </div>
    </div>
  </div>
</footer>

<script>
const tools=[''' + tools_js + '''];
const catsStr=''' + cats_str + ''';
const iconsStr=''' + icons_str + ''';
const colorsStr=''' + colors_str + ''';
const pCols={free:'#10b981',freemium:'#f59e0b',paid:'#ec4899'};
let aCat='All',aPrc='All',lastQ='';

function filterCat(c){aCat=c;document.querySelectorAll('.cat-btn').forEach(b=>b.classList.remove('active'));const b=document.getElementById('cat-'+c);if(b)b.classList.add('active');document.getElementById('toolsTitle').textContent=c==='All'?'Featured Tools':c;apply();}
function filterPrice(p){aPrc=p;document.querySelectorAll('.fil-btn').forEach(b=>b.classList.remove('active'));const b=document.getElementById('prc-'+p);if(b)b.classList.add('active');apply();}
function quickSearch(q){document.getElementById('searchInput').value=q;doSearch();}
function doSearch(){const q=document.getElementById('searchInput').value.trim().toLowerCase();lastQ=q;if(!q){apply();return;}let list=tools.filter(t=>t.name.toLowerCase().includes(q)||t.desc.toLowerCase().includes(q)||t.cat.toLowerCase().includes(q));if(aCat!=='All')list=list.filter(t=>t.cat===aCat);if(aPrc!=='All')list=list.filter(t=>t.pricing===aPrc);document.getElementById('toolsTitle').textContent='Results for "'+q+'"';render(list);if(q&&!localStorage.getItem('ml_'+q))openModal(q);}
function apply(){let list=tools;if(aCat!=='All')list=list.filter(t=>t.cat===aCat);if(aPrc!=='All')list=list.filter(t=>t.pricing===aPrc);document.getElementById('toolsTitle').textContent=aCat==='All'?'Featured Tools':aCat;render(list);}
function render(list){const g=document.getElementById('toolGrid');const n=document.getElementById('noResults');document.getElementById('toolCount').innerHTML='Showing <strong>'+list.length+'</strong> tools';if(list.length===0){g.style.display='none';n.style.display='block';return;}g.style.display='grid';n.style.display='none';g.innerHTML=list.slice(0,50).map(t=>{const col=colorsStr[t.cat]||'#6b7280';const ic=iconsStr[t.cat]||'🔧';const pc=pCols[t.pricing]||'#6b7280';const vk=t.views>=1000?(t.views/1000).toFixed(0)+'K':t.views;return '<div class="card"><div class="card-top"><div class="card-icon" style="background:'+col+'18;border:1px solid '+col+'30"><span style="font-size:20px">'+ic+'</span></div><div class="card-body"><div class="card-name">'+t.name+'</div><div class="card-cat" style="color:'+col+'">'+t.cat+'</div></div><div class="card-price" style="background:'+pc+'18;color:'+pc+'">'+t.pricing+'</div></div><p class="card-desc">'+t.desc.substring(0,130)+'...</p><div class="card-foot"><span class="card-views">👁 '+vk+'/mo</span><a href="'+t.website+'" target="_blank" class="card-link">🌐 Visit →</a></div></div>';}).join('');}
function openModal(q){lastQ=q;document.getElementById('modal').style.display='flex';document.getElementById('mSub').textContent='Enter your email — we\'ll email you when new AI tools matching "'+q+'" are added to the directory.';document.getElementById('mEmoji').textContent='📬';document.getElementById('mTitle').textContent='Get Notified First';document.getElementById('mOk').style.display='none';document.getElementById('mEmail').style.display='block';document.getElementById('mBtn').style.display='block';document.getElementById('mClose').textContent="No thanks, I'll search later";}
function closeModal(){document.getElementById('modal').style.display='none';}
function saveLead(){const e=document.getElementById('mEmail').value.trim();if(!e||!e.includes('@'))return;const leads=JSON.parse(localStorage.getItem('aitools_leads')||'[]');leads.push({email:e,query:lastQ||'general',date:new Date().toISOString()});localStorage.setItem('aitools_leads',JSON.stringify(leads));if(lastQ)localStorage.setItem('ml_'+lastQ,'1');document.getElementById('mEmoji').textContent='🎉';document.getElementById('mTitle').textContent="You're on the list!";document.getElementById('mSub').textContent="We'll email you when new tools matching your search are added. Check your inbox!";document.getElementById('mEmail').style.display='none';document.getElementById('mBtn').style.display='none';document.getElementById('mOk').style.display='block';document.getElementById('mOk').textContent='✅ '+e;document.getElementById('mClose').textContent='Close';}
function resetAll(){aCat='All';aPrc='All';document.getElementById('searchInput').value='';document.getElementById('toolsTitle').textContent='Featured Tools';document.querySelectorAll('.cat-btn').forEach(b=>b.classList.remove('active'));document.getElementById('cat-All').classList.add('active');document.querySelectorAll('.fil-btn').forEach(b=>b.classList.remove('active'));document.getElementById('prc-All').classList.add('active');apply();}
function submitTool(){const name=document.getElementById('s-name').value.trim();const url=document.getElementById('s-url').value.trim();const cat=document.getElementById('s-cat').value;const email=document.getElementById('s-email').value.trim();const desc=document.getElementById('s-desc').value.trim();if(!name||!url||!cat||!email||!desc){alert('Please fill in all required fields.');return;}const leads=JSON.parse(localStorage.getItem('aitools_leads')||'[]');leads.push({type:'submission',name,url,cat,email,desc,date:new Date().toISOString()});localStorage.setItem('aitools_leads',JSON.stringify(leads));document.getElementById('submitSuccess').style.display='block';document.getElementById('s-name').value='';document.getElementById('s-url').value='';document.getElementById('s-email').value='';document.getElementById('s-desc').value='';setTimeout(()=>document.getElementById('submitSuccess').style.display='none',5000);}
apply();
</script>
</body>
</html>''')

# Restore %% in CSS back to %
html = html.replace('%%', '%')

with open('/workspace/ai-tools-directory/dist/index.html','w',encoding='utf-8') as f:
    f.write(html)

size = os.path.getsize('/workspace/ai-tools-directory/dist/index.html')
print('DONE: %d bytes' % size)
print('Tools: %d' % len(tools))
print('Categories: %d' % ncat)
