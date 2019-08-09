from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json


class TwitchBot:

    def __init__(self, username, password, target):
        self.username = username
        self.password = password
        self.target = target
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--mute-audio')
        self.driver = webdriver.Chrome(
            executable_path='chromedriver.exe', chrome_options=chrome_options)
        self.base_url = 'https://www.twitch.tv/'

    def login(self):
        self.driver.find_element_by_xpath(
            '(//button[@data-a-target="login-button"])').click()
        time.sleep(3)
        self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div/div/div/div/div[1]/div/div/form/div/div[1]/div/div[2]/input').send_keys(self.username)
        self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div/div/div/div/div[1]/div/div/form/div/div[2]/div/div[1]/div[2]/div[1]/input').send_keys(self.password)
        time.sleep(2)
        self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div/div/div/div/div[1]/div/div/form/div/div[3]/button').click()
        time.sleep(2)

        # shouldn't popup with modified exe
        # self.check_captcha()

    def check_captcha(self):
        try:
            # first get iframe and swap to frame mode then get ->
            self.driver.find_element_by_xpath(
                '#//*[@id="recaptcha-anchor"]/div[1]').click()
        except:
            print('no captcha')
        # /html/body/div[2]/div/div/div/div/div/div[1]/div/div/div[3]/div/div/span[1]
        # We need to make sure you're not a robot!
        # //*[@id="recaptcha-anchor"]/div[1]

    def open(self):
        self.driver.get(self.base_url)
        time.sleep(1)
        self.driver.maximize_window()
        time.sleep(3)

    def watch_target(self):
        self.driver.get(f'{self.base_url}{self.target}')


class Brain:

    def __init__(self, target):
        self.target = target
        self.bots = []
        self.credentials = []

    def __call__(self):
        self.get_credentials()
        self.init_instances()
        self.bot_action()

    def get_credentials(self):
        with open("credentials.json", "r") as read_file:
            self.credentials = json.load(read_file)

    def init_instances(self):
        self.bots = [TwitchBot(self.credentials[i]["username"], self.credentials[i]
                               ["password"], self.target) for i in range(len(self.credentials))]

    def bot_action(self):
        for bot in self.bots:
            bot.open()
            bot.login()
            bot.watch_target()


brain = Brain('mrposh')
brain()
