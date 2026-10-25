'use strict';

const AliquotLengths = (() => {
  const cap = 100;
  const ticks = [1, 2, 5, 10, 20, 50, cap];
  const resolved = row => row.status === 'terminated' || row.status === 'cycle';
  const level = row => resolved(row) ? row.steps : row.lower_bound;
  function geometry(width, height, bound) {
    const left = 62, right = width - 24, top = 48, bottom = height - 56;
    return {
      left, right, top, bottom,
      x: seed => left + (Number(seed) - 1) / (bound - 1) * (right - left),
      y: steps => bottom - Math.log10(Math.max(1, Math.min(cap, steps))) / Math.log10(cap) * (bottom - top),
    };
  }
  function description(row) {
    const steps = n => `${n} step${n === 1 ? '' : 's'}`;
    const clipped = row.steps >= cap ? ' · displayed at 100+' : '';
    if (row.status === 'terminated') return `${steps(row.steps)} to 0${clipped}.`;
    if (row.status === 'cycle') return `${steps(row.steps)} to the first repeat · ${row.cycle.length === 1 ? 'fixed point' : 'cycle'} ${row.cycle.join(' → ')} → ${row.cycle[0]}${clipped}.`;
    const reason = {factorization_limit: 'exact-factorization budget', source_limit: 'source-value ceiling', step_limit: 'step budget'}[row.status];
    return `Unresolved · at least ${steps(row.lower_bound)} to resolution. ${steps(row.steps)} verified before the ${reason}; this is not a measured length or evidence of divergence.`;
  }
  function pointDetails(row, edge) {
    const n = BigInt(row.seed), fmt = value => BigInt(value).toLocaleString('en-CA');
    const factors = edge?.factors.map(([prime, exponent]) => ({prime: BigInt(prime), exponent}));
    const basic = AliquotPointInfo.basic(n, edge ? BigInt(edge.to) : undefined);
    if (factors?.length === 1 && factors[0].prime === n && factors[0].exponent === 1) basic.status = 'Prime · deficient';
    return {title: `Seed ${fmt(n)}`, ...basic, ...AliquotPointInfo.divisors(n, factors),
      length: description(row), peak: fmt(row.peak),
      frontier: `${fmt(row.end)}${resolved(row) ? ' · resolved' : ' · unresolved within limits'}`};
  }
  return {cap, ticks, resolved, level, geometry, description, pointDetails};
})();

if (typeof document !== 'undefined') (() => {
  const data = AliquotLengthData, M = AliquotLengths;
  const $ = id => document.getElementById(id);
  const svg = $('length-chart'), range = $('seed-range'), chart = $('chart'), card = $('point-details');
  const bySeed = new Map(data.orbits.map(row => [row.seed, row]));
  const edges = new Map(data.edges.map(edge => [edge.from, edge])), detailsCache = new Map();
  let focusedSeed = '138', hovered = null, pinned = null, suppressed = null;
  let points = new Map(), hitBuckets = new Map(), viewWidth = 0, viewHeight = 0, geometry, halo;
  const ns = 'http://www.w3.org/2000/svg';
  function element(tag, attrs = {}, text) {
    const node = document.createElementNS(ns, tag);
    for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
    if (text !== undefined) node.textContent = text;
    return node;
  }
  function positionCard(point) {
    const svgBox = svg.getBoundingClientRect(), chartBox = chart.getBoundingClientRect();
    const x = svgBox.left - chartBox.left + point.x * svgBox.width / viewWidth;
    const y = svgBox.top - chartBox.top + point.y * svgBox.height / viewHeight;
    const width = chartBox.width, height = svgBox.height, box = card.getBoundingClientRect();
    const inset = 8, gap = 14;
    let left = x + gap, top = y + gap;
    if (left + box.width > width - inset) left = x - box.width - gap;
    if (top + box.height > height - inset) top = y - box.height - gap;
    card.style.left = `${Math.max(inset, Math.min(left, Math.max(inset, width - box.width - inset)))}px`;
    card.style.top = `${Math.max(inset, Math.min(top, Math.max(inset, height - box.height - inset)))}px`;
  }
  function showCard() {
    const active = pinned ?? hovered, base = active && points.get(active.seed);
    card.hidden = !base;
    halo.setAttribute('visibility', base ? 'visible' : 'hidden');
    if (!base) return;
    const point = {...base, y: active.top ? geometry.top : base.y};
    halo.setAttribute('cx', point.x); halo.setAttribute('cy', point.y);
    if (!detailsCache.has(active.seed)) detailsCache.set(active.seed, M.pointDetails(bySeed.get(active.seed), edges.get(active.seed)));
    const details = detailsCache.get(active.seed);
    for (const field of ['title', 'value', 'length', 'status', 'next', 'size', 'residue', 'divisors', 'divisor-summary', 'peak', 'frontier']) {
      $(`point-${field}`).textContent = details[field];
    }
    PageLatex.render($('point-factorization'), details.factorizationTex, {fallback: details.factorization});
    card.dataset.pinned = String(pinned !== null);
    $('point-mode').textContent = pinned ? 'Pinned' : 'Click to pin';
    $('point-orbit').href = `/orbits/?n=${active.seed}`;
    $('point-reverse').href = `/reverse/?n=${active.seed}`;
    positionCard(point);
  }
  function clearCard() {
    suppressed = (pinned ?? hovered)?.seed ?? null;
    pinned = hovered = null;
    showCard();
  }
  function addHit(point) {
    const bucket = Math.floor(point.x);
    if (!hitBuckets.has(bucket)) hitBuckets.set(bucket, []);
    hitBuckets.get(bucket).push(point);
  }
  function draw() {
    const bound = Number(range.value);
    const rows = data.orbits.filter(row => Number(row.seed) <= bound);
    const rect = svg.getBoundingClientRect();
    const width = Math.max(280, rect.width), height = Math.max(360, rect.height);
    const g = M.geometry(width, height, bound);
    geometry = g; viewWidth = width; viewHeight = height;
    points = new Map(); hitBuckets = new Map(); hovered = null;
    if (pinned && Number(pinned.seed) > bound) pinned = null;
    if (Number(focusedSeed) > bound) focusedSeed = '1';
    svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
    svg.replaceChildren(
      element('title', {id: 'length-title'}, `Aliquot resolution times for starts 1–${bound}; logarithmic y-axis capped at 100+`),
      element('rect', {x: g.left, y: g.top - 12, width: g.right - g.left, height: 24, class: 'length-cap'}),
    );
    for (const tick of M.ticks) {
      const y = g.y(tick);
      svg.append(element('line', {x1: g.left, x2: g.right, y1: y, y2: y, class: 'length-grid'}),
        element('text', {x: g.left - 9, y: y + 4, 'text-anchor': 'end', class: 'length-tick'}, tick === M.cap ? '100+' : String(tick)));
    }
    const interval = bound <= 100 ? 20 : bound <= 300 ? 50 : bound <= 1000 ? 200 : bound <= 5000 ? 1000 : 2000;
    const xTicks = [1];
    for (let n = interval; n <= bound; n += interval) xTicks.push(n);
    for (const tick of xTicks) {
      const x = g.x(tick);
      svg.append(element('line', {x1: x, x2: x, y1: g.bottom, y2: g.bottom + 5, class: 'length-grid'}),
        element('text', {x, y: g.bottom + 21, 'text-anchor': 'middle', class: 'length-tick'}, tick.toLocaleString('en-US')));
    }
    svg.append(element('text', {x: (g.left + g.right) / 2, y: height - 9, 'text-anchor': 'middle', class: 'length-axis'}, 'Starting number n'),
      element('text', {transform: `translate(17 ${(g.top + g.bottom) / 2}) rotate(-90)`, 'text-anchor': 'middle', class: 'length-axis'}, 'Steps · log scale'));
    const radius = bound > 1000 ? 2 : bound > 300 ? 2.7 : 3.5;
    for (const row of rows) {
      const x = g.x(row.seed), y = g.y(M.level(row));
      const kind = M.resolved(row) ? row.status : 'unresolved';
      const point = {seed: row.seed, x, y, top: false};
      points.set(row.seed, point); addHit(point);
      const group = element('g', {class: `length-point ${kind}`, 'data-seed': row.seed});
      // Shared hover cards replace per-node native titles/hit circles. Keep the
      // 10,000-point SVG small and use x buckets for nearest-point inspection.
      if (!M.resolved(row)) {
        if (M.level(row) < M.cap) {
          addHit({...point, y: g.top, top: true});
          group.append(element('line', {x1: x, x2: x, y1: y, y2: g.top, class: 'length-range'}),
            element('circle', {cx: x, cy: y, r: radius, class: 'length-mark'}));
        }
        group.append(element('path', {d: `M ${x - 4} ${g.top + 3} L ${x} ${g.top - 4} L ${x + 4} ${g.top + 3} Z`, class: 'length-mark'}));
      } else if (kind === 'cycle') {
        group.append(element('path', {d: `M ${x} ${y - 4} L ${x + 4} ${y} L ${x} ${y + 4} L ${x - 4} ${y} Z`, class: 'length-mark'}));
      } else {
        group.append(element('circle', {cx: x, cy: y, r: radius, class: 'length-mark'}));
      }
      svg.append(group);
    }
    for (const seed of ['138', '276']) {
      if (Number(seed) > bound) continue;
      const row = bySeed.get(seed), x = g.x(seed);
      const text = M.resolved(row) ? `${seed} · ${row.steps} steps` : `${seed} · unresolved`;
      const anchor = x > width - 155 ? 'end' : 'start';
      const stagger = Math.abs(g.x('276') - g.x('138')) < 170;
      svg.append(element('text', {x, y: seed === '276' && stagger ? 14 : 29,
        'text-anchor': anchor, class: `length-annotation${M.resolved(row) ? '' : ' unresolved'}`}, text));
    }
    halo = element('circle', {r: 6, class: 'length-halo', visibility: 'hidden'});
    svg.append(halo);
    showCard();
    const terminated = rows.filter(row => row.status === 'terminated').length;
    const cycles = rows.filter(row => row.status === 'cycle').length;
    const clipped = rows.filter(row => M.resolved(row) && row.steps >= M.cap).length;
    $('length-summary').textContent = `${bound.toLocaleString('en-US')} starts · ${terminated.toLocaleString('en-US')} reach 0 · ${cycles} reach a repeat · ${rows.length - terminated - cycles} unresolved within these bounds. ${clipped} resolved lengths are clipped at 100+.`;
  }
  range.addEventListener('change', () => { suppressed = null; draw(); });
  for (const button of document.querySelectorAll('.length-shortcuts button')) button.addEventListener('click', () => {
    if (Number(button.dataset.seed) > Number(range.value)) range.value = '300';
    focusedSeed = button.dataset.seed;
    pinned = {seed: focusedSeed, top: false}; hovered = suppressed = null;
    draw();
  });
  function hit(event) {
    if (!Number.isFinite(event.clientX) || !Number.isFinite(event.clientY)) {
      const group = event.target.closest('[data-seed]');
      return group && svg.contains(group) ? points.get(group.dataset.seed) : null;
    }
    const rect = svg.getBoundingClientRect();
    const x = (event.clientX - rect.left) * viewWidth / rect.width;
    const y = (event.clientY - rect.top) * viewHeight / rect.height;
    const radius = event.pointerType === 'touch' ? 24 : 8;
    let nearest = null, distance = radius ** 2;
    for (let bucket = Math.floor(x - radius); bucket <= Math.floor(x + radius); bucket++) {
      for (const point of hitBuckets.get(bucket) ?? []) {
        const d = (x - point.x) ** 2 + (y - point.y) ** 2;
        if (d < distance) { nearest = point; distance = d; }
      }
    }
    return nearest;
  }
  svg.addEventListener('pointermove', event => {
    if (pinned || event.pointerType === 'touch') return;
    let point = hit(event);
    if (point?.seed === suppressed) point = null;
    else suppressed = null;
    if (hovered === point) return;
    hovered = point;
    if (point) focusedSeed = point.seed;
    showCard();
  });
  svg.addEventListener('pointerleave', () => { hovered = suppressed = null; showCard(); });
  svg.addEventListener('click', event => {
    const point = hit(event);
    if (!point || point.seed === pinned?.seed) { clearCard(); return; }
    pinned = point; focusedSeed = point.seed; hovered = suppressed = null;
    showCard();
  });
  svg.addEventListener('blur', () => { if (!pinned) { hovered = null; showCard(); } });
  svg.addEventListener('keydown', event => {
    if (event.key === 'Escape') { event.preventDefault(); clearCard(); return; }
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      if (pinned) clearCard();
      else { pinned = hovered ?? points.get(focusedSeed); hovered = suppressed = null; showCard(); }
      return;
    }
    const bound = Number(range.value), n = Number((pinned ?? hovered)?.seed ?? focusedSeed);
    const moves = {ArrowLeft: Math.max(1, n - 1), ArrowRight: Math.min(bound, n + 1), Home: 1, End: bound};
    if (Object.hasOwn(moves, event.key)) {
      event.preventDefault(); suppressed = null; focusedSeed = String(moves[event.key]);
      if (pinned) pinned = points.get(focusedSeed);
      else hovered = points.get(focusedSeed);
      showCard();
    }
  });
  $('point-close').addEventListener('click', () => { clearCard(); svg.focus({preventScroll: true}); });
  $('download-lengths').addEventListener('click', () => {
    const url = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'}));
    const link = document.createElement('a');
    link.href = url;
    link.download = `aliquot-orbit-lengths-${data.limits.seed_bound}.json`;
    document.body.append(link);
    link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
  window.addEventListener('resize', draw);
  draw();
})();
