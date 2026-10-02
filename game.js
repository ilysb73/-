/* =====================================================================
   사라진 인천을 찾아서 — 비주얼 노벨 엔진 (외부 라이브러리 없음)
   story.js 가 이 파일의 함수(bg, show, say, choose, ...)를 사용해요.
   ===================================================================== */
'use strict';
const $ = s => document.querySelector(s);
const stage = $('#stage'), overlay = $('#overlay');
const wait = ms => new Promise(r => setTimeout(r, ms));
const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const SAVE_KEY = 'incheon-heritage-vn-v1';

/* ---------- 화면 크기 맞추기 ---------- */
function fit(){
  const s = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
  stage.style.transform = `translate(-50%,-50%) scale(${s})`;
}
window.addEventListener('resize', fit); fit();

/* ---------- 상태 ---------- */
const G = { name:'탐정', score:0, clues:[], flags:{}, log:[], chapter:0, snap:null, visited:[] };
function save(){ try{ localStorage.setItem(SAVE_KEY, JSON.stringify(G)); }catch(e){} }
function loadSave(){ try{ return JSON.parse(localStorage.getItem(SAVE_KEY) || 'null'); }catch(e){ return null; } }
function clearSave(){ try{ localStorage.removeItem(SAVE_KEY); }catch(e){} }
function snapshot(){ G.snap = JSON.stringify({score:G.score, clues:G.clues, flags:G.flags, log:G.log, visited:G.visited}); save(); }
function restoreSnapshot(){ if(G.snap){ Object.assign(G, JSON.parse(G.snap)); } }

/* ---------- 소리 ---------- */
const AUDIO = {}; let muted = false, music = null, musicName = null;
try{ muted = localStorage.getItem('heritage-muted') === '1'; }catch(e){}
function snd(name){
  if(muted) return;
  try{ const a = new Audio(`assets/audio/${name}.mp3`); a.volume = .8; a.play().catch(()=>{}); }catch(e){}
}
function playMusic(name){
  if(musicName === name && music) return;
  if(music){ music.pause(); }
  musicName = name;
  try{ music = new Audio(`assets/audio/${name}.mp3`); music.loop = true; music.volume = .45; if(!muted) music.play().catch(()=>{}); }catch(e){}
}
function toggleSound(){
  muted = !muted;
  try{ localStorage.setItem('heritage-muted', muted ? '1' : '0'); }catch(e){}
  $('#btnSound').textContent = muted ? '🔇' : '🔊';
  if(music){ if(muted) music.pause(); else music.play().catch(()=>{}); }
}
$('#btnSound').textContent = muted ? '🔇' : '🔊';

/* ---------- 배경 ---------- */
let bgFront = 'A';
function bg(name){
  const next = bgFront === 'A' ? $('#bgB') : $('#bgA');
  const cur  = bgFront === 'A' ? $('#bgA') : $('#bgB');
  next.src = `assets/bg/${name}.webp`;
  next.style.opacity = 1; cur.style.opacity = 0;
  bgFront = bgFront === 'A' ? 'B' : 'A';
}

/* ---------- 캐릭터 ---------- */
const POS = { left:.24, center:.5, right:.76, farleft:.16, farright:.84 };
const YOFF = { riri:-24, minjun:0, grandma:0, curator:0 };
const chars = {};
function show(id, pose='normal', pos='right'){
  let el = chars[id];
  if(!el){ el = document.createElement('img'); el.className = 'char'; el.alt = ''; $('#chars').appendChild(el); chars[id] = el;
    if(id === 'riri') el.classList.add('float'); }
  el.src = `assets/char/${id}_${pose}.webp`;
  el.style.left = (POS[pos] * 1920 - 380) + 'px';
  el.style.bottom = (-40 - (YOFF[id]||0)) + 'px';
  requestAnimationFrame(() => el.classList.add('on'));
}
function hide(id){ const el = chars[id]; if(el){ el.classList.remove('on'); } }
function hideAll(){ Object.keys(chars).forEach(hide); }
function hop(id){ const el = chars[id]; if(!el) return; el.classList.remove('float'); el.classList.remove('hop'); void el.offsetWidth; el.classList.add('hop');
  setTimeout(() => { el.classList.remove('hop'); if(id === 'riri') el.classList.add('float'); }, 400); }

/* ---------- 대사 ---------- */
const NAMES = { riri:'리리', minjun:'민준', grandma:'순이 할머니', curator:'학예사 선생님', me:null };
let advance = null, typing = null;
function fmt(s){ return esc(s.replace(/\{name\}/g, G.name)).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>'); }
function tokens(html){ const out = []; const re = /(<[^>]+>|&[a-z#0-9]+;|[\s\S])/g; let m; while((m = re.exec(html))) out.push(m[0]); return out; }
function say(who, text){
  return new Promise(resolve => {
    const tb = $('#textbox'), nb = $('#namebox'), tx = $('#text');
    tb.classList.remove('hidden');
    nb.className = who || '';
    nb.textContent = who === 'me' ? G.name : (who ? (NAMES[who] || who) : '');
    tx.className = who ? '' : 'narr';
    const toks = tokens(fmt(text)); let i = 0; tx.innerHTML = ''; $('#ctc').style.visibility = 'hidden';
    const finish = () => { clearInterval(typing); typing = null; tx.innerHTML = toks.join(''); $('#ctc').style.visibility = 'visible'; };
    typing = setInterval(() => { i++; tx.innerHTML = toks.slice(0, i).join(''); if(i >= toks.length) finish(); }, 26);
    advance = () => { if(typing){ finish(); return; } advance = null; resolve(); };
  });
}
const narr = t => say(null, t);
function hideText(){ $('#textbox').classList.add('hidden'); }
stage.addEventListener('click', e => {
  if(e.target.closest('#overlay > *') || e.target.closest('#hud')) return;
  if(advance) advance();
});
document.addEventListener('keydown', e => {
  if((e.key === ' ' || e.key === 'Enter') && advance && !overlay.children.length){ e.preventDefault(); advance(); }
});

/* ---------- 상단 정보 ---------- */
function hud(on=true){ $('#hud').classList.toggle('hidden', !on); }
function setPlace(p){ $('#hudPlace').textContent = '📍 ' + p.name; $('#hudStep').textContent = '읽걷쓰 4P · ' + p.step; }
function addScore(n){ G.score += n; $('#hudScore').textContent = `⭐ ${G.score}점`; if(n > 0) toast(`+${n}점!`); }
function refreshHud(){ $('#hudScore').textContent = `⭐ ${G.score}점`; $('#noteCount').textContent = G.clues.length; }
function toast(msg){ const t = document.createElement('div'); t.textContent = msg; $('#toast').appendChild(t); setTimeout(() => t.remove(), 2300); }
async function placeCard(p){
  setPlace(p); snd('sfx_whoosh');
  $('#placecard').innerHTML = `<div class="pc"><div class="s">읽걷쓰 4P · ${esc(p.step)}</div><div class="n">${esc(p.name)}</div><div class="t">${esc(p.topic)}</div></div>`;
  await wait(900);
}

/* ---------- 오버레이 도우미 ---------- */
function openOverlay(html){ overlay.innerHTML = html; return overlay.firstElementChild; }
function closeOverlay(){ overlay.innerHTML = ''; }

/* ---------- 선택지 ---------- */
function choose(q, opts, head='탐정의 선택'){
  hideText();
  return new Promise(resolve => {
    const box = openOverlay(`<div class="dim"><div class="q"><small>${esc(head)}</small>${fmt(q)}</div>${
      opts.map((o,i) => `<button class="opt" data-i="${i}"><span class="num">${i+1}</span><span>${fmt(o.t || o)}</span></button>`).join('')}</div>`);
    const pick = i => { document.removeEventListener('keydown', key); snd('sfx_click'); closeOverlay(); resolve(i); };
    const key = e => { const n = parseInt(e.key, 10); if(n >= 1 && n <= opts.length) pick(n - 1); };
    document.addEventListener('keydown', key);
    box.querySelectorAll('.opt').forEach(b => b.onclick = () => pick(+b.dataset.i));
  });
}

/* 선택 결과 카드: o = {tag:'best'|'ok'|'low', pts, fb} */
const HEAD = { best:['명탐정의 선택!', '#3f8f80'], ok:['괜찮지만 아쉬워요', '#c98a12'], low:['다시 생각해 볼까요?', '#d0664c'] };
function feedback(o, title){
  const [h, col] = HEAD[o.tag] || ['결과', '#3b3a4a'];
  if(o.pts) addScore(o.pts);
  snd(o.tag === 'best' ? 'sfx_best' : o.tag === 'ok' ? 'sfx_ok' : 'sfx_low');
  G.log.push({title: title || '', tag:o.tag, pts:o.pts||0});
  return card(title ? `${h}` : h, o.fb, col, o.pts ? [`+${o.pts}점`] : []);
}
function card(title, text, color='#e0724f', tags=[], btn='다음으로 ▶'){
  hideText();
  return new Promise(resolve => {
    const el = openOverlay(`<div class="dim"><div class="card"><h2 style="color:${color}">${fmt(title)}</h2>${
      tags.length ? `<div class="tags">${tags.map(t => `<span class="tag">${esc(t)}</span>`).join('')}</div>` : ''}<p>${fmt(text)}</p><button class="big">${esc(btn)}</button></div></div>`);
    el.querySelector('.big').onclick = () => { snd('sfx_click'); closeOverlay(); resolve(); };
  });
}

/* ---------- 증거 카드(탐정 수첩) ---------- */
function clueHTML(c, stamp=false){
  return `<div class="clue">${stamp ? '<div class="stamp">증거 획득!</div>' : ''}<div class="h">🔎 ${esc(c.title)}</div><div class="b">${fmt(c.text)}</div><div class="src">출처: ${esc(c.src)}</div></div>`;
}
function clue(id){
  const c = CLUES[id]; if(!c || G.clues.includes(id)) return Promise.resolve();
  G.clues.push(id); refreshHud(); hideText(); snd('sfx_coin');
  return new Promise(resolve => {
    const el = openOverlay(`<div class="dim">${clueHTML(c, true)}<button class="big teal">탐정 수첩에 넣기 📓</button></div>`);
    el.querySelector('.big').onclick = () => { snd('sfx_click'); closeOverlay(); resolve(); };
  });
}
function openNotebook(force=false, onClose=closeOverlay){
  if(!force && overlay.children.length && !overlay.querySelector('.modal')) return;
  const list = G.clues.map(id => clueHTML(CLUES[id])).join('') || '<div class="empty">아직 모은 증거 카드가 없어요. 현장을 조사해 보세요!</div>';
  const el = openOverlay(`<div class="dim"><div class="modal"><h2>📓 탐정 수첩 · 증거 카드 ${G.clues.length}/${Object.keys(CLUES).length}</h2><div class="notes">${list}</div><button class="big sub x">닫기</button></div></div>`);
  el.querySelector('.x').onclick = onClose;
}
function openMap(){
  if(overlay.children.length && !overlay.querySelector('.modal')) return;
  const cur = G.place || '';
  const pins = PLACES_ORDER.map(k => { const p = PLACES[k]; const st = G.visited.includes(k) ? 'done' : (k === cur ? 'now' : '');
    return `<div class="pin ${k === cur ? 'now' : st}" style="left:${p.map[0]/19.2}%;top:${p.map[1]/10.8}%"><span>${esc(p.short)}</span><i></i></div>`; }).join('');
  const el = openOverlay(`<div class="dim"><div class="modal"><h2>🗺️ 부평·계양 탐정 지도</h2><div class="mapwrap"><img src="assets/bg/map.webp" alt="부평구와 계양구 그림 지도">${pins}</div><button class="big sub x">닫기</button></div></div>`);
  el.querySelector('.x').onclick = closeOverlay;
}
$('#btnNote').onclick = e => { e.stopPropagation(); openNotebook(); };
$('#btnMap').onclick = e => { e.stopPropagation(); openMap(); };
$('#btnSound').onclick = e => { e.stopPropagation(); toggleSound(); };

/* =====================================================================
   미니게임
   ===================================================================== */

/* 1) 사라진 것 찾기 (그림에서 클릭) — targets: [{x,y,w,h,name,msg,kind:'gone'|'info'}] (1920×1080 기준) */
function gameSpot({ img, title, goal, targets, need }){
  hideText();
  return new Promise(resolve => {
    let found = 0, miss = 0, finished = false; const done = new Set();
    const el = openOverlay(`<div class="dim" style="background:rgba(43,42,54,.84)"><div class="gbar"><span class="t">🔍 ${esc(title)}</span><span>${esc(goal)}</span><span class="spacer"></span><span id="gCount">찾은 것 0/${need}</span></div>
      <div class="stagebox" id="sbox"><img src="assets/bg/${img}.webp" alt=""></div><div class="tip" id="gTip">그림을 눌러 보세요!</div></div>`);
    const box = el.querySelector('#sbox'), tip = el.querySelector('#gTip'); const k = 1600 / 1920;
    box.onclick = e => {
      if(finished) return;
      const r = box.getBoundingClientRect(); const sx = r.width / 1600;
      const x = (e.clientX - r.left) / sx / k, y = (e.clientY - r.top) / sx / k;
      const t = targets.find(t => x >= t.x && x <= t.x + t.w && y >= t.y && y <= t.y + t.h);
      if(!t){ miss++; snd('sfx_low'); const m = document.createElement('div'); m.className = 'miss'; m.style.left = (x*k)+'px'; m.style.top = (y*k)+'px'; box.appendChild(m); setTimeout(()=>m.remove(), 800);
        tip.textContent = '여기는 아니에요. 지금 모습과 비교해 보세요!'; return; }
      tip.innerHTML = fmt(t.msg);
      if(done.has(t.name)) return;
      done.add(t.name);
      const mk = document.createElement('div'); mk.className = 'mark' + (t.kind === 'gone' ? '' : ' info');
      Object.assign(mk.style, { left:t.x*k+'px', top:t.y*k+'px', width:t.w*k+'px', height:t.h*k+'px' }); box.appendChild(mk);
      if(t.kind === 'gone'){ found++; snd('sfx_best'); el.querySelector('#gCount').textContent = `찾은 것 ${found}/${need}`; } else snd('sfx_ok');
      if(found >= need){
        finished = true;
        const pts = Math.max(6, 15 - miss);
        setTimeout(() => { closeOverlay(); addScore(pts); resolve({pts, miss}); }, 1600);
      }
    };
  });
}

/* 2) 사실 / 추측 분류 — cards: [{t, fact:bool, why}] */
function gameSort({ title, cards }){
  hideText();
  return new Promise(resolve => {
    let i = 0, ok = 0;
    const el = openOverlay(`<div class="dim" style="background:rgba(43,42,54,.84)"><div class="gbar"><span class="t">🧩 ${esc(title)}</span><span>자료로 확인된 <b>사실</b>일까, 내 생각인 <b>추측</b>일까?</span><span class="spacer"></span><span id="gCount"></span></div>
      <div class="sortcard" id="scard"></div><div class="row"><button class="sortbtn fact" data-v="1">✔ 사실</button><button class="sortbtn guess" data-v="0">💭 추측</button></div><div class="tip" id="gTip" style="display:none"></div></div>`);
    const draw = () => { el.querySelector('#scard').innerHTML = fmt(cards[i].t); el.querySelector('#gCount').textContent = `${i+1}/${cards.length} · 맞힌 개수 ${ok}`; };
    let lock = false;
    el.querySelectorAll('.sortbtn').forEach(b => b.onclick = async () => {
      if(lock) return; lock = true;
      const c = cards[i], ans = b.dataset.v === '1', right = ans === c.fact;
      if(right){ ok++; snd('sfx_best'); } else snd('sfx_low');
      const tip = el.querySelector('#gTip'); tip.style.display = 'block';
      tip.innerHTML = (right ? '⭕ 정답! ' : '❌ 아쉬워요! ') + fmt(c.why);
      await wait(2300); tip.style.display = 'none';
      i++; lock = false;
      if(i >= cards.length){ closeOverlay(); const pts = ok * 2; addScore(pts); resolve({pts, ok}); } else draw();
    });
    draw();
  });
}

/* 3) 순서 맞추기 — items: 올바른 순서의 문장 배열 */
function gameOrder({ title, goal, items }){
  hideText();
  return new Promise(resolve => {
    const order = items.map((t,i) => ({t,i})).sort(() => Math.random() - .5);
    let next = 0, miss = 0;
    const el = openOverlay(`<div class="dim" style="background:rgba(43,42,54,.84)"><div class="gbar"><span class="t">⏳ ${esc(title)}</span><span>${esc(goal)}</span><span class="spacer"></span><span id="gCount">실수 0</span></div>
      <div class="orderlist">${order.map(o => `<button class="ordercard" data-i="${o.i}"><span class="num">?</span><span>${fmt(o.t)}</span></button>`).join('')}</div></div>`);
    el.querySelectorAll('.ordercard').forEach(b => b.onclick = () => {
      if(b.classList.contains('picked')) return;
      if(+b.dataset.i === next){ b.classList.add('picked'); b.querySelector('.num').textContent = next + 1; next++; snd('sfx_ok');
        if(next === items.length){ snd('sfx_best'); setTimeout(() => { closeOverlay(); const pts = Math.max(4, 12 - miss * 2); addScore(pts); resolve({pts, miss}); }, 900); }
      } else { miss++; snd('sfx_low'); b.classList.remove('bad'); void b.offsetWidth; b.classList.add('bad'); el.querySelector('#gCount').textContent = `실수 ${miss}`; }
    });
  });
}

/* 4) 좋은 인터뷰 질문 고르기 — qs: [{t, good, why}], need 개 */
function gamePick({ title, goal, qs, need }){
  hideText();
  return new Promise(resolve => {
    const sel = new Set();
    const el = openOverlay(`<div class="dim" style="background:rgba(43,42,54,.84)"><div class="gbar"><span class="t">🎤 ${esc(title)}</span><span>${esc(goal)}</span><span class="spacer"></span><span id="gCount">0/${need}</span></div>
      <div class="pickgrid">${qs.map((q,i) => `<button class="pick" data-i="${i}">${fmt(q.t)}</button>`).join('')}</div><button class="big" id="gGo" disabled>이 질문으로 인터뷰하기 ▶</button></div>`);
    const btns = [...el.querySelectorAll('.pick')], go = el.querySelector('#gGo');
    btns.forEach(b => b.onclick = () => { const i = +b.dataset.i;
      if(sel.has(i)) sel.delete(i); else if(sel.size < need) sel.add(i);
      btns.forEach((x,j) => x.classList.toggle('on', sel.has(j))); snd('sfx_click');
      el.querySelector('#gCount').textContent = `${sel.size}/${need}`; go.disabled = sel.size !== need; });
    go.onclick = async () => {
      go.disabled = true; let good = 0;
      btns.forEach((b,j) => { b.onclick = null; if(sel.has(j)){ b.classList.add(qs[j].good ? 'good' : 'badq'); if(qs[j].good) good++; } });
      snd(good === need ? 'sfx_best' : 'sfx_ok');
      await wait(1800); closeOverlay();
      const pts = good * 4; addScore(pts); resolve({pts, good, picked:[...sel]});
    };
  });
}

/* 5) AI 팩트체크 (O/X) — items: [{t, ok:bool, why}] */
function gameCheck({ title, goal, items }){
  hideText();
  return new Promise(resolve => {
    const ans = items.map(() => null);
    const el = openOverlay(`<div class="dim" style="background:rgba(43,42,54,.84);gap:14px"><div class="gbar"><span class="t">🤖 ${esc(title)}</span><span>${esc(goal)}</span></div>
      <div style="height:90px"></div>${items.map((it,i) => `<div class="checkrow" data-i="${i}"><div class="s">${fmt(it.t)}<div class="why" style="display:none"></div></div><button class="ox o">⭕ 맞아</button><button class="ox x">❌ 틀려</button></div>`).join('')}
      <button class="big" id="gGo" disabled>채점하기 ▶</button></div>`);
    const rows = [...el.querySelectorAll('.checkrow')], go = el.querySelector('#gGo');
    rows.forEach((r,i) => { r.querySelector('.o').onclick = () => set(i, true); r.querySelector('.x').onclick = () => set(i, false); });
    function set(i, v){ ans[i] = v; snd('sfx_click'); rows[i].querySelector('.o').classList.toggle('on', v === true); rows[i].querySelector('.x').classList.toggle('on', v === false); go.disabled = ans.includes(null); }
    go.onclick = async () => {
      let ok = 0; go.disabled = true;
      rows.forEach((r,i) => { const right = ans[i] === items[i].ok; if(right) ok++; r.classList.add(right ? 'right' : 'wrong');
        const w = r.querySelector('.why'); w.style.display = 'block'; w.innerHTML = (items[i].ok ? '사실이에요. ' : '리리가 틀렸어요! ') + fmt(items[i].why);
        r.querySelectorAll('.ox').forEach(b => b.onclick = null); });
      snd(ok === items.length ? 'sfx_best' : 'sfx_ok');
      go.textContent = '확인했어요 ▶'; go.disabled = false;
      go.onclick = () => { closeOverlay(); const pts = ok * 3; addScore(pts); resolve({pts, ok}); };
    };
  });
}

/* 6) 기억 카드 짝 맞추기 — pairs: [[a,b],...] */
function gameMemory({ title, goal, pairs }){
  hideText();
  return new Promise(resolve => {
    const cards = []; pairs.forEach((p,i) => { cards.push({i, t:p[0]}); cards.push({i, t:p[1]}); });
    cards.sort(() => Math.random() - .5);
    let open = [], flips = 0, matched = 0, lock = false;
    const el = openOverlay(`<div class="dim" style="background:rgba(43,42,54,.84)"><div class="gbar"><span class="t">🃏 ${esc(title)}</span><span>${esc(goal)}</span><span class="spacer"></span><span id="gCount">뒤집은 횟수 0</span></div>
      <div style="height:80px"></div><div class="memgrid">${cards.map((c,k) => `<div class="mem" data-k="${k}"><div class="in"><div class="bk">?</div><div class="f">${fmt(c.t)}</div></div></div>`).join('')}</div></div>`);
    const els = [...el.querySelectorAll('.mem')];
    els.forEach(m => m.onclick = async () => {
      const k = +m.dataset.k; if(lock || m.classList.contains('flip') || m.classList.contains('ok')) return;
      m.classList.add('flip'); open.push(k); snd('sfx_click');
      if(open.length === 2){
        flips++; el.querySelector('#gCount').textContent = `뒤집은 횟수 ${flips}`;
        const [a,b] = open;
        if(cards[a].i === cards[b].i){ matched++; snd('sfx_best'); els[a].classList.add('ok'); els[b].classList.add('ok'); open = [];
          if(matched === pairs.length){ await wait(800); closeOverlay(); const pts = Math.max(6, 16 - Math.max(0, flips - pairs.length)); addScore(pts); resolve({pts, flips}); }
        } else { lock = true; await wait(1000); els[a].classList.remove('flip'); els[b].classList.remove('flip'); open = []; lock = false; }
      }
    });
  });
}

/* 7) 안내판 쓰기 */
function gameWrite({ sites, aiText }){
  hideText();
  return new Promise(resolve => {
    let usedAI = false;
    const el = openOverlay(`<div class="dim"><div class="writebox"><h2>✍️ 우리 동네 문화유산 안내판 쓰기</h2>
      <div style="font-size:34px">지킬 곳을 고르고, 탐정 수첩의 <b>사실</b>을 넣어 한두 문장으로 써 보세요.</div>
      <select id="wSite">${sites.map(s => `<option>${esc(s)}</option>`).join('')}</select>
      <textarea id="wText" maxlength="120" placeholder="예) 이곳은 ○○이 있던 곳이에요. ○○ 때문에 사라졌지만, 우리는 ○○하며 기억할 거예요."></textarea>
      <div class="hintline" id="wCount">0/120자 · 10자 이상 써야 해요</div>
      <label><input type="checkbox" id="wAI"> 리리(AI)의 도움을 받은 부분이 있어요 (솔직하게 밝히기)</label>
      <div style="display:flex;gap:24px;justify-content:center"><button class="big sub" id="wHelp">🤖 리리에게 첫 문장 도움받기</button><button class="big" id="wGo" disabled>안내판 세우기 ▶</button></div></div></div>`);
    const ta = el.querySelector('#wText'), go = el.querySelector('#wGo'), cnt = el.querySelector('#wCount');
    const upd = () => { const n = ta.value.trim().length; cnt.textContent = `${n}/120자 · 10자 이상 써야 해요`; go.disabled = n < 10; };
    ta.addEventListener('input', upd);
    ta.addEventListener('keydown', e => e.stopPropagation());
    el.querySelector('#wHelp').onclick = () => { usedAI = true; snd('sfx_ok'); const s = el.querySelector('#wSite').value;
      ta.value = (aiText[s] || '') + ' '; ta.focus(); upd(); toast('리리가 첫 문장을 도와줬어요. 이어서 내 생각을 써 보세요!'); };
    go.onclick = () => {
      const text = ta.value.trim(), site = el.querySelector('#wSite').value, disclosed = el.querySelector('#wAI').checked;
      closeOverlay(); resolve({ site, text, usedAI, disclosed });
    };
  });
}

/* ---------- 타이틀 ---------- */
function titleScreen(){
  hud(false); hideText(); hideAll(); bg('office');
  const sv = loadSave();
  const canContinue = sv && sv.chapter > 0 && sv.chapter < CHAPTERS.length;
  return new Promise(resolve => {
    const el = openOverlay(`<div class="title"><div class="card">
      <div style="font-size:36px;color:#3f8f80" class="jua">부평·계양 문화유산 탐정단</div>
      <h1>사라진 인천을<br>찾아서</h1>
      <div class="sub">읽고 · 걷고 · 쓰는 읽걷쓰 AI 탐정 비주얼 노벨</div>
      <div class="badges"><span>문화유산</span><span>도시개발</span><span>인권·평화</span><span>AI 리터러시</span><span>세계시민</span></div>
      <input id="tName" maxlength="8" placeholder="탐정 이름을 쓰세요" value="${esc(sv && sv.name && sv.name !== '탐정' ? sv.name : '')}">
      <div class="chips">${['하늘','바다','별빛','새싹','씩씩이'].map(n => `<button class="chip">${n}</button>`).join('')}</div>
      <div style="display:flex;gap:24px;justify-content:center">
        <button class="big" id="tStart">새로 시작 ▶</button>${canContinue ? `<button class="big teal" id="tCont">이어 하기 (${sv.chapter + 1}장)</button>` : ''}
      </div><div class="hintline" style="font-size:28px;color:#8a7f73;margin-top:16px">등장인물은 가상 인물이고, 장소와 역사 내용은 실제 기록을 바탕으로 했어요.</div></div></div>`);
    const nm = el.querySelector('#tName');
    nm.addEventListener('keydown', e => { e.stopPropagation(); if(e.key === 'Enter') el.querySelector('#tStart').click(); });
    el.querySelectorAll('.chip').forEach(c => c.onclick = () => { nm.value = c.textContent; snd('sfx_click'); });
    const nameOf = () => (nm.value.trim().replace(/[<>{}\[\]]/g, '') || '탐정').slice(0, 8);
    el.querySelector('#tStart').onclick = () => { Object.assign(G, { name:nameOf(), score:0, clues:[], flags:{}, log:[], chapter:0, snap:null, visited:[] }); closeOverlay(); resolve(0); };
    const c = el.querySelector('#tCont');
    if(c) c.onclick = () => { Object.assign(G, sv); G.name = nameOf() === '탐정' ? sv.name : nameOf(); restoreSnapshot(); closeOverlay(); resolve(sv.chapter); };
  });
}

/* ---------- 실행 ---------- */
async function main(){
  while(true){
    const from = await titleScreen();
    playMusic('bgm_main'); hud(true); refreshHud();
    for(let i = from; i < CHAPTERS.length; i++){
      G.chapter = i; snapshot();
      hideAll();
      await CHAPTERS[i]();
    }
    G.chapter = CHAPTERS.length; save();
  }
}
