import datetime
import json
import os.path

from aiogram.client.session import aiohttp
from aiohttp.web_exceptions import HTTPUnauthorized
from dotenv import load_dotenv

from instruktor.botapi import params, need_login


# @need_login
async def search(text: str, tg_id: int = 0) -> str:
    pass
    # async with aiohttp.ClientSession() as session:
    #     headers = {'content-type': 'application/json',
    #                'accept': 'application/json',
    #                "authorization": f"Bearer {params.TOKEN}"}
    #     async with session.post(url=params.ENDPOINTS.tg_user_appeal_params,
    #                             data=json.dumps({'tg_id': tg_id, 'text': text}),
    #                             headers=headers) as resp:
    #         if resp.status == 401:
    #             raise HTTPUnauthorized()
    #         search_result: str = (await resp.json())
    #         if search_result is not None:
    #             return search_result
    #         else:
    #             raise Exception('User Appeal is None in response server')


# @need_login
def manufacturers(tg_id: int = 0) -> list:
    manufacturers_list = ['Bolid', 'Рубеж']
    return manufacturers_list
    # async with aiohttp.ClientSession() as session:
    #     headers = {'content-type': 'application/json',
    #                'accept': 'application/json',
    #                "authorization": f"Bearer {params.TOKEN}"}
    #     async with session.post(url=params.ENDPOINTS.tg_user_appeal_params,
    #                             data=json.dumps({'tg_id': tg_id}),
    #                             headers=headers) as resp:
    #         if resp.status == 401:
    #             raise HTTPUnauthorized()
    #         user_appeal: str = (await resp.json())
    #         if user_appeal is not None:
    #             return user_appeal
    #         else:
    #             raise Exception('User Appeal is None in response server')
