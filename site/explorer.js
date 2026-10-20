'use strict';
const $=id=>document.getElementById(id),canvas=$('graph'),ctx=canvas.getContext('2d');
const BLUE='#285cff',AMBER='#bd7410',AUTOPLAY_BLOCK=100;
let checkpointPaused=false,framePending=false;
function requestDraw(){if(framePending)return;framePending=true;requestAnimationFrame(now=>{framePending=false;draw(now);});}
let points=[],seen=new Map(),cache=new Map(),factorCache=new Map(),playing=true,busy=false,token=0,peak=0n,animation=null,nextAt=0,width=0,height=0,discovered=false,lastFrame=0;
let view={lo:0,hi:2,xhi:12};
const duration=()=>1100-Number($('speed').value)*90;
const fmt=n=>n.toLocaleString('en-CA');
let chartExponent=0,chartMode='log';
const transform=n=>AliquotMath.coordinate(n,$('scale').value,chartExponent);
function syncChart(){const mode=$('scale').value,exponent=mode==='linear'?Math.max(0,peak.toString().length-6):0;if(mode!==chartMode||exponent!==chartExponent){chartMode=mode;chartExponent=exponent;view={lo:0,hi:Math.max(2,...points.map(p=>transform(p.n)))*1.2,xhi:Math.max(12,points[points.length-1]?.k+1||12)};}}
// Inspect only computed data: moving over a point must never trigger factoring.
let screenPoints=[],hoveredPoint=null,pinnedPoint=null,suppressedPoint=null,pointer=null,cyclePeriod=null,inspectionJob=null;
function divisorDetails(p){
  if(p.n===0n)return {factorization:'Not defined for 0',divisors:'Not defined: 0 has infinitely many positive divisors.', 'divisor-summary':'s(0) is undefined; the plotted zero loop is visualization only.',canCompute:false};
  if(p.divisorCard)return p.divisorCard;
  const factors=p.n===1n?[]:(p.factors??factorCache.get(p.n.toString()));
  if(!factors)return {
    factorization:'Not computed yet',divisors:'Compute once to list the proper divisors.',
    'divisor-summary':p.divisorIssue?`Unresolved: ${p.divisorIssue}`:inspectionJob?.point===p?'Computing within the factorization work budget…':'No extra factorization runs on hover. Pin this point and choose Compute divisors.',canCompute:true,
  };
  const info=AliquotMath.properDivisorsFromFactors(p.n,factors);
  const shown=[];let characters=0;
  for(const d of info.values){const text=fmt(d);if(characters+text.length+2>8000)break;shown.push(text);characters+=text.length+2;}
  const truncated=BigInt(shown.length)<info.count;
  p.divisorCard={
    factorization:factors.length?factors.map(({prime,exponent})=>fmt(prime)+(exponent>1?`^${exponent}`:'')).join(' × '):'1 (no prime factors)',
    divisors:shown.length?shown.join(', '):'None (1 has no proper positive divisors)',
    'divisor-summary':`${fmt(info.count)} proper divisor${info.count===1n?'':'s'} · exact sum = ${fmt(info.sum)}${truncated?`. Showing ${shown.length} as a sample, not necessarily the smallest (display limit: 200 entries / 8,000 characters).`:'. Complete list.'}`,
    canCompute:false,
  };
  return p.divisorCard;
}
function pointDetails(p){
  const next=p.n===0n?null:(p.next??(p.n===1n?0n:cache.get(p.n.toString())));
  const delta=p.previous===undefined?null:p.n-p.previous;
  let status='Next term not computed yet; no abundance or primality claim.';
  if(p.n===0n)status='Terminated at 0; s(0) is undefined. Further zeros are visualization only.';
  else if(p.n===1n)status='Terminal positive term: 1 → 0.';
  else if(next!==undefined)status=next===p.n?'Perfect number: s(n) = n.':next>p.n?'Abundant: s(n) > n.':'Deficient: s(n) < n.';
  if(p.issue)status+=` Calculation stopped: ${p.issue}`;
  if(p.n>0n&&p.firstSeen!==undefined&&p.firstSeen!==null)status+=` Repeats step ${fmt(p.firstSeen)}; cycle period ${fmt(p.period)}.`;
  return {
    title:`Point · step ${fmt(p.k)}`,
    value:fmt(p.n),
    size:`${fmt(p.n.toString().length)} decimal digit${p.n.toString().length===1?'':'s'} · ${p.n%2n===0n?'even':'odd'}`,
    residue:`${p.n%12n} · n = ${p.n.toString(12).toUpperCase()} (base 12; A=10, B=11)${p.n%12n===6n?' · driver-six class (6 mod 12)':''}`,
    previous:p.previous===undefined?'Starting value (no previous term)':fmt(p.previous),
    change:delta===null?'Not applicable':`${delta>0n?'+':''}${fmt(delta)}${delta===0n?' · unchanged':delta>0n?' · increased':' · decreased'}`,
    next:p.n===0n?'0 → 0 is a visual extension, not s(0)':next===undefined?'Not computed yet':fmt(next),
    status,
    ...divisorDetails(p),
  };
}
function showPointDetails(){
  const p=pinnedPoint||hoveredPoint;
  $('point-details').hidden=!p;
  if(!p)return;
  const details=pointDetails(p);
  for(const field of ['title','value','size','residue','previous','change','next','status','factorization','divisors','divisor-summary'])$('point-'+field).textContent=details[field];
  $('point-compute').hidden=!details.canCompute;
  $('point-compute').disabled=!pinnedPoint||busy;
  $('point-compute').textContent=inspectionJob?.point===p?'Computing…':!pinnedPoint?'Pin point to compute divisors':busy?'Calculation in progress…':'Compute divisors (bounded)';
  $('point-mode').textContent=pinnedPoint?'Pinned · click this point again, click empty chart space, or Close to dismiss.':'Preview · click or tap this point to pin its details.';
}
function clearPointDetails(){
  if(inspectionJob){inspectionJob=null;busy=false;}
  suppressedPoint=pinnedPoint||hoveredPoint;
  pinnedPoint=null;hoveredPoint=null;pointer=null;
  showPointDetails();requestDraw();
}
function hoverPoint(p){
  if(p===suppressedPoint)p=null;
  else suppressedPoint=null;
  if(hoveredPoint!==p){hoveredPoint=p;showPointDetails();requestDraw();}
}
function hitPoint(event){
  const box=canvas.getBoundingClientRect();
  const x=(event.clientX-box.left)*width/box.width,y=(event.clientY-box.top)*height/box.height;
  let closest=null,distance=event.pointerType==='touch'?24:12;
  for(const target of screenPoints){
    const d=Math.hypot(target.x-x,target.y-y);
    if(d<=distance){distance=d;closest=target.point;}
  }
  return closest;
}
canvas.onpointermove=event=>{pointer={clientX:event.clientX,clientY:event.clientY,pointerType:event.pointerType};hoverPoint(hitPoint(pointer));};
canvas.onpointerleave=()=>{pointer=null;hoveredPoint=null;suppressedPoint=null;showPointDetails();requestDraw();};
canvas.onclick=event=>{
  const p=hitPoint(event);
  if(!p||p===pinnedPoint){clearPointDetails();return;}
  pinnedPoint=p;hoveredPoint=null;suppressedPoint=null;showPointDetails();requestDraw();
};
canvas.onkeydown=event=>{
  if(event.key==='Escape'){event.preventDefault();clearPointDetails();return;}
  const visible=screenPoints.map(target=>target.point);
  if(!visible.length)return;
  const current=pinnedPoint||hoveredPoint;
  if(event.key==='Enter'||event.key===' '){
    event.preventDefault();
    if(pinnedPoint){clearPointDetails();return;}
    pinnedPoint=current||visible[visible.length-1];showPointDetails();requestDraw();return;
  }
  if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
  event.preventDefault();pointer=null;suppressedPoint=null;
  const index=visible.indexOf(current);
  const next=event.key==='Home'?0:event.key==='End'?visible.length-1:index<0?(event.key==='ArrowLeft'?visible.length-1:0):Math.max(0,Math.min(visible.length-1,index+(event.key==='ArrowLeft'?-1:1)));
  if(pinnedPoint)pinnedPoint=visible[next];else hoveredPoint=visible[next];
  showPointDetails();requestDraw();
};
$('point-close').onclick=()=>{clearPointDetails();canvas.focus();};
$('point-compute').onclick=async()=>{
  const p=pinnedPoint;
  if(!p||busy||p.n<2n)return;
  const job={point:p},t=token;
  inspectionJob=job;busy=true;playing=false;playLabel();delete p.divisorIssue;showPointDetails();
  const cancelled=()=>t!==token||inspectionJob!==job;
  try{
    const next=await aliquot(p.n,t,cancelled);
    if(cancelled())return;
    p.next=next;p.factors=factorCache.get(p.n.toString());delete p.issue;
  }catch(e){if(!cancelled())p.divisorIssue=e.message;}
  finally{if(!cancelled()){inspectionJob=null;busy=false;showPointDetails();requestDraw();}}
};
function playLabel(){$('play').textContent=playing?'Ⅱ Pause':checkpointPaused?'▶ Resume':'▶ Play';}
function pauseAtCheckpoint(k,message='',mark=false){if(k%AUTOPLAY_BLOCK!==0)return;playing=false;checkpointPaused=true;playLabel();note((message?message+' ':'')+`Autoplay paused at step ${fmt(k)} to save CPU. Click Resume to continue to step ${fmt(k+AUTOPLAY_BLOCK)}.`,mark);}
function note(text,discovery=false){$('note').textContent=text;$('note').className='note'+(discovery?' discovery':'');}
function stats(){const p=points[points.length-1];$('index').textContent=fmt(p.k);$('value').textContent=fmt(p.n);$('peak').textContent=fmt(peak);showPointDetails();}
function reset(){const raw=$('seed').value.trim();if(!/^\d+$/.test(raw)){note('Enter a non-negative integer.');return;}if(raw.length>AliquotMath.MAX_DIGITS){note('Input exceeds the 1,000-digit browser resource budget.');return;}const n=BigInt(raw);clearPointDetails();screenPoints=[];suppressedPoint=null;cyclePeriod=null;checkpointPaused=false;token++;busy=false;animation=null;peak=n;seen=new Map([[n.toString(),0]]);discovered=n===0n;points=[{n,k:0,mark:n===0n,label:n===0n?'Zero':''}];playing=true;nextAt=0;playLabel();stats();syncChart();view={lo:0,hi:Math.max(2,transform(n)*1.2),xhi:12};note(n===0n?'Zero · continuing with 0 → 0.':'Blue: sequence. Amber: first discovery only.',n===0n);}
async function aliquot(n,t,cancelled=()=>t!==token){if(cancelled())throw new Error('cancelled');if(n<2n)return 0n;const key=n.toString();if(cache.has(key))return cache.get(key);let factors;const answer=await AliquotMath.sum(n,{cancelled,onFactors:value=>{factors=value;}});if(cancelled())throw new Error('cancelled');if(cache.size>=1000){const oldest=cache.keys().next().value;cache.delete(oldest);factorCache.delete(oldest);}cache.set(key,answer);if(factors)factorCache.set(key,factors);return answer;}
async function advance(){if(busy||animation)return;busy=true;const t=token,prev=points[points.length-1];try{const n=await aliquot(prev.n,t);if(t!==token)return;if(n.toString().length>AliquotMath.MAX_DIGITS)throw new Error('Next term exceeds the 1,000-digit browser resource budget. No divergence conclusion.');prev.next=n;prev.factors=factorCache.get(prev.n.toString());delete prev.issue;const k=prev.k+1,key=n.toString(),firstSeen=seen.get(key)??null;if(cyclePeriod===null&&n>0n&&firstSeen!==null)cyclePeriod=k-firstSeen;let label='',message='',mark=false;if(!discovered){if(n===0n){label='Zero';message='Reached zero · continuing with 0 → 0.';mark=true;}else if(n===prev.n){label='Perfect';message='Perfect number: '+fmt(n)+' · s(n) = n.';mark=true;}else if(seen.has(key)){const period=k-seen.get(key);label='Period '+period;message='Cycle detected · period '+period+'.';mark=true;}if(mark){discovered=true;note(message,true);}}if(!seen.has(key))seen.set(key,k);if(n>peak)peak=n;points.push({n,k,mark,label,previous:prev.n,firstSeen,period:cyclePeriod});if(points.length>180)points.shift();animation={start:performance.now(),length:duration(),fraction:0};pauseAtCheckpoint(k,message,mark);stats();requestDraw();}catch(e){if(t!==token)return;prev.issue=e.message;showPointDetails();playing=false;playLabel();note(e.message);}finally{if(t===token){busy=false;showPointDetails();}}}
function resize(){const box=canvas.getBoundingClientRect(),dpr=window.devicePixelRatio||1;width=box.width;height=box.height;canvas.width=Math.round(width*dpr);canvas.height=Math.round(height*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);}
window.addEventListener('resize',()=>{screenPoints=[];resize();requestDraw();});
function draw(now){const ease=1-Math.exp(-Math.min(80,now-(lastFrame||now-16))/110);lastFrame=now;if(animation){const t=Math.min(1,(now-animation.start)/animation.length);animation.fraction=t*t*(3-2*t);if(t>=1){animation=null;nextAt=now+80;}}syncChart();const first=points[0],last=points[points.length-1];if(!first)return;const ys=points.map(p=>transform(p.n));const ymin=Math.min(...ys),ymax=Math.max(...ys),span=Math.max($('scale').value==='log'?.5:1,ymax-ymin);const target={lo:Math.max(0,ymin-span*.22),hi:ymax+span*.32,xhi:Math.max(12,last.k+1)};for(const key of ['lo','hi','xhi'])view[key]+=(target[key]-view[key])*ease;const left=58,right=20,top=30,bottom=38,W=width-left-right,H=height-top-bottom,xlo=first.k;const x=k=>left+(k-xlo)/Math.max(1,view.xhi-xlo)*W;const y=v=>top+H-(v-view.lo)/Math.max(1e-9,view.hi-view.lo)*H;ctx.clearRect(0,0,width,height);ctx.font='11px monospace';ctx.lineWidth=1;for(let i=0;i<=4;i++){const v=view.lo+(view.hi-view.lo)*i/4,Y=y(v);ctx.strokeStyle='#edf0f2';ctx.beginPath();ctx.moveTo(left,Y);ctx.lineTo(width-right,Y);ctx.stroke();ctx.fillStyle='#87919a';ctx.textAlign='right';ctx.fillText(AliquotMath.axisLabel(v,$('scale').value,chartExponent),left-9,Y+4);}ctx.fillStyle='#87919a';ctx.textAlign='center';for(let i=0;i<=4;i++){const k=Math.round(xlo+(view.xhi-xlo)*i/4);ctx.fillText(k,x(k),height-13);}ctx.save();ctx.beginPath();ctx.rect(left-9,top-25,W+18,H+34);ctx.clip();let tip=null;screenPoints=[];for(let i=0;i<points.length;i++){const p=points[i],X=x(p.k),Y=y(ys[i]);const partial=i===points.length-1&&animation&&i>0;if(i>0){const q=points[i-1],a=partial?animation.fraction:1;const end={x:x(q.k)+(X-x(q.k))*a,y:y(ys[i-1])+(Y-y(ys[i-1]))*a};ctx.strokeStyle=BLUE;ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(x(q.k),y(ys[i-1]));ctx.lineTo(end.x,end.y);ctx.stroke();tip=end;}else tip={x:X,y:Y};if(!partial){if(X>=left-9&&X<=width-right+9&&Y>=top-25&&Y<=height-bottom+9)screenPoints.push({point:p,x:X,y:Y});ctx.fillStyle=BLUE;ctx.beginPath();ctx.arc(X,Y,2.5,0,Math.PI*2);ctx.fill();}}
if(pointer)hoverPoint(hitPoint(pointer));
canvas.style.cursor=hoveredPoint||pinnedPoint?'pointer':'default';
const selected=pinnedPoint||hoveredPoint;
for(const target of screenPoints){if(target.point!==selected)continue;ctx.strokeStyle=BLUE;ctx.lineWidth=2;ctx.beginPath();ctx.arc(target.x,target.y,7,0,Math.PI*2);ctx.stroke();}
// Draw discovery markers last: one marker, never an amber segment or repeated state.
for(let i=0;i<points.length;i++){const p=points[i];if(!p.mark||(i===points.length-1&&animation))continue;const X=x(p.k),Y=y(ys[i]);ctx.fillStyle='white';ctx.beginPath();ctx.arc(X,Y,6,0,Math.PI*2);ctx.fill();ctx.fillStyle=AMBER;ctx.beginPath();ctx.arc(X,Y,4,0,Math.PI*2);ctx.fill();ctx.font='11px monospace';ctx.textAlign=X>width-120?'right':'left';ctx.fillText(p.label,X+(X>width-120?-9:9),Y-12);}
if(tip){ctx.strokeStyle=BLUE;ctx.fillStyle=BLUE;ctx.globalAlpha=.25;ctx.lineWidth=1.5;ctx.beginPath();ctx.arc(tip.x,tip.y,8+2*Math.sin(now/220),0,Math.PI*2);ctx.stroke();ctx.globalAlpha=1;const tail=points[points.length-1];if(animation||!tail.mark){ctx.beginPath();ctx.arc(tip.x,tip.y,3.5,0,Math.PI*2);ctx.fill();}}ctx.restore();if(playing&&!busy&&!animation&&now>=nextAt)advance();if(playing||busy||animation)requestDraw();}
$('form').onsubmit=e=>{e.preventDefault();reset();};
$('play').onclick=()=>{playing=!playing;if(playing&&checkpointPaused){checkpointPaused=false;note(`Continuing · next automatic pause at step ${fmt((Math.floor(points[points.length-1].k/AUTOPLAY_BLOCK)+1)*AUTOPLAY_BLOCK)}.`);}playLabel();requestDraw();};
$('step').onclick=()=>{playing=false;if(checkpointPaused)note('Manual step · autoplay is paused.');checkpointPaused=false;playLabel();advance();requestDraw();};
$('scale').onchange=requestDraw;
document.querySelectorAll('[data-n]').forEach(b=>b.onclick=()=>{$('seed').value=b.dataset.n;reset();});resize();reset();requestDraw();
