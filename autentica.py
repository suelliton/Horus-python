
import pyrebase

class Autentica(object):
    def __init__(self,apiKey,authDomain,databaseUrl,storageBucket,serviceAccount,email,password):
        super(Autentica, self).__init__()
        self._apiKey = apiKey
        self._authDomain = authDomain
        self._databaseUrl = databaseUrl
        self._storageBucket = storageBucket
        self._serviceAccount =  serviceAccount
        self._email = email
        self._password = password

    def logar(self):
        config = {
         "apiKey": self._apiKey,
          "authDomain": self._authDomain,
          "databaseURL": self._databaseUrl,
          "storageBucket": self._storageBucket,
          "serviceAccount":self._serviceAccount
        }
        firebase = pyrebase.initialize_app(config)
        auth = firebase.auth()
        user_login = auth.sign_in_with_email_and_password(self._email, self._password)
        database = firebase.database()
        storage = firebase.storage()
        return (database, storage)


    def getApiKey(self):
        return self._apiKey
    def setApiKey(self,apiKey):
        self._apiKey = apiKey

    apiKey = property(
        fget = getApiKey,
        fset = setApiKey
    )
    def getAuthDomain(self):
        return self._authDomain
    def setAuthDomain(self,authDomain):
        self._authDomain = authDomain
    authDomain = property(
        fget = getAuthDomain,
        fset = setAuthDomain
    )
    def getDatabaseUrl(self):
        return self._databaseUrl
    def setDatabaseUrl(self,databaseURL):
        self._databaseUrl = databaseURL
    databaseURL = property(
        fget = getDatabaseUrl,
        fset = setDatabaseUrl
    )
    def getStorageBucket(self):
        return self._storageBucket
    def setStorageBucket(self,storageBucket):
        self._storageBucket = storageBucket
    storageBucket = property(
        fget = getStorageBucket,
        fset = setStorageBucket
    )
    def getServiceAccount(self):
        return self._serviceAccount
    def setServiceAccount(self,serviceAccount):
        self._serviceAccount = serviceAccount
    serviceAccount = property(
        fget = getServiceAccount,
        fset = setServiceAccount
    )
    def getEmail(self):
        return self._email
    def setEmail(self,email):
        self._email = email
    email = property(
        fget = getEmail,
        fset = setEmail
    )
    def getPassword(self):
        return self._password
    def setPassword(self,password):
        self._password = password
    password = property(
        fget = getPassword,
        fset = setPassword
    )
