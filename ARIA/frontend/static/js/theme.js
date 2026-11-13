(function(){
  var KEY='aria-theme',root=document.documentElement;
  var saved=null;try{saved=localStorage.getItem(KEY)}catch(e){}
  var pref=saved||(matchMedia('(prefers-color-scheme: light)').matches?'light':'dark');
  root.setAttribute('data-theme',pref);
  window.addEventListener('DOMContentLoaded',function(){
    var b=document.getElementById('themeToggle');if(!b)return;
    function label(){b.textContent=root.getAttribute('data-theme')==='dark'?'Light mode':'Dark mode'}
    label();
    b.addEventListener('click',function(){
      var n=root.getAttribute('data-theme')==='dark'?'light':'dark';
      root.setAttribute('data-theme',n);try{localStorage.setItem(KEY,n)}catch(e){}label();
    });
  });
})();
