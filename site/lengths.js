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
  return {cap, ticks, resolved, level, geometry, description};
})();

if (typeof document !== 'undefined') (() => {
  const data = AliquotLengthData, M = AliquotLengths;
  const svg = document.getElementById('length-chart');
  const range = document.getElementById('seed-range');
  const bySeed = new Map(data.orbits.map(row => [row.seed, row]));
  let selected = '138', marks = new Map(), hitTargets = [], viewWidth = 0, viewHeight = 0;
  const ns = 'http://www.w3.org/2000/svg';
  function element(tag, attrs = {}, text) {
    const node = document.createElementNS(ns, tag);
    for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
    if (text !== undefined) node.textContent = text;
    return node;
  }
  function select(seed) {
    const row = bySeed.get(seed);
    if (!row || Number(seed) > Number(range.value)) return;
    marks.get(selected)?.classList.remove('selected');
    selected = seed;
    marks.get(selected)?.classList.add('selected');
    document.getElementById('selected-title').textContent = `Seed ${seed}`;
    document.getElementById('selected-result').textContent = M.description(row);
    document.getElementById('selected-detail').textContent = `Largest verified term: ${row.peak}. ${M.resolved(row) ? 'Final recorded value' : 'Unresolved frontier'}: ${row.end}.`;
    document.getElementById('open-orbit').href = `/orbits/?n=${seed}`;
  }
  function draw() {
    const bound = Number(range.value);
    const rows = data.orbits.filter(row => Number(row.seed) <= bound);
    const rect = svg.getBoundingClientRect();
    const width = Math.max(280, rect.width), height = Math.max(360, rect.height);
    const g = M.geometry(width, height, bound);
    viewWidth = width; viewHeight = height; hitTargets = [];
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
    const interval = bound === 1000 ? 200 : bound === 300 ? 50 : 20;
    const xTicks = [1];
    for (let n = interval; n <= bound; n += interval) xTicks.push(n);
    for (const tick of xTicks) {
      const x = g.x(tick);
      svg.append(element('line', {x1: x, x2: x, y1: g.bottom, y2: g.bottom + 5, class: 'length-grid'}),
        element('text', {x, y: g.bottom + 21, 'text-anchor': 'middle', class: 'length-tick'}, tick.toLocaleString('en-US')));
    }
    svg.append(element('text', {x: (g.left + g.right) / 2, y: height - 9, 'text-anchor': 'middle', class: 'length-axis'}, 'Starting number n'),
      element('text', {transform: `translate(17 ${(g.top + g.bottom) / 2}) rotate(-90)`, 'text-anchor': 'middle', class: 'length-axis'}, 'Steps · log scale'));
    marks = new Map();
    const radius = bound > 300 ? 2.7 : 3.5;
    for (const row of rows) {
      const x = g.x(row.seed), y = g.y(M.level(row));
      const kind = M.resolved(row) ? row.status : 'unresolved';
      hitTargets.push({seed: row.seed, x, y});
      if (!M.resolved(row)) hitTargets.push({seed: row.seed, x, y: g.top});
      const group = element('g', {class: `length-point ${kind}`, 'data-seed': row.seed});
      group.append(element('title', {}, `Seed ${row.seed}: ${M.description(row)}`));
      if (!M.resolved(row)) {
        if (M.level(row) < M.cap) {
          group.append(element('line', {x1: x, x2: x, y1: y, y2: g.top, class: 'length-range'}),
            element('circle', {cx: x, cy: y, r: radius, class: 'length-mark'}));
        }
        group.append(element('path', {d: `M ${x - 4} ${g.top + 3} L ${x} ${g.top - 4} L ${x + 4} ${g.top + 3} Z`, class: 'length-mark'}),
          element('circle', {cx: x, cy: g.top, r: 7, class: 'length-hit'}));
      } else if (kind === 'cycle') {
        group.append(element('path', {d: `M ${x} ${y - 4} L ${x + 4} ${y} L ${x} ${y + 4} L ${x - 4} ${y} Z`, class: 'length-mark'}));
      } else {
        group.append(element('circle', {cx: x, cy: y, r: radius, class: 'length-mark'}));
      }
      group.append(element('circle', {cx: x, cy: y, r: 6, class: 'length-halo'}),
        element('circle', {cx: x, cy: y, r: 7, class: 'length-hit'}));
      svg.append(group);
      marks.set(row.seed, group);
    }
    // Named examples are annotations, not unverified special-case heights.
    for (const seed of ['138', '276']) {
      if (Number(seed) > bound) continue;
      const row = bySeed.get(seed), x = g.x(seed);
      const text = M.resolved(row) ? `${seed} · ${row.steps} steps` : `${seed} · unresolved`;
      const anchor = x > width - 155 ? 'end' : 'start';
      svg.append(element('text', {x, y: seed === '276' && width < 650 ? 14 : 29,
        'text-anchor': anchor, class: `length-annotation${M.resolved(row) ? '' : ' unresolved'}`}, text));
    }
    if (Number(selected) > bound) selected = '1';
    select(selected);
    const terminated = rows.filter(row => row.status === 'terminated').length;
    const cycles = rows.filter(row => row.status === 'cycle').length;
    const clipped = rows.filter(row => M.resolved(row) && row.steps >= M.cap).length;
    document.getElementById('length-summary').textContent = `${bound.toLocaleString('en-US')} starts · ${terminated} reach 0 · ${cycles} reach a repeat · ${rows.length - terminated - cycles} unresolved within these bounds. ${clipped} resolved lengths are clipped at 100+.`;
  }
  range.addEventListener('change', draw);
  for (const button of document.querySelectorAll('.length-shortcuts button')) button.addEventListener('click', () => {
    if (Number(button.dataset.seed) > Number(range.value)) range.value = '300';
    selected = button.dataset.seed;
    draw();
  });
  const inspect = event => {
    if (Number.isFinite(event.clientX) && Number.isFinite(event.clientY)) {
      // Hit-test actual coordinates, not SVG paint order: dense prime rows overlap.
      const rect = svg.getBoundingClientRect();
      const x = (event.clientX - rect.left) * viewWidth / rect.width;
      const y = (event.clientY - rect.top) * viewHeight / rect.height;
      let nearest = null, distance = 64;
      for (const point of hitTargets) {
        const d = (x - point.x) ** 2 + (y - point.y) ** 2;
        if (d < distance) { nearest = point.seed; distance = d; }
      }
      if (nearest !== null) select(nearest);
    } else {
      const group = event.target.closest('[data-seed]');
      if (group && svg.contains(group)) select(group.dataset.seed);
    }
  };
  svg.addEventListener('pointermove', inspect);
  svg.addEventListener('click', inspect);
  svg.addEventListener('keydown', event => {
    const bound = Number(range.value), n = Number(selected);
    const moves = {ArrowLeft: Math.max(1, n - 1), ArrowRight: Math.min(bound, n + 1), Home: 1, End: bound};
    if (Object.hasOwn(moves, event.key)) {
      event.preventDefault();
      select(String(moves[event.key]));
    }
  });
  document.getElementById('download-lengths').addEventListener('click', () => {
    const url = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'}));
    const link = document.createElement('a');
    link.href = url;
    link.download = 'aliquot-orbit-lengths-1000.json';
    document.body.append(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
  window.addEventListener('resize', draw);
  draw();
})();
