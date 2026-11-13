(function(){
  var drop=document.getElementById('drop'),file=document.getElementById('toolPhoto');if(!drop)return;
  drop.addEventListener('click',function(){file.click()});
  ['dragover','dragenter'].forEach(function(n){drop.addEventListener(n,function(e){e.preventDefault();drop.classList.add('over')})});
  ['dragleave','drop'].forEach(function(n){drop.addEventListener(n,function(){drop.classList.remove('over')})});
  drop.addEventListener('drop',function(e){e.preventDefault();file.files=e.dataTransfer.files;drop.textContent=file.files[0].name});
  file.addEventListener('change',function(){if(file.files[0])drop.textContent=file.files[0].name});
  document.getElementById('toolForm').addEventListener('submit',async function(e){
    e.preventDefault();
    try{var r=await fetch('/api/faculty/tools',{method:'POST',body:new FormData(e.target)});
      if(!r.ok)throw 0;toast('Saved. ARIA can now answer "where is it".');}
    catch(x){toast('Upload failed, backend not connected')}
  });
})();
