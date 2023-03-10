import os
from utils.action import convert_cookies_to_dict, user
from dotenv import load_dotenv, dotenv_values
from tqdm import tqdm
import utils.const as const
from utils.case import case
from utils.logger import logger as log
load_dotenv()
loglevel = dotenv_values()['LOGLEVEL']
if dotenv_values()['SAVELOG'] == '1':
    logger = log(log_level=loglevel, log_file='debug.log')
    logger.status = 1
    logger.debug(
        f'[DEBUG] Successfully set logger level to {loglevel} and output to terminal and debug.log')
else:
    logger = log(log_level=loglevel)
    logger.status = 0
    logger.debug(
        f'[DEBUG] Successfully set logger level to {loglevel} and output to terminal.')
SESSDATA, CSRF, OFFSET, COOKIE = dotenv_values()['SESSDATA'], dotenv_values()[
    'CSRF'], dotenv_values()['OFFSET'], dotenv_values()['COOKIE']
if SESSDATA == '' or CSRF == '' or COOKIE == '':
    logger.error(
        '[ERROR] You must configure SESSDATA, CSRF and COOKIE to use this script!')
    os._exit(-1)
else:
    logger.debug(
        f'[DEBUG] Successfully set SESSDATA to {SESSDATA}, CSRF to {CSRF} and COOKIE to {COOKIE}, case vote offset has been set to {OFFSET}')
UA = dotenv_values()['UA']
if UA == '':
    UA = const.UA
    logger.warn(
        f'[WARN] It seems that you haven\'t configurate the UA, use fallback UA [{UA}] instead.')
else:
    logger.debug(f'[DEBUG] Successfully set custom UA {UA}')

headers = {
    'cookie': f'SESSDATA={SESSDATA}',
    'Host': 'api.bilibili.com',
    'User-Agent': UA
}

my = user(SESSDATA, CSRF, UA, logger)
my.applyFor()
for case_count in tqdm(range(1, 21)):
    cid = my.getCase()
    c = case(cid, SESSDATA, UA, CSRF, COOKIE, OFFSET, logger)
    c.goVote()
    logger.info('[INFO] Done!')