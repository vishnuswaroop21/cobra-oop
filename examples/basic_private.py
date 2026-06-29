from cobra import CobraObject
from cobra import private


class Bank(CobraObject):

    @private
    def reset_pin(self):
        print("PIN reset")

    def change_pin(self):
        self.reset_pin()


bank = Bank()

bank.change_pin()