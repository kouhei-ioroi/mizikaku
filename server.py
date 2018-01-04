# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.escape
import tornado.options
from tornado.options import define, options
import os
import string
import random
import json
url_list = json.load(open("urllist.json" , "r"))
define("port", default=80, type=int)
options.parse_command_line()
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/s', ShortServiceHandler),
            (r'/domainpool', DomainPoolHandler),
            (r'/(favicon.ico)', tornado.web.StaticFileHandler, {"path": "/static/favicon.ico"}),
            (r'/(robots.txt)', tornado.web.StaticFileHandler, {"path": "/static/robots.txt"}),
        ]
        settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            autoescape="xhtml_escape",
            debug=True,
            )
        tornado.web.Application.__init__(self, handlers, **settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("form.html",url_list_math=len(url_list),url_short="短縮結果が返されます。")
    def post(self):
        url = self.get_argument("element_1")
        if url in url_list.values():
            url_list_key = list(url_list.keys())[list(url_list.values()).index(url)]
            self.render("form.html",url_list_math=len(url_list),url_short="http://www.mizikaku.ga/s?k="+url_list_key)
            #self.write('<meta name="viewport" content="width=device-width,initial-scale=1.0"><p>Punycode(日本語URL):<a href="http://www.短く.ga/s?k='+url_list_key+'" target="_blank">http://www.短く.ga/s?k='+url_list_key+'<a></p><p>Unicode(通常URL):<a href="http://www.mizikaku.ga/s?k='+url_list_key+'" target="_blank">http://www.mizikaku.ga/s?k='+url_list_key+'<a></p><p>LINEで共有:<a href="http://line.me/R/msg/text/?http://www.mizikaku.ga/s?k='+url_list_key+'" target="_blank">LINEで共有<a></p>')
        else:
            url_list_key = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(8)])
            url_list[url_list_key]=url
            json.dump(url_list,open("urllist.json" , "w"))
            self.render("form.html",url_list_math=len(url_list),url_short="http://www.mizikaku.ga/s?k="+url_list_key)
            #self.write('<meta name="viewport" content="width=device-width,initial-scale=1.0"><p>Punycode(日本語URL):<a href="http://www.短く.ga/s?k='+url_list_key+'" target="_blank">http://www.短く.ga/s?k='+url_list_key+'<a></p><p>Unicode(通常URL):<a href="http://www.mizikaku.ga/s?k='+url_list_key+'" target="_blank">http://www.mizikaku.ga/s?k='+url_list_key+'<a></p><p>LINEで共有:<a href="http://line.me/R/msg/text/?http://www.mizikaku.ga/s?k='+url_list_key+'" target="_blank">LINEで共有<a></p>')
class ShortServiceHandler(tornado.web.RequestHandler):
    def get(self):
        key = self.get_argument('k', 'None')
        if key == "None":
            self.write("Error:引数が不足しています。")
        else:
            if key in url_list:
                try:
                    self.redirect(url_list[key])
                except:
                    self.write("転送中にエラーが発生しました。存在しないURLです。")
            else:
                self.write("存在しない短縮URLです。")
class DomainPoolHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('このドメインは<a href="https://twitter.com/Kohe_Ioroi/" target="_blank">Kohe_Ioroi</a>が管理しています。')
def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
    main()
