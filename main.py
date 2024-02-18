import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

registers = [["+558199998295", 0, False]]

@app.route('/bot', methods=['POST'])
def bot():
    
    original_msg = request.values.get('Body', '')
    number_requested = request.values.get('From', '')
    number_requested= number_requested[9:]    

    find = False
    
    for i in registers:
        if i[0] == str(number_requested):
            resps_order = i[1]
            find = True
            indice = registers.index(i)
            break

    if find == False:
        new_costumer = []
        new_costumer.append(number_requested)
        new_costumer.append(0)
        new_costumer.append(False)
        registers.append(new_costumer)
        resps_order = 0

    resp= MessagingResponse()
    msg = resp.message()

    lower_msg = original_msg.lower()
    lower_msg = lower_msg.replace(' ', '')
    lower_msg = lower_msg.replace('\n', '')

    
    if resps_order == 0 or lower_msg in ['voltar', 'volta']:
        message = '''Olá!    
                    
Meu nome é Adriana e gostaria de saber se você deseja atendimento para:
                
            1 - Feira Bom Jesus; 
            2 - Feira da Aurora;
        
Digite o número da feira que deseja:'''
        registers[indice][1] = 1
    
    elif resps_order == 1:
        
        if lower_msg in ['1', 'feirabomjesus', 'bomjesus']:
            message = '''\tA Feira Bom Jesus acontece aos domingos das 10:00h às 19:00h, podendo postergar o horário de encerramneto em dias de maior movimento.
                         
Valores: 
   
   Expositores fixos: R$95,00 por semana;
   Expositores extras: R$110,00 por feira;
                              
Você tem interesse em participar? responda com 'S' para sim ou 'N' para não. Ou digite 'voltar' para voltar para o menu inicial. '''
            registers[indice][1] = 2
        
        elif lower_msg in ['2', 'feiradaaurora', 'feiraaurora', 'aurora']:
            message = '''A Feira da Aurora acontece aos Sábados das 15:00h às 20:00h. 
                         
Valor: R$120,00 por feira; 
                            
Você tem interesse em participar? responda com 'S' para sim ou 'N' para não. Ou digite 'voltar' para voltar para o menu inicial.'''
            registers[indice][1] = 2
        
        else:
            message = '''Não entendi! 
                         
Digite o número da feira que deseja: '''
            
    elif resps_order == 2:

            if lower_msg in ['s', 'sim']:
                message = '''Antes de iniciar sua participação você precisa se submeter a uma curadoria e para isso é necessário preencher o formulário abaixo:
Formulário: '''
                registers[indice][1] = 0
            
            elif lower_msg in ['n', 'nao', 'não']:
                message = '''Obrigada pelo contato. Até a próxima'''
                registers[indice][1] = 0
            
            else:    
                message = '''Não entendi!
Você tem interesse em participar? responda com 'S' para sim ou 'N' para não. '''
    msg.body(message)
    return str(resp)

@app.route('/')
def hello_world():
    return 'chat botasasss mais outra uma vez por favor'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


