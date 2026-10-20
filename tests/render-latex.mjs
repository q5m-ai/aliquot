// Python-driven checks of the same renderer and KaTeX bundle served by the site.
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
const input=JSON.parse(readFileSync(0,'utf8'));
const context=vm.createContext({document:{querySelectorAll:()=>[]}});
if(!input.withoutLibrary)vm.runInContext(readFileSync(new URL('../site/vendor/katex/katex.min.js',import.meta.url),'utf8'),context);
vm.runInContext(readFileSync(new URL('../site/latex.js',import.meta.url),'utf8'),context);
const results=[];
for(const formula of input.formulas){
  let markup='',assignments=0,text='Readable fallback';
  context.element={dataset:{},get textContent(){return text},set textContent(value){text=value;markup=''},
    get innerHTML(){return markup},set innerHTML(value){markup=value;assignments++}};
  context.formula=formula;
  const ok=vm.runInContext('PageLatex.render(element,formula.tex,{displayMode:!!formula.display})',context);
  // Repeated hover updates must not repeatedly typeset an unchanged expression.
  if(ok)vm.runInContext('PageLatex.render(element,formula.tex,{displayMode:!!formula.display})',context);
  results.push({ok,markup,text,error:context.element.dataset.mathError||null,assignments});
}
console.log(JSON.stringify(results));
