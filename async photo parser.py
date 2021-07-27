import requests
from bs4 import BeautifulSoup as bs
import asyncio
import aiohttp
import random
from time import time
import aiofiles
stranno =  'qwertyuiopasdfghjklzxcvbnm0123456789-'



#
# r = requests.get('https://www.istockphoto.com/search/2/image?page=1&phrase=bitcoin')
# soup = bs(r.content,'lxml')
# img = soup.find_all('img',class_='MosiacAsset-module__thumb___L2F4y')
# for i in list(img):
#     # print(i['src'])
#     with open('photos/'+''.join([random.choice(stranno) for i in range(25)])+'.jpg','wb') as f:
#         q = requests.get(i['src'])
#         text = q.content
#         # print(q.text)
#         print(q.text.encode('utf-8'))
#         # f.write(text)
#     break

async def download(im):
    async with aiohttp.ClientSession() as session:
        # print(i['src'])
        async with aiofiles.open('photos/' + ''.join([random.choice(stranno) for i in range(25)]) + '.jpg', 'wb') as f:
            q = await session.get(im)
            texto = await q.content.read()
            await f.write(texto)



async  def pars(i):



    async with aiohttp.ClientSession() as session:
        taks = []
        s = await session.get(f'https://www.istockphoto.com/search/2/image?page={str(i)}&phrase=bitcoin')
        s_text = await s.text()
        soup = bs(s_text, 'lxml')
        img = [i['src'] for i in soup.find_all('img',class_='MosiacAsset-module__thumb___L2F4y')]
        print(i,len(img))
        for im in img:
            taks.append(asyncio.create_task(download(im)))


        await asyncio.gather(*taks)






async def main():

    tasks = []

    for i in range(1, 10):

        tasks.append(asyncio.create_task(pars(i)))

    await asyncio.gather(*tasks)




if __name__ == '__main__':
    t1 = time()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
    print(time()-t1)