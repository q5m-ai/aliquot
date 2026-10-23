'use strict';
(() => {
  const $ = id => document.getElementById(id);
  const svg = $('graph'), world = $('graph-world'), card = $('point-details');
  const model = AliquotOrbitGraph.create(AliquotOrbitData);
  let layout = AliquotOrbitGraph.layout(model, {vertical: svg.clientWidth < 760});
  const nodeElements = new Map(), edgeElements = new Map(), pointers = new Map();
  let selected = null, hovered = null, detailsHidden = false, camera, width = 1, height = 1;
  let anchor = null, dragged = false, tapNode = null;
  const fmt = id => BigInt(id).toLocaleString('en-CA');
  const svgElement = (tag, attrs, text) => {
    const element = document.createElementNS('http://www.w3.org/2000/svg', tag);
    for (const [key, value] of Object.entries(attrs)) element.setAttribute(key, String(value));
    if (text !== undefined) element.textContent = text;
    return element;
  };
  for (const band of layout.bands) {
    $('graph-bands').append(svgElement('text', {x: 22, y: band.top + 15, class: 'graph-band'}, band.label));
  }
  for (const edge of model.data.edges) {
    const element = svgElement('path', {class: 'graph-edge', 'data-source': edge.from,
      d: AliquotOrbitGraph.curve(layout.positions.get(edge.from), layout.positions.get(edge.to), edge.from === edge.to, layout.vertical),
      'marker-end': 'url(#arrow)'});
    edgeElements.set(edge.from, element);
    $('graph-edges').append(element);
  }
  for (const node of model.nodes.values()) {
    const position = layout.positions.get(node.id);
    const type = node.id === '0' || node.id === '1' ? 'terminal' : node.next === node.id ? 'perfect' : node.prime ? 'prime' : node.unresolved ? 'unresolved' : 'composite';
    const element = svgElement('g', {class: `graph-node ${type}`, 'data-node': node.id,
      transform: `translate(${position.x} ${position.y})`, tabindex: 0, role: 'button', 'aria-pressed': 'false',
      'aria-label': `${fmt(node.id)}, ${type}${node.untouchable ? ', proved no predecessor' : node.leaf ? ', leaf in this graph only' : ''}. Inspect and trace forward.`});
    element.append(svgElement('circle', {r: Math.max(11, position.r + 4), class: 'node-hit'}));
    if (node.untouchable) element.append(svgElement('circle', {r: position.r + 4, class: 'node-ring'}));
    element.append(svgElement('circle', {r: position.r, class: 'node-core'}));
    element.append(svgElement('text', {x: layout.vertical ? 0 : position.r + 5, y: layout.vertical ? position.r + 16 : 4,
      'text-anchor': layout.vertical ? 'middle' : 'start', class: 'node-label'}, fmt(node.id)));
    element.addEventListener('pointerenter', event => {
      if (event.pointerType !== 'touch' && !pointers.size && !selected) { hovered = node.id; inspect(); }
    });
    element.addEventListener('pointerleave', () => { if (!selected && !pointers.size) { hovered = null; inspect(); } });
    element.addEventListener('focus', () => { if (!selected && !pointers.size && element.matches(':focus-visible')) { hovered = node.id; center(node.id, false); inspect(); } });
    element.addEventListener('blur', () => { if (!selected) { hovered = null; inspect(); } });
    element.addEventListener('keydown', event => {
      if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); event.stopPropagation(); choose(node.id); }
    });
    // Assistive technologies can synthesize a click without pointer events.
    element.addEventListener('click', event => { if (event.detail === 0) choose(node.id); });
    nodeElements.set(node.id, element);
    $('graph-nodes').append(element);
  }
  $('graph-summary').textContent = `${model.data.orbits.length} starts · ${model.nodes.size} values · ${model.data.edges.length} arrows · ${model.data.nodes.filter(n => n.leaf).length} leaves in this graph · ${model.data.nodes.filter(n => n.untouchable).length} proved no-predecessor nodes`;
  const overview = model.data.complete_orbits
    ? 'Every starting orbit is resolved. The arrows at 6 and 28 are self-loops; 0 has no outgoing edge.'
    : 'Some starting orbits are unresolved within the stated limits. Missing edges do not prove termination.';
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
  function inspect() {
    const id = selected ?? hovered, trace = id === null ? null : model.trace(id);
    const active = new Set(trace?.path ?? []);
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
    $('clear-trace').disabled = id === null;
    $('route-status').textContent = trace
      ? `${trace.path.map(fmt).join(' → ')} · ${trace.status === 'cycle' ? 'cycle repeats' : trace.status === 'terminated' ? 'terminated' : 'unresolved within limits'}` : overview;
    if (id !== null) {
      const node = model.nodes.get(id), details = model.info(id);
      const basic = AliquotPointInfo.basic(BigInt(id), node.next === null ? undefined : BigInt(node.next));
      if (node.prime) basic.status = 'Prime · deficient';
      if (node.unresolved) basic.status = `Unresolved · ${node.unresolved}`;
      const divisorInfo = AliquotPointInfo.divisors(BigInt(id), node.factors?.map(f => ({prime: BigInt(f.prime), exponent: f.exponent})));
      for (const [key, value] of Object.entries({...basic, ...divisorInfo, ...details})) {
        const element = $(`point-${key}`);
        if (element && key !== 'factorization') element.textContent = value;
      }
      PageLatex.render($('point-factorization'), divisorInfo.factorizationTex, {fallback: divisorInfo.factorization});
      card.dataset.pinned = String(selected !== null);
      $('point-mode').textContent = selected !== null ? 'Pinned · orbit' : 'Click to pin';
      $('point-reverse').href = `/reverse/?n=${id}`;
    }
    paintCard();
  }
  function choose(id) {
    selected = selected === id && !detailsHidden ? null : id;
    hovered = null; detailsHidden = false;
    if (selected) $('find-node').value = selected;
    $('input-status').textContent = '';
    inspect();
  }
  function clear() { selected = hovered = null; detailsHidden = false; inspect(); }
  function fit() { camera = AliquotOrbitGraph.fit(width, height, layout); paintCamera(); }
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
    width = svg.clientWidth; height = svg.clientHeight;
    if (layout.vertical !== (width < 760)) {
      layout = AliquotOrbitGraph.layout(model, {vertical: width < 760});
      for (const [id, element] of nodeElements) {
        const p = layout.positions.get(id), label = element.lastElementChild;
        element.setAttribute('transform', `translate(${p.x} ${p.y})`);
        label.setAttribute('x', layout.vertical ? 0 : p.r + 5);
        label.setAttribute('y', layout.vertical ? p.r + 16 : 4);
        label.setAttribute('text-anchor', layout.vertical ? 'middle' : 'start');
      }
      for (const edge of model.data.edges) {
        edgeElements.get(edge.from).setAttribute('d', AliquotOrbitGraph.curve(layout.positions.get(edge.from), layout.positions.get(edge.to), edge.from === edge.to, layout.vertical));
      }
      [...$('graph-bands').children].forEach((element, index) => element.setAttribute('y', layout.bands[index].top + 15));
    }
    world.classList.toggle('vertical', layout.vertical);
    svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
    fit();
    if (selected) center(selected, true);
  }
  function zoom(factor, point = {x: width / 2, y: height / 2}) {
    camera = AliquotOrbitGraph.zoom(camera, factor, point, Math.min(.1, AliquotOrbitGraph.fit(width, height, layout).scale / 2));
    hovered = null; inspect(); paintCamera();
  }
  function find(raw) {
    const text = raw.trim();
    if (!/^\d{1,20}$/.test(text)) {
      $('input-status').textContent = 'Enter the integer label of a displayed node.'; return;
    }
    const id = BigInt(text).toString();
    if (!model.nodes.has(id)) { $('input-status').textContent = `${fmt(id)} is not in the graph from starts 1–100.`; return; }
    selected = id; hovered = null; detailsHidden = false;
    $('find-node').value = id; $('input-status').textContent = '';
    center(id, true); inspect();
  }
  $('find-form').addEventListener('submit', event => { event.preventDefault(); find($('find-node').value); });
  $('clear-trace').addEventListener('click', () => { clear(); fit(); });
  $('point-close').addEventListener('click', () => { detailsHidden = true; paintCard(); });
  $('fit').addEventListener('click', fit);
  $('zoom-in').addEventListener('click', () => zoom(1.4));
  $('zoom-out').addEventListener('click', () => zoom(1 / 1.4));
  const local = event => { const box = svg.getBoundingClientRect(); return {x: event.clientX - box.left, y: event.clientY - box.top}; };
  svg.addEventListener('wheel', event => { event.preventDefault(); zoom(Math.exp(-Math.max(-200, Math.min(200, event.deltaY)) * .005), local(event)); }, {passive: false});
  function snapshot() { anchor = {camera: {...camera}, points: [...pointers.values()].map(p => ({...p}))}; }
  svg.addEventListener('pointerdown', event => {
    if (event.button !== 0) return;
    if (!pointers.size) {
      dragged = false;
      tapNode = event.target.closest('[data-node]')?.getAttribute('data-node') ?? null;
    } else { dragged = true; tapNode = null; }
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
      if (dragged) camera = {...anchor.camera, x: anchor.camera.x + dx, y: anchor.camera.y + dy};
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
    tapNode = null;
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
    const content = {...model.data, selection: selected === null ? null : {start: selected, ...model.trace(selected)}};
    const url = URL.createObjectURL(new Blob([JSON.stringify(content, null, 2)], {type: 'application/json'}));
    const link = document.createElement('a');
    link.href = url; link.download = 'aliquot-orbits-1-100.json';
    document.body.append(link); link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
  resize(); inspect();
  new ResizeObserver(resize).observe(svg);
  const initial = new URLSearchParams(location.search).get('n');
  if (initial !== null) find(initial);
})();
