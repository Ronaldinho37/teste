from django import template

register = template.Library()
#dict: dicionário com todas eletivas
#nome_da_eletiva: nome da eletiva desejada
def pesquisar_professor(dict,nome_da_eletiva):
    #pegando os professores 
    var = dict.get(f'professor_de_{nome_da_eletiva}')
    #pegando o tamanho da variável acima
    tam_var = len(var)
    #mensagem que retornará uma string contendo os nomes dos professores
    mensagem_final = ''
    if tam_var == 2:
        mensagem_final += f"{var[0].get('nome')} e {var[1].get('nome')}"
    elif tam_var == 1:
        mensagem_final += f"{var[0].get('nome')}"
      #se não for igual a nenhuma das alternativas acima é porque não tem nenhum professor na eletiva 
    else:
        mensagem_final += "Nenhum professor nessa eletiva"
    #retornando a mensagem final
    return mensagem_final
#fazendo o registro da nova tag
register.filter('pesquisar_professor', pesquisar_professor)