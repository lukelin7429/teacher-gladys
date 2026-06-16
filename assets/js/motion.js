/* Teacher Gladys portfolio — interactions: nav, scroll reveal, lightbox */
(function(){
  // sticky nav shadow
  var nav=document.querySelector('.nav');
  if(nav){
    var onScroll=function(){nav.classList.toggle('scrolled',window.scrollY>10);};
    window.addEventListener('scroll',onScroll,{passive:true});onScroll();
  }
  // mobile menu
  var tog=document.querySelector('.nav-toggle'),links=document.querySelector('.nav-links');
  if(tog&&links){tog.addEventListener('click',function(){links.classList.toggle('show');});}

  // scroll reveal (getBoundingClientRect-based so it works in any container)
  var items=[].slice.call(document.querySelectorAll('.rvl'));
  function reveal(){
    var h=window.innerHeight;
    items.forEach(function(el){
      if(el.classList.contains('in'))return;
      var r=el.getBoundingClientRect();
      if(r.top<h-70&&r.bottom>0)el.classList.add('in');
    });
  }
  window.addEventListener('scroll',reveal,{passive:true});
  window.addEventListener('resize',reveal);reveal();
  setTimeout(reveal,200);

  // lightbox for galleries
  var imgs=[].slice.call(document.querySelectorAll('.gallery .gi img'));
  if(imgs.length){
    var lb=document.createElement('div');lb.className='lb';
    lb.innerHTML='<span class="x">&times;</span><span class="nav-btn prev">&#8249;</span>'+
      '<img alt="Photo"><span class="nav-btn next">&#8250;</span>';
    document.body.appendChild(lb);
    var big=lb.querySelector('img'),cur=0;
    function show(i){cur=(i+imgs.length)%imgs.length;big.src=imgs[cur].dataset.full||imgs[cur].src;}
    imgs.forEach(function(im,i){im.addEventListener('click',function(){show(i);lb.classList.add('open');});});
    lb.querySelector('.x').addEventListener('click',function(){lb.classList.remove('open');});
    lb.querySelector('.prev').addEventListener('click',function(e){e.stopPropagation();show(cur-1);});
    lb.querySelector('.next').addEventListener('click',function(e){e.stopPropagation();show(cur+1);});
    lb.addEventListener('click',function(e){if(e.target===lb)lb.classList.remove('open');});
    document.addEventListener('keydown',function(e){
      if(!lb.classList.contains('open'))return;
      if(e.key==='Escape')lb.classList.remove('open');
      if(e.key==='ArrowLeft')show(cur-1);
      if(e.key==='ArrowRight')show(cur+1);
    });
  }

  // lazy count-up for stats
  var stats=[].slice.call(document.querySelectorAll('.stat .n[data-to]'));
  function countUp(){
    stats.forEach(function(el){
      if(el.dataset.done)return;
      var r=el.getBoundingClientRect();
      if(r.top<window.innerHeight-40){
        el.dataset.done=1;
        var to=+el.dataset.to,t0=null,dur=1300,suf=el.dataset.suf||'';
        (function step(t){if(!t0)t0=t;var p=Math.min((t-t0)/dur,1);
          el.textContent=Math.floor(p*to)+suf;if(p<1)requestAnimationFrame(step);})(performance.now());
      }
    });
  }
  window.addEventListener('scroll',countUp,{passive:true});countUp();
})();
