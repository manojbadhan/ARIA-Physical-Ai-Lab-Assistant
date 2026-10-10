const $=s=>document.querySelector(s),pad=n=>String(n).padStart(2,"0");
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const SR=window.SpeechRecognition||window.webkitSpeechRecognition,TTS=window.speechSynthesis;
const voiceOK=!!(SR&&TTS);
let turns=[],busy=false,fromVoice=false;
const L="ABCDEFGHIJKLMNOPQRSTUVWXYZ";
function sessionId(){const d=new Date(),r=[0,0,0].map(()=>L[Math.random()*26|0]).join("");$("#sess").textContent="Session "+pad(d.getDate())+pad(d.getMonth()+1)+"-"+r}
$("#kc").textContent=CHUNKS.toLocaleString("en-US")+" chunks";
$("#vt").textContent=voiceOK?"Ready":"Not in this browser";if(voiceOK)$("#vs").classList.add("on");
function mode(m){document.body.dataset.mode=m;$("#t-home").classList.toggle("on",m=="home");$("#t-chat").classList.toggle("on",m=="chat")}
$("#t-home").onclick=()=>mode("home");$("#t-chat").onclick=()=>mode("chat");

function render(){
 const box=$("#msgs");
 if(!turns.length){box.innerHTML='<div class="empty">No conversation yet. Ask ARIA below.</div>'}
 else box.innerHTML=turns.map((t,i)=>{
  let a;
  if(t.pending)a='<div class="wait m up">Searching '+CHUNKS.toLocaleString("en-US")+' chunks<div class="bar"><i></i></div></div>';
  else{
   const r=t.r;
   if(!r)a='<p>No passage in the lab knowledge base answers this closely enough. Name the topic or document and try again.</p><div class="nf m up">Nothing found in lab knowledge</div>';
   else a=r.t.map(p=>"<p>"+esc(p)+"</p>").join("")+(r.f?'<div class="fx">'+esc(r.f)+"</div>":"")+
    '<details open class="trail"><summary class="m up">Found in lab knowledge · '+pad(r.s.length)+' sources</summary><div class="grid">'+
    r.s.map((s,j)=>'<button class="src"><span class="m"><span class="n">'+pad(j+1)+'</span> <span class="d">D-'+pad(s[0]+1)+'</span></span><span class="ti">'+esc(DOCS[s[0]])+'</span><span class="sec m">'+esc(s[1])+'</span><span class="rel m"><span class="trk"><i style="width:'+Math.round(s[2]*100)+'%"></i></span>relevance '+s[2].toFixed(2)+'</span><span class="ps">'+esc(s[3])+"</span></button>").join("")+"</div></details>";
  }
  return '<div class="turn" id="turn-'+i+'"><div class="u">'+esc(t.q)+'</div><div class="a"><div class="h m up">ARIA · '+t.time+"</div>"+a+"</div></div>";
 }).join("");
 const n=turns.length;
 $("#cn").textContent=n?" "+n:"";
 $("#ql").innerHTML=n?turns.map((t,i)=>'<li><button data-i="'+i+'"><span class="m">Q'+pad(i+1)+"</span><span>"+esc(t.q)+"</span></button></li>").join(""):'<li class="none">No questions yet</li>';
 const last=[...turns].reverse().find(t=>t.r);const used=new Set(last?last.r.s.map(s=>s[0]):[]);
 $("#docs").innerHTML=DOCS.map((d,i)=>'<li class="'+(used.has(i)?"used":"")+'"><span class="m">D-'+pad(i+1)+"</span><span>"+esc(d)+"</span></li>").join("");
 const k=Math.min(n,8);
 $("#mem").innerHTML=Array.from({length:8},(_,i)=>'<i class="'+(i<k?"f":"")+'"></i>').join("");
 $("#memt").textContent=k+" of 8 turns kept";
}
$("#msgs").addEventListener("click",e=>{const b=e.target.closest(".src");if(b)b.classList.toggle("open")});
$("#ql").addEventListener("click",e=>{const b=e.target.closest("button");if(!b)return;mode("chat");const el=$("#turn-"+b.dataset.i);if(el)el.scrollIntoView({block:"start"})});

async function send(text){
 text=(text||"").trim();if(!text||busy)return null;
 busy=true;mode("chat");
 const d=new Date(),t={q:text,time:pad(d.getHours())+":"+pad(d.getMinutes()),pending:true};
 turns.push(t);if(turns.length>8)turns=turns.slice(-8);
 render();$("#chat").scrollTop=1e6;
 try{t.r=await ask(text)}catch(e){t.r=null}
 t.pending=false;busy=false;render();$("#chat").scrollTop=1e6;
 return t.r;
}
const q=$("#q");
function grow(){q.style.height="62px";const h=Math.min(q.scrollHeight,110);q.style.height=Math.max(h,62)+"px";q.style.overflowY=q.scrollHeight>110?"auto":"hidden"}
q.addEventListener("input",grow);
function submit(){const v=q.value;q.value="";grow();send(v)}
q.addEventListener("keydown",e=>{if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();submit()}});
$("#send").onclick=submit;
document.querySelectorAll(".start button").forEach(b=>b.onclick=()=>send(b.dataset.q));
$("#new").onclick=()=>{turns=[];render();mode("home");sessionId();q.value="";grow()};

/* voice */
const vo=$("#vo"),cv=$("#cv"),cx=cv.getContext("2d");
let vstate="listening",rec=null,raf=0,open=false,vrun=0;
const WORD={listening:"Listening",thinking:"Thinking",speaking:"Speaking",ready:"Ready"};
const SUB={listening:"Microphone open",thinking:"Searching lab knowledge",speaking:"Reading answer aloud",ready:"Ready"};
function setV(s){vstate=s;$("#vw").textContent=WORD[s];$("#vsub").textContent=SUB[s]}
function draw(ts){
 const w=cv.clientWidth,h=110,dpr=devicePixelRatio||1;
 if(cv.width!==w*dpr){cv.width=w*dpr;cv.height=h*dpr}
 cx.setTransform(dpr,0,0,dpr,0,0);cx.clearRect(0,0,w,h);
 const amp=vstate=="listening"?1:vstate=="speaking"?.45:.03,t=ts/1000;
 cx.lineWidth=2;cx.strokeStyle=vstate=="speaking"?"#e0b43a":"#8a9bff";cx.beginPath();
 for(let x=0;x<=w;x+=2){const u=x/w,env=Math.pow(Math.sin(Math.PI*u),1.5);
  const y=h/2+env*amp*(h*.38)*(Math.sin(u*14+t*3)*.5+Math.sin(u*27-t*4.3)*.3+Math.sin(u*43+t*6.1)*.2);
  x?cx.lineTo(x,y):cx.moveTo(x,y)}
 cx.stroke();
 if(open&&!matchMedia("(prefers-reduced-motion:reduce)").matches)raf=requestAnimationFrame(draw);
}
function closeV(){open=false;vrun++;vo.classList.remove("open");cancelAnimationFrame(raf);try{rec&&rec.abort()}catch(e){}if(TTS)TTS.cancel()}
function openV(){
 if(!voiceOK)return;
 open=true;const my=++vrun;$("#tr").textContent="";setV("listening");vo.classList.add("open");raf=requestAnimationFrame(draw);
 rec=new SR();rec.lang="en-IN";rec.interimResults=true;rec.continuous=false;let final="";
 rec.onresult=e=>{let s="";for(const r of e.results){s+=r[0].transcript;if(r.isFinal)final=s}$("#tr").textContent=s;};
 rec.onend=async()=>{
  if(my!==vrun)return;
  const text=($("#tr").textContent||final).trim();
  if(!text){setV("ready");return}
  setV("thinking");const r=await send(text);
  if(my!==vrun)return;
  const say=r?r.t.join(" "):"No passage in the lab knowledge base answers this closely enough. Name the topic or document and try again.";
  $("#tr").textContent=say;setV("speaking");
  const u=new SpeechSynthesisUtterance(say);u.lang="en-IN";u.onend=()=>{if(my===vrun)setV("ready")};TTS.speak(u);
 };
 rec.onerror=()=>{if(my===vrun)setV("ready")};
 try{rec.start()}catch(e){setV("ready")}
}
$("#mic").onclick=()=>{if(voiceOK)openV()};
$("#stop").onclick=closeV;
document.addEventListener("keydown",e=>{if(e.key==="Escape"&&open)closeV()});
sessionId();render();
