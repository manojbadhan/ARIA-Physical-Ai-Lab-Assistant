(function(){
  var box=document.getElementById('msgs'),form=document.getElementById('chatForm'),inp=document.getElementById('chatInput');
  if(!box)return;
  window.addMsg=function(text,who){
    var d=document.createElement('div');d.className='msg '+(who||'bot');d.textContent=text;
    box.appendChild(d);box.scrollTop=box.scrollHeight;return d;
  };
  window.askAria=async function(text){
    addMsg(text,'me');var wait=addMsg('Thinking...','sys');
    try{
      var r=await api('/api/chat',{method:'POST',body:JSON.stringify({message:text})});
      wait.remove();addMsg(r.reply,'bot');
      if(r.photo)addMsg('Photo: '+r.photo,'sys');
    }catch(e){wait.remove();addMsg('Could not reach ARIA. Is the backend running?','sys');}
  };
  form.addEventListener('submit',function(e){
    e.preventDefault();var t=inp.value.trim();if(!t)return;inp.value='';askAria(t);
  });
  addMsg('Ask about a board, a sensor, or where a tool was last placed.','sys');
})();
