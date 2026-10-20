import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import { readFileSync } from 'node:fs';

const root = new URL('../', import.meta.url);
const source = ['site/vendor/katex/katex.min.js','site/latex.js','site/math.js','site/explorer.js']
  .map(path=>readFileSync(new URL(path,root),'utf8')).join('\n');
function browser({dpr=1,chartWidth=900,chartHeight=400,cardHeight=Math.min(300,chartHeight-16)}={}) {
  const elements = new Map();
  const labels = [], frames = [];
  const presets=[...readFileSync(new URL('site/index.html',root),'utf8').matchAll(/<button type="button" data-n="(\d+)" data-kind="([^"]+)" data-description="([^"]+)">/g)]
    .map(([,n,kind,description])=>({dataset:{n,kind,description},attributes:{},setAttribute(name,value){this.attributes[name]=value;}}));
  const context2d = new Proxy({}, { get: (_, name) => (...args) => {
    for (const arg of args) if (typeof arg === 'number') assert.ok(Number.isFinite(arg), `non-finite canvas argument in ${String(name)}`);
    if (name === 'fillText') labels.push(args[0]);
  }, set: () => true });
  const element = id => {
    if (!elements.has(id)) elements.set(id, {
      value: id === 'seed' ? '12' : id === 'scale' ? 'log' : id === 'speed' ? '8' : '5',
      textContent: '', innerHTML:'', dataset:{}, className: '', width: 0, height: 0, hidden:false, style:{},
      focus() { this.focused=true; },
      getContext: () => context2d,
      getBoundingClientRect: () => ({ left:40, top:60,
        width:id==='point-details'?Math.min(320,chartWidth-16):chartWidth,
        height:id==='point-details'?cardHeight:chartHeight }),
    });
    return elements.get(id);
  };
  const context = vm.createContext({
    document: { getElementById: element, querySelectorAll: selector => selector==='[data-n]'?presets:[] },
    window: { devicePixelRatio: dpr, addEventListener() {} },
    requestAnimationFrame(callback) { frames.push(callback); return frames.length; }, performance, setTimeout,
  });
  vm.runInContext(source, context);
  return { element, labels, presets, run: code => vm.runInContext(code, context),
    frame: (now=performance.now()) => { const callback=frames.shift(); if(callback)callback(now); },
    pendingFrames: () => frames.length };
}

test('exact proper-divisor sums, including visualization zero extension', async () => {
  const { run } = browser();
  for (const [n, sum] of [[0n, 0n], [1n, 0n], [2n, 1n], [12n, 16n], [28n, 28n], [220n, 284n], [284n, 220n], [12496n, 14288n], [999983n, 1n]]) {
    assert.equal(await run(`aliquot(${n}n, token)`), sum);
  }
});

test('220 detects its first cycle, never a repeated amber marker', async () => {
  const { run, element } = browser();
  element('seed').value = '220'; run('reset()');
  for (let i = 0; i < 4; i++) await run('animation = null; advance()');
  assert.equal(run('points.filter(p => p.mark).length'), 1);
  assert.equal(element('note').textContent, 'Cycle detected · period 2.');
});

test('zero, perfect numbers, input validation and step control', async () => {
  const { run, element } = browser();
  element('seed').value = '28'; run('reset()'); await run('advance()');
  assert.match(element('note').textContent, /Perfect number/);
  element('seed').value = '0'; run('reset()');
  assert.equal(run('points[0].mark'), true);
  for (const invalid of ['-1', '1.5', 'abc']) {
    element('seed').value = invalid; run('reset()');
    assert.equal(element('note').textContent, 'Enter a non-negative integer.');
  }
  element('seed').value = '1'.repeat(1001); run('reset()');
  assert.match(element('note').textContent, /1,000-digit/);
  element('seed').value = '1000000000000001'; run('reset()');
  assert.equal(run('points[0].n'), 1000000000000001n);
  element('seed').value = '12'; run('reset()');
  element('step').onclick();
  await new Promise(resolve => setTimeout(resolve, 0));
  assert.equal(run('playing'), false);
  assert.equal(element('value').textContent, '16');
});

test('reset cancels stale work and drawing remains callable', async () => {
  const { run, element } = browser();
  const calculation = run('aliquot(999999999999989n, token)');
  element('seed').value = '12'; run('reset()');
  await assert.rejects(calculation, /cancelled/);
  run('draw(performance.now())');
});

test('steps cross the former ceiling and retain exact displayed integers', async () => {
  const { run, element } = browser();
  element('seed').value = '1000000000000000'; run('reset()');
  await run('advance()');
  assert.ok(run('points[1].n > 1000000000000000n'));
  assert.equal(element('value').textContent, run('fmt(points[1].n)'));
  run('playing=false; draw(performance.now())');
});

test('hundreds of digits plot finite coordinates in both scales', async () => {
  const { run, element, labels } = browser();
  element('seed').value = String(2n ** 2000n); run('reset()');
  await run('advance()');
  assert.equal(run('points[1].n'), 2n ** 2000n - 1n);
  run('playing=false; animation=null; draw(performance.now())');
  element('scale').value = 'linear'; run('draw(performance.now())');
  assert.ok(labels.some(label => /e\d+/.test(label)));
  assert.ok(labels.every(label => !/Infinity|NaN/.test(label)));
  element('scale').value = 'log'; run('draw(performance.now())');
});

test('budget failures and resource limits never advance or cache partial sums', async () => {
  const { run, element } = browser();
  await assert.rejects(run('AliquotMath.sum(999983n,{maxWork:10})'), /unresolved/);
  await assert.rejects(run('AliquotMath.sum(2n**100n,{maxWork:10})'), /unresolved/);
  await assert.rejects(run('AliquotMath.sum(0n)'), /positive/);
  element('seed').value = '999983'; run('reset()');
  run('const originalSum=AliquotMath.sum; AliquotMath.sum=(n,options)=>originalSum(n,{...options,maxWork:10})');
  await run('advance()');
  assert.equal(run('points.length'), 1);
  assert.equal(run('playing'), false);
  assert.equal(run('cache.has("999983")'), false);
  assert.match(element('note').textContent, /unresolved/);
  assert.match(run('pointDetails(points[0]).status'), /Calculation stopped:.*unresolved/);
  run('AliquotMath.sum=originalSum');
  // A successor can exceed the digit budget even when its source fits.
  element('seed').value = '1'+'0'.repeat(999); run('reset()');
  run('AliquotMath.sum=async()=>10n**1000n');
  await run('advance()');
  assert.equal(run('points.length'), 1);
  assert.match(element('note').textContent, /resource budget/);
});

test('repeated-factor work yields and can be cancelled', async () => {
  const { run } = browser();
  assert.equal(await run('AliquotMath.sum(2n**1000n,{yieldUI:async()=>{}})'), 2n ** 1000n - 1n);
  await assert.rejects(run('let cancelled=false; AliquotMath.sum(2n**1000n,{cancelled:()=>cancelled,yieldUI:async()=>{cancelled=true}})'), /cancelled/);
});

function pointEvent(run,index=0){
  const target=run(`screenPoints[${index}]`);
  assert.ok(target,'a rendered hit target exists');
  return {clientX:target.x+40,clientY:target.y+60,pointerType:'mouse'};
}

test('hover shows exact point data and leaves without computing anything', async () => {
  const {run,element}=browser();
  await run('advance()');
  run('playing=false; animation=null; draw(performance.now()); AliquotMath.sum=()=>{throw new Error("hover must not factor")};');
  element('graph').onpointermove(pointEvent(run,1));
  assert.equal(element('point-details').hidden,false);
  assert.equal(element('point-title').textContent,'Point · step 1');
  assert.equal(element('point-value').textContent,'16');
  assert.equal(element('point-previous').textContent,'12');
  assert.equal(element('point-change').textContent,'+4');
  assert.equal(element('point-next').textContent,'Not computed');
  assert.match(element('point-status').textContent,/not computed/);
  assert.match(element('point-size').textContent,/2 digits · even/);
  element('graph').onpointerleave();
  assert.equal(element('point-details').hidden,true);
  assert.equal(run('points.length'),2);
});

test('click toggles a pin, switches points, and empty space or Close dismisses', async () => {
  const {run,element}=browser();
  await run('advance()');run('playing=false; animation=null; draw(performance.now())');
  const graph=element('graph'),first=pointEvent(run),second=pointEvent(run,1);
  graph.onclick(first);
  assert.match(element('point-mode').textContent,/Pinned/);
  assert.equal(element('point-next').textContent,'16');
  assert.match(element('point-status').textContent,/Abundant/);
  graph.onpointerleave();
  assert.equal(element('point-details').hidden,false);
  graph.onpointermove(second);
  assert.equal(element('point-title').textContent,'Point · step 0');
  graph.onclick(second);
  assert.equal(element('point-title').textContent,'Point · step 1');
  graph.onclick(second);
  assert.equal(element('point-details').hidden,true);
  graph.onpointermove(second);
  assert.equal(element('point-details').hidden,true,'same-point hover cannot immediately reopen a toggled box');
  graph.onpointermove(first);
  assert.equal(element('point-details').hidden,false);
  graph.onclick(first);graph.onclick({clientX:0,clientY:0});
  assert.equal(element('point-details').hidden,true);
  graph.onclick(first);element('point-close').onclick();
  assert.equal(element('point-details').hidden,true);
  assert.equal(graph.focused,true);
});

test('pins survive advancement and retained-window eviction but reset clears them', async () => {
  const {run,element}=browser();
  run('playing=false; draw(performance.now())');
  element('graph').onclick(pointEvent(run));
  await run('advance()');
  assert.equal(element('point-next').textContent,'16');
  assert.match(element('point-status').textContent,/Abundant/);
  for(let i=0;i<181;i++)await run('animation=null; advance()');
  assert.equal(run('points.length'),180);
  assert.ok(run('points[0].k>0'));
  assert.equal(element('point-value').textContent,'12');
  assert.equal(element('point-next').textContent,'16');
  run('reset()');
  assert.equal(element('point-details').hidden,true);
  assert.equal(run('screenPoints.length'),0);
});

test('keyboard inspection, pinning, and Escape work without a mouse', async () => {
  const {run,element}=browser();
  await run('advance()');run('playing=false; animation=null; draw(performance.now())');
  const graph=element('graph');
  const press=key=>{let prevented=false;graph.onkeydown({key,preventDefault(){prevented=true;}});assert.equal(prevented,true);};
  press('Home');assert.equal(element('point-title').textContent,'Point · step 0');
  press('ArrowRight');assert.equal(element('point-title').textContent,'Point · step 1');
  press('Enter');assert.match(element('point-mode').textContent,/Pinned/);
  press('ArrowLeft');assert.equal(element('point-title').textContent,'Point · step 0');
  press('End');assert.equal(element('point-title').textContent,'Point · step 1');
  press('Escape');assert.equal(element('point-details').hidden,true);
});

test('hit targets use CSS coordinates at high DPR and exclude unfinished endpoints', async () => {
  const {run,element}=browser({dpr:2});
  await run('advance()');run('playing=false; draw(performance.now())');
  assert.equal(run('screenPoints.length'),1);
  assert.equal(element('graph').width,1800);
  element('graph').onpointermove(pointEvent(run));
  assert.equal(element('point-value').textContent,'12');
  run('animation=null; draw(performance.now())');
  assert.equal(run('screenPoints.length'),2);
  element('scale').value='linear';run('draw(performance.now())');
  element('graph').onclick({...pointEvent(run,1),pointerType:'touch'});
  assert.equal(element('point-value').textContent,'16');
});

test('details distinguish zero, terminal 1, perfect numbers, repeats, and C6', async () => {
  const {run,element}=browser();
  assert.equal(run('pointDetails(points[0]).residue'),'0 · 10₁₂');
  element('seed').value='6';run('reset()');
  assert.equal(run('pointDetails(points[0]).residue'),'6 · 6₁₂');
  await run('advance()');
  assert.match(run('pointDetails(points[0]).status'),/Perfect/);
  assert.match(run('pointDetails(points[1]).status'),/period 1/);
  element('seed').value='220';run('reset()');
  for(let i=0;i<2;i++)await run('animation=null; advance()');
  assert.match(run('pointDetails(points[2]).status'),/period 2 · first seen at 0/);
  for(let i=0;i<2;i++)await run('animation=null; advance()');
  assert.match(run('pointDetails(points[4]).status'),/period 2 · first seen at 0/);
  element('seed').value='1';run('reset()');
  assert.equal(run('pointDetails(points[0]).next'),'0');
  assert.match(run('pointDetails(points[0]).status'),/Terminal/);
  await run('advance()');
  assert.match(run('pointDetails(points[1]).status'),/s\(0\) is undefined/);
  assert.equal(run('pointDetails(points[1]).next'),'Undefined');
});

test('hundreds-digit point details preserve the exact integer without factoring', () => {
  const {run,element}=browser();
  element('seed').value=String(2n**2000n);run('reset(); playing=false; draw(performance.now())');
  element('graph').onpointermove(pointEvent(run));
  assert.equal(element('point-value').textContent,(2n**2000n).toLocaleString('en-CA'));
  assert.match(element('point-size').textContent,/603 digits/);
  assert.equal(element('point-previous').textContent,'—');
});

test('autoplay pauses at each 100-step boundary and requires explicit resume', async () => {
  const {run,element,frame,pendingFrames}=browser();
  for(let checkpoint=100;checkpoint<=300;checkpoint+=100){
    for(let k=checkpoint-99;k<=checkpoint;k++)await run('animation=null; advance()');
    assert.equal(run('points[points.length-1].k'),checkpoint);
    assert.equal(run('playing'),false);
    assert.equal(element('play').textContent,'▶ Resume');
    assert.equal(element('play').dataset.playing,'false');
    assert.match(element('note').textContent,new RegExp(`paused at step ${checkpoint}`));
    frame(1e9*checkpoint);
    assert.equal(pendingFrames(),0,'paused chart must not keep scheduling idle animation frames');
    assert.equal(run('points[points.length-1].k'),checkpoint,'finishing animation must not compute another term');
    element('play').onclick();
    assert.equal(run('playing'),true);
    assert.equal(element('play').textContent,'Pause');
    assert.equal(element('play').dataset.playing,'true');
    assert.match(element('note').textContent,new RegExp(`next automatic pause at step ${checkpoint+100}`));
    assert.equal(pendingFrames(),1,'resume restarts rendering');
  }
});

test('manual stepping past a checkpoint stays paused and reset restores the first block', async () => {
  const {run,element,frame,pendingFrames}=browser();
  for(let i=0;i<100;i++)await run('animation=null; advance()');
  frame(1e9);
  element('step').onclick();
  await new Promise(resolve=>setTimeout(resolve,0));
  assert.equal(run('points[points.length-1].k'),101);
  assert.equal(run('playing'),false);
  assert.equal(element('play').textContent,'▶ Play');
  frame(2e9);
  assert.equal(pendingFrames(),0);
  element('play').onclick();
  for(let i=102;i<=200;i++)await run('animation=null; advance()');
  assert.equal(run('playing'),false);
  assert.match(element('note').textContent,/paused at step 200/);
  run('reset()');
  assert.equal(run('playing'),true);
  assert.equal(run('checkpointPaused'),false);
  assert.equal(run('points[0].k'),0);
});

test('pausing early does not move the checkpoint; paused interactions redraw on demand', async () => {
  const {run,element,frame,pendingFrames}=browser();
  for(let i=0;i<42;i++)await run('animation=null; advance()');
  element('play').onclick();
  assert.equal(run('playing'),false);
  frame(1e9);
  assert.equal(pendingFrames(),0);
  element('graph').onpointermove(pointEvent(run));
  assert.equal(pendingFrames(),1,'hover requests a frame even when idle');
  frame(1e9+1);
  assert.equal(pendingFrames(),0);
  element('scale').value='linear';element('scale').onchange();
  assert.equal(pendingFrames(),1,'scale changes redraw a paused chart');
  frame(1e9+2);
  element('play').onclick();
  for(let i=43;i<=100;i++)await run('animation=null; advance()');
  assert.equal(run('points[points.length-1].k'),100);
  assert.equal(run('playing'),false);
});

test('base-12 values use compact subscript notation beside the remainder', () => {
  const {run,element}=browser();
  for(const [n,base12] of [[0,'0'],[10,'A'],[11,'B'],[12,'10'],[143,'BB'],[144,'100'],[1728,'1000']]){
    element('seed').value=String(n);run('reset()');
    const text=run('pointDetails(points[0]).residue');
    assert.equal(text,`${n%12} · ${base12}₁₂`);
  }
});

test('cards reuse proven factors to show complete proper divisors, count, and sum', async () => {
  const {run,element}=browser();
  await run('advance()');run('playing=false; animation=null; draw(performance.now())');
  run('AliquotMath.sum=()=>{throw new Error("no refactoring on hover")};');
  element('graph').onpointermove(pointEvent(run));
  assert.equal(element('point-factorization').textContent,'2^2 × 3');
  assert.match(element('point-factorization').innerHTML,/<msup>/);
  assert.equal(element('point-factorization').dataset.mathError,undefined);
  assert.equal(element('point-divisors').textContent,'1, 2, 3, 4, 6');
  assert.equal(element('point-divisor-summary').textContent,'5 divisors · sum 16');
  assert.equal(element('point-mode').textContent,'Click to pin');
  assert.equal(element('point-residue').textContent,'0 · 10₁₂');
  assert.equal(element('point-status').textContent,'Abundant');
  assert.equal(element('point-compute').hidden,true);
  element('graph').onpointermove(pointEvent(run,1));
  assert.equal(element('point-compute').hidden,false);
  assert.equal(element('point-compute').disabled,true,'preview must be pinned before requesting work');
});

test('explicit divisor computation pauses autoplay but does not advance the sequence', async () => {
  const {run,element}=browser();
  run('playing=false; draw(performance.now())');
  element('graph').onclick(pointEvent(run));
  assert.equal(element('point-compute').disabled,false);
  const computation=element('point-compute').onclick();
  assert.equal(run('busy'),true);
  assert.equal(element('point-compute').disabled,true);
  await computation;
  assert.equal(run('busy'),false);
  assert.equal(run('playing'),false);
  assert.equal(run('points.length'),1);
  assert.equal(element('point-next').textContent,'16');
  assert.equal(element('point-divisors').textContent,'1, 2, 3, 4, 6');
  assert.equal(element('point-compute').hidden,true);
  await run('advance()');
  assert.equal(run('points[1].n'),16n,'a later manual step reuses the exact sum');
});

test('zero, one, primes and squares have correctly labelled divisor lists', async () => {
  const {run,element}=browser();
  for(const [n,divisors,summary] of [
    ['1','None','0 divisors · sum 0'],
    ['13','1','1 divisor · sum 1'],
    ['36','1, 2, 3, 4, 6, 9, 12, 18','8 divisors · sum 55'],
  ]){
    element('seed').value=n;run('reset(); playing=false; draw(performance.now())');
    element('graph').onclick(pointEvent(run));
    if(n!=='1')await element('point-compute').onclick();
    assert.equal(element('point-divisors').textContent,divisors);
    assert.equal(element('point-divisor-summary').textContent,summary);
  }
  element('seed').value='0';run('reset(); playing=false; draw(performance.now())');
  element('graph').onclick(pointEvent(run));
  assert.equal(element('point-divisors').textContent,'Undefined');
  assert.equal(element('point-divisor-summary').textContent,'Undefined');
  assert.match(element('point-status').textContent,/s\(0\) is undefined/);
  assert.equal(element('point-compute').hidden,true);
});

test('large divisor counts and long lists are explicitly bounded samples', async () => {
  const {run,element}=browser();
  element('seed').value=String(2n**2000n);run('reset(); playing=false; draw(performance.now())');
  element('graph').onclick(pointEvent(run));
  await element('point-compute').onclick();
  assert.match(element('point-divisor-summary').textContent,/2,000 divisors/);
  assert.match(element('point-divisor-summary').textContent,/shown \(sample\)/);
  const entries=element('point-divisors').textContent.split(', ').length;
  assert.ok(entries>0&&entries<=200);
  assert.ok(element('point-divisors').textContent.length<=8000);
  // A power of the known Mersenne prime 2^127-1 has only 26 proper divisors,
  // but their decimal strings exceed the independent character budget.
  const text=run('const mersenne=2n**127n-1n; const largePoint={n:mersenne**26n,factors:[{prime:mersenne,exponent:26}]}; divisorDetails(largePoint)["divisor-summary"]');
  assert.match(text,/26 divisors.*shown \(sample\)/);
  assert.ok(run('largePoint.divisorCard.divisors.length')<=8000);
});

test('divisor failures and cancellation never cache incomplete factors or advance', async () => {
  const {run,element}=browser();
  element('seed').value='999983';run('reset(); playing=false; draw(performance.now())');
  element('graph').onclick(pointEvent(run));
  run('const original=AliquotMath.sum; AliquotMath.sum=(n,options)=>original(n,{...options,maxWork:10});');
  await element('point-compute').onclick();
  assert.match(element('point-divisor-summary').textContent,/Unresolved:.*work limit/);
  assert.equal(run('cache.has("999983")||factorCache.has("999983")'),false);
  assert.equal(run('points.length'),1);
  assert.equal(run('busy'),false);
  run('AliquotMath.sum=original');
  element('seed').value='999999999999989';run('reset(); playing=false; draw(performance.now())');
  element('graph').onclick(pointEvent(run));
  const calculation=element('point-compute').onclick();
  element('point-close').onclick();
  await calculation;
  assert.equal(element('point-details').hidden,true);
  assert.equal(run('busy'),false);
  assert.equal(run('cache.has("999999999999989")||factorCache.has("999999999999989")'),false);
  // Reset also cancels inspector work without overwriting the new run's state.
  run('draw(performance.now())');element('graph').onclick(pointEvent(run));
  const stale=element('point-compute').onclick();
  element('seed').value='12';run('reset()');
  await stale;
  assert.equal(run('points[0].n'),12n);
  assert.equal(run('busy'),false);
  assert.equal(element('point-details').hidden,true);
});

test('factor publication is complete-only and divisor sampling has exact large counts', async () => {
  const {run}=browser();
  run('let published=false');
  await assert.rejects(run('AliquotMath.sum(999983n,{maxWork:10,onFactors:()=>{published=true}})'),/work limit/);
  assert.equal(run('published'),false);
  const sample=await run(`(async()=>{
    const n=2n**8n*3n**5n*5n**3n;let factors;
    await AliquotMath.sum(n,{onFactors:value=>{factors=value}});
    return AliquotMath.properDivisorsFromFactors(n,factors);
  })()`);
  assert.equal(sample.values.length,200);
  assert.equal(sample.count,215n);
  assert.equal(sample.truncated,true);
  const count=run(`const fs=[2n,3n,5n,7n,11n,13n,17n,19n,23n,29n,31n,37n,41n,43n,47n,53n,59n,61n,67n,71n].map(prime=>({prime,exponent:10}));
    AliquotMath.properDivisorsFromFactors(fs.reduce((n,f)=>n*f.prime**10n,1n),fs).count`);
  assert.equal(count,11n**20n-1n);
  assert.ok(count>BigInt(Number.MAX_SAFE_INTEGER));
  assert.throws(()=>run('AliquotMath.properDivisorsFromFactors(12n,[{prime:2n,exponent:2}])'),/reconstruct/);
  assert.throws(()=>run('AliquotMath.properDivisorsFromFactors(0n,[])'),/positive/);
});

test('overlay anchors beside points and flips/clamps at every chart edge', () => {
  for(const [chartWidth,chartHeight,dpr] of [[900,400,1],[340,280,2]]){
    const {run,element}=browser({chartWidth,chartHeight,dpr});
    run('playing=false; draw(performance.now())');
    const card=element('point-details'),box=card.getBoundingClientRect();
    for(const [x,y] of [[60,40],[chartWidth-12,40],[60,chartHeight-12],[chartWidth-12,chartHeight-12]]){
      run(`screenPoints=[{point:points[0],x:${x},y:${y}}]`);
      element('graph').onpointermove(pointEvent(run));run('positionPointDetails()');
      const left=parseFloat(card.style.left),top=parseFloat(card.style.top);
      assert.equal(card.dataset.pinned,'false');
      assert.ok(left>=8&&left+box.width<=chartWidth-8);
      assert.ok(top>=8&&top+box.height<=chartHeight-8);
      if(chartWidth===900&&x===60)assert.equal(left,x+14,'prefer beside the point');
      if(chartWidth===900&&x===chartWidth-12)assert.equal(left,x-box.width-14,'flip to the left at the right edge');
    }
    element('graph').onclick(pointEvent(run));
    assert.equal(card.dataset.pinned,'true');
    element('graph').onpointerleave();
    assert.equal(card.hidden,false,'pinned overlay survives leaving the canvas for card controls');
  }
});

test('pinned overlays track rendered points and stay bounded after resize or eviction', async () => {
  const {run,element}=browser();
  run('playing=false; draw(performance.now())');
  element('graph').onclick(pointEvent(run));
  const card=element('point-details');
  run('screenPoints[0].x=400; screenPoints[0].y=50; positionPointDetails()');
  assert.equal(card.style.left,'414px');
  run('screenPoints=[]; positionPointDetails()');
  assert.equal(card.style.left,'414px','retain a pin even when its point leaves the rolling window');
  element('graph').getBoundingClientRect=()=>({left:40,top:60,width:340,height:320});
  run('resize(); positionPointDetails()');
  assert.ok(parseFloat(card.style.left)+320<=332);
  assert.ok(parseFloat(card.style.top)+300<=312);
  run('reset()');
  assert.equal(card.hidden,true);
  assert.equal(run('pointAnchor'),null);
});

test('tall pinned cards retain natural height instead of clipping or vertically scrolling', () => {
  const {run,element}=browser({cardHeight:600});
  run('playing=false; draw(performance.now())');
  element('graph').onclick(pointEvent(run));
  const card=element('point-details');
  assert.equal(card.hidden,false);
  assert.equal(card.getBoundingClientRect().height,600);
  assert.equal(card.style.top,'8px');
  assert.equal(card.style.height,undefined);
  assert.equal(card.style.maxHeight,undefined);
  assert.ok(parseFloat(card.style.left)+320<=900-8,'horizontal bounds still apply');
});

test('seed buttons adjust by exactly one and restart at step zero', async () => {
  const {run,element}=browser();
  await run('advance()');
  element('seed-increment').onclick();
  assert.equal(element('seed').value,'13');
  assert.equal(run('points[0].n'),13n);
  assert.equal(run('points.length'),1);
  assert.equal(run('playing'),true);
  element('seed-decrement').onclick();
  assert.equal(run('points[0].n'),12n);
  element('seed').value='9007199254740993';
  element('seed-increment').onclick();
  assert.equal(element('seed').value,'9007199254740994');
  assert.equal(run('points[0].n'),9007199254740994n);
  element('seed-decrement').onclick();
  assert.equal(run('points[0].n'),9007199254740993n);
  const stale=run('aliquot(999999999999989n,token)');
  element('seed-increment').onclick();
  await assert.rejects(stale,/cancelled/);
});

test('seed adjustments respect zero, invalid input, and the digit budget', () => {
  const {run,element}=browser();
  element('seed').value='0';run('reset()');
  assert.equal(element('seed-decrement').disabled,true);
  const token=run('token');
  element('seed-decrement').onclick();
  assert.equal(run('token'),token,'decrementing zero does not reset or create a negative seed');
  element('seed-increment').onclick();
  assert.equal(run('points[0].n'),1n);
  assert.equal(element('seed-decrement').disabled,false);
  element('seed').value='9'.repeat(1000);element('seed').oninput();
  assert.equal(element('seed-increment').disabled,true);
  element('seed-increment').onclick();
  assert.equal(run('points[0].n'),1n);
  assert.match(element('note').textContent,/resource budget/);
  for(const invalid of ['-1','1.5','bad','1'.repeat(1001)]){
    element('seed').value=invalid;element('seed').oninput();
    assert.equal(element('seed-increment').disabled,true);
    assert.equal(element('seed-decrement').disabled,true);
    element('seed-increment').onclick();
    assert.equal(run('points[0].n'),1n);
  }
  element('seed').value='0002';element('seed').oninput();
  assert.equal(element('seed-decrement').disabled,false);
  element('seed-decrement').onclick();
  assert.equal(element('seed').value,'1');
});

test('top shortcuts select their seed and preserve the 100-step autoplay checkpoints', async () => {
  const {run,element,presets}=browser();
  for(const preset of presets){
    preset.onclick();
    assert.equal(element('seed').value,preset.dataset.n);
    assert.equal(run('points[0].n'),BigInt(preset.dataset.n));
    assert.equal(run('points[0].k'),0);
  }
  presets.find(preset=>preset.dataset.n==='28').onclick();
  element('speed').value='20';element('speed').oninput();
  for(let i=0;i<100;i++)await run('animation=null; advance()');
  assert.equal(run('points[points.length-1].k'),100);
  assert.equal(run('playing'),false);
});

test('expanded speed range is monotonic with a twice-as-fast target maximum', async () => {
  const {run,element}=browser();
  let previous=Infinity;
  for(let speed=1;speed<=20;speed++){
    element('speed').value=String(speed);element('speed').oninput();
    const interval=run('stepInterval()');
    assert.ok(interval<previous);
    assert.ok(run('duration()')>0);
    previous=interval;
  }
  assert.equal(run('duration()+STEP_GAP'),(200+80)/2);
  assert.equal(element('speed-readout').textContent,'7.1/s');
  await run('advance()');
  assert.equal(run('animation.length'),100);
  run('playing=false; draw(animation.start+animation.length+1)');
  assert.ok(Math.abs(run('nextAt-lastFrame')-40)<1e-6);
  element('speed').value='1';element('speed').oninput();
  assert.equal(run('stepInterval()'),2040);
  assert.equal(element('speed-readout').textContent,'0.5/s');
  for(const raw of ['bad','0','21']){
    element('speed').value=raw;
    assert.ok(Number.isFinite(run('duration()'))&&run('duration()')>0);
  }
});

test('educational preset descriptions and selection follow the starting seed', async () => {
  const {run,element,presets}=browser();
  assert.equal(presets.length,10);
  const aspiring=presets.find(preset=>preset.dataset.n==='95');
  aspiring.onclick();
  assert.match(element('preset-info').textContent,/Aspiring: 95 → 25 → 6 → 6/);
  assert.equal(element('preset-info').hidden,false);
  assert.equal(aspiring.attributes['aria-pressed'],'true');
  assert.ok(presets.filter(preset=>preset.attributes['aria-pressed']==='true').length===1);
  assert.equal(aspiring.title,aspiring.dataset.description);
  for(let i=0;i<3;i++)await run('animation=null; advance()');
  assert.match(element('preset-info').textContent,/Aspiring/,'discovery notes must not erase the explanation');
  const unresolved=presets.find(preset=>preset.dataset.n==='276');
  unresolved.onclick();
  assert.match(element('preset-info').textContent,/not known to terminate or cycle/);
  assert.match(element('preset-info').textContent,/not proof of divergence/);
  assert.equal(aspiring.attributes['aria-pressed'],'false');
  element('seed').value='13';run('reset()');
  assert.equal(element('preset-info').hidden,true);
  assert.equal(element('preset-info').textContent,'');
  assert.ok(presets.every(preset=>preset.attributes['aria-pressed']==='false'));
  element('seed').value='95';run('reset()');
  assert.equal(aspiring.attributes['aria-pressed'],'true','manual Set uses the same preset metadata');
});

test('pause uses a two-bar CSS icon with a plain accessible label', () => {
  const {element}=browser();
  assert.equal(element('play').textContent,'Pause');
  assert.equal(element('play').dataset.playing,'true');
  element('play').onclick();
  assert.equal(element('play').textContent,'▶ Play');
  assert.equal(element('play').dataset.playing,'false');
  element('play').onclick();
  assert.equal(element('play').textContent,'Pause');
  assert.equal(element('play').dataset.playing,'true');
  const html=readFileSync(new URL('site/index.html',root),'utf8');
  assert.ok(!html.includes('Ⅱ'));
  const css=readFileSync(new URL('site/site.css',root),'utf8');
  assert.match(css,/#play\[data-playing=true\]::before\{[^}]*border-left:3px solid currentColor;[^}]*border-right:3px solid currentColor/);
});

test('site has q5m research chrome, accessible controls, and matching icons', () => {
  const html = readFileSync(new URL('site/index.html', root), 'utf8');
  for (const marker of ['aliquot<span>.q5m.ai', 'https://www.q5m.ai', 'https://github.com/q5m-ai/aliquot', 'not a proof', 'aria-label="Main navigation"', 'role="status"', 'aria-describedby="point-help"', 'aria-labelledby="point-title"', 'id="point-details"', 'tabindex="0"']) assert.ok(html.includes(marker), marker);
  assert.equal(readFileSync(new URL('favicon.svg', root), 'utf8'), readFileSync(new URL('site/favicon.svg', root), 'utf8'));
});
