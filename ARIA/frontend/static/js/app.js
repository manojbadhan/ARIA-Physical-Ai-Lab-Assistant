window.toast=function(msg){
  var t=document.getElementById('toast');if(!t)return;
  t.textContent=msg;t.classList.add('on');clearTimeout(t._h);t._h=setTimeout(function(){t.classList.remove('on')},2600);
};
window.api=async function(url,opts){
  var r=await fetch(url,Object.assign({headers:{'Content-Type':'application/json'}},opts||{}));
  if(!r.ok)throw new Error((await r.text())||r.statusText);
  return r.json();
};
document.addEventListener('click',function(e){
  var b=e.target.closest('.b');
  if(b){var r=b.getBoundingClientRect(),s=document.createElement('span');
    s.className='rp';s.style.setProperty('--x',e.clientX-r.left+'px');s.style.setProperty('--y',e.clientY-r.top+'px');
    b.appendChild(s);setTimeout(function(){s.remove()},650);}
  if(e.target.closest('#menuBtn')){var sb=document.querySelector('.sb');sb&&sb.classList.toggle('open');}
});
