import telegram
import logging
import requests
from bs4 import BeautifulSoup
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater
updater = Updater(token="Token")###INSIRA UM TOKEN



dispatcher = updater.dispatcher
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",level=logging.INFO)


### Extrai dados das cartas web do site oficial do jogo
def data_extract(x):
    limit = 1
    number = ''
    page_number = ('http://www.gwentdb.com/cards')
    page= requests.get(page_number)
    bs = BeautifulSoup(page.content,"html.parser")
    Card = []
    Faction = []
    Abilities =  []
    Data_base = []
    i = 0
    while True:
        for link in bs.find_all('img'):
            Card.append(link.get('alt'))
            Card.append(link.get('src'))
            Data_base.append(Card)
            Card = []
        for link in bs.find_all('a', attrs = {"class":"faction-link"}):
            Faction.append(link.get_text())
        for link in bs.find_all('div', attrs = {"class":"card-abilities"}):
            Abilities.append(link.get_text().strip())
        if "Next" in bs.prettify():
            limit = limit + 1
            number = 'cards?page=' + str(limit)
            page_number =('http://www.gwentdb.com/'+ number)
            page= requests.get(page_number)
            bs = BeautifulSoup(page.content,"html.parser")
        else:
            break
    
    if i <= len(Data_base):
        for f in Data_base:
            f.append(Faction[i])
            i = i+1
    i = 0
    if i <= len(Data_base):
        for a in Data_base:
            a.append(Abilities[i])
            i = i+1
            
    return x.extend(Data_base)
###

DIC = {"Monsters":"<b>MONSTROS</b> \n\n O mundo de The Witcher é infestado de horrores indizíveis, e a maioria está reunida na temível facção de Monstros. O mau tempo não prejudica essas feras – na verdade, elas prosperam em condições difíceis. Os Monstros atacam em grandes números, que podem crescer em hordas com a habilidade de procriação e, quando força bruta é necessária, consomem seus semelhantes, absorvendo sua força.",
"Skellige" :"<b>SKELLIGE</b> \n\n Skelligers aceitam a glória da morte, sabendo que suas sacerdotisas e médicos podem invocar os heróis mortos da pilha de descarte para lutar novamente. Um jogador Skellige envia unidades para a pilha de descarte de propósito... só para trazê-las de volta mais fortes do que nunca. Skelligers também usam feridas a seu favor, incitando seus guerreiros sangrentos a atacar com força redobrada.",
"Scoiatael" :"<b>SCOIATAEL</b> \n\nOs Scoiatael são incrivelmente ágeis e capazes de enganar seus inimigos com unidades que podem ser posicionadas em qualquer fileira. Como é próprio de guerrilheiros, eles costumam fazer emboscadas: cartas usadas viradas para baixo que se revelam somente quando a armadilha já foi preparada. Para reforçar seus números, os Scoiatael rapidamente criam novos comandos, neófitos zelosos que pegam o oponente de surpresa.",
"Northern Realms" :"<b>REINOS DO NORTE</b> \n\nOs Reinos do Norte tentam ganhar o controle do campo de batalha reforçando seus números. Seus valorosos comandantes marcham nas linhas de frente para inspirar suas unidades e estimular sua força. Suas tropas podem ser imunizadas contra ataques e feitiços de clima com a promoção a status de ouro, enquanto médicos podem devolver força aos soldados caídos para que eles possam lutar novamente.",
"Nilfgaard" :"<b>NILFGAARD</b> \n\n Mais que qualquer outra facção de GWENT, Nilfgaard se utiliza da diplomacia e de subterfúgios para perturbar as estratégias do inimigo e pôr as suas em prática.\n O império infiltra espiões atrás das linhas inimigas para realizar sabotagem e revelar cartas na mão do oponente. Ciente das vantagens do poder, os nilfgaardianos se focam nas unidades inimigas mais fortes, incapacitando-as ou eliminando-as totalmente"}


BD = []#Lista onde sera armazenado os dados extraidos pela funçãodata_extract   
data_extract(BD)


###Funçoes da API TELEGRAM
def start(bot, update):
    msg = "Ola .... Este é o universo de GWENT... Seja bem vindo \n"
    msg += "Em que posso ser util? \n"
    msg += "Deseja saber sobre as facções ? Use o comando /faction e escolha uma ou se quer apenas dar uma pesquisada..."
    msg += "basta digitar o nome de uma carta!                                "
    bot.sendMessage(chat_id=update.message.chat_id, text = msg)
 
def pesquisa(bot, update):
    c = 0
    if update.message.text in ["Monsters", "Scoiatael", "Skellige" ,"Northern Realms" ,"Nilfgaard"] :
        bot.sendMessage(chat_id=update.message.chat_id, text = DIC[update.message.text],parse_mode =telegram.ParseMode.HTML)
        
    else:
        while c < len(BD):
            if update.message.text not in BD[c][0]:
                c = c + 1
            else:
                break
        if c == len(BD):
            bot.sendMessage(chat_id=update.message.chat_id, text = "Carta não encontrada ou inexistente, por favor tente reescrever sua pesquisa",parse_mode =telegram.ParseMode.HTML)
        else:
            bot.sendPhoto(chat_id=update.message.chat_id,photo = BD[c][1],caption = "\t\r--------Card name--------\n"+"\t\r"+BD[c][0])
            bot.sendMessage(chat_id=update.message.chat_id, text="<i>\n---------Faction---------</i>\n"+ BD[c][2]+"\n<i> --Ability descripition--</i>\n"+ BD[c][3],parse_mode =telegram.ParseMode.HTML)
####

def faction(bot,update):
    faction_list = [[telegram.KeyboardButton("Monsters")],
                    [telegram.KeyboardButton("Skellige")],
                    [telegram.KeyboardButton("Scoiatael")],
                    [telegram.KeyboardButton("Northern_Realms")],
                    [telegram.KeyboardButton("Nilfgaard")]]
    reply_kb_markup = telegram.ReplyKeyboardMarkup(faction_list,resize_keyboard=True, one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id,text="Escolha uma Facção\n",reply_markup=reply_kb_markup)
    

###


### Handlers TELEGRAM API
from telegram.ext import CommandHandler
start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

pesquisa_handler = MessageHandler(Filters.text, pesquisa)
dispatcher.add_handler(pesquisa_handler)

faction_handler = CommandHandler("faction",faction)
dispatcher.add_handler(faction_handler)




###

updater.start_polling()


 


 
 
 
 
