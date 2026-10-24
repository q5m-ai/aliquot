'use strict';
(() => {
  const $ = id => document.getElementById(id);
  const svg = $('graph'), world = $('graph-world'), card = $('point-details');
  const session = AliquotOrbitSession.create(AliquotOrbitData);
  let model = session.model, layout;
  const windowView = AliquotOrbitGraph.createWindow(model), actionHistory = [];
  let visible = windowView.ids;
  const nodeElements = new Map(), edgeElements = new Map(), pointers = new Map(), manualPositions = new Map();
  const revealed = new Set();
  let selected = null, hovered = null, detailsHidden = false, camera, width = svg.clientWidth, height = svg.clientHeight;
  let anchor = null, dragged = false, tapNode = null, dragNode = null, job = null;
  const fmt = id => BigInt(id).toLocaleString('en-CA');
  const svgElement = (tag, attrs, text) => {
    const element = document.createElementNS('http://www.w3.org/2000/svg', tag);
    for (const [key, value] of Object.entries(attrs)) element.setAttribute(key, String(value));
    if (text !== undefined) element.textContent = text;
    return element;
  };
  function edgeCurve(source) {
    const target = model.nodes.get(source).next;
    return AliquotOrbitGraph.curve(layout.positions.get(source), layout.positions.get(target), source === target);
  }
  function drawNode(node) {
    const position = layout.positions.get(node.id);
    const type = node.id === '0' || node.id === '1' ? 'terminal' : node.next === node.id ? 'perfect' : node.prime ? 'prime' : node.unresolved ? 'unresolved' : 'composite';
    const element = svgElement('g', {class: `graph-node ${type}`, 'data-node': node.id,
      transform: `translate(${position.x} ${position.y})`, tabindex: 0, role: 'button', 'aria-pressed': 'false',
      'aria-label': `${fmt(node.id)}, ${type}${node.untouchable ? ', proved no predecessor' : node.leaf ? ', leaf in the loaded graph' : ''}${node.next !== null && !visible.has(node.next) ? ', known continuation outside window' : ''}. Inspect and trace forward.`});
    element.append(svgElement('circle', {r: Math.max(11, position.r + 4), class: 'node-hit'}));
    if (node.untouchable) element.append(svgElement('circle', {r: position.r + 4, class: 'node-ring'}));
    element.append(svgElement('circle', {r: position.r, class: 'node-core'}));
    element.append(svgElement('text', {x: position.r + 5, y: 4,
      'text-anchor': 'start', class: 'node-label'}, AliquotOrbitGraph.label(node.id)));
    if (node.next !== null && !visible.has(node.next)) {
      element.append(svgElement('text', {x: position.r + 5, y: 18, class: 'node-more', 'aria-hidden': 'true'}, '→ …'));
    }
    element.addEventListener('pointerenter', event => {
      if (event.pointerType !== 'touch' && !pointers.size && !selected) { hovered = node.id; inspect(); }
    });
    element.addEventListener('pointerleave', () => { if (!selected && !pointers.size) { hovered = null; inspect(); } });
    element.addEventListener('focus', () => { if (!selected && !pointers.size && element.matches(':focus-visible')) { hovered = node.id; center(node.id, false); inspect(); } });
    element.addEventListener('blur', () => { if (!selected) { hovered = null; inspect(); } });
    element.addEventListener('keydown', event => {
      if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); event.stopPropagation(); choose(node.id, true); }
    });
    // Assistive technologies can synthesize a click without pointer events.
    element.addEventListener('click', event => { if (event.detail === 0) choose(node.id, true); });
    nodeElements.set(node.id, element);
    $('graph-nodes').append(element);
  }
  function rebuild({arrange = false, focus = null, overview = false} = {}) {
    model = session.model; visible = windowView.ids;
    if (!visible.has(selected)) selected = null;
    hovered = null;
    if (arrange) manualPositions.clear();
    layout = AliquotOrbitGraph.layout(model, {visible});
    for (const [id, position] of manualPositions) {
      if (layout.positions.has(id)) Object.assign(layout.positions.get(id), position);
      else if (!model.nodes.has(id)) manualPositions.delete(id);
    }
    nodeElements.clear(); edgeElements.clear();
    $('graph-bands').replaceChildren(); $('graph-edges').replaceChildren(); $('graph-nodes').replaceChildren();
    for (const band of layout.bands) $('graph-bands').append(svgElement('text', {x: 22, y: band.top + 15, class: 'graph-band'}, band.label));
    for (const edge of model.data.edges) {
      if (!visible.has(edge.from) || !visible.has(edge.to)) continue;
      const element = svgElement('path', {class: 'graph-edge', 'data-source': edge.from, d: edgeCurve(edge.from), 'marker-end': 'url(#arrow)'});
      edgeElements.set(edge.from, element); $('graph-edges').append(element);
    }
    for (const id of visible) drawNode(model.nodes.get(id));
    svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
    $('graph-summary').textContent = `${visible.size}/${windowView.limits.maxNodes} nodes in window · ${edgeElements.size} arrows shown · ${fmt(model.nodes.size)} values available from ${fmt(model.data.orbits.length)} starts · ${[...visible].filter(id => model.nodes.get(id).untouchable).length} proved no-predecessor nodes shown`;
    fit();
    if (focus !== null && visible.has(focus)) center(focus, true);
    else if (overview && camera.scale < .75 && visible.has('12')) center('12', true);
    inspect();
  }
  function bounds() {
    const points = [...layout.positions.values()];
    const left = Math.min(0, ...points.map(p => p.x - 45)), top = Math.min(0, ...points.map(p => p.y - 45));
    return {left, top, width: Math.max(layout.width, ...points.map(p => p.x + 100)) - left,
      height: Math.max(layout.height, ...points.map(p => p.y + 55)) - top};
  }
  function paintCard() {
    const id = selected ?? hovered;
    card.hidden = id === null || dragged || detailsHidden;
    if (card.hidden) return;
    const position = layout.positions.get(id);
    const x = camera.x + position.x * camera.scale, y = camera.y + position.y * camera.scale;
    const boxWidth = card.offsetWidth;
    let left = x + 18;
    if (left + boxWidth + 8 > width) left = x - boxWidth - 18;
    card.style.left = `${Math.max(8, Math.min(width - boxWidth - 8, left))}px`;
    card.style.top = `${Math.max(8, Math.min(height - card.offsetHeight - 8, y + 18))}px`;
  }
  function paintCamera() {
    world.setAttribute('transform', `translate(${camera.x} ${camera.y}) scale(${camera.scale})`);
    paintCard();
  }
  function needsForwardReveal(trace) {
    // A long orbit can exceed the display cap. Once its actual computation
    // frontier is visible, older hidden terms must not block further work.
    return trace.path.some(id => !visible.has(id)) && !(trace.status === 'unresolved' && visible.has(trace.path.at(-1)));
  }
  function inspect() {
    const id = selected ?? hovered, trace = id === null ? null : model.trace(id);
    const active = new Set(trace?.path ?? []);
    if (selected) for (const source of revealed) if (model.nodes.has(source)) {
      for (const value of model.trace(source).path) active.add(value);
    }
    world.classList.toggle('has-trace', id !== null);
    for (const [value, element] of nodeElements) {
      element.classList.toggle('active', active.has(value));
      element.classList.toggle('selected', value === selected);
      element.setAttribute('aria-pressed', String(value === selected));
    }
    for (const [source, element] of edgeElements) {
      const on = active.has(source);
      element.classList.toggle('active', on);
      element.setAttribute('marker-end', on ? 'url(#arrow-active)' : 'url(#arrow)');
    }
    $('clear-trace').disabled = false;
    $('undo').disabled = actionHistory.length === 0;
    $('find-button').disabled = job !== null;
    $('stop-work').hidden = job === null;
    svg.setAttribute('aria-busy', String(job !== null));
    const hiddenForward = trace ? [...new Set(trace.path)].filter(value => !visible.has(value)).length : 0;
    const overview = `Showing a rolling window, not the entire graph. Explore any start or expand a node; older branches leave the window, not the loaded data. ${model.data.complete_orbits ? 'Every included starting orbit is resolved.' : 'Some loaded orbits have unresolved computation frontiers.'}`;
    $('route-status').textContent = trace
      ? `${trace.path.slice(0, 32).map(AliquotOrbitGraph.label).join(' → ')}${trace.path.length > 32 ? ` → … (${trace.path.length - 32} further terms retained)` : ''} · ${trace.status === 'cycle' ? 'cycle repeats' : trace.status === 'terminated' ? 'terminated' : 'unresolved within limits'}${hiddenForward ? ` · ${hiddenForward} known terms outside window (not a computation limit)` : ''}${revealed.size ? ' · incoming branches highlighted' : ''}` : overview;
    if (id !== null) {
      const node = model.nodes.get(id), details = model.info(id, visible);
      const knownSum = node.sum ?? node.next;
      const basic = AliquotPointInfo.basic(BigInt(id), knownSum === null ? undefined : BigInt(knownSum));
      if (node.prime) basic.status = 'Prime · deficient';
      if (node.unresolved) basic.status = knownSum === null ? `Unresolved · ${node.unresolved}` : `${basic.status} · ${node.unresolved}`;
      const divisorInfo = AliquotPointInfo.divisors(BigInt(id), node.factors?.map(f => ({prime: BigInt(f.prime), exponent: f.exponent})));
      for (const [key, value] of Object.entries({...basic, ...divisorInfo, ...details})) {
        const element = $(`point-${key}`);
        if (element && key !== 'factorization') element.textContent = value;
      }
      PageLatex.render($('point-factorization'), divisorInfo.factorizationTex, {fallback: divisorInfo.factorization});
      card.dataset.pinned = String(selected !== null);
      $('point-mode').textContent = selected !== null ? 'Pinned · orbit' : 'Click to pin';
      $('point-reverse').href = `/reverse/?n=${id}`;
      const allShown = node.predecessors.status === 'complete' && node.predecessors.values.every(source => visible.has(source) && model.nodes.get(source)?.next === id);
      $('point-expand').disabled = job !== null || allShown;
      $('point-expand').textContent = node.untouchable ? 'No predecessors · proved' : allShown ? 'All predecessors shown'
        : node.incoming.some(source => !visible.has(source)) ? 'Show / add predecessors' : 'Add predecessors';
      const showForward = needsForwardReveal(trace);
      $('point-forward').disabled = job !== null || (!showForward && trace.status !== 'unresolved');
      $('point-forward').textContent = showForward ? 'Show next +16' : trace.status === 'unresolved' ? 'Extend forward +64' : 'Forward complete';
      $('point-compute').hidden = !divisorInfo.canCompute;
      $('point-compute').disabled = job !== null;
    } else {
      $('point-expand').disabled = $('point-forward').disabled = true;
    }
    paintCard();
  }
  function cancelJob(message = 'Stopped; the unfinished graph action was discarded.') {
    if (!job) return;
    job.cancelled = true; job = null;
    $('input-status').textContent = message;
    inspect();
  }
  function checkpoint() { return {data: session.data, view: windowView.save(), selected, detailsHidden}; }
  function remember(before) {
    const ids = windowView.ids;
    if (before.data === session.data && before.view.visible.length === ids.size && before.view.visible.every(id => ids.has(id))) return;
    actionHistory.push({view: before.view, selected: before.selected, detailsHidden: before.detailsHidden, math: before.data !== session.data});
    if (actionHistory.length > session.limits.history) actionHistory.shift();
  }
  function choose(id, keyboard = false) {
    if (!model.nodes.has(id)) return;
    cancelJob(); revealed.clear();
    const before = checkpoint();
    selected = selected === id && !detailsHidden ? null : id;
    hovered = null; detailsHidden = false;
    if (selected) {
      $('find-node').value = selected;
      const added = windowView.forward(model, selected, true);
      remember(before);
      if (added.length) {
        rebuild({focus: selected});
        if (keyboard) nodeElements.get(selected).focus({preventScroll: true});
        return;
      }
    }
    inspect();
  }
  function clear() { cancelJob(); revealed.clear(); selected = hovered = null; detailsHidden = false; inspect(); }
  function fit() { camera = AliquotOrbitGraph.fit(width, height, bounds()); paintCamera(); }
  function center(id, force) {
    const p = layout.positions.get(id), x = camera.x + p.x * camera.scale, y = camera.y + p.y * camera.scale;
    if (force || camera.scale < .75 || x < 25 || x > width - 25 || y < 25 || y > height - 25) {
      camera = {scale: Math.max(camera.scale, 1), x: 0, y: 0};
      camera.x = width / 2 - p.x * camera.scale;
      camera.y = height / 2 - p.y * camera.scale;
      paintCamera();
    }
  }
  function resize() {
    if (width === svg.clientWidth && height === svg.clientHeight) return;
    cancelJob('Stopped because the graph view changed; unfinished changes discarded.');
    width = svg.clientWidth; height = svg.clientHeight;
    svg.setAttribute('viewBox', `0 0 ${width} ${height}`); fit();
    if (selected) center(selected, true);
    else if (camera.scale < .75 && visible.has('12')) center('12', true);
  }
  function zoom(factor, point = {x: width / 2, y: height / 2}) {
    camera = AliquotOrbitGraph.zoom(camera, factor, point, Math.min(.1, AliquotOrbitGraph.fit(width, height, bounds()).scale / 2));
    hovered = null; inspect(); paintCamera();
  }
  function forward() {
    if (job || selected === null) return;
    if (needsForwardReveal(model.trace(selected))) {
      const before = checkpoint(), added = windowView.forward(model, selected);
      remember(before); detailsHidden = false;
      $('input-status').textContent = `Revealed ${added.length} known forward terms. The ${windowView.limits.maxNodes}-node window rolls forward; hidden terms remain in the full graph.`;
      rebuild({focus: added.at(-1) ?? selected});
    } else return act('extend', selected);
  }
  async function act(kind, id) {
    if (job || id === null) return;
    const before = checkpoint(), task = {cancelled: false};
    job = task; inspect();
    $('input-status').textContent = kind === 'expand' ? 'Finding exact predecessors…' : kind === 'divisors' ? 'Computing exact divisors…' : 'Extending the orbit…';
    try {
      const options = {cancelled: () => task.cancelled, onProgress: text => { if (job === task) $('input-status').textContent = text; }};
      if (kind === 'expand') {
        const text = $('source-bound').value.trim();
        if (!/^\d{1,7}$/.test(text)) throw new Error('Source bound must be an integer from 1 to 1,000,000.');
        options.bound = Number(text);
      }
      const result = await session[kind](id, options);
      if (job !== task) return;
      job = null; revealed.clear(); selected = id; hovered = null;
      $('find-node').value = id;
      detailsHidden = kind === 'expand';
      model = session.model;
      let focus = id;
      if (kind === 'expand') {
        for (const source of windowView.incoming(model, id, result.revealed)) revealed.add(source);
        const coverage = result.complete ? 'Complete predecessor set' : result.infinite
          ? `Infinite predecessor set; finite scan through ${fmt(result.checked)} is partial`
          : `Partial search through ${fmt(result.checked)}; larger sources remain unchecked`;
        $('input-status').textContent = `Added ${result.edges} predecessor arrow${result.edges === 1 ? '' : 's'} to the full graph (${result.added.length} new nodes); revealed ${revealed.size} incoming branches at ${fmt(id)}. ${coverage}. ${result.remaining ? `${result.remaining.toLocaleString('en-CA')} found predecessors are not in the loaded graph yet; add another batch.` : 'All matches from this search are in the loaded graph.'} The window shows at most ${windowView.limits.maxNodes} nodes; other branches remain available.${result.limited ? ' Full graph node limit reached; undo or reset to make room.' : ''}`;
      } else if (kind === 'extend') {
        const added = windowView.forward(model, id, !visible.has(id));
        if (visible.has(id)) focus = added.at(-1) ?? id;
        $('input-status').textContent = `Added ${result.added.length} nodes and ${result.edges} exact arrows to the full graph. ${result.status === 'unresolved' ? `Unresolved frontier: ${result.reason}. Extend explicitly to try further.` : result.status === 'cycle' ? 'A repeated value closes a cycle.' : 'This orbit terminates at 0.'} Show next reveals cached terms in batches of 16.`;
      } else $('input-status').textContent = `Exact divisors of ${fmt(id)} computed; the graph edges are unchanged.`;
      remember(before);
      rebuild({focus});
    } catch (error) {
      if (job === task) $('input-status').textContent = error.message === 'cancelled' ? 'Stopped; unfinished changes discarded.' : error.message;
    } finally {
      if (job === task) job = null;
      inspect();
    }
  }
  async function find(raw) {
    let id;
    try { id = session.parse(raw); } catch (error) { $('input-status').textContent = error.message; return; }
    cancelJob(); revealed.clear();
    if (!model.nodes.has(id)) return act('extend', id);
    const before = checkpoint();
    selected = id; hovered = null; detailsHidden = false;
    windowView.forward(model, id, true); remember(before);
    $('find-node').value = id; $('input-status').textContent = '';
    rebuild({focus: id});
  }
  $('find-form').addEventListener('submit', event => { event.preventDefault(); return find($('find-node').value); });
  $('point-expand').addEventListener('click', () => act('expand', selected));
  $('point-forward').addEventListener('click', forward);
  $('point-compute').addEventListener('click', () => act('divisors', selected));
  $('stop-work').addEventListener('click', () => cancelJob());
  $('undo').addEventListener('click', () => {
    cancelJob(); revealed.clear();
    const previous = actionHistory.pop();
    if (previous) {
      if (previous.math) session.undo();
      windowView.restore(previous.view, session.model);
      selected = previous.selected; detailsHidden = previous.detailsHidden;
      rebuild(); $('input-status').textContent = 'Undid the last graph/window action.';
    }
  });
  $('reset-graph').addEventListener('click', () => {
    cancelJob(); session.reset(); actionHistory.length = 0; revealed.clear(); selected = hovered = null; detailsHidden = false;
    windowView.reset(session.model);
    $('find-node').value = '12'; rebuild({arrange: true, overview: true});
    $('input-status').textContent = `Reset to the original starts 1–${fmt(session.data.initial_limits.seed_max)} and the small starting window.`;
  });
  $('arrange').addEventListener('click', () => { cancelJob(); rebuild({arrange: true}); });
  $('clear-trace').addEventListener('click', () => {
    const before = checkpoint(); clear(); windowView.reset(model); remember(before); rebuild({arrange: true, overview: true});
    $('input-status').textContent = 'Small overview restored. All loaded values and completed computations are still available.';
  });
  $('point-close').addEventListener('click', () => { detailsHidden = true; paintCard(); });
  $('fit').addEventListener('click', fit);
  $('zoom-in').addEventListener('click', () => zoom(1.4));
  $('zoom-out').addEventListener('click', () => zoom(1 / 1.4));
  const local = event => { const box = svg.getBoundingClientRect(); return {x: event.clientX - box.left, y: event.clientY - box.top}; };
  svg.addEventListener('wheel', event => { event.preventDefault(); zoom(Math.exp(-Math.max(-200, Math.min(200, event.deltaY)) * .005), local(event)); }, {passive: false});
  function snapshot() {
    anchor = {camera: {...camera}, points: [...pointers.values()].map(p => ({...p})),
      node: dragNode === null ? null : {...layout.positions.get(dragNode)}};
  }
  function moveNode(id, x, y) {
    const p = layout.positions.get(id); p.x = x; p.y = y;
    manualPositions.set(id, {x, y});
    nodeElements.get(id).setAttribute('transform', `translate(${x} ${y})`);
    for (const source of new Set([id, ...model.nodes.get(id).incoming])) {
      if (edgeElements.has(source)) edgeElements.get(source).setAttribute('d', edgeCurve(source));
    }
  }
  svg.addEventListener('pointerdown', event => {
    if (event.button !== 0) return;
    cancelJob();
    if (!pointers.size) {
      dragged = false;
      tapNode = event.target.closest('[data-node]')?.getAttribute('data-node') ?? null;
      dragNode = event.shiftKey ? null : tapNode;
    } else { dragged = true; tapNode = dragNode = null; }
    pointers.set(event.pointerId, local(event));
    svg.setPointerCapture(event.pointerId);
    snapshot();
  });
  svg.addEventListener('pointermove', event => {
    if (!pointers.has(event.pointerId)) return;
    pointers.set(event.pointerId, local(event));
    const current = [...pointers.values()], initial = anchor.points;
    if (current.length === 1) {
      const dx = current[0].x - initial[0].x, dy = current[0].y - initial[0].y;
      if (Math.hypot(dx, dy) > 4) dragged = true;
      if (dragged && dragNode !== null) moveNode(dragNode, anchor.node.x + dx / anchor.camera.scale, anchor.node.y + dy / anchor.camera.scale);
      else if (dragged) camera = {...anchor.camera, x: anchor.camera.x + dx, y: anchor.camera.y + dy};
    } else {
      const middle = points => ({x: (points[0].x + points[1].x) / 2, y: (points[0].y + points[1].y) / 2});
      const distance = points => Math.hypot(points[0].x - points[1].x, points[0].y - points[1].y);
      const before = middle(initial), after = middle(current);
      camera = AliquotOrbitGraph.zoom(anchor.camera, distance(current) / Math.max(1, distance(initial)), before);
      camera.x += after.x - before.x; camera.y += after.y - before.y;
    }
    svg.classList.toggle('dragging', dragged);
    if (dragged) { hovered = null; paintCamera(); }
  });
  function release(event, cancelled) {
    if (!pointers.has(event.pointerId)) return;
    pointers.delete(event.pointerId);
    if (pointers.size) { dragged = true; snapshot(); return; }
    const isTap = !dragged && !cancelled;
    dragged = false; anchor = null;
    svg.classList.remove('dragging');
    if (isTap) { if (tapNode !== null) choose(tapNode); else clear(); }
    else inspect();
    tapNode = dragNode = null;
  }
  svg.addEventListener('pointerup', event => release(event, false));
  svg.addEventListener('pointercancel', event => release(event, true));
  svg.addEventListener('lostpointercapture', event => release(event, true));
  $('chart').addEventListener('keydown', event => {
    if (event.key === 'Escape') { event.preventDefault(); clear(); }
  });
  svg.addEventListener('keydown', event => {
    if (event.key === '+' || event.key === '=') { event.preventDefault(); zoom(1.4); }
    else if (event.key === '-') { event.preventDefault(); zoom(1 / 1.4); }
    else if (event.key === '0' || event.key === 'Home') { event.preventDefault(); fit(); }
    else if (event.target === svg && ['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(event.key)) {
      event.preventDefault();
      camera.x += event.key === 'ArrowLeft' ? 60 : event.key === 'ArrowRight' ? -60 : 0;
      camera.y += event.key === 'ArrowUp' ? 60 : event.key === 'ArrowDown' ? -60 : 0;
      paintCamera();
    }
  });
  $('download').addEventListener('click', () => {
    const content = {...model.data, selection: selected === null ? null : {start: selected, ...model.trace(selected)},
      window: {limits: windowView.limits, visible: [...visible]}};
    const url = URL.createObjectURL(new Blob([JSON.stringify(content, null, 2)], {type: 'application/json'}));
    const link = document.createElement('a');
    link.href = url; link.download = 'aliquot-orbit-graph.json';
    document.body.append(link); link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
  rebuild({overview: true});
  new ResizeObserver(resize).observe(svg);
  const initial = new URLSearchParams(location.search).get('n');
  if (initial !== null) find(initial);
})();
