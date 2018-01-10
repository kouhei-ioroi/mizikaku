import tornado.ioloop,tornado.web,tornado.escape,tornado.options
from tornado.options import define, options
import os,string,random,json
url_list = json.load(open("urllist.json" , "r"))
define("port", default=80, type=int)
options.parse_command_line()
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/s', ShortServiceHandler),
            (r'/api', apiHandler),
            (r'/(favicon.ico)', tornado.web.StaticFileHandler, {"path": "/static/favicon.ico"}),
            (r'/(robots.txt)', tornado.web.StaticFileHandler, {"path": "/static/robots.txt"}),
            (r'/........+', DirectShortServiceHandler),
            (r'/[\S]+', ReturnNothingServiceHandler),
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
            self.render("form.html",url_list_math=len(url_list),url_short="http://mzkk.ga/"+url_list_key)
        else:
            url_list_key = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(8)])
            url_list[url_list_key]=url
            json.dump(url_list,open("urllist.json" , "w"))
            self.render("form.html",url_list_math=len(url_list),url_short="http://mzkk.ga/"+url_list_key)
class DirectShortServiceHandler(tornado.web.RequestHandler):
        def get(self):
            key = self.request.path[1:]
            if key in url_list:
                try:
                    self.redirect(url_list[key])
                except:
                    self.write("転送中にエラーが発生しました。存在しないURLです。")
            else:
                self.write("存在しない短縮URLです。")
class ShortServiceHandler(tornado.web.RequestHandler):
    def get(self):
        key = self.get_argument('k', 'None')
        if key == "None":
            self.write("引数が不足しています。")
        else:
            if key in url_list:
                try:
                    self.redirect(url_list[key])
                except:
                    self.write("転送中にエラーが発生しました。存在しないURLです。")
            else:
                self.write("存在しない短縮URLです。")
class apiHandler(tornado.web.RequestHandler):
    def get(self):
        url = self.get_argument('url', 'None')
        if url == "None":
            self.write('{code":"500","id":"null","message":"No_Argument"}')
        else:
            if url in url_list.values():
                url_list_key = list(url_list.keys())[list(url_list.values()).index(url)]
                self.write('{"code":"200","id":'+url_list_key+'","message":"OK"}')
            else:
                url_list_key = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(8)])
                url_list[url_list_key]=url
                json.dump(url_list,open("urllist.json" , "w"))
                self.write('{"code":"200","id":'+url_list_key+'","message":"OK"}')
class ReturnNothingServiceHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("存在しない短縮URLです。")
def main():
    tornado.options.parse_command_line()
    Application().listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
    main()