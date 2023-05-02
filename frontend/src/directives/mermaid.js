import mermaid from 'mermaid';

mermaid.initialize({
  startOnLoad: false,
  securityLevel: 'loose',
});

export default {
  beforeMount(el, binding) {
    el.innerHTML = `<pre class="mermaid">${binding.value}</pre>`;
    mermaid.init(undefined, el);
  },
  updated(el, binding) {
    el.innerHTML = `<pre class="mermaid">${binding.value}</pre>`;
    mermaid.init(undefined, el);
  },
};
