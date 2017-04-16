class Profile:
    __brokerAccounts = None
    __journals = None

    def __init__(self):
        pass

    def add_broker_account(self, bk_account):
        # TODO:
        # id = insert_broker_account(bk_account)
        # self.__brokerAccounts.append(id: bk_account)
        bk_account_id = -1

        return bk_account_id

    def remove_broker_account(self, bk_account_id):
        bk_account_id = -1
        return bk_account_id

    def add_journal(self, journal):
        # TODO:
        # id = insert_db(journal)
        # self.__journals.append(id: journal)
        journal_id = -1
        return journal_id

    def remove_journal(self, journal_id):
        journal_id = -1
        return journal_id

    def load_journals(self):
        # TODO: load journals from db
        pass

    def load_broker_accounts(self):
        pass
