# -*- coding:utf-8 -*-
import json
import requests


class DoubanMovieSpider(object):
    """豆瓣电影信息"""
    def __init__(self):
        self.start_url = 'https://movie.douban.com/j/search_subjects?type=movie&tag={}&sort=rank&page_limit=20&page_start={}'
        self.headers = {
            'Host': 'movie.douban.com',
            'Referer': 'https: // movie.douban.com / explore',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.id_list = []
        with open('result.json', 'w', encoding='utf-8') as f:
            f.write('[')

    def get_tip_list(self):
        """获取分类标签列表"""
        url = 'https://movie.douban.com/j/search_tags?type=movie&source='
        response = self.get_response(url)
        tip_list = json.loads(response)['tags']
        return tip_list

    def get_response(self, url):
        """获取响应"""
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def get_ret(self, response):
        """提取数据"""
        info_list = json.loads(response)['subjects']
        return info_list

    def save_info(self, info_list):
        """保存数据"""
        with open('result.json', 'a', encoding='utf-8') as f:
            for info in info_list:
                # 数据去重
                if info not in self.id_list:
                    f.write(json.dumps(info, ensure_ascii=False))
                    f.write(',\n')

    def run(self):
        tip_list = self.get_tip_list()
        for tip in tip_list:
            print('正在获取[{}]类电影数据'.format(tip))
            # 1.start_url
            num = 0
            url = self.start_url
            while True:
                # 2.拼接下一页
                next_url = url.format(tip, num)
                # 3.获取响应
                response = self.get_response(next_url)
                # 4.提取数据
                info_list = self.get_ret(response)
                # 5.保存数据
                self.save_info(info_list)
                num += 20
                if len(info_list) < 20:
                    print('[{}]类电影数据保存完毕'.format(tip))
                    print('*' * 30)
                    break

        with open('result.json', 'a', encoding='utf-8') as f:
            f.write(']')


if __name__ == '__main__':
    douban = DoubanMovieSpider()
    douban.run()
