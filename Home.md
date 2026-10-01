---
type: index
id: home
title: "Home"
description: "Start page of BioFAIRnCARE: today's note, quick links, experiments and records at a glance."
created: 2026-10-01
updated: 2026-10-02
status: active
owner: Lab
confidentiality: internal
license: lab-internal
ai_assisted: false
lab_owned: true
cssclasses:
  - wide-page
  - lab-home
---

```dataviewjs
/* ─── HEADER: Lab Logo + Live Clock ─── */
const hdr = dv.el("div","",{cls:"lab-header"});

// Mobile & PC compatible logo path resolution using Obsidian API
const logoFile = app.vault.getAbstractFileByPath("Resources/lab_resources/assets/home_page_image_20261001.png");
const logoSrc = logoFile ? app.vault.getResourcePath(logoFile) : app.vault.adapter.getResourcePath("Resources/lab_resources/assets/home_page_image_20261001.png");

hdr.createEl("img",{attr:{src:logoSrc, class:"lab-logo", alt:"Lab Logo"}});

const tEl = hdr.createEl("div",{cls:"lab-time"});
const dEl = hdr.createEl("div",{cls:"lab-date"});

(function tick(){
  const n = new Date();
  tEl.textContent = n.toLocaleTimeString("en-GB",{hour:"2-digit",minute:"2-digit",second:"2-digit"});
  dEl.textContent = n.toLocaleDateString("en-US",{weekday:"long",year:"numeric",month:"long",day:"numeric"});
  setTimeout(tick, 1000 - n.getMilliseconds());
})();
```

> [!multi-column]
>
>> [!blank-container|wide-3]
>> #### Calendar
>>```dataviewjs
>>/* ─── INTERACTIVE CALENDAR ─── */
>>const allP = dv.pages('-"_Examples" and -"Resources/templates" and -"Resources/note-templates"');
>>const mMap = {};
>>for(const p of allP){
>>  const k = p.file.mtime.toFormat("yyyy-MM-dd");
>>  (mMap[k] = mMap[k]||[]).push(p);
>>}
>>const dnSet = new Set(dv.pages('"daily_notes"').map(p=>p.file.name).array());
>>
>>let Y=new Date().getFullYear(), M=new Date().getMonth();
>>const calEl  = dv.el("div","",{cls:"hp-cal"});
>>const paneEl = dv.el("div","",{cls:"hp-pane"});
>>
>>function draw(y,m){
>>  calEl.empty();
>>  const ts = new Date().toISOString().slice(0,10);
>>  const h  = calEl.createEl("div",{cls:"hp-cal-hdr"});
>>  const pv = h.createEl("button",{text:"‹",cls:"hp-nav"});
>>  h.createEl("span",{
>>    text:new Date(y,m,1).toLocaleString("default",{month:"long",year:"numeric"}),
>>    cls:"hp-cal-title"
>>  });
>>  const nx = h.createEl("button",{text:"›",cls:"hp-nav"});
>>  pv.onclick=()=>{M--;if(M<0){M=11;Y--;}draw(Y,M);};
>>  nx.onclick=()=>{M++;if(M>11){M=0;Y++;}draw(Y,M);};
>>
>>  const g  = calEl.createEl("div",{cls:"hp-cal-grid"});
>>  ["S","M","T","W","T","F","S"].forEach(d=>g.createEl("div",{text:d,cls:"hp-dh"}));
>>  const fd=new Date(y,m,1).getDay(), dm=new Date(y,m+1,0).getDate();
>>  for(let i=0;i<fd;i++) g.createEl("div");
>>  for(let d=1;d<=dm;d++){
>>    const ds=`${y}-${String(m+1).padStart(2,"0")}-${String(d).padStart(2,"0")}`;
>>    const c=g.createEl("div",{cls:"hp-dc"+(ds===ts?" hp-today":"")});
>>    c.createEl("span",{text:String(d),cls:"hp-dn"});
>>    if(mMap[ds]) c.createEl("div",{cls:"hp-dot"});
>>    c.onclick=()=>showDay(ds);
>>  }
>>}
>>
>>function showDay(ds){
>>  paneEl.empty();
>>  const notes=mMap[ds]||[];
>>  if(dnSet.has(ds)){
>>    const r=paneEl.createEl("div",{cls:"hp-pr"});
>>    const a=r.createEl("a",{text:"📅 Daily note — "+ds,cls:"hp-pl"});
>>    a.onclick=e=>{e.preventDefault();app.workspace.openLinkText("daily_notes/"+ds,"",false);};
>>  }
>>  if(notes.length){
>>    paneEl.createEl("div",{text:notes.length+" note"+(notes.length>1?"s":"")+" modified on "+ds,cls:"hp-ph"});
>>    notes.slice(0,15).forEach(p=>{
>>      const r=paneEl.createEl("div",{cls:"hp-pr"});
>>      const a=r.createEl("a",{text:p.file.name,cls:"hp-pl"});
>>      a.onclick=e=>{e.preventDefault();app.workspace.openLinkText(p.file.path,"",false);};
>>      r.createEl("span",{text:" "+p.file.mtime.toFormat("HH:mm"),cls:"hp-pt"});
>>    });
>>  } else if(!dnSet.has(ds)){
>>    paneEl.createEl("p",{text:"No activity on this day.",cls:"hp-pe"});
>>  }
>>}
>>
>>draw(Y,M);
>>```
>
>> [!blank-container|wide-2]
>> #### Navigate
>>```dataviewjs
>>await dv.view("Resources/lab_resources/scripts/lab-buttons", { buttons: [] });
>>const CMD="templater-obsidian:Resources/templates/commands/";
>>const items=[
>>  ["📅","Today's note","cmd","daily-notes"],
>>  ["🧪","New experiment","cmd",CMD+"New experiment.md"],
>>  ["⏳","In progress","note","Experiments/_Index"],
>>  ["📖","Catalogue","note","Resources/lab_resources/Experiment catalogue"],
>>  ["🎯","Projects","note","Projects/Auto_summary/_Index"],
>>  ["🧫","Samples","note","Samples/_Index"],
>>  ["🧴","Materials","note","Materials/_Index"],
>>  ["📋","Protocols","note","Protocols/_Index"],
>>  ["💾","Data register","note","Data/_Index"],
>>  ["💡","Concepts","note","Concepts/_Index"],
>>  ["✅","Tasks","note","Todo Lists/_Index"],
>>  ["🗂️","Templates","note","Resources/lab_resources/Template register"],
>>  ["🩺","Vault Health","note","Resources/lab_resources/Vault Health"],
>>  ["🚀","Start here","note","Resources/lab_resources/NoteTaking/New Student Note-Taking Guide"],
>>  ["🌐","FAIR & CARE","note","Resources/lab_resources/FAIR guide"],
>>];
>>const g=dv.el("div","",{cls:"hp-nav-grid"});
>>items.forEach(([ic,lb,kind,target])=>{
>>  const b=g.createEl("div",{cls:"hp-nav-btn"});
>>  b.createEl("span",{text:ic,cls:"hp-nav-ic"});
>>  b.createEl("span",{text:lb,cls:"hp-nav-lb"});
>>  b.onclick=()=>{
>>    if(kind==="cmd" && target.startsWith(CMD)) window.labvaultRun(target,{openDaily:true});
>>    else if(kind==="cmd") app.commands.executeCommandById(target);
>>    else app.workspace.openLinkText(target,"",false);
>>  };
>>});
>>```
>>
>> #### Vault Stats
>>```dataviewjs
>>const ps  = dv.pages('-"_Examples" and -"Resources/templates" and -"Resources/note-templates"');
>>const now = Date.now();
>>const wk  = ps.filter(p=>(now-p.file.mtime.toMillis())<604800000).length;
>>const mo  = ps.filter(p=>(now-p.file.mtime.toMillis())<2592000000).length;
>>const s   = dv.el("div","",{cls:"hp-stats"});
>>[[`📚 ${ps.length}`,"notes"],[`✏️ ${wk}`,"this week"],[`📆 ${mo}`,"this month"]].forEach(([v,l])=>{
>>  const sp=s.createEl("span",{cls:"hp-stat-badge"});
>>  sp.innerHTML=`<b>${v}</b> ${l}`;
>>});
>>```

> [!multi-column]
>
>> [!blank-container]
>> #### Recently Modified
>>```dataview
>>TABLE WITHOUT ID file.link AS "Note", file.mtime AS "Modified"
>>FROM -"_Examples" AND -"Resources/templates" AND -"Resources/note-templates"
>>SORT file.mtime DESC
>>LIMIT 10
>>```
>
>> [!blank-container]
>> #### Recently Created
>>```dataview
>>TABLE WITHOUT ID file.link AS "Note", file.ctime AS "Created"
>>FROM -"_Examples" AND -"Resources/templates" AND -"Resources/note-templates"
>>SORT file.ctime DESC
>>LIMIT 10
>>```

---

**Quick links** (work even without plugins): [[Experiments/_Index|Experiments]] ·
[[Resources/lab_resources/Experiment catalogue|Experiment catalogue]] ·
[[Projects/Auto_summary/_Index|Projects]] · [[Samples/_Index|Samples]] ·
[[Materials/_Index|Materials]] · [[Protocols/_Index|Protocols]] · [[Data/_Index|Data register]] ·
[[Concepts/_Index|Concepts]] · [[Events/_Index|Events]] · [[Todo Lists/_Index|Todo lists]] ·
[[daily_notes/_Index|Daily notes]] · [[MoM/Table of Tags|Table of Tags]] ·
[[Resources/lab_resources/Template register|Template register]] ·
[[Resources/lab_resources/Plugin register|Plugin register]] ·
[[Resources/lab_resources/Vault Health|Vault Health]] ·
[[Resources/lab_resources/NoteTaking/New Student Note-Taking Guide|Start here]] ·
[[Resources/lab_resources/FAIR guide|FAIR guide]] · [[Resources/lab_resources/CARE guide|CARE guide]] ·
[[Resources/lab_resources/OKF guide|OKF guide]] ·
[[Resources/lab_resources/Data capture guide|Data capture guide]] ·
[[Resources/lab_resources/Feature preservation register|Feature preservation register]] ·
[[Resources/Vault settings|Vault settings]] · [[Resources/lab_resources/Lab members|Lab members]]
