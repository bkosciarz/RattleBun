import requests
import ast

class game:
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
        print(r.content)#DEBUG info
        self.response = ast.literal_eval(r.content)
        return self.response
 
class account:
    def __init__(self, game_obj):
        self.game_obj = game_obj
        self.login_name = ""
        self.password = ""
        self.auth_token = ""
    def logout(self):
                 pass
    def login(self, login_name, password):   
        self.login_name = login_name
        self.password = password
        self.get_auth()

    def get_auth(self):
        self.game_obj.url_fragment = "/resources/auth_token?d=android&v=2.7.2&r=false&dummy=1398.085"
        self.game_obj.headers["X-HTTP-Method-Override"] = "POST"
        self.game_obj.params =  {"login_name":self.login_name,"password":self.password}
        self.game_obj.headers["Content-Length"] = len(str(self.game_obj.params))

        response = self.game_obj.send_request()
        if "_error" in response.keys():
            print response["_error"]["message"]
        else:
            self.auth_token = response["auth_token"]
        #some kind of error mitigation?

    def change_password(self, new_password):
                 pass
                 #make sure self.auth is valid

    def complete_daily(self):
        #TODO: check if logged in and set auth_token
        self.game_obj.url_fragment = "/actions/collect_daily_objective?d=android&v=2.7.2&r=false&dummy=362.002"
        self.game_obj.headers["X-HTTP-Method-Override"] = "POST"
        self.game_obj.headers["Authoriaztion"] = "token " + self.auth_token
        self.game_obj.params = {}
        #1,2,3 are valid daily ojectives

        for id in xrange(1,4):
            self.game_obj.params["objective_id"] = id
            self.game_obj.headers["Content-Length"] = len(str(self.game_obj.params))
            self.game_obj.send_request()
    def complete_objectives(self):
        #1-197 are valid objectives
                 pass
    def current_objectives(self):
                 pass
        
                 
class account_cracker:
    def __init__(self):
        pass
    def lookup_username(self):
        pass
        #lookup a players login name from their username

    '''lets just use hydra...'''
    


fragment = '/resources/player?d=android&v=2.7.2&r=false&dummy=206.5406'

def menu1():
    choice = raw_input('''
                           1: Create an account
                           2: Login to existing account
                           3: Exit

                       ''')
    pass

def menu2():
    #have bool for logged in, and then stay at this menu until they logout
    choice = raw_input('''
                           1: Complete all daily objectives
                           2: Complete all objectives
                           3: Change Password
                           4: Logout
                       ''')
    pass 

def tester():
    my_game = game()
    acc = account(my_game)
    return acc



