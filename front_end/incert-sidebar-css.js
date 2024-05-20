// body {
//   font-family: "Lato", sans-serif;
// }

console.info("Verificando se o plugin está ativado para mostrar sidebar: ", localStorage.getItem("pluginAtivado"));
if (localStorage.getItem("pluginAtivado")) {
  showSidebar();
};

function showSidebar() {
  let styleContentSidebar = `

/* inicio @cgustavoof */

/* The actual popup */

* , ::before, ::after {
  --tw-border-spacing-x: 0;
  --tw-border-spacing-y: 0;
  --tw-translate-x: 0;
  --tw-translate-y: 0;
  --tw-rotate: 0;
  --tw-skew-x: 0;
  --tw-skew-y: 0;
  --tw-scale-x: 1;
  --tw-scale-y: 1;
  --tw-pan-x: ;
  --tw-pan-y: ;
  --tw-pinch-zoom: ;
  --tw-scroll-snap-strictness: proximity;
  --tw-ordinal: ;
  --tw-slashed-zero: ;
  --tw-numeric-figure: ;
  --tw-numeric-spacing: ;
  --tw-numeric-fraction: ;
  --tw-ring-inset: ;
  --tw-ring-offset-width: 0px;
  --tw-ring-offset-color: #fff;
  --tw-ring-color: rgb(59 130 246 / 0.5);
  --tw-ring-offset-shadow: 0 0 #0000;
  --tw-ring-shadow: 0 0 #0000;
  --tw-shadow: 0 0 #0000;
  --tw-shadow-colored: 0 0 #0000;
  --tw-blur: ;
  --tw-brightness: ;
  --tw-contrast: ;
  --tw-grayscale: ;
  --tw-hue-rotate: ;
  --tw-invert: ;
  --tw-saturate: ;
  --tw-sepia: ;
  --tw-drop-shadow: ;
  --tw-backdrop-blur: ;
  --tw-backdrop-brightness: ;
  --tw-backdrop-contrast: ;
  --tw-backdrop-grayscale: ;
  --tw-backdrop-hue-rotate: ;
  --tw-backdrop-invert: ;
  --tw-backdrop-opacity: ;
  --tw-backdrop-saturate: ;
  --tw-backdrop-sepia: ;
  --tw-bg-opacity: 0.5;
  --tw-bg-color-indigo: rgb(79 70 229 / var(--tw-bg-opacity));
  --tw-border-radius: 15px;
}

.font-sans {
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
    font-feature-settings: normal;
}

.popuptext {
  --tw-width: 350px;
  visibility: hidden;
  width: var(--tw-width)!important;
  border-radius: var(--tw-border-radius);
  padding: 8px 10px;
  position: absolute;
  z-index: 1;
  bottom: 125%;
  left: calc(0.45 * var(--tw-width))!important;
}

.popupHeader{
  align-items: center;
  display: flex;
  flex-direction: row;
  background-color: var(--tw-bg-color-indigo);
  display: block;
  width: 100%;
  border-top-left-radius:  var(--tw-border-radius);
  border-top-right-radius: var(--tw-border-radius);
  min-height: 35px;
  border-bottom: 1px inset #e6e6e6;
}

.popupBody{
  padding: 10px;
  border-bottom-left-radius:  var(--tw-border-radius);
  border-bottom-right-radius: var(--tw-border-radius);
}

.detailpopup {
  /*padding: 10px;*/
  border-radius: var(--tw-border-radius);
  background-color: #fcfcfc;
  /*box-shadow: 0 5px 15px rgba(0, 0, 0, 0.8);*/
  box-shadow: 0 0 0.5px rgb(0 0 0 / 70%), 0 2px 8px rgb(26 33 52 / 20%);
}



.linksug {
  cursor: pointer;
}

/*.linksug:hover {
  background-color: #0078aa;
  opacity:0.5;
}*/

.linksug.sugestao{
  display: block;
  padding: 2px 5px;
  position:relative;
}
.linksug.sugestao:after{
  display: block;
  width: 100%;
  height: 100%;
  content: " ";
  position: absolute;
  top: 0;
  left: -2px;
}

.linksug.sugestao:hover:after{
  animation-name: right-animate;
  animation-duration: 1s;
  --tw-bg-opacity: 0.3;
  background-color: var(--tw-bg-color-indigo);
}

.linksug.sugestao:hover{

}

/* Toggle this class - hide and show the popup */
.show {
  visibility: visible;
  -webkit-animation: fadeIn 1s;
  animation: fadeIn 1s;
}

/* Add animation (fade in the popup) */
@-webkit-keyframes fadeIn {
  from {opacity: 0;} 
  to {opacity: 1;}
}

@keyframes fadeIn {
  from {opacity: 0;}
  to {opacity:1 ;}
}
/* fim @cgustavoof*/

.sidebar {
  height: 100%;
  width: 0;
  position: fixed;
  z-index: 1;
  top: 0;
  right: 0;
  background-color: #fff;
  box-shadow: 0 0 0 1px rgb(0 0 0 / 5%), 0 4px 20px rgb(0 0 0 / 15%);
  transition: -webkit-transform .5s;
  transition: transform .5s;
  transition: transform .5s,-webkit-transform .5s;
  -webkit-align-items: start;
  align-items: start;
  overflow-x: hidden;
  transition: 0.5s;
  padding-top: 20px;
}

.sidebar a {
  padding: 8px 8px 8px 8px;
  text-decoration: none;
  font-size: 12px;
  color: #fffdfa;
  display: block;
  transition: 0.3s;
}

/* .sidebar a:hover {
      color: #f1f1f1;
    }
*/


div.separator{
  z-index: 2;
    margin: 0.25rem 1.2rem;
    min-height: 1px;
    width: calc(100% - 2rem);
    background-color: #f0f2fc;
}

.sidebar .closebtn {
  position: relative;
    padding: 8px;
    /* top: 0; */
    /* right: 25px; */
    font-size: 12px;
    /* margin-left: 50px; */
    color: rgba(14, 16, 26,0.6);
    display: block;
    
  color: rgba(14, 16, 26,0.6);
}

.sidebar .closebtn:hover{
  --tw-bg-opacity: 1;
  background-color: rgb(229 231 235 / var(--tw-bg-opacity));
}

.sidebar .closebtn span.menuTitle{
  float: right;
  margin-right: 5px;
}

i.icon{
  width: 1rem;
    transition: -webkit-transform .4s linear;
    transition: transform .4s linear;
    transition: transform .4s linear,-webkit-transform .4s linear;
    transform: scale(1);
    align-items: center;
    display: inline-flex;
    fill: #6D758D;
    justify-content: center;
    min-height: calc(2px * var(--rem));
    min-width: calc(2px * var(--rem));
    stroke: #6D758D;
    transition: fill .2s, stroke .2s;
    vertical-align: middle;
    margin-left:5px;
    margin-right:5px;
}

i.icon svg{
  width:12px;
  height:12px;
}


.openbtn {
  --tw-color-opacity: 0.4;
  font-size: 20px;
  cursor: pointer;
  background-color: #FFFFFF;
  color: rgba(14, 16, 26,var(--tw-color-opacity));
  padding: 6px 12px 4px;
  border: none;
  min-height: 2rem;
  border-radius: 1rem;
  box-shadow: 0 0 0 1px rgb(0 0 0 / 5%), 0 1px 8px rgb(0 0 0 / 15%);
  transition-timing-function: ease-in-out;
  pointer-events: all;
  position: fixed;
  top: 20px;
  right: 10px;
}

.openbtn:hover {
  background-color: rgba(14, 16, 26,0.2);
  --tw-color-opacity: 0.6;
}

#main {
  transition: margin-left .5s;
  padding: 16px;
}

.element-fixed {
  position: fixed;
  bottom: 0;
  right: 0;
}

// .sidebar-ctnt{
//     overflow:auto;
// }




/* On smaller screens, where height is less than 450px, change the style of the sidenav (less padding and a smaller font size) */
@media screen and (max-height: 450px) {
  .sidebar {padding-top: 15px;}
  .sidebar a {font-size: 18px;}
}



/*css para os elementos que colapsam dentro do sidebar */


.collapsible {

  --tw-bg-opacity: 0.5;
    background-color: rgb(79 70 229 / var(--tw-bg-opacity));
  /*background-color: #3f92b7;*/
  /*color: white;*/
  color:#0E101A;
  cursor: pointer;
  padding: 18px;
  /*width: 100%;*/
  border: none;
  text-align: left;
  outline: none;
  font-size: 15px;
  border-radius: 8px;
}

.active-colaps, .collapsible:hover {
  /*background-color: #257598;*/
  --tw-bg-opacity: 0.9;
    color: white;
}

.content-colaps {
  padding: 0 18px;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.2s ease-out;
  /*background-color: #5199b9;*/

}


/*css para os elementos dentro do popUp */


#popup{
  display:none;
  background-color: white;
  position: absolute;
  top: 0px;
  z-index: 9999;
  box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
  border-radius: 10px;
  min-width: 630px;
  min-height: 415px;

}
#popup_content,#popup_bar{
  padding: 1rem;
}
#popup_content{
  /*height: -webkit-fill-available;*/
  height: 65%;
  top: 0;
  left: 0;
  display: flex;
  position: relative;
}

#popup_sidebar {
  /*background-color: #005980 !important;*/
  width: 30% !important;
  top: 0 !important;
  left: 0 !important;
  overflow: auto;
  margin-right:10px
}

#popup_main {
  width: 67%;
  border-left: 2px solid #d8d9e2;
  box-shadow: rgb(204, 219, 232) 3px 3px 6px 0px inset, rgba(255, 255, 255, 0.5) -3px -3px 6px 1px inset;
}

#popup_sidebar_element{
  text-align: center;
  justify-content: center;
  /*background-color: aliceblue;*/
  box-shadow: rgba(0, 0, 0, 0.15) 1.95px 1.95px 2.6px;
  height: 40px;
  align-items: center !important;
  display: flex;
  font-family: Arial;
  font-weight: bold;
  color: #626262;
  cursor: pointer;
  margin-bottom: 3px;
  padding: 15px 5px;
  --psel-bg-opacity: 0;
  background-color: rgb(79 70 229 / var(--psel-bg-opacity));
}

#popup_sidebar_element:hover{
  --psel-bg-opacity: 0.9;
  color:white;
}

#popup_bar{
  /*background-color: #0078aa;*/
  --tw-bg-opacity: 0.9;
  background-color: rgb(79 70 229 / var(--tw-bg-opacity));
  position: relative;
  top: 0;
  border-radius: 10px 10px 0 0;
  text-align: center;
  cursor: move;
  font-family: Arial;
  font-weight: bold;
  color: #e7e7e7;
  justify-content: center !important;
  align-items: center !important;
  display: flex;

}

#btn_close, .closeIconSug {
  cursor: pointer;
  display: inline-block;
  border-radius: 1rem;
  --tw-bg-opacity: 0;
  background-color: rgb(79 70 229 / var(--tw-bg-opacity));
}

#btn_close:hover{
  --tw-bg-opacity: 1;
}
.closeIconSug:hover{
  --tw-bg-opacity: 0.6;
}

#btn_close i.icon, .closeIconSug i.icon{
  fill:#ffffff;
  stroke:#ffffff;
  color: #ffffff;
}

.closeIconSug{
  float: right;
  margin: 6px;
}

#popup_main_text{
  margin: 20px;
  margin-bottom: 40px;
  overflow: auto;
  height: -webkit-fill-available;
  width: -webkit-fill-available;
  position: absolute;
}

#popup_title {
  width: 95%;
  display: inline-block;
}


#popup_main_menu{
  position: absolute;
  bottom: 0;
  right: 0;
  margin: 10px;
}



#popup_sidebar_juris_element{
  margin-bottom: 5px;
  display: flex;
  justify-content: left;
  /*background-color: #8ecaff;*/
  width: 100%;
  padding: 10px 5px;
  cursor:pointer;
  border-bottom: 2px solid #d8d9e2;
  --tw-bg-opacity: 0;
  background-color: rgb(229 231 235 / var(--tw-bg-opacity));
}

#popup_sidebar_juris_element:hover{
  --tw-bg-opacity: 1;
}

.dialog-overlay{
  display:none;
  position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1200;
    background-color: rgba(0,0,0,.5);
    transition: opacity .15s linear;
}

.resizable {
  position: relative;
}
.resizer {
  /* All resizers are positioned absolutely inside the element */
  position: absolute;
}

/* Placed at the right side */
.resizer-r {
  cursor: col-resize;
  height: 100%;
  right: 0;
  top: 0;
  width: 5px;
}

/* Placed at the bottom side */
.resizer-b {
  bottom: 0;
  cursor: row-resize;
  height: 5px;
  left: 0;
  width: 100%;
}

.button {
  font-family: inherit;
  font-size: 100%;
  font-weight: inherit;
  line-height: inherit;
  color: inherit;
  margin: 0;
  padding: 0;
  text-transform: none;
  background-image: none;
  cursor: pointer;
  box-sizing: border-box;
  border-width: 0;
  border-style: solid;
  border-color: #e5e7eb;
}

.pointer-events-auto {
  pointer-events: auto;
}

.text-white {
  --tw-text-opacity: 1;
  color: rgb(255 255 255 / var(--tw-text-opacity));
}


.leading-5 {
  line-height: 1.25rem;
}

.font-semibold {
  font-weight: 600;
}

.text-\[0\.8125rem\] {
  font-size: 0.8125rem;
}

.px-3 {
  padding-left: 0.75rem;
  padding-right: 0.75rem;
}

.py-2 {
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
}

.bg-indigo-600 {
  --tw-bg-opacity: 1;
  background-color: rgb(79 70 229 / var(--tw-bg-opacity));
}

.hover\:bg-indigo-500:hover {
  --tw-bg-opacity: 1;
  background-color: rgb(99 102 241 / var(--tw-bg-opacity));
}

#popup_main_copyBtn:hover{
  --tw-bg-opacity: 1;
  background-color: rgb(99 102 241 / var(--tw-bg-opacity));
}

.rounded-md {
  border-radius: 0.375rem;
}

.items-center {
  align-items: center;
}

.flex {
  display: flex;
}

.p-4 {
  padding: 1rem;
}

.gap-3 {
  gap: 0.75rem;
}

.justify-between {
  justify-content: space-between;
}

.space-x-2 > :not([hidden]) ~ :not([hidden]) {
  --tw-space-x-reverse: 0;
  margin-right: calc(0.5rem * var(--tw-space-x-reverse));
  margin-left: calc(0.5rem * calc(1 - var(--tw-space-x-reverse)));
}

`;


  const styleSidebar = document.createElement('style');
  styleSidebar.textContent = styleContentSidebar;
  //const x = document.querySelector("iframe").contentWindow;
  let headMainPage = document.querySelector("head");
  let bodyMainPage = document.querySelector("body");
  headMainPage.appendChild(styleSidebar);


  bodyMainPage.insertAdjacentHTML("afterend",
    `

   
    <div id="mySidebar" class="sidebar font-sans">
        <a href="javascript:void(0)" class="closebtn"><i class="icon closeIconExpanded " aria-hidden="true"><svg viewBox="0 0 24 24"><path fill="currentColor" d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z" /></svg></i><span class="menuTitle">Fechar</span></a>
        <div class="separator"></div>
        <div class="sidebar-ctnt"></div>
    </div>

    <button class="openbtn"><svg style="width:24px;height:24px" viewBox="0 0 24 24">
    <path fill="currentColor" d="M5,13L9,17L7.6,18.42L1.18,12L7.6,5.58L9,7L5,11H21V13H5M21,6V8H11V6H21M21,16V18H11V16H21Z" />
</svg>
<!-- SVG da Logo -->
<svg xmlns="http://www.w3.org/2000/svg" version="1.0" viewBox="0 0 375 375" style="
width: 28px;">
  <defs>
    <clipPath id="e">
      <path d="M5.328 5.328h359.82v359.82H5.328Zm0 0"/>
    </clipPath>
    <clipPath id="f">
      <path d="M185.238 5.328c-99.363 0-179.91 80.547-179.91 179.91 0 99.36 80.547 179.91 179.91 179.91 99.36 0 179.91-80.55 179.91-179.91 0-99.363-80.55-179.91-179.91-179.91"/>
    </clipPath>
    <clipPath id="g">
      <path d="M383.574 170.574c0 117.637-95.363 213-213 213s-213-95.363-213-213 95.364-213 213-213c117.637 0 213 95.364 213 213Zm0 0"/>
    </clipPath>
    <clipPath id="b">
      <path d="M0 0h375v376H0z"/>
    </clipPath>
    <radialGradient id="d" cx="213.001" cy="213.001" r="213.001" fx="213.001" fy="213.001" gradientTransform="matrix(1 0 0 -1 -42.426 417.466)" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#4F46E5"/>
      <stop offset="1" stop-color="#4F46E5"/>
    </radialGradient>
    <pattern id="h" width="375" height="376" x="0" y="0" patternTransform="matrix(1 0 0 -1 0 375.04)" patternUnits="userSpaceOnUse" preserveAspectRatio="xMidYMid meet">
      <g clip-path="url(#b)" mask="url(#c)">
        <path fill="url(#d)" d="M-82.5-82.46h540v540h-540z"/>
      </g>
    </pattern>
    <filter id="a" width="100%" height="100%" x="0%" y="0%">
      <feColorMatrix color-interpolation-filters="sRGB" values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 1 0"/>
    </filter>
    <mask id="c">
      <g filter="url(#a)"/>
    </mask>
  </defs>
  <g clip-path="url(#e)">
    <g clip-path="url(#f)">
      <path fill="#5271ff" d="M5.328 5.328h359.82v359.82H5.328Zm0 0"/>
    </g>
  </g>
  <g clip-path="url(#g)">
    <path fill="url(#h)" d="M-37.5-37.5h450v450h-450z"/>
  </g>
  <path fill="#fff" d="M95.314 144.055c-.184-.457-.368-1.012-.551-1.379-1.473-4.781-5.887-8.184-10.942-8.184-2.3 0-4.507.645-6.347 1.934-.551.273-1.012.64-1.38.918-1.378 1.195-2.757 3.402-4.046 6.71l-25.656 63.727c-.274.829-.368 1.657-.184 2.208.094.554.555 1.382 2.024 1.382h10.117c1.195 0 2.113-.738 2.574-1.933l5.242-13.149h20.137c1.012 0 1.933-.46 2.39-1.289.555-.734.645-1.746.372-2.664l-3.313-8.187c-.46-1.102-1.473-1.836-2.668-1.836H71.681l11.773-29.797c.09-.184.184-.274.184-.274h.367l.09.184 22.808 56.922c.457 1.285 1.38 2.023 2.664 2.023h9.84c1.473 0 1.84-.922 2.024-1.382.183-.551.093-1.38-.278-2.208ZM151.96 135.504h-8.462c-.734 0-2.574.367-2.574 3.219v69.43c0 2.847 1.84 3.218 2.574 3.218h8.461c.739 0 2.575-.37 2.575-3.218v-69.43c0-2.852-1.836-3.219-2.575-3.219ZM226.907 197.668h-29.886c-1.934 0-3.497-.183-4.782-.644-1.105-.368-2.023-1.012-2.668-2.024-.738-1.011-1.289-2.39-1.562-4.047-.371-1.836-.461-4.136-.461-6.894v-45.336c0-2.942-1.84-3.219-2.574-3.219h-8.461c-.828 0-2.668.277-2.668 3.219v43.773c0 5.149.46 9.563 1.289 13.149.828 3.68 2.113 6.715 3.953 9.011 1.84 2.391 4.23 4.137 7.172 5.149 2.762 1.012 6.254 1.566 10.3 1.566h30.348c.824 0 2.574-.37 2.574-3.218v-7.266c0-2.852-1.75-3.219-2.574-3.219ZM298.079 144.055c-.184-.457-.367-1.012-.551-1.379-1.473-4.781-5.887-8.184-10.941-8.184-2.301 0-4.508.645-6.348 1.934-.55.273-1.012.64-1.379.918-1.379 1.195-2.758 3.402-4.047 6.71l-25.656 63.727c-.274.829-.367 1.657-.184 2.208.094.554.555 1.382 2.024 1.382h10.117c1.195 0 2.113-.738 2.574-1.933l5.242-13.149h20.137c1.012 0 1.934-.46 2.39-1.289.555-.734.645-1.746.372-2.664l-3.313-8.187c-.46-1.102-1.472-1.836-2.668-1.836h-11.402l11.773-29.797c.09-.184.184-.274.184-.274h.367l.09.184 22.809 56.922c.457 1.285 1.379 2.023 2.664 2.023h9.84c1.472 0 1.84-.922 2.023-1.382.184-.551.094-1.38-.277-2.208Zm0 0"/>
</svg>
</button>  

    <div id="smoke" class="dialog-overlay">&nbsp;</div>
    
    <div id="popup" class="font-sans">
      <div id="popup_bar" ><div id="popup_title">Consulta Legislação </div> <span id="btn_close"><i class="icon closeIconExpanded " aria-hidden="true"><svg style="width:24px;height:24px" viewBox="0 0 24 24">
      <path fill="currentColor" d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z" />
  </svg></i></span></div>
      
      <div id="popup_content">
        <div id="popup_sidebar">
          
        </div>

        <div id="popup_main">
          <div id="popup_main_text">
          </div>

        </div>

        
        <div class="resizer resizer-r"></div>
        <div class="resizer resizer-b"></div>
      </div>
      <div id="popup_footer" class="flex gap-3 p-4 justify-between">
          <div id="popup_main_menu">
            <button id="popup_main_copyBtn" class="button flex items-center space-x-2 pointer-events-auto rounded-md bg-indigo-600 py-2 px-3 text-[0.8125rem] font-semibold leading-5 text-white hover:bg-indigo-500"><svg style="width:24px;height:24px" viewBox="0 0 24 24">
            <path fill="currentColor" d="M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z" />
        </svg> <span>Copiar Texto</span></button>
          </div>
        </div>
    </div>
`);

  const closebtn = document.querySelector(".closebtn");
  const openbtn = document.querySelector(".openbtn");
  closebtn.addEventListener("click", closeNav);
  openbtn.addEventListener("click", openNav)

}
function openNav() {
  document.getElementById("mySidebar").style.width = "250px";
  //document.getElementById("main").style.marginLeft = "0px";
}

function closeNav() {
  document.getElementById("mySidebar").style.width = "0";
  //document.getElementById("main").style.marginLeft= "0";
}