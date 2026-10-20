// JSON bridge used by Python to check the actual served browser arithmetic.
import vm from 'node:vm';
import { readFileSync } from 'node:fs';
const context = vm.createContext({setTimeout});
vm.runInContext(readFileSync(new URL('../site/math.js', import.meta.url), 'utf8'), context);
const inputs = JSON.parse(readFileSync(0, 'utf8'));
const results = [];
for (const input of inputs) {
  context.n = BigInt(input);
  const result = await vm.runInContext(`(async()=>{
    let factors;
    const sum=await AliquotMath.sum(n,{onFactors:value=>{factors=value;}});
    return {sum,factors,base12:n.toString(12).toUpperCase(),divisors:AliquotMath.properDivisorsFromFactors(n,factors)};
  })()`, context);
  // Never pass BigInts through floating point in interchange data.
  results.push(JSON.parse(JSON.stringify(result, (_, value) => typeof value==='bigint'?String(value):value)));
}
console.log(JSON.stringify(results));
