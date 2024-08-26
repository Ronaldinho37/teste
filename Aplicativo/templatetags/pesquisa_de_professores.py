from django import template

register = template.Library()

def pesquisar_professor(dict,nome_da_eletiva):
    var = dict.get(f'professor_de_{nome_da_eletiva}')
    tam_var = len(var)
    mensagem_final = ''
    if tam_var == 2:
        mensagem_final += f"{var[0].get('nome')} e {var[1].get('nome')}"
    elif tam_var == 1:
        mensagem_final += f"{var[0].get('nome')}"
    else:
        mensagem_final += "Nenhum professor nessa eletiva"
       
    return mensagem_final

register.filter('pesquisar_professor', pesquisar_professor)