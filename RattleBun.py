import requests
import ast
import datetime
import hashlib

DEBUG = False

class Game:
    def __init__(self):
        self.url = "http://api.battlerungame.com"
        self.url_fragment= ""
        self.headers = {
            "X-Unity-Version": "4.5.5f1",
            "X-HTTP-Method-Override": "POST",
            "Authorization": "token ",
            "Content-Type": "application/json",
            "Accept": "application/vnd.gamehive.battlerun-v2.7.2+json",
            "User-Agent": "Mozilla/5.0 (Android; Mobile; rv:40.0) Gecko/40.0 Firefox/40.0",
            "Host": "api.battlerungame.com",
            "Connection": "close",
            "Accept-Encoding": "gzip",
            "Content-Length": 0}
        self.params = {}
        self.response = {}
        
    def get_url(self):
        return (self.url + self.url_fragment)
    def str_to_dict(self, in_str, out_dict):
        out_dict = ast.literal_eval(in_str)
    def send_request(self):
        r = requests.post(self.get_url(), json=self.params, headers=self.headers)
        if DEBUG:
            print(r.content)
        try: 
            self.response = ast.literal_eval(r.content)
            return self.response
        except ValueError:
            return {}
 
class Account:
    def __init__(self, game = Game()):
        self.game = game
        self.login_name = ""
        self.password = ""
        self.auth_token = ""

    def create_account(self, login_name, password = "123456"):
        self.game.url_fragment = "/resources/player?d=android&v=2.7.2&r=false&dummy=206.5406"
        self.game.headers["X-HTTP-Method-Override"] = "POST"
        
        self.game.params = {"login_name":login_name, "password":password, "device_id":"test"}
        self.game.headers["Content-Length"] = len(str(self.game.params))
        self.game.send_request()

        #if successful then"
        self.login_name = login_name
        self.password = password
        self.get_auth()
    def logout(self):
                 pass
    def login(self, login_name, password):   
        self.login_name = login_name
        self.password = password
        self.get_auth()

    def get_auth(self):
        self.game.url_fragment = "/resources/auth_token?d=android&v=2.7.2&r=false&dummy=1398.085"
        self.game.headers["X-HTTP-Method-Override"] = "POST"
        self.game.params =  {"login_name":self.login_name,"password":self.password}
        self.game.headers["Content-Length"] = len(str(self.game.params))

        response = self.game.send_request()
        if "_error" in response.keys():
            print response["_error"]["message"]
        else:
            self.auth_token = response["auth_token"]
        #some kind of error mitigation?

    def change_password(self, new_password):
        self.get_auth()
        self.game.url_fragment = '/actions/player/change_password?d=android&v=2.7.2&r=false&dummy=1237.268'
        self.game.headers["X-HTTP-Method-Override"] = "PUT"
        self.game.headers["Authorization"] = "token " + self.auth_token

        self.game.params =  {"new_password":new_password}
        self.game.headers["Content-Length"] = len(str(self.game.params))
        self.game.send_request()
        #error checking?

    def complete_daily(self):
        self.game.url_fragment = "/actions/collect_daily_objective?d=android&v=2.7.2&r=false&dummy=362.002"
        self.game.headers["X-HTTP-Method-Override"] = "POST"
        self.game.headers["Authorization"] = "token " + self.auth_token
        self.game.params = {}
        #1,2,3 are valid daily ojectives

        for id in xrange(1,4):
            self.game.params["objective_id"] = id
            self.game.headers["Content-Length"] = len(str(self.game.params))
            self.game.send_request()
    def complete_objectives(self):
        #1-193 are valid objectives

        self.game.url_fragment = "/actions/player/collect_objective?d=android&v=2.7.2&r=false&dummy=632.7889"
        self.game.headers["X-HTTP-Method-Override"] = "POST"
        self.game.headers["Authorization"] = "token " + self.auth_token
        self.game.params = {}

        #maybe get current objectives and then not do every single one
        num_objectives = 193
        for id in xrange(1,num_objectives+1):
            self.game.params["objective_id"] = id
            self.game.headers["Content-Length"] = len(str(self.game.params))
            self.game.send_request()

    def current_objectives(self):
        self.game.url_fragment = "/resources/current_objectives?d=android&v=2.7.2&r=false&dummy=643.3849"
        self.game.headers["X-HTTP-Method-Override"] = "GET"
        self.game.headers["Authorization"] = "token " + self.auth_token
        self.game.headers["Content-Length"] = 1
        self.game.params = {}
    def buy_mount_slot(self):
        #default payment type is coins, but can also be diamonds
        self.game.url_fragment = "/actions/buy_mount_slot?d=android&v=2.7.2&r=false&dummy=1503.509"
        self.game.headers["X-HTTP-Method-Override"] = "POST"
        self.game.headers["Authorization"] = "token " + self.auth_token
        
        self.game.params = {"payment_type":"coins"}
        self.game.headers["Content-Length"] = len(str(self.game.params))
        self.game.send_request()

    def buy_egg_pack(self):
        self.game.url_fragment = "/actions/buy_egg_pack?d=android&v=2.7.2&r=false&dummy=1528.794"
        self.game.headers["X-HTTP-Method-Override"] = "POST"
        self.game.headers["Authorization"] = "token " + self.auth_token
        self.game.params = {"egg_pack":"legendary0"}
        self.game.headers["Content-Length"] = len(str(self.game.params))
        self.game.send_request()

    def hatch_egg(self):
        self.game.url_fragment = "/actions/hatch_egg?d=android&v=2.7.2&r=false&dummy=1569.972"
        self.game.headers["X-HTTP-Method-Override"] = "POST"
        self.game.headers["Authorization"] = "token " + self.auth_token
        self.game.params = {"egg_type":"legendary"}
        self.game.headers["Content-Length"] = len(str(self.game.params))
        response = self.game.send_request()
        
        #error checking 
        return response["id"]

    def collect_mount(self, mount_id):
        self.game.url_fragment = "/actions/collect_mount?d=android&v=2.7.2&r=false&dummy=2387.565"
        self.game.headers["X-HTTP-Method-Override"] = "POST"
        self.game.headers["Authorization"] = "token " + self.auth_token
        self.game.params = {"mount_id":mount_id}
        self.game.headers["Content-Length"] = len(str(self.game.params))
        response = self.game.send_request()

        #error checking
        return response["stats"]

    def pet_boost_helper(self):
    #complete all objectives and then buy/hatch pet 
        self.complete_daily()
        self.complete_objectives()
        self.buy_mount_slot()
        self.buy_egg_pack()
        mount_id = self.hatch_egg()
        return self.collect_mount(mount_id)
        #order is speed, attack_time, damage, life

class AccountBooster:
    def __init__(self):
        self.account = Account()
 
    def pet_bruteforce(self, threshold=300):
        login_name = hashlib.md5(str(datetime.datetime.now())).hexdigest()
        self.account = Account()
        self.account.create_account(login_name)
        mount_stats =  self.account.pet_boost_helper()
        if sum(mount_stats[:-1]) < threshold:
            self.pet_bruteforce(threshold)
            print(self.account.login_name + ":" + str(mount_stats))
        else:
            print(self.account.login_name + ":" + self.account.password + ":" + str(mount_stats) + "YAEH")
            self.pet_bruteforce(threshold)
def menu1():
    choice = raw_input('''
                           1: Create an account
                           2: Login to existing account
                           3: Exit

                       ''')
    return

def menu2():
    #have bool for logged in, and then stay at this menu until they logout
    choice = raw_input('''
                           1: Complete all daily objectives
                           2: Complete all objectives
                           3: Change Password
                           4: Logout
                       ''')
    return

def tester():
    game = Game()
    account = Account(Game)
    return acc



