let acao_anterior = []
function desocultar(x){
    let id = x.dataset.id
    let div = document.querySelector(`div[id="botoes-${id}"]`)
    if(acao_anterior.length != 0 && id != acao_anterior[0]){
        let div_anterior = document.querySelector(`div[id="botoes-${acao_anterior[0]}"]`)
        let p_anterior = document.querySelector(`p[id="botao-oculto-${acao_anterior[0]}"]`)
        document.documentElement.style.setProperty(`--display-${acao_anterior[0]}`, "none")
        div_anterior.style.display = "none"
        div_anterior.classList.remove('d_active')
        p_anterior.classList.remove('p_active') 
        acao_anterior = []

    }
    
    
    if(x.getAttribute("class") == 'nav-link'){
        document.documentElement.style.setProperty(`--display-${id}`, "flex")
        div.style.display = ""
        div.classList.add('d_active')
        x.classList.add('p_active')
        acao_anterior.push(id) 
        

    } else {
        div.style.display = "none"
        document.documentElement.style.setProperty(`--display-${id}`, "none")
        div.classList.remove('d_active')
        x.classList.remove('p_active') 
        acao_anterior = []
    }
    
    
    }