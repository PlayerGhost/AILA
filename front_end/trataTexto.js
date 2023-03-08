
var bodyifr;
var body;
var sidebarCtn;
var ifr;
var sidebar;
var caret;
var setCaret;


if (typeof caret === 'undefined') {
    caret = () => {
        const range = document.querySelector("iframe").contentDocument.getSelection().getRangeAt(0);
        const prefix = range.cloneRange();
        prefix.selectNodeContents(bodyifr);
        prefix.setEnd(range.endContainer, range.endOffset);
        return prefix.toString().length;
    };
}

if (typeof setCaret === 'undefined') {
    setCaret = (pos, parent = bodyifr) => {
        for (const node of parent.childNodes) {
            if (node.nodeType == Node.TEXT_NODE) {
                if (node.length >= pos) {
                    const range = document.querySelector("iframe").contentDocument.createRange();
                    const sel = document.querySelector("iframe").contentDocument.getSelection();
                    range.setStart(node, pos);
                    range.collapse(true);
                    sel.removeAllRanges();
                    sel.addRange(range);
                    return -1;
                } else {
                    pos = pos - node.length;
                }
            } else {
                pos = setCaret(pos, node);
                if (pos < 0) {
                    return pos;
                }
            }
        }
        return pos;
    };
}

console.info("Verificando se o plugin está ativado: ", localStorage.getItem("pluginAtivado"));
if (localStorage.getItem("pluginAtivado")) {
    trataTexto();
};

function trataTexto() {
    //let body = document.querySelector("body")
    ifr = document.querySelector("iframe").contentWindow;
    const pagAtual = document;
    sidebar = document.getElementById("mySidebar");
    sidebarCtn = document.querySelector(".sidebar-ctnt");

    bodyifr = ifr.document.querySelector("body");



    body = bodyifr;
    let VetAuxSubs = [];
    //@ mudei aqui para receber dado simulado
    bodyifr.addEventListener('input', enviaTrataTexto);

    //bodyifr.addEventListener('input', recebeTrataTexto(dadoSaidaFake["extensao"]["dadoSaidaJson"]));



    let btnCopyPUtxt = document.querySelector("#popup_main_copyBtn")
    btnCopyPUtxt.addEventListener('click', function () {
        let textPopUp = document.querySelector("#popup_main_text");
        copiarClipboard(textPopUp)
    })

    //@cgustavoof - click do popup de sugestao
    bodyifr.addEventListener('click', function (e) {
        for (let element of document.getElementsByClassName('popuptext show')) {
            element.classList.toggle("show");
        }

        if (e.target.tagName == 'MARK') {
            if (e.target.id.includes('mark_') == true)
                popup_sugestao(document, e.target.id.replaceAll('mark_', 'popuptext_'), e.clientY + "px", e.clientX + "px")
        } else if (e.target.tagName == 'A') {
            substituir(e.target);
        } else if (e.target.tagName == 'IMG') {
            ignorar(e.target);
        }
    });

    bodyifr.focus();
    const pos = caret();
    bodyifr.innerHTML = bodyifr.innerText + '';
    setCaret(pos);
    //@cgustavoof


    let btnOriginalFunction;
    interceptOnClick()

    bodyifr.parentElement.oncopy = function (e) {
        //alert('prestes a copiar: ' + window.getSelection().toString());
        //let copiado = window.getSelection().toString()
        let copiado = ifr.getSelection().toString()
        navigator.clipboard.writeText(copiado)
            .then(() => {
                console.log("Texto copiado para memória...")
            })
            .catch(err => {
                console.log('Algo de errado', err);
            })
        console.log(copiado)
    }

    bodyifr.addEventListener("keydown", function (ev) {
        //console.log("detec-Keydown")
        // capturando o evento da janela
        ev = ev || window.event;  // Objeto evento 'ev'
        var key = ev.which || ev.keyCode; // Detectando keyCode

        // Detectando Ctrl
        var ctrl = ev.ctrlKey ? ev.ctrlKey : ((key === 17)
            ? true : false);

        if (key == 67 && ctrl) {

            // Se pressionado o C e o ctrl é true.
            console.log("Ctrl+C is pressed.");

            //let text = document.getElementById("demo").innerText;
            //console.log(document.getElementById("demo"))
            //console.log(text);
        }

    }, false);
}

function insertAfter(newNode, existingNode) {
    existingNode.parentNode.insertBefore(newNode, existingNode.nextSibling);
}

function interceptOnClick() {
    const pagAtual = document;
    let buttonSalvar = pagAtual.querySelector("#j_id608");
    btnOriginalFunction = buttonSalvar.getAttribute("onClick");
    //console.log("button-salvar-onclick:"+(buttonSalvar.getAttribute("onClick")=''));

    buttonSalvar.removeAttribute("onClick")
    buttonSalvar.removeAttribute("click")


    buttonSalvar.setAttribute("onclick", `(()=>{

        const ifr = document.querySelector("iframe").contentWindow;
        let bodyifr = ifr.document.querySelector("body");

        //pega todas as sugestões ainda não marcadas e converte pra texto(como se ignorase todas)
    let divSugVigent = bodyifr.querySelectorAll(".sugestao");
    for (let i = 0; i < divSugVigent.length; i++) {
        let textoelement = divSugVigent[i].childNodes[0].innerText;
        let textoSugNode = document.createTextNode(textoelement);
        divSugVigent[i].parentNode.replaceChild(textoSugNode, divSugVigent[i]);
    }

    //pega todas as sugestões substituidas e converte tra texto(como se ignorase todas)
    let elementsJaSubs = bodyifr.querySelectorAll(".j_su");
    for (let i = 0; i < elementsJaSubs.length; i++) {
        let textoelement = elementsJaSubs[i].innerText;
        let textoSugNode = document.createTextNode(textoelement);
        elementsJaSubs[i].parentNode.replaceChild(textoSugNode, elementsJaSubs[i]);
    }

    })();`+ btnOriginalFunction);
}

function enviaTrataTexto() {
    //pega todas as sugestões ainda não marcadas e converte tra texto(como se ignorase todas)
    console.log("Enviando o texto digitado...")
    let elementsJaSubs = body.querySelectorAll(".j_su");
    for (let i = 0; i < elementsJaSubs.length; i++) {
        VetAuxSubs[i] = elementsJaSubs[i].innerText;
        elementsJaSubs[i].innerText = '';
        //console.log(elementsJaSubs[i]);
    }

    let texto = bodyifr.innerText;

    elementsJaSubs = body.querySelectorAll(".j_su");
    for (let i = 0; i < elementsJaSubs.length; i++) {
        elementsJaSubs[i].innerText = VetAuxSubs[i]
    }

    console.debug("texto:" + texto)
    //----para o sinapses-----------------------
    let mensagemSinapse = { "mensagem": { "tipo": "TEXTO_PURO", "conteudo": texto } }
    let dado = mensagemSinapse
    //--------testando localmmente-----------------
    //var dado = { "texto": texto };

    let dadoJson = JSON.stringify(dado);

    let xhr = new XMLHttpRequest();
    let url = "http://18.214.121.114:5001/aila";
    // var url = "http://192.168.68.114:5001/tratatexto";
    // let url = "https://sinapses-backend.ia.pje.jus.br/rest/modelo/executarServico/-cnj-pnud-acad-unifor/GEN_TRATA_TEXTO_UNIFOR/1";
    const method = "POST";
    xhr.open(method, url);

    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader('Authorization', 'Basic NjQyNzY2NDMzNjg6Z3VnYUAxOTEyNzk=');


    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status == 200) {
            //Comentato apenas para puxar os dados fake
            let dadoSaidaJson = JSON.parse(xhr.responseText);
            console.debug("Dados enviados pelo serviço:", dadoSaidaJson)

            //recebeTrataTexto(dadoSaidaJson["dado_saida_json"]);
            recebeTrataTexto(dadoSaidaJson["extensao"]["dadoSaidaJson"]);
        }
    }

    xhr.send(dadoJson);

}

function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

function copiarClipboard(element) {
    console.debug("elemento copiar" + element.innerText)
    navigator.clipboard.writeText(element.innerText);
}



//@cgustavoof - show popup sugestao
function popup_sugestao(parent, id, top, left) {
    pp = parent.getElementById(id)
    pp.style.left = left;
    pp.style.top = top;
    pp.classList.toggle("show");
}

//@cgustavoof - substituir texto por sugestao
function substituir(element) {
    arr = element.id.split('_');
    id = arr[1] + '_' + arr[2];
    div = ifr.document.getElementById('mark_' + id);
    div.id = 'markAlterado_' + id;
    div.classList.toggle('marcador');
    div.innerText = element.innerText;

    var elem = document.getElementById('popuptext_' + id);
    if (elem) elem.remove();

    enviaTrataTexto();
}

//@cgustavoof - ignorar sugestao
function ignorar(element) {
    arr = element.id.split('_');
    id = arr[1] + '_' + arr[2];
    div = ifr.document.getElementById('mark_' + id);
    div.id = 'markIgnorado_' + id;
    div.classList.toggle('marcador');

    var elem = document.getElementById('popuptext_' + id);
    if (elem) elem.remove();
}

//@cgustavoof - criar marcador
function criarMarcador(dado, id) {
    if (dado['tipo'] == 'sugestao_dispositivo' || dado['tipo'] == 'sugestao_artigo' || dado['tipo'] == 'consulta_legislacao') {
        marcador = document.createElement("mark");
        marcador.setAttribute('id', 'mark_' + id)
        marcador.setAttribute('class', ' marcador')
        marcador.appendChild(document.createTextNode(dado['marcador']));

        span = document.createElement("span");
        span.setAttribute('class', 'popuptext');
        span.setAttribute('id', 'popuptext_' + id);

        conteudoSug = document.createElement("div");
        conteudoSug.setAttribute('class', 'detailpopup');

        //Header do popup
        divHeader = document.createElement("div");
        divHeader.setAttribute('class', 'popupHeader');
        divHeader.setAttribute('id', 'popupHeader' + id);
        conteudoSug.appendChild(divHeader);

        //Body do popup
        divBody = document.createElement("div");
        divBody.setAttribute('class', 'popupBody');
        divBody.setAttribute('id', 'popupBody' + id);
        conteudoSug.appendChild(divBody);

        strong = document.createElement("b")
        strong.appendChild(document.createTextNode('Sugestão:'));
        divBody.appendChild(strong);
        divBody.appendChild(document.createElement("br"));
        divBody.appendChild(document.createElement("br"));

        for (var i = 0; i < dado['sugestoes'].length; i++) {
            sugElement = document.createElement("a");
            sugElement.setAttribute('class', 'linksug sugestao');
            sugElement.setAttribute('title', 'Clique aqui para aceitar a sugestão');
            sugElement.setAttribute("id", 'a' + String(i) + '_' + id);
            sugElement.setAttribute("contenteditable", "false");
            sugElement.appendChild(document.createTextNode(dado['sugestoes'][i]));

            sugElement.addEventListener('click', function () {
                substituir(this);
            });

            divBody.appendChild(sugElement);
            divBody.appendChild(document.createElement("br"));
        }
        divBody.appendChild(document.createElement("br"));

        sugElementIgn = document.createElement("a");
        sugElementIgn.setAttribute("class", "closeIconSug");
        sugElementIgn.setAttribute("title", "Rejeitar a sugestão");
        sugElementIgn.setAttribute("contenteditable", "false");
        sugElementIgn.setAttribute("id", 'icon_' + id);

        imgIcon = document.createElement("i");
        imgIcon.setAttribute('class', 'icon closeIconExpanded');
        imgIcon.setAttribute('aria-hidden', 'true');
        imgIcon.setAttribute("id", '1icon_' + id);
        imgIcon.innerHTML = "<svg style=\"width:24px;height:24px\" viewBox=\"0 0 24 24\"><path fill=\"currentColor\" d=\"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z\" />";
        //imgIcon.src = chrome.runtime.getURL('/icons/ignore.png');
        //imgIcon.setAttribute("style", "width:12px;height:12px;");
        sugElementIgn.appendChild(imgIcon);

        sugElementIgn.addEventListener('click', function () {
            ignorar(this);
        });
        divHeader.appendChild(sugElementIgn);

        span.appendChild(conteudoSug)

        var elem = document.getElementById('popuptext_' + id);
        if (elem) elem.remove();
        document.body.appendChild(span);

        return marcador.outerHTML
    }
}

//@cgustavoof - marcar as palavras
function marcarPalavras(dado, texto) {
    if (dado['posicao'][0][0])
        id = dado['posicao'][0][0] + '_' + dado['posicao'][0][1];
    else
        id = dado['posicao'][0] + '_' + dado['posicao'][1];

    texto = texto.replaceAll(dado['marcador'], criarMarcador(dado, id));
    texto = texto.split('\n').join('<br/>');

    return texto
}
//@cgustavoof

function recebeTrataTexto(dados) {
    console.log(dados);

    let anch;
    let text_node_anch = "";
    //let sidebar;
    if (sidebarCtn.childNodes.length > 0) {
        removeAllChildNodes(sidebarCtn);
    }
    //sidebar.removeChild()

    texto = bodyifr.innerText
    for (let i = 0; i < dados.length; i++) {
        if (dados[i]['tipo'] == 'sugestao_dispositivo' || dados[i]['tipo'] == 'sugestao_artigo' || dados[i]['tipo'] == 'consulta_legislacao') {
            console.debug("Consulta elegível para marcação");
            const pos = caret();
            texto = marcarPalavras(dados[i], texto);
            bodyifr.innerHTML = texto;
            setCaret(pos);
        }

        //verificar o tipo do objeto
        if (dados[i]['tipo'] == 'consulta_legislacao' || dados[i]['tipo'] == 'consulta_dispositivo') {
            ///if(dados[i]['tipo'] == 'consulta_dispositivo'){}
            anch = document.createElement("a");
            text_node_anch = document.createTextNode(dados[i]['marcador'])

            buttonColap = document.createElement("div");
            buttonColap.setAttribute("class", "collapsible");
            buttonColap.appendChild(text_node_anch);


            anch.appendChild(buttonColap);

            anch.setAttribute("id", "id_" + dados[i]['marcador'].replace(/[^a-zA-Z0-9]/g, '_'));

            anch.addEventListener('click', function () {
                chamarPopUp(dados[i]);
            });
            sidebarCtn.appendChild(anch);
        }
    }
    anch = document.createElement("a");
    text_node_anch = document.createElement("br")
    anch.appendChild(text_node_anch);
    text_node_anch = document.createElement("br")
    anch.appendChild(text_node_anch);
    sidebarCtn.insertAdjacentHTML("beforeend", anch.outerHTML);

}


function chamarPopUp(dado) {
    // smoke
    spreadSmoke(true);
    // reset div position

    let popMainTxt = document.querySelector("#popup_main_text")
    let popTitle = document.querySelector("#popup_title")
    //let dadoTxt = document.createTextNode(dado['sugestoes'])
    popTitle.innerText = dado['marcador'];



    //---- adicionar conteudo no sidebar do pop up ----

    let txtElementSideBar;
    if (dado['tipo'] == 'consulta_legislacao') {
        txtElementSideBar = 'legislação'
        popMainTxt.innerText = dado['sugestoes'];
        createPopUpSidebarElement(txtElementSideBar, dado['sugestoes'])

        if (dado['jurisprudencias'] != undefined) {
            if (dado['jurisprudencias'].length != 0) {
                if (dado['jurisprudencias']['posicionamentos_agrupados_stj'].length != 0) {
                    let aux_data = dado['jurisprudencias']['posicionamentos_agrupados_stj'];
                    createPopUpSidebarElementJurisprud('posicionamentos agrupados stj', aux_data);
                }
                if (dado['jurisprudencias']['posicionamentos_isolados_stj'].length != 0) {
                    let aux_data = dado['jurisprudencias']['posicionamentos_isolados_stj'];
                    createPopUpSidebarElementJurisprud('posicionamentos isolados stj', aux_data);
                }
            }
        }
    }

    if (dado['tipo'] == 'consulta_dispositivo') {
        txtElementSideBar = 'dispositivo'
        popMainTxt.innerText = dado['sugestoes'];
        createPopUpSidebarElement(txtElementSideBar, dado['sugestoes'])
    }


    popup.style.top = (window.innerHeight / 2 - SCROLL_WIDTH) / 2 + "px";
    popup.style.left = (window.innerWidth / 2 - SCROLL_WIDTH) / 2 + "px";
    popup.style.width = window.innerWidth / 2 - SCROLL_WIDTH + "px";
    popup.style.height = window.innerHeight / 2 - SCROLL_WIDTH + "px";
    popup.style.display = "block";
}

function createPopUpSidebarElement(txtElementSideBar, contentText4Main) {
    let popMainTxt = document.querySelector("#popup_main_text")
    let popSidebar = document.querySelector("#popup_sidebar");

    popSideElement = document.createElement("div");
    popSideElement.setAttribute("id", "popup_sidebar_element");
    popSideElement_txt = document.createTextNode(txtElementSideBar);
    popSideElement.appendChild(popSideElement_txt);
    popSideElement.addEventListener('click', function () {
        popMainTxt.innerText = contentText4Main;
    });
    popSidebar.appendChild(popSideElement);
}

function createPopUpSidebarElementJurisprud(txtElementSideBar, dadosJuris) {
    let popSidebar = document.querySelector("#popup_sidebar");
    //console.log(dadosJuris);

    popSideElement = document.createElement("div");
    popSideElement.setAttribute("id", "popup_sidebar_element");
    popSideElement_txt = document.createTextNode(txtElementSideBar);
    popSideElement.appendChild(popSideElement_txt);
    popSideElement.addEventListener('click', function () { //colocar a função de sumir e voltar
        //popMainTxt.innerText = contentText4Main;
        this.classList.toggle("active-colaps");
        var content = this.nextElementSibling;
        if (content.style.maxHeight) {
            content.style.maxHeight = null;
        } else {
            content.style.maxHeight = content.scrollHeight + "px";
        }
    });
    popSidebar.appendChild(popSideElement);

    //---'posicionamentos_agrupados_stj'---
    let colapsedJurisprud = document.createElement("div");
    colapsedJurisprud.setAttribute("class", "content-colaps");
    //colapsedJurisprud.setAttribute("id", "popup_sidebar_colapsed_element");

    for (let i = 0; i < dadosJuris.length; i++) {
        //console.log(dadosJuris[i]['titulo']);
        let jurisElement = document.createElement("div");
        jurisElement.setAttribute("id", "popup_sidebar_juris_element");//
        let jurisElement_txt = document.createTextNode(dadosJuris[i]['titulo']);
        jurisElement.appendChild(jurisElement_txt);
        jurisElement.addEventListener('click', function () { //colocar a função de chamar cabeçalho jurisprud na main pop up
            //popMainTxt.innerText = contentText4Main;
            createJurisprudMainTxt(dadosJuris[i]);
        });
        colapsedJurisprud.appendChild(jurisElement);
    }
    popSidebar.appendChild(colapsedJurisprud);

    // cria elementos escondidos das jurisprudencia



}

function createJurisprudMainTxt(dadosJuris) {

    let popMainTxt = document.querySelector("#popup_main_text")

    let jurisTxt = document.createElement("div");

    let jurisTitulo = document.createElement("div");
    let jurisTitulo_txt = document.createTextNode("Título: " + dadosJuris['titulo']);
    jurisTitulo.appendChild(jurisTitulo_txt);

    let jurisData = document.createElement("div");
    let jurisData_txt = document.createTextNode("Data: " + dadosJuris['data_publicacao']);
    jurisData.appendChild(jurisData_txt);

    let jurisRelator = document.createElement("div");
    let jurisRelator_txt = document.createTextNode("Relator: " + dadosJuris['relator']);
    jurisRelator.appendChild(jurisRelator_txt);

    let jurisHR = document.createElement("hr");

    let jurisConteudo = document.createElement("div");
    //let jurisConteudo_txt = document.createTextNode(dadosJuris['conteudo']);
    let jurisConteudo_txt = document.createRange().createContextualFragment(dadosJuris['conteudo']);//para aproveitar o html ja existente na jurisprudencia
    jurisConteudo.appendChild(jurisConteudo_txt);

    jurisTxt.appendChild(jurisTitulo);
    jurisTxt.appendChild(jurisData);
    jurisTxt.appendChild(jurisRelator);
    jurisTxt.appendChild(jurisHR);
    jurisTxt.appendChild(jurisConteudo);



    popMainTxt.innerHTML = jurisTxt.outerHTML;

}
