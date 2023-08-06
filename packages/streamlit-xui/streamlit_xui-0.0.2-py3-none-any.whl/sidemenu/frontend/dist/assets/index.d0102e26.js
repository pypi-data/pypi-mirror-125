import{S as i}from"./vendor.919a7b4c.js";const k=function(){const t=document.createElement("link").relList;if(t&&t.supports&&t.supports("modulepreload"))return;for(const e of document.querySelectorAll('link[rel="modulepreload"]'))a(e);new MutationObserver(e=>{for(const d of e)if(d.type==="childList")for(const r of d.addedNodes)r.tagName==="LINK"&&r.rel==="modulepreload"&&a(r)}).observe(document,{childList:!0,subtree:!0});function u(e){const d={};return e.integrity&&(d.integrity=e.integrity),e.referrerpolicy&&(d.referrerPolicy=e.referrerpolicy),e.crossorigin==="use-credentials"?d.credentials="include":e.crossorigin==="anonymous"?d.credentials="omit":d.credentials="same-origin",d}function a(e){if(e.ep)return;e.ep=!0;const d=u(e);fetch(e.href,d)}};k();const O=`
body {
  margin: 0;
}

#app {
  margin: 0;
}

/* Fixed sidenav, full height */
.sidenav {
  font-family: Arial;
  height: 100%;
  width: 100%;
  position: fixed;
  z-index: 1;
  top: 0;
  left: 0;
  background-color: #111;
  overflow-x: hidden;
  /* padding-top: 20px; */
}

/* Style the sidenav links and the dropdown button */
.sidenav a, .dropdown-btn {
  padding: 6px 8px 6px 16px;
  text-decoration: none;
  font-size: 20px;
  color: #818181;
  display: block;
  border: none;
  background: none;
  width:100%;
  text-align: left;
  cursor: pointer;
  outline: none;
}

/* On mouse-over */
.sidenav a:hover, .dropdown-btn:hover {
  color: #f1f1f1;
}

/* Main content */
.main {
  margin-left: 200px; /* Same as the width of the sidenav */
  font-size: 20px; /* Increased text to enable scrolling */
  padding: 0px 10px;
}

/* Add an active class to the active dropdown button */
.sidenav a.selected {
  background-color: green;
  color: white;
}

/* Dropdown container (hidden by default). Optional: add a lighter background color and some left padding to change the design of the dropdown content */
.dropdown-container {
  display: none;
  background-color: #262626;
  padding-left: 8px;
}

/* Optional: Style the caret down icon */
.fa-caret-down {
  float: right;
  padding-right: 8px;
}
`;let f=280,w=1;function v(l){l=l*w;let t=l-f;t<0&&(t=f),document.getElementById("app").style.height=t+"px",i.setFrameHeight()}function I(l,t){i.setComponentValue({selected:l,opened:t})}function S(l){const t=l.detail,u=t.args.items;let a=t.args.selected||"",e=t.args.opened||[];const{customStyle:d=null,OPEN_ICON:r=">+",CLOSE_ICON:x=">-",HEIGHT_REDUCE:L=280,HEIGHT_FACTOR:T=1}=t.args.options;f=L,w=T;const h=x,g=r,H=d||O,m=document.createElement("style");m.innerText=H,document.head.appendChild(m);const s=document.createElement("div");s.classList.add("sidenav");function y(n){const o=document.createElement("a");return a===n.label&&o.classList.add("selected"),o.onclick=()=>{a=n.label,I(a,e)},o.innerHTML=n.label,o}u.forEach(n=>{if(n.children){const o=document.createElement("button");o.classList.add("dropdown-btn");const c=document.createElement("div");c.classList.add("dropdown-container"),e.includes(n.label)?(c.style.display="block",o.innerHTML=h+n.label):o.innerHTML=g+n.label,o.onclick=b=>{const p=c;p.style.display==="block"?(e=e.filter(C=>n.label!==C),o.innerHTML=g+n.label,p.style.display="none"):(e.push(n.label),o.innerHTML=h+n.label,p.style.display="block")},s.appendChild(o),n.children.forEach(b=>{const p=y(b);c.appendChild(p)}),s.appendChild(c)}else{const o=y(n);s.appendChild(o)}}),document.getElementById("app").appendChild(s),v(window.outerHeight),document.getElementById("app").style.overflow="auto",i.setFrameHeight()}i.events.addEventListener(i.RENDER_EVENT,S);i.setComponentReady();i.setFrameHeight();let E=null;window.parent.addEventListener("resize",function(){clearTimeout(E),E=setTimeout(()=>v(window.outerHeight),500)});
