// Python drives the actual served sieve, then checks it independently.
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
const request = JSON.parse(readFileSync(0, 'utf8'));
const context = vm.createContext({setTimeout});
vm.runInContext(readFileSync(new URL('../site/reverse-math.js', import.meta.url), 'utf8'), context);
context.bound = request.bound;
context.table = await vm.runInContext('AliquotReverse.sieve(bound, {yieldUI: async () => {}})', context);
const samples = request.samples || Array.from({length: request.bound}, (_, i) => i + 1);
const sums = samples.map(n => [String(n), String(context.table.sums[n])]);
const results = (request.targets || []).map(target => {
  context.target = BigInt(target);
  return vm.runInContext('AliquotReverse.predecessors(table, target)', context);
});
process.stdout.write(JSON.stringify({sums, results}, (_, value) => typeof value === 'bigint' ? value.toString() : value));
