let tabela = document.querySelector('table[id="tabela"]').dataset.user

function adicionar_linha(x){
    window.location.href = `/area-restrita/update/${tabela}/${x.id}`
}