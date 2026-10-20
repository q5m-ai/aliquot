import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import { readFileSync } from 'node:fs';

const root = new URL('../', import.meta.url);
const source = readFileSync(new URL('site/math.js', root), 'utf8') + '\n' +
  readFileSync(new URL('site/explorer.js', root), 'utf8');
function browser({dpr=1}={}) {
  const elements = new Map();
  const labels = [], frames = [];
  const context2d = new Proxy({}, { get: (_, name) => (...args) => {
    for (const arg of args) if (typeof arg === 'number') assert.ok(Number.isFinite(arg), `non-finite canvas argument in ${String(name)}`);
    if (name === 'fillText') labels.push(args[0]);
  }, set: () => true });
  const element = id => {
    if (!elements.has(id)) elements.set(id, {
      value: id === 'seed' ? '12' : id === 'scale' ? 'log' : '5',
      textContent: '', className: '', width: 0, height: 0, hidden:false, style:{},
      focus() { this.focused=true; },
      getContext: () => context2d,
      getBoundingClientRect: () => ({ left:40, top:60, width: 900, height: 400 }),
    });
    return elements.get(id);
  };
  const context = vm.createContext({
    document: { getElementById: element, querySelectorAll: () => [] },
    window: { devicePixelRatio: dpr, addEventListener() {} },
    requestAnimationFrame(callback) { frames.push(callback); return frames.length; }, performance, setTimeout,
  });
  vm.runInContext(source, context);
  return { element, labels, run: code => vm.runInContext(code, context),
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
  assert.match(element('point-change').textContent,/\+4 · increased/);
  assert.equal(element('point-next').textContent,'Not computed yet');
  assert.match(element('point-status').textContent,/not computed/);
  assert.match(element('point-size').textContent,/2 decimal digits · even/);
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
  assert.match(run('pointDetails(points[0]).residue'),/^0$/);
  element('seed').value='6';run('reset()');
  assert.match(run('pointDetails(points[0]).residue'),/driver-six/);
  await run('advance()');
  assert.match(run('pointDetails(points[0]).status'),/Perfect/);
  assert.match(run('pointDetails(points[1]).status'),/period 1/);
  element('seed').value='220';run('reset()');
  for(let i=0;i<2;i++)await run('animation=null; advance()');
  assert.match(run('pointDetails(points[2]).status'),/Repeats step 0; cycle period 2/);
  for(let i=0;i<2;i++)await run('animation=null; advance()');
  assert.match(run('pointDetails(points[4]).status'),/Repeats step 0; cycle period 2/);
  element('seed').value='1';run('reset()');
  assert.equal(run('pointDetails(points[0]).next'),'0');
  assert.match(run('pointDetails(points[0]).status'),/Terminal/);
  await run('advance()');
  assert.match(run('pointDetails(points[1]).status'),/s\(0\) is undefined/);
  assert.match(run('pointDetails(points[1]).next'),/not s\(0\)/);
});

test('hundreds-digit point details preserve the exact integer without factoring', () => {
  const {run,element}=browser();
  element('seed').value=String(2n**2000n);run('reset(); playing=false; draw(performance.now())');
  element('graph').onpointermove(pointEvent(run));
  assert.equal(element('point-value').textContent,(2n**2000n).toLocaleString('en-CA'));
  assert.match(element('point-size').textContent,/603 decimal digits/);
  assert.match(element('point-previous').textContent,/Starting value/);
});

test('autoplay pauses at each 100-step boundary and requires explicit resume', async () => {
  const {run,element,frame,pendingFrames}=browser();
  for(let checkpoint=100;checkpoint<=300;checkpoint+=100){
    for(let k=checkpoint-99;k<=checkpoint;k++)await run('animation=null; advance()');
    assert.equal(run('points[points.length-1].k'),checkpoint);
    assert.equal(run('playing'),false);
    assert.equal(element('play').textContent,'▶ Resume');
    assert.match(element('note').textContent,new RegExp(`paused at step ${checkpoint}`));
    frame(1e9*checkpoint);
    assert.equal(pendingFrames(),0,'paused chart must not keep scheduling idle animation frames');
    assert.equal(run('points[points.length-1].k'),checkpoint,'finishing animation must not compute another term');
    element('play').onclick();
    assert.equal(run('playing'),true);
    assert.equal(element('play').textContent,'Ⅱ Pause');
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

test('site has q5m research chrome, accessible controls, and matching icons', () => {
  const html = readFileSync(new URL('site/index.html', root), 'utf8');
  for (const marker of ['aliquot<span>.q5m.ai', 'https://www.q5m.ai', 'https://github.com/q5m-ai/aliquot', 'not a proof', 'aria-label="Main navigation"', 'role="status"', 'aria-describedby="point-help"', 'aria-labelledby="point-title"', 'id="point-details"', 'tabindex="0"']) assert.ok(html.includes(marker), marker);
  assert.equal(readFileSync(new URL('favicon.svg', root), 'utf8'), readFileSync(new URL('site/favicon.svg', root), 'utf8'));
});
