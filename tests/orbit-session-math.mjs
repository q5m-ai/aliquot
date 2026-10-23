// Python independently verifies the actual served live-expansion adapter.
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
const context = vm.createContext({setTimeout});
vm.runInContext(['math', 'reverse-math', 'orbit-data', 'orbit-graph', 'orbit-session']
  .map(name => readFileSync(new URL(`../site/${name}.js`, import.meta.url), 'utf8')).join('\n') +
  '\nconst session = AliquotOrbitSession.create(AliquotOrbitData);', context);
await vm.runInContext('session.expand("12")', context);
await vm.runInContext('session.expand("121", {bound:14400})', context);
for (const id of ['220', '284', '101', '1184', '790', '999983', '9007199254740992']) {
  await vm.runInContext(`session.extend('${id}')`, context);
}
await vm.runInContext('session.divisors("121")', context);
console.log(vm.runInContext('JSON.stringify(session.data)', context));
