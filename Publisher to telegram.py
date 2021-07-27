import requests
from bs4 import BeautifulSoup as bs
import json
from datetime import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import asyncio
import os
import random




TOKEN = '123'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

async def periodic():
    while True:
        if int(datetime.now().strftime('%H')) == 9:

            r = requests.get('https://coinmarketcap.com')
            soup = bs(r.content,'lxml')

            market_cap,vol_24,dominance = [x.text for x in soup.find('div',class_='sc-5tazol-0').find_all('span')[2:5]]
            market_cap = '$'+''.join(market_cap.split('  ')[1][1:].split(',')[::-1][3:][::-1])+'.'+ market_cap.split('  ')[1][1:].split(',')[::-1][2]+'B'
            vol_24 = '$'+''.join(vol_24.split('  ')[1][1:].split(',')[::-1][3:][::-1])+'.'+ vol_24.split('  ')[1][1:].split(',')[::-1][2]+'B'
            dominance = dominance.split('  ')[1].split('ETH')[0][5:]
            month = ['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря'][int(datetime.now().strftime('%m'))-1]
            year = datetime.now().strftime('%Y')
            day = datetime.now().strftime('%d')
            ########################################################################
            container_courses = []
            r = requests.get('https://api.coincap.io/v2/assets')
            r = json.loads(r.text)
            count_lengh = 0
            for i in r['data']:
                if count_lengh >= 10:
                    break
                else:
                    if 'Tether' in i['name'] or 'USD Coin' in i['name'] or 'Binance USD' in i['name']:
                        pass
                    else:
                        container_courses.append('✅'+' '+'#'+i['name']+' '+'('+i['symbol']+')'+' '+('+'+i['changePercent24Hr'].split('.')[0]+'.'+i['changePercent24Hr'].split('.')[1][:2] if '-' not in i['changePercent24Hr'].split('.')[0]+'.'+i['changePercent24Hr'].split('.')[1][:2] else i['changePercent24Hr'].split('.')[0]+'.'+i['changePercent24Hr'].split('.')[1][:2]))
                        count_lengh += 1
            qu = '\n'
            result = f'''
            Доброго всем утра! ☕️🤝
💰 Капитализация крипты: <b>{market_cap}</b>
💵 Общий объем торгов: <b>{vol_24}</b>
💥 Доля биткоина: <b>{dominance}</b>
        
ТОП-10 —  <b>{day} {month}</b> {year}
Изменения курса за <b>24 часа в %.</b>
        
{qu.join(container_courses)}

@BeefsTrend
            '''
            with open('photos/'+random.choice(os.listdir('photos')),'rb') as f:
                await bot.send_photo(-1001226219964,photo=f,caption=result,parse_mode='HTML')
            await asyncio.sleep(4000)
        await asyncio.sleep(1000)
if __name__ == '__main__':
    loop2 = asyncio.get_event_loop()
    loop2.create_task(periodic())
    executor.start_polling(dp, skip_updates=True)



