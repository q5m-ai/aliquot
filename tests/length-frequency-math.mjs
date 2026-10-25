// Exercise the actual served aggregator; Python supplies independently checked records.
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const context = vm.createContext({});
vm.runInContext(readFileSync(new URL('../site/length-frequency.js', import.meta.url), 'utf8'), context);
const model = vm.runInContext('AliquotLengthFrequency', context);
const {orbits, options} = JSON.parse(readFileSync(0, 'utf8'));
process.stdout.write(JSON.stringify(options.map(option => model.series(orbits, option))));
