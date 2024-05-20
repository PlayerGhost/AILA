const form = document.querySelector('form');//pega o form do popup da extensão
const btnAtivar = document.getElementById('ativar');
const btnDesativar = document.getElementById('desativar');

btnDesativar && btnDesativar.addEventListener("click", function () {
    desativarPlugin();
});


const pluginAtivado = 'pluginAtivado';

async function getStrorage() {
    let [paginaAtual] = await chrome.tabs.query({ active: true, currentWindow: true })

    // Execute script in the current tab
    const fromPageLocalStore = await chrome.scripting.executeScript({
        target: { tabId: paginaAtual.id },
        func: () => {
            return JSON.stringify(localStorage)
        }
    })

    const localStorageItems = fromPageLocalStore[0] ? JSON.parse(fromPageLocalStore[0].result): null;

    if (localStorageItems && localStorageItems.pluginAtivado) {
        btnAtivar.setAttribute("style", "display:none");
        executarPlugin();
    } else {
        btnDesativar.setAttribute("style", "display:none");
    }
}


async function desativarPlugin() {
    let [paginaAtual] = await chrome.tabs.query({ active: true, currentWindow: true })

    // Execute script in the current tab
    chrome.scripting.executeScript({
        target: { tabId: paginaAtual.id },
        func: () => {
            localStorage.removeItem('pluginAtivado')
            console.log('Desativando plugin')
            location.reload()

        }
    })

    window.close();
}

getStrorage();


async function executarPlugin() {
    console.log("Executando plugin");

    const [paginaAtual] = await chrome.tabs.query({ active: true, currentWindow: true });//vai fazer uma busca pelas paginas atuais em execussão

    //crome.scripting insere uma função na pagina atual
    chrome.scripting.executeScript({
        target: { tabId: paginaAtual.id },
        func: () => {
            localStorage.setItem('pluginAtivado',true)
        }
    });
    chrome.scripting.executeScript({
        target: { tabId: paginaAtual.id },
        files: ['jquery.min.js', 'incert-sidebar-css.js', 'trata-texto.js', 'trataTexto.js', 'pop-up-func.js']
    });

    
}

//esse trexo abaixo injeta codigo js na pagina atual que estiver aberto
form && form.addEventListener('submit', async (event) => {//foi transformada em uma função assincrona para esperar o resultado do await
    event.preventDefault();//para previnir que recarregue a pagina "o pop up no caso"
    form.style = "display:none;"
    console.log("Executando o submit", event);
    executarPlugin();
    window.close();
});