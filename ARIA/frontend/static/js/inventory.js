(function(){
  var body=document.getElementById('invBody');if(!body)return;
  var q=document.getElementById('invSearch'),rows=[];
  function draw(){
    var s=(q.value||'').toLowerCase();
    body.innerHTML=rows.filter(function(r){return (r.name+r.location).toLowerCase().includes(s)}).map(function(r){
      return '<tr><td>'+r.name+'</td><td>'+r.location+'</td><td><span class="tag'+(r.qty?'':' bad')+'">'+(r.qty?r.qty+' in stock':'missing')+'</span></td><td class="mono">'+r.updated+'</td></tr>';
    }).join('')||'<tr><td colspan="4" class="mono">No tools found</td></tr>';
  }
  api('/api/inventory').then(function(d){rows=d.items||[];draw()}).catch(function(){
    rows=[{name:'Multimeter',location:'Rack 2, Box 3',qty:4,updated:'today'},{name:'ESP32 DevKit',location:'Almirah A, Box 1',qty:9,updated:'yesterday'},{name:'Soldering iron',location:'Rack 1',qty:0,updated:'3 days ago'}];
    draw();toast('Showing sample data, backend not connected');
  });
  q.addEventListener('input',draw);
})();
