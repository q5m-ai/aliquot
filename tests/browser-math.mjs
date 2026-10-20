// JSON bridge used by Python to check the actual served browser arithmetic.
import vm from 'node:vm';
import { readFileSync } from 'node:fs';
const context = vm.createContext({setTimeout});
vm.runInContext(readFileSync(new URL('../site/math.js', import.meta.url), 'utf8'), context);
const inputs = JSON.parse(readFileSync(0, 'utf8'));
const results = [];
for (const input of inputs) {
  context.n = BigInt(input);
  results.push(String(await vm.runInContext('AliquotMath.sum(n)', context)));
}
console.log(JSON.stringify(results));
