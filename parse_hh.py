import logging
import re
from pprint import pprint

import requests
from bs4 import BeautifulSoup

from .models import Company

logger = logging.getLogger(__name__)


class ParserHH:
    digit = re.compile('\d+')
    agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    url_base = 'https://spb.hh.ru'
    url_vacancy = '/search/vacancy'
    url_login = '/account/login'


    def request(self, url, params):
        headers = {'User-Agent': self.agent}
        res = requests.get(self.url_base + url, headers=headers, params=params)
        return res

    def request_direct(self, url):
        url = 'https://spb.hh.ru/account/login'
        headers = {'User-Agent': self.agent}
        session = requests.Session()
        r = session.get(url, headers=headers)
        session.headers.update({'Referer': url})
        session.headers.update(headers)
        _xsrf = session.cookies.get('_xsrf', domain=".hh.ru")
        post_request = session.post(url, {
            'backUrl': 'https://spb.hh.ru/',
            'username': 'egor@itpw.ru',
            'password': 'Crane21!',
            '_xsrf': _xsrf,
            'remember': 'yes',
        })
        return post_request

    def run(self):
        page = 1
        while True:
            html = self.get_vacancies(page)
            page += 1
            print(page)
            if isinstance(html, int):
                return f'error {html}'
            if html:
                self.get_vacancy_url(html)
                break
            else:
                break
        return 'Все компании подгружены'

    def get_vacancies(self, page):
        params = {
            'page': page,
            'text': 'системный администратор',
        }
        res = self.request(self.url_vacancy, params)
        logger.debug(res.status_code)
        if res.status_code == 200:
            return res.text
        else:
            return res.status_code

    def get_company_list(self, html):
        soup = BeautifulSoup(html, features='html.parser')
        companies = soup.find_all('a', class_='bloko-link bloko-link_secondary')
        for company in companies:
            href = company['href']
            logger.debug('hh_id перобразование в int')
            hh_id = self.digit.findall(href)
            if hh_id:
                hh_id = hh_id[0]
            else:
                continue
            c, created = Company.objects.get_or_create(hh_id=hh_id)
            c.name = company.text
            c.save()
        logger.info(f'Обработано {len(companies)} комапний')

    def get_vacancy_url(self, html):
        soup = BeautifulSoup(html, features='html.parser')
        link_list = soup.find_all('a', class_='bloko-link', href=re.compile('https://spb.hh.ru/vacancy/'))
        for link in link_list:
            href = link['href']
            res = self.request_direct(href)
            if res.status_code == 200:
                print(res.text)
                print(res.text)