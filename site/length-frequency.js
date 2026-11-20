'use strict';

// Counts use the certified lengths/lower bounds only. No orbit calculation,
// independence assumption, extrapolation, or probable-prime shortcut is involved.
const AliquotLengthFrequency = (() => {
  const resolved = row => row.status === 'terminated' || row.status === 'cycle';
  function classify(row, threshold) {
    if (!Number.isSafeInteger(threshold) || threshold < 1) throw new Error('Invalid length threshold.');
    if ((resolved(row) ? row.steps : row.lower_bound) >= threshold) return 'long';
    return resolved(row) ? 'short' : 'unknown';
  }
  function series(rows, {threshold = 100, population = 'all', bound = rows.length, window = 1000} = {}) {
    if (!Number.isSafeInteger(bound) || bound < 1 || bound > rows.length || bound > 10000 ||
        !Number.isSafeInteger(window) || window < 1 || !Number.isSafeInteger(threshold) || threshold < 1 ||
        !['all', 'even', 'odd'].includes(population)) throw new Error('Invalid frequency bounds.');
    const cumulative = [{x: 0, from: 1, total: 0, lower: 0, upper: 0}], recent = [], blocks = [];
    let total = 0, lower = 0, upper = 0;
    const interval = (from, to) => {
      const a = cumulative[from - 1], b = cumulative[to];
      return {x: to, from, total: b.total - a.total, lower: b.lower - a.lower, upper: b.upper - a.upper};
    };
    for (let x = 1; x <= bound; x++) {
      const row = rows[x - 1];
      if (row.seed !== String(x)) throw new Error('Frequency data must contain consecutive seeds starting at 1.');
      if (population === 'all' || x % 2 === (population === 'even' ? 0 : 1)) {
        total++;
        const state = classify(row, threshold);
        if (state === 'long') { lower++; upper++; }
        else if (state === 'unknown') upper++;
      }
      cumulative.push({x, from: 1, total, lower, upper});
      if (x >= window) recent.push(interval(x - window + 1, x));
      if (x % window === 0 || x === bound) blocks.push(interval(Math.floor((x - 1) / window) * window + 1, x));
    }
    return {threshold, population, bound, window, cumulative, recent, blocks};
  }
  function percentage(point) {
    const {total, lower, upper} = point;
    if (!total) return '— (no eligible seeds)';
    if (lower === upper) return `${lower * 10000 % total ? '≈ ' : ''}${(100 * lower / total).toFixed(2)}%`;
    // Outward rounding preserves valid bounds; these are not confidence limits.
    return `${(Math.floor(lower * 10000 / total) / 100).toFixed(2)}–${(Math.ceil(upper * 10000 / total) / 100).toFixed(2)}%`;
  }
  function values(point, mode) {
    if (mode === 'count') return [point.lower, point.upper];
    return point.total ? [100 * point.lower / point.total, 100 * point.upper / point.total] : null;
  }
  function axis(maximum, count) {
    const raw = Math.max(maximum, 1) / 4, power = 10 ** Math.floor(Math.log10(raw)), unit = raw / power;
    let step = (unit >= 5 ? 5 : unit >= 2 ? 2 : 1) * power;
    if (count) step = Math.max(1, step);
    const ceiling = Math.max(step, Math.ceil(maximum / step) * step);
    const ticks = Array.from({length: Math.round(ceiling / step) + 1}, (_, i) => i * step);
    return {ceiling, ticks, decimals: Math.max(0, -Math.floor(Math.log10(step)))};
  }
  return {classify, series, percentage, values, axis};
})();

if (typeof document !== 'undefined') (() => {
  const F = AliquotLengthFrequency, data = AliquotLengthData;
  const $ = id => document.getElementById(id);
  const svg = $('frequency-chart'), chart = $('frequency-plot'), card = $('frequency-details');
  const controls = ['threshold', 'measure', 'population', 'bound'].map(id => $(`frequency-${id}`));
  const fmt = n => n.toLocaleString('en-US');
  const ns = 'http://www.w3.org/2000/svg';
  let model, samples, mode, geometry, width, height, focusX = 10000, hovered = null, pinned = null, suppressed = null;
  let cursor, lowerMark, upperMark;
  const element = (tag, attrs = {}, text) => {
    const node = document.createElementNS(ns, tag);
    for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
    if (text !== undefined) node.textContent = text;
    return node;
  };
  const rangeText = point => `${fmt(point.from)}–${fmt(point.x)}`;
  const countText = point => point.lower === point.upper ? fmt(point.lower) : `${fmt(point.lower)}–${fmt(point.upper)}`;
  const pointAt = x => mode === 'recent' ? model.recent[x - model.window] : model.cumulative[x];
  function showCard() {
    const x = pinned ?? hovered, point = x === null ? null : pointAt(x);
    card.hidden = !point;
    for (const mark of [cursor, lowerMark, upperMark]) mark.setAttribute('visibility', point ? 'visible' : 'hidden');
    if (!point) return;
    const value = F.values(point, mode);
    cursor.setAttribute('x1', geometry.x(x)); cursor.setAttribute('x2', geometry.x(x));
    if (value) {
      lowerMark.setAttribute('cx', geometry.x(x)); lowerMark.setAttribute('cy', geometry.y(value[0]));
      upperMark.setAttribute('cx', geometry.x(x)); upperMark.setAttribute('cy', geometry.y(value[1]));
    } else {
      lowerMark.setAttribute('visibility', 'hidden'); upperMark.setAttribute('visibility', 'hidden');
    }
    $('frequency-card-title').textContent = `Seeds ${rangeText(point)}`;
    $('frequency-card-mode').textContent = pinned === null ? 'Click to pin' : 'Pinned';
    $('frequency-card-count').textContent = `${countText(point)} with length ≥ ${model.threshold}`;
    $('frequency-card-share').textContent = F.percentage(point);
    $('frequency-card-total').textContent = `${fmt(point.total)} ${model.population === 'all' ? 'starting values' : `${model.population} starts`}`;
    $('frequency-card-known').textContent = fmt(point.lower);
    $('frequency-card-uncertain').textContent = fmt(point.upper - point.lower);
    $('frequency-card-short').textContent = fmt(point.total - point.upper);
    card.dataset.pinned = String(pinned !== null);
    const rect = svg.getBoundingClientRect(), parent = chart.getBoundingClientRect(), box = card.getBoundingClientRect();
    const px = rect.left - parent.left + geometry.x(x) * rect.width / width;
    const py = rect.top - parent.top + geometry.y(value ? value[1] : 0) * rect.height / height;
    let left = px + 14, top = py + 14;
    if (left + box.width > parent.width - 8) left = px - box.width - 14;
    if (top + box.height > rect.height - 8) top = py - box.height - 14;
    card.style.left = `${Math.max(8, Math.min(left, Math.max(8, parent.width - box.width - 8)))}px`;
    card.style.top = `${Math.max(8, Math.min(top, Math.max(8, rect.height - box.height - 8)))}px`;
  }
  function clearCard() {
    suppressed = pinned ?? hovered; pinned = hovered = null; showCard();
  }
  function draw() {
    mode = $('frequency-measure').value;
    if (!['count', 'share', 'recent'].includes(mode)) throw new Error('Invalid frequency measure.');
    model = F.series(data.orbits, {threshold: Number($('frequency-threshold').value),
      population: $('frequency-population').value, bound: Number($('frequency-bound').value)});
    samples = mode === 'recent' ? model.recent : model.cumulative.slice(mode === 'count' ? 0 : 1);
    const minX = mode === 'recent' ? model.window : 0, maxX = model.bound;
    const rect = svg.getBoundingClientRect(); width = Math.max(280, rect.width); height = Math.max(320, rect.height);
    const left = 64, right = width - 25, top = 25, bottom = height - 55;
    const drawable = samples.map(point => ({point, values: F.values(point, mode)})).filter(entry => entry.values);
    const scale = F.axis(drawable.reduce((max, entry) => Math.max(max, entry.values[1]), 0), mode === 'count');
    geometry = {left, right, top, bottom, minX, maxX,
      x: x => left + (x - minX) / Math.max(1, maxX - minX) * (right - left),
      y: y => bottom - y / scale.ceiling * (bottom - top)};
    const measureLabel = mode === 'count' ? 'Cumulative count' : mode === 'share' ? 'Cumulative share' : 'Share in the last 1,000 seed values';
    $('frequency-measure-label').textContent = `${measureLabel} · linear y-axis`;
    PageLatex.render($('frequency-formula'), `L_{${model.threshold}}(x)=\\#\\{n\\in P:n\\le x,\\ T(n)\\ge ${model.threshold}\\}`, {
      fallback: `L${model.threshold}(x) = number of selected starts n ≤ x with orbit length at least ${model.threshold}.`,
    });
    svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
    svg.replaceChildren(element('title', {id: 'frequency-title'}, `${measureLabel} of ${model.threshold}+-step aliquot orbits; ${model.population} seeds`));
    for (const tick of scale.ticks) {
      const y = geometry.y(tick);
      svg.append(element('line', {x1: left, x2: right, y1: y, y2: y, class: 'length-grid'}),
        element('text', {x: left - 9, y: y + 4, 'text-anchor': 'end', class: 'length-tick'},
          mode === 'count' ? fmt(tick) : `${tick.toFixed(scale.decimals)}%`));
    }
    const xTicks = [...new Set(Array.from({length: 5}, (_, i) => Math.round(minX + (maxX - minX) * i / 4)))];
    for (const x of xTicks) svg.append(element('text', {x: geometry.x(x), y: bottom + 21, 'text-anchor': 'middle', class: 'length-tick'}, fmt(x)));
    svg.append(element('text', {x: (left + right) / 2, y: height - 9, 'text-anchor': 'middle', class: 'length-axis'}, 'Seed bound x'),
      element('text', {transform: `translate(16 ${(top + bottom) / 2}) rotate(-90)`, 'text-anchor': 'middle', class: 'length-axis'}, mode === 'count' ? 'Long-orbit count' : 'Long-orbit share'));
    const coordinates = side => {
      const result = [];
      for (const {point, values} of drawable) {
        const pair = [geometry.x(point.x).toFixed(2), geometry.y(values[side]).toFixed(2)];
        if (mode === 'count' && result.length) result.push([pair[0], result.at(-1)[1]]);
        result.push(pair);
      }
      return result;
    };
    const low = coordinates(0), high = coordinates(1);
    const path = coordinates => coordinates.map((pair, i) => `${i ? 'L' : 'M'}${pair.join(' ')}`).join('');
    if (high.length) {
      svg.append(element('path', {d: `${path(high)}${low.slice().reverse().map(pair => `L${pair.join(' ')}`).join('')}Z`, class: 'frequency-band'}),
        element('path', {d: path(high), class: 'frequency-upper'}),
        element('path', {d: path(low), class: 'frequency-lower'}));
      // A single complete recent window still has visible endpoints.
      for (const [x, y] of [low.at(-1), high.at(-1)]) svg.append(element('circle', {cx: x, cy: y, r: 3, class: 'frequency-end'}));
    }
    cursor = element('line', {y1: top, y2: bottom, class: 'frequency-cursor', visibility: 'hidden'});
    lowerMark = element('circle', {r: 4, class: 'frequency-focus', visibility: 'hidden'});
    upperMark = element('circle', {r: 4, class: 'frequency-focus', visibility: 'hidden'});
    svg.append(cursor, lowerMark, upperMark);
    hovered = null;
    focusX = Math.max(Math.max(minX, 1), Math.min(maxX, focusX));
    if (pinned !== null) pinned = Math.max(Math.max(minX, 1), Math.min(maxX, pinned));
    showCard();
    const last = samples.at(-1);
    $('frequency-summary').textContent = `Seeds ${rangeText(last)} · ${fmt(last.total)} ${model.population === 'all' ? 'starts' : `${model.population} starts`} · ${fmt(last.lower)} confirmed ${model.threshold}+-step orbits · ${fmt(last.upper - last.lower)} still uncertain at this threshold · share ${F.percentage(last)}.`;
    const tbody = $('frequency-blocks'); tbody.replaceChildren();
    for (const point of model.blocks) {
      const row = document.createElement('tr');
      for (const text of [rangeText(point), fmt(point.total), countText(point), F.percentage(point)]) {
        const cell = document.createElement('td'); cell.textContent = text; row.append(cell);
      }
      tbody.append(row);
    }
  }
  function hit(event) {
    const box = svg.getBoundingClientRect(), x = (event.clientX - box.left) * width / box.width;
    const y = (event.clientY - box.top) * height / box.height;
    if (!Number.isFinite(x) || !Number.isFinite(y) || x < geometry.left || x > geometry.right || y < geometry.top - 8 || y > geometry.bottom + 8) return null;
    return Math.max(Math.max(geometry.minX, 1), Math.min(geometry.maxX,
      Math.round(geometry.minX + (x - geometry.left) / (geometry.right - geometry.left) * (geometry.maxX - geometry.minX))));
  }
  for (const control of controls) control.addEventListener('change', () => { suppressed = null; draw(); });
  svg.addEventListener('pointermove', event => {
    if (pinned !== null || event.pointerType === 'touch') return;
    let x = hit(event);
    if (x === suppressed) x = null; else suppressed = null;
    if (hovered === x) return;
    hovered = x; if (x !== null) focusX = x; showCard();
  });
  svg.addEventListener('pointerleave', () => { hovered = suppressed = null; showCard(); });
  svg.addEventListener('click', event => {
    const x = hit(event);
    if (x === null || x === pinned) { clearCard(); return; }
    pinned = focusX = x; hovered = suppressed = null; showCard();
  });
  svg.addEventListener('blur', () => { if (pinned === null) { hovered = null; showCard(); } });
  svg.addEventListener('keydown', event => {
    if (event.key === 'Escape') { event.preventDefault(); clearCard(); return; }
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      if (pinned !== null) clearCard();
      else { pinned = hovered ?? focusX; hovered = suppressed = null; showCard(); }
      return;
    }
    const x = pinned ?? hovered ?? focusX, first = Math.max(geometry.minX, 1);
    const moves = {ArrowLeft: Math.max(first, x - 1), ArrowRight: Math.min(model.bound, x + 1), Home: first, End: model.bound};
    if (Object.hasOwn(moves, event.key)) {
      event.preventDefault(); suppressed = null; focusX = moves[event.key];
      if (pinned !== null) pinned = focusX; else hovered = focusX;
      showCard();
    }
  });
  $('frequency-close').addEventListener('click', () => { clearCard(); svg.focus({preventScroll: true}); });
  $('frequency-download').addEventListener('click', () => {
    const artifact = {schema: 'aliquot-length-frequency-v1', source_schema: data.schema, source_limits: data.limits,
      definition: 'T(n) counts transitions to 0 or the first repeat; lower <= count(T >= threshold) <= upper.', ...model};
    const url = URL.createObjectURL(new Blob([JSON.stringify(artifact, null, 2)], {type: 'application/json'}));
    const link = document.createElement('a'); link.href = url;
    link.download = `aliquot-frequency-${model.threshold}-${model.population}-${model.bound}.json`;
    document.body.append(link); link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
  window.addEventListener('resize', draw);
  draw();
})();
