'use strict';
// Transactional, exact graph growth. Cancellation discards the whole unfinished
// action; a computation limit publishes only verified edges and an open frontier.
const AliquotOrbitSession = (() => {
  const LIMITS = {maxNodes: 5000, maxSteps: 64, maxDigits: AliquotMath.MAX_DIGITS,
    maxWork: AliquotMath.MAX_WORK, batchSize: 25, history: 10};
  const copy = value => JSON.parse(JSON.stringify(value));
  const compare = (a, b) => BigInt(a) < BigInt(b) ? -1 : BigInt(a) > BigInt(b) ? 1 : 0;
  function create(initial, options = {}) {
    const limits = {...LIMITS, ...options};
    for (const [key, maximum] of Object.entries(LIMITS)) {
      if (!Number.isSafeInteger(limits[key]) || limits[key] < 1 || limits[key] > maximum) throw new Error(`Invalid ${key} limit.`);
    }
    if (initial.nodes.length > limits.maxNodes) throw new Error('Initial graph exceeds the node limit.');
    const history = [];
    let revision = 0, table = null;
    function fresh() {
      const data = copy(initial);
      data.schema = 'aliquot-orbit-session-v1';
      data.initial_limits = data.limits;
      data.limits = {...limits, predecessorSourceCap: String(AliquotReverse.MAX_BOUND)};
      return data;
    }
    let data = fresh(), model = AliquotOrbitGraph.create(data);
    function parse(raw) {
      const text = String(raw).trim();
      if (!/^\d+$/.test(text) || text.length > limits.maxDigits) throw new Error(`Enter a non-negative integer of at most ${limits.maxDigits} digits.`);
      return BigInt(text).toString();
    }
    function newNode(id) {
      const ceiling = AliquotReverse.ceiling(BigInt(id));
      return {id, next: null, factors: null, prime: id === '0' || id === '1' ? false : null,
        seed: false, starts: [], incoming: [], leaf: true, untouchable: false,
        unresolved: id === '0' ? null : 'not expanded',
        predecessors: {status: id === '1' ? 'infinite' : 'unsearched',
          ceiling: ceiling === null ? null : String(ceiling), checked_through: null, values: null}};
    }
    function transaction(cancelled = () => false) {
      const version = revision, draft = copy(data), nodes = new Map(draft.nodes.map(n => [n.id, n]));
      const seeds = new Set(draft.orbits.map(o => o.seed));
      const added = [], edges = [];
      let changed = false;
      const isCancelled = () => cancelled() || version !== revision;
      const check = () => { if (isCancelled()) throw new Error('cancelled'); };
      function ensure(id) {
        if (!nodes.has(id)) {
          if (nodes.size >= limits.maxNodes) throw new Error(`Graph limit: ${limits.maxNodes} nodes. Undo or reset to make room.`);
          nodes.set(id, newNode(id)); added.push(id); changed = true;
        }
        return nodes.get(id);
      }
      function seed(id) { if (id !== '0' && !seeds.has(id)) { seeds.add(id); changed = true; } }
      function link(id, next, verification) {
        const node = nodes.get(id);
        if (id === '0') throw new Error('s(0) is undefined.');
        if ((node.next !== null && node.next !== next) || (node.sum != null && node.sum !== next)) throw new Error('Exact successor mismatch.');
        node.sum = next; node.prime = id !== '1' && next === '1'; node.verification = verification;
        changed = true;
        if (next.length > limits.maxDigits) {
          node.unresolved = `next edge not drawn: ${limits.maxDigits}-digit limit`; return false;
        }
        if (!nodes.has(next) && nodes.size >= limits.maxNodes) {
          node.unresolved = `next edge not drawn: ${limits.maxNodes}-node limit`; return false;
        }
        ensure(next);
        if (node.next === null) edges.push(id);
        node.next = next; node.unresolved = null;
        return true;
      }
      async function compute(id) {
        check();
        let factors;
        const next = await AliquotMath.sum(BigInt(id), {maxWork: limits.maxWork, cancelled: isCancelled,
          onFactors: value => { factors = value; }});
        check();
        if (!factors || AliquotMath.properDivisorsFromFactors(BigInt(id), factors, 1).sum !== next) throw new Error('Exact factorization check failed.');
        return {next: String(next), factors: factors.map(f => ({prime: String(f.prime), exponent: f.exponent}))};
      }
      function commit() {
        check();
        if (!changed) return;
        draft.nodes = [...nodes.values()].sort((a, b) => compare(a.id, b.id));
        draft.edges = [];
        for (const node of draft.nodes) { node.incoming = []; node.starts = []; node.seed = seeds.has(node.id); }
        for (const node of draft.nodes) {
          if (node.next !== null) {
            draft.edges.push({from: node.id, to: node.next}); nodes.get(node.next).incoming.push(node.id);
          }
        }
        const nextModel = AliquotOrbitGraph.create(draft);
        draft.orbits = [...seeds].sort(compare).map(id => {
          const trace = nextModel.trace(id);
          for (const value of new Set(trace.path)) nodes.get(value).starts.push(id);
          return {seed: id, ...trace};
        });
        for (const node of draft.nodes) {
          node.leaf = node.incoming.length === 0;
          node.untouchable = node.id !== '0' && node.predecessors.status === 'complete' && node.predecessors.values.length === 0;
        }
        draft.complete_orbits = draft.orbits.every(o => o.status !== 'unresolved');
        history.push(data);
        if (history.length > limits.history) history.shift();
        data = draft; model = nextModel; revision++;
      }
      return {draft, nodes, added, edges, ensure, seed, link, compute, commit, check, isCancelled,
        markChanged() { changed = true; }};
    }
    async function extend(raw, {cancelled, onProgress = () => {}} = {}) {
      const id = parse(raw), tx = transaction(cancelled);
      tx.check(); tx.ensure(id); tx.seed(id);
      const seen = new Set();
      let current = id, computed = 0;
      while (current !== '0' && !seen.has(current)) {
        tx.check(); seen.add(current);
        const node = tx.nodes.get(current);
        if (node.next !== null) { current = node.next; continue; }
        if (computed >= limits.maxSteps) { node.unresolved = `${limits.maxSteps}-step action limit`; tx.markChanged(); break; }
        onProgress(`Computing exact step ${computed + 1}/${limits.maxSteps}…`);
        let result;
        try { result = await tx.compute(current); }
        catch (error) {
          tx.check(); node.unresolved = `exact computation unresolved: ${error.message}`; tx.markChanged(); break;
        }
        node.factors = result.factors;
        computed++;
        if (!tx.link(current, result.next, 'browser exact factorization')) break;
        current = result.next;
      }
      tx.commit();
      const trace = model.trace(id);
      return {id, added: tx.added, edges: tx.edges.length, computed, status: trace.status,
        reason: trace.status === 'unresolved' ? model.nodes.get(trace.path.at(-1)).unresolved : null};
    }
    async function expand(raw, {bound = 10000, cancelled, onProgress = () => {}} = {}) {
      const id = parse(raw);
      if (!Number.isSafeInteger(bound) || bound < 1 || bound > AliquotReverse.MAX_BOUND) throw new Error('Source bound must be an integer from 1 to 1,000,000.');
      if (!model.nodes.has(id)) throw new Error('Select a displayed node first.');
      const tx = transaction(cancelled), node = tx.nodes.get(id);
      tx.check();
      let inverse = node.predecessors;
      if (inverse.status !== 'complete' && (!inverse.values || BigInt(inverse.checked_through ?? '0') < BigInt(bound))) {
        onProgress(`Checking predecessor sources through ${bound.toLocaleString('en-CA')}…`);
        if (!table || table.bound < bound) {
          const completed = await AliquotReverse.sieve(bound, {cancelled: tx.isCancelled});
          tx.check(); table = completed;
        }
        const result = AliquotReverse.predecessors(table, BigInt(id), bound);
        tx.check();
        inverse = {status: id === '1' ? 'infinite' : result.complete ? 'complete' : 'partial',
          ceiling: result.ceiling === null ? null : String(result.ceiling), checked_through: String(result.checked),
          values: result.values.map(String)};
        node.predecessors = inverse; tx.markChanged();
      }
      const missing = inverse.values.filter(source => tx.nodes.get(source)?.next !== id);
      const revealed = [];
      let limited = false;
      for (const source of missing.slice(0, limits.batchSize)) {
        tx.check();
        if (!tx.nodes.has(source) && tx.nodes.size >= limits.maxNodes) { limited = true; break; }
        tx.ensure(source); tx.seed(source);
        tx.link(source, id, 'completed exhaustive predecessor census');
        revealed.push(source);
      }
      tx.commit();
      return {id, added: tx.added, revealed, edges: tx.edges.length, found: inverse.values.length,
        remaining: missing.length - revealed.length, complete: inverse.status === 'complete',
        infinite: inverse.status === 'infinite', checked: inverse.checked_through, limited};
    }
    async function divisors(raw, {cancelled} = {}) {
      const id = parse(raw);
      if (!model.nodes.has(id) || id === '0') throw new Error('Select a positive displayed node.');
      const tx = transaction(cancelled), node = tx.nodes.get(id);
      const result = await tx.compute(id);
      if ((node.next !== null && node.next !== result.next) || (node.sum != null && node.sum !== result.next)) throw new Error('Exact successor mismatch.');
      // Factor inspection does not draw an edge or falsely resolve a frontier.
      node.factors = result.factors; node.sum = result.next; node.prime = id !== '1' && result.next === '1';
      tx.markChanged(); tx.commit();
      return {id};
    }
    return {parse, extend, expand, divisors, limits,
      get data() { return data; }, get model() { return model; }, get canUndo() { return history.length > 0; },
      undo() { if (!history.length) return false; data = history.pop(); model = AliquotOrbitGraph.create(data); revision++; return true; },
      reset() { data = fresh(); model = AliquotOrbitGraph.create(data); history.length = 0; revision++; }};
  }
  return {create, LIMITS};
})();
