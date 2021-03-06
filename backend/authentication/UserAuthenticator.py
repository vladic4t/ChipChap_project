from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.types import SubscribeOptions, PublishOptions
from twisted.internet.defer import Deferred, inlineCallbacks
from twisted.logger import Logger



class UserAuth(ApplicationSession):

    logger = Logger()

    # sessionID:userIDS
    sessions = {}

    # authID prototype for testing
    userIDS = [
            {'v114o': {"name": "Vladimir", "contacts": ['i114o', 'q114o']}},
            {'i114o': {"name": "Ivan", "contacts": ['v114o', 'q114o']}},
            {'q114o': {"name": "Quantum", "contacts": ['v114o', 'i114o']}}
    ]

    # track *****testing*****
    trackme = 0

    def onConnect(self):
        self.join("chat", ["ticket"], "user_authenticator")

    def onChallenge(self, challenge):
        if challenge.method == 'ticket':
            return 'doauthuser'

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info("*** USERAUTH COMPONENT JOINED SUCCESSFULY ****")
        yield self.subscribe(self.onSessionJoined, 'wamp.session.on_join')
        yield self.subscribe(self.onSessionLeave, 'wamp.session.on_leave')
        yield self.register(self.getUserID, 'com.chipchap.users.actions:getUserID')
        yield self.register(self.getUserInfo, 'com.chipchap.users.actions:getUserInfo')

    def onSessionJoined(self, session):
        self.log.info("A client has established a session with SESSION: <{}>".format(session['session']))
        if session['authrole'] == 'user':
            """
            BEWARE: This logic only handles 3 unique sessions which are
            accomodated without any authentication; tracking comes from the websocket connection.
            Logic session for demonstration purposes only. For a further and robust way handling of
            sessions consider implementing an authentication design yourself.
            """
            userid = UserAuth.userIDS[UserAuth.trackme]
            UserAuth.sessions[session['session']] = userid
            UserAuth.trackme += 1
        print("SESSIONS LIST: {}".format(UserAuth.sessions))

    def onSessionLeave(self, session):
        UserAuth.sessions.pop(session)
        UserAuth.trackme -= 1

    def getUserID(self, sessionId):
        return UserAuth.sessions[sessionId]

    def getUserInfo(self, id):
        for user in UserAuth.userIDS:
            if user.get(id):
                return user[id]['name']
