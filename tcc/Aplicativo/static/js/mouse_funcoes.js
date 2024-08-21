function entrou(x){
    let div = document.querySelector(`div[id="${x.dataset.id}"]`)
    console.log(div)
    div.style.display = 'flex'
}
function saiu(x){
    let div = document.querySelector(`div[id="${x.dataset.id}"]`)
    div.style.display = 'none'
}