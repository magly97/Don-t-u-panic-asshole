import pygame
import json
import os
import threading
import queue
import time

from lib import gamestates
from lib import intro
from lib import login
from lib import colors
from lib.game.game_runner import GameRunner
from lib.music import MenuMusic
from lib import main_menu
from lib import server_list
from lib import creators_menu
from lib import controls
from lib.connections import connector
from lib.connections import udp_connector
from lib.connections.request import request_types


QUEUE_SIZE = 20
RECONNECT_TRY_DELAY = 10
GET_RESPONSE_TIMEOUT = 2
SECOND_IN_MILISECONDS = 1000.0


class TcpConnectionThread(threading.Thread):
    def __init__(self, game):
        threading.Thread.__init__(self)
        self.__game = game
        self.__last_reconnect_try = time.process_time()

    def run(self):
        conn = self.__game.get_connector()
        while not self.__game.thread_status():
            if not self.__check_server_connection(conn):
                continue
            response = conn.get_response(timeout=GET_RESPONSE_TIMEOUT)
            if response is not False:
                self.__game.queue_put(response)

    def __check_server_connection(self, conn):
        if not conn.is_connected():
            if time.process_time() - self.__last_reconnect_try > RECONNECT_TRY_DELAY:
                conn.try_reconnect()
            return False
        else:
            return True


class UdpConnectionThread(threading.Thread):

    def __init__(self, game):
        threading.Thread.__init__(self)
        self.__game = game
        self.__stop_thread = False

    def run(self):
        last_response_time = time.time()
        conn = self.__game.get_udp_connector()
        conn.send_packet(request_types.UDP_LOGIN, [self.__game.get_logged_user()], 8)
        while self.__stop_thread is False:
            #conn.send_packet(request_types.UDP_GET_OBJECT, [''], 8)
            response = conn.get_response()
            if response is not False:
                last_response_time = time.time()
                self.__game.queue_put(response)
            if time.time()-last_response_time > 10:
                self.__game.set_state(gamestates.MAIN_MENU)
                self.__game.stop_udp()


class Game:
    def __init__(self):
        self.__game_title = 'Dont\'t u panic asshole'
        self.__settings = None
        self.__settings_file = "./settings.json"
        self.__state = None
        self.__clock = None
        self.__screen = None
        self.__events = None
        self.__conn = connector.Connector()
        self.__udp_conn = udp_connector.UdpConnector()
        self.__queue = queue.Queue(QUEUE_SIZE)
        self.__server_responses = []
        self.__thread = TcpConnectionThread(self)
        self.__udp_thread = None
        self.__thread_stop = False
        self.__udp_thread_stop = False
        self.__logged_user = None
        self.__thread.start()

    def thread_status(self):
        return self.__thread_stop

    def udp_thread_status(self):
        return self.__udp_thread_stop

    def stop_udp(self):
        self.__udp_thread_stop = True

    def get_connector(self):
        return self.__conn

    def set_logged_user(self, user):
        self.__logged_user = user

    def get_logged_user(self):
        return self.__logged_user

    def get_udp_connector(self):
        return self.__udp_conn

    def queue_put(self, data):
        self.__queue.put(data)

    def get_server_responses(self):
        return self.__server_responses

    def __get_data_from_queue(self):
        self.__server_responses.clear()
        while not self.__queue.empty():
            self.__server_responses.append(self.__queue.get())

    def get_screen(self):
        return self.__screen

    def get_events(self):
        return self.__events

    def update_events(self):
        self.__events = pygame.event.get()

    def get_settings(self):
        file_exists = os.path.isfile(self.__settings_file)
        if not file_exists:
            self.crash("Settings file does not exists")
        with open(self.__settings_file) as json_file:
            data = json.load(json_file)
        self.__settings = data
        return data

    def init(self):
        if self.__settings is None:
            self.get_settings()
        width = self.__settings['width']
        height = self.__settings['height']
        if self.__settings['fullscreen']:
            display_mode = pygame.FULLSCREEN
        else:
            display_mode = 0
        self.__clock = pygame.time.Clock()
        pygame.init()
        self.__screen = pygame.display.set_mode((width, height), display_mode)
        pygame.display.set_caption(self.__game_title)
        if self.__settings['intro_enable']:
            self.__state = gamestates.INTRO
        else:
            self.__state = gamestates.LOGIN
        print("Game initialized")

    def get_state(self):
        return self.__state

    def handle_quit_event(self):
        for event in self.__events:
            if event.type == pygame.QUIT:
                self.set_state(gamestates.QUIT)

    def set_state(self, state):
        self.__state = state

    def tick(self):
        pygame.display.flip()
        self.__clock.tick_busy_loop(self.__settings['fps_max'])
        self.__get_data_from_queue()
        self.__screen.fill(colors.WHITE)

    def get_delta_time(self):
        return self.__clock.get_time() / SECOND_IN_MILISECONDS

    def quit(self):
        print("Bye bye :(")
        self.__thread_stop = True
        self.__udp_thread_stop = True
        pygame.quit()
        exit(0)

    def crash(self, msg):
        print(msg)
        self.__thread_stop = True
        pygame.quit()
        exit(-1)

    def create_udp_connection_thread(self):
        if self.__udp_thread is None:
            self.__udp_thread = UdpConnectionThread(self)
            self.__udp_thread.start()


if __name__ == "__main__":
    main = Game()
    main.init()
    music_obj = MenuMusic()
    intro_obj = intro.Intro(main)
    login_obj = login.Login(main)
    main_menu_obj = main_menu.MainMenu(main)
    creators_menu_obj = creators_menu.CreatorsMenu(main)
    server_list_obj = server_list.ServerList(main)
    settings_obj = None
    settings_controls_obj = controls.Controls(main)
    settings_video_obj = None
    settings_audio_obj = None
    creators_obj = None
    game_obj = GameRunner(main)
    music_obj.start_music()
    while True:
        main.update_events()
        main.handle_quit_event()
        if main.get_state() == gamestates.QUIT:
            main.quit()
        elif main.get_state() == gamestates.INTRO:
            intro_obj.loop()
        elif main.get_state() == gamestates.LOGIN:
            login_obj.loop()
        elif main.get_state() == gamestates.MAIN_MENU:
            main_menu_obj.loop()
        elif main.get_state() == gamestates.SERVER_LIST:
            server_list_obj.loop()
        elif main.get_state() == gamestates.SETTINGS:
            pass
        elif main.get_state() == gamestates.SETTINGS_VIDEO:
            pass
        elif main.get_state() == gamestates.CONTROLS:
            settings_controls_obj.loop()
        elif main.get_state() == gamestates.SETTINGS_AUDIO:
            pass
        elif main.get_state() == gamestates.CREATORS:
            creators_menu_obj.loop()
        elif main.get_state() == gamestates.GAME:
            music_obj.stop_music()
            game_obj.loop()
        else:
            main.crash("Unknown game state")
        main.tick()
