(function(){
  var mic=document.getElementById('micBtn');if(!mic)return;
  var SR=window.SpeechRecognition||window.webkitSpeechRecognition;
  if(!SR){mic.disabled=true;mic.title='Speech recognition not supported in this browser';return;}
  var rec=new SR();rec.lang='en-IN';rec.interimResults=false;
  rec.onstart=function(){mic.classList.add('rec')};
  rec.onend=function(){mic.classList.remove('rec')};
  rec.onresult=function(e){var t=e.results[0][0].transcript;if(window.askAria)askAria(t);};
  rec.onerror=function(){toast('Mic error, try again')};
  mic.addEventListener('click',function(){mic.classList.contains('rec')?rec.stop():rec.start();});
  window.speak=function(text){
    if(!window.speechSynthesis)return;
    var u=new SpeechSynthesisUtterance(text);u.lang='en-IN';speechSynthesis.cancel();speechSynthesis.speak(u);
  };
})();
