console.info("Verificando se o plugin está ativado para aplicar estilo css: ", localStorage.getItem("pluginAtivado"));
if (localStorage.getItem("pluginAtivado")) {
  aplicarEstilo();
};

function aplicarEstilo() {
  let styleContent = `

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
}

.marcador {
    display: inline-block;
    position:relative;
    /*background: url(http://i.imgur.com/HlfA2is.gif) bottom repeat-x;*/
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}
.marcador:after {
  border-bottom: 2px solid #FF99AB;
  display: block;
  width: 100%;
  height: 2px;
  background:#FF99AB;
  content: " ";
  animation-name: right-animate;
  animation-duration: 1s;
  border-radius: 1em;
}

.marcador:hover:after {
  border-bottom: 2px solid red;
  background:red;
}
@keyframes right-animate {
  from {width: 0;}
  to {width: 100%;}
}

.marcador:hover {
    background-color: #ffbeb3;
    cursor: pointer;
}

mark {
    // background-color: #04AA6D;
    background-color: white;
    /* padding: 16px; */
    /* font-size: 16px; */
    border: none;
}

.sugestao {
    position: relative;
    display: inline-block;
}

.conteudo_sugestao {
    display: none;
    position: absolute;
    background-color: #04AA6D;
    /* background-color: #f1f1f1; */
    min-width: 300px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
    z-index: 1;
    border-radius: 5%;
   

    height: 145px;
    overflow: auto;
}

::-webkit-scrollbar {
  width: 15px;
}

/* Track */
.conteudo_sugestao::-webkit-scrollbar {
    /* background: transparent; */
    background-color: #f1f1f1;
    border-radius: 10px 10px 10px 0;
}
.conteudo_sugestao::-webkit-scrollbar-track {
  box-shadow: inset 0 0 5px grey; 
  background-color: #f1f1f1;
  border-radius: 10px;
  
}
 
/* Handle */
.conteudo_sugestao::-webkit-scrollbar-thumb {
  background: #c0c0c0; 
  border-radius: 10px;
}

/* Handle on hover */
.conteudo_sugestao::-webkit-scrollbar-thumb:hover {
  background: #a5a5a5; 
}

.conteudo_sugestao a {
    color: black;
    padding: 12px 16px;
    font-weight: bold;
    background-color: #f1f1f1;
    color: #4f4f4f;
    text-decoration: none;
    font-family: Arial;
    display: block;
}

.conteudo_sugestao a:hover {background-color: #ddd;}

.sugestao:hover .conteudo_sugestao {display: block;}

.sugestao:hover mark {background-color: #3e8e41;}

.sugestao_label{
    padding: 2px 16px;
    color: #595959 !important;
    font-weight: bold;
    font-family: Arial;
    
    /* height: fit-content; */
}

`;


  const style = document.createElement('style');
  style.textContent = styleContent;
  const x = document.querySelector("iframe").contentWindow;
  let head = x.document.querySelector("head");
  head.appendChild(style);


  // const script = document.createElement('script');
  // script.src='/trataTexto2.js';
  // script.setAttribute("type", "text/javascript");
  // head.appendChild(script);
  // document.querySelector("body").appendChild(script);
  // document.body

  // let iframe = document.querySelector("iframe").contentWindow
  // let iframebody = iframe.document.querySelector("body").contentWindow

  //document.getElementById('myIframe').src
  //iframe.src='trata-texto.html'






  //--------------------------------------------------------------------------------------------------------------


  // //function replaceText(){//essa função vai ser inserida na pagina em execusão
  //     const x = document.querySelector("iframe").contentWindow;
  //     let teste = x.document.querySelector("body").textContent;
  //     console.log(x);
  //     console.log(teste);
  //     //alert("oi2");
  //     texto=('Nosso plug-in identificou que talvez voce esteja tentando dizer isso\n\n'+
  //     teste+'\n'+'________________________________________\n\n'+"trata texto");

  //     if (confirm(texto)) {

  //         x.document.querySelector("body").textContent = "trata texto";
  //       } else {
  //         txt = "You pressed Cancel!";
  //       }

  //       //aadicionar elemento dentro de html via js
  //       // x.document.querySelector("body").insertAdjacentHTML("afterend",
  //       // "<h3>This is the text which has been inserted by JS</h3>");

  //       x.document.querySelector("body").insertAdjacentHTML("afterend",
  //       "<div class='fab'> + </div>");
  //       x.document.querySelector("head").insertAdjacentHTML("afterend",
  //       "<style>.fab {width: 70px;height: 70px;          background-color: red;       border-radius: 50%;       box-shadow: 0 6px 10px 0 #666;    font-size: 50px;    line-height: 70px;          color: white;        text-align: center;          position: fixed;          right: 50px;          bottom: 50px;                   transition: all 0.1s ease-in-out;       }       .fab:hover {        box-shadow: 0 6px 14px 0 #666;          transform: scale(1.05);       }      </style>");

  // //}

}