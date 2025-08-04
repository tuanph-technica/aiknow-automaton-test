import configparser
config = configparser.RawConfigParser()
config.read('.\\configfiles\\config.ini')
class ReadConfig:
    @staticmethod
    def get_application_url():
        url = config.get('common info','baseURL')
        return url
    @staticmethod
    def get_userName():
        user_name = config.get('common info','user_name')
        return user_name

    @staticmethod
    def get_password():
        pass_word= config.get('common info', 'pass_word')
        return pass_word







