(function(){
  var v=document.getElementById('camVideo');if(!v)return;
  var start=document.getElementById('camStart'),snap=document.getElementById('camSnap'),stream=null;
  start.addEventListener('click',async function(){
    if(stream){stream.getTracks().forEach(function(t){t.stop()});stream=null;v.srcObject=null;start.textContent='Start camera';return;}
    try{stream=await navigator.mediaDevices.getUserMedia({video:true});v.srcObject=stream;start.textContent='Stop camera';}
    catch(e){toast('Camera permission denied')}
  });
  snap.addEventListener('click',async function(){
    if(!stream)return toast('Start the camera first');
    var c=document.createElement('canvas');c.width=v.videoWidth;c.height=v.videoHeight;
    c.getContext('2d').drawImage(v,0,0);
    c.toBlob(async function(b){
      var fd=new FormData();fd.append('image',b,'frame.jpg');
      try{var r=await (await fetch('/api/vision/identify',{method:'POST',body:fd})).json();
        if(window.addMsg)addMsg(r.label||'Nothing recognised','bot');}
      catch(e){toast('Vision request failed')}
    },'image/jpeg',.9);
  });
})();
