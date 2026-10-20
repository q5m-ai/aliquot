'use strict';
// Render only explicit TeX fields, not arbitrary page text or user input.
// Native MathML needs no KaTeX CSS, font downloads, inline styles, or CSP changes.
const PageLatex = (() => {
  function render(element, tex, {displayMode=false, fallback=element.textContent}={}) {
    const key=tex ? `${displayMode}:${tex}` : '';
    if(key && element.dataset.mathTex===key)return true;
    element.textContent=fallback;
    delete element.dataset.mathTex;
    delete element.dataset.mathError;
    if(!tex)return false;
    if(typeof katex==='undefined')return false; // Keep readable fallback copy.
    try {
      if(tex.length>4096)throw new Error('Formula display budget exceeded.');
      const markup=katex.renderToString(tex, {
        output:'mathml',displayMode,throwOnError:true,trust:false,strict:'error',
        maxExpand:1000,maxSize:10,
      });
      element.innerHTML=markup;
      element.dataset.mathTex=key;
      return true;
    } catch {
      element.dataset.mathError='true';
      return false; // Invalid formulas never replace the safe text fallback.
    }
  }
  document.querySelectorAll('[data-tex]').forEach(element=>{
    render(element,element.dataset.tex,{displayMode:element.dataset.display==='true'});
  });
  return {render};
})();
