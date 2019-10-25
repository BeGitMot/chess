import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time


def login(browser, username, password):
    link = "https://www.chess.com/login_and_go?returnUrl=https%3A%2F%2Fwww.chess.com%2Fregister"
    browser.get(link)

    elem = browser.find_element_by_id("username")
    elem.send_keys(username)

    elem = browser.find_element_by_id("password")
    elem.send_keys(password)

    button_play = browser.find_element_by_id("login")
    button_play.click()

def closePopup(browser):
    try:
        close_x = browser.find_element_by_css_selector("a.x")
        close_x.click()
        print("popup closed")
    except:
        print("popup not found")

def start_play(driver):

    while driver.current_url != "https://www.chess.com/live":
        driver.get('https://www.chess.com/live')

    print(driver.current_url)

    closePopup(browser)

    #переключаем на вкладку Играть
    elem = driver.find_element(By.CSS_SELECTOR, 'li[data-tab="challenge"]')
    browser.execute_script("return arguments[0].scrollIntoView(true);", elem)
    elem.click()

    # вызываем игру
    #time.sleep(2)
    elem = driver.find_element_by_css_selector("button.quick-challenge-play")
    elem.click()

    # скроллим вверх
    #time.sleep(1)
    elem = driver.find_element_by_css_selector("a.user-tagline-username")
    browser.execute_script("return arguments[0].scrollIntoView(true);", elem)

    return

def get_user_color(driver, username):
    while (1):
        try:
            myElem = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-notification="gameNewGamePlaying"]>.username')))
            print("User Color Detected!")
            break
        except TimeoutException:
            print("Searching for Opponent!")

    players = driver.find_elements_by_css_selector('div[data-notification="gameNewGamePlaying"]>.username')
    #print(elem.text)
    #players = re.findall(r'(\w+)\s\(\d+\)', elem.text)

    white_player = players[0].text
    black_player = players[1].text

    if white_player == username:
        print(username + ' is white')
        return "white"
    else:
        print(username + ' is black')
        return "black"

def new_game(driver, username, chessEngine):
    start_play(driver)
    time.sleep(3)
    user_color = get_user_color(driver, username)
    #print(user_color)
    play_game(driver, user_color, chessEngine)
    return

def highlight_move(driver, user_color, best_move):
    driver.execute_script("""
        element = document.getElementsByClassName('chessboard')[0];
        x = element.style.width.replace(/\D/g,'') / 8;

        chessboard_id = document.getElementsByClassName('chessboard')[0].id + '_boardarea';

        if(arguments[4].localeCompare("white") == 0){
            var from_position_coordinate = [(arguments[0].charCodeAt(0) - 97) * x, (8 - parseInt(arguments[1])) * x];
            var to_position_coordinate = [(arguments[2].charCodeAt(0) - 97) * x, (8 - parseInt(arguments[3])) * x];
        }
        else{
            var from_position_coordinate = [(7 - (arguments[0].charCodeAt(0) - 97)) * x, (parseInt(arguments[1]) - 1) * x];
            var to_position_coordinate = [(7 - (arguments[2].charCodeAt(0) - 97)) * x, (parseInt(arguments[3]) - 1) * x];
        }


        var pos_old = "position: absolute; z-index: 2; pointer-events: none; opacity: 0.9; background-color: rgb(244, 42, 50); width:" + x + "px; height: " + x + "px; transform: translate(" + from_position_coordinate[0] + "px," +  from_position_coordinate[1] + "px);";
        var pos_new = "position: absolute; z-index: 2; pointer-events: none; opacity: 0.9; background-color: rgb(244, 42, 50); width:" + x + "px; height: " + x + "px; transform: translate(" + to_position_coordinate[0] + "px," +  to_position_coordinate[1] + "px);";

        element = document.createElement('div');            
        element.setAttribute("id", "highlight1");    
        element.setAttribute("style", pos_old);    
        document.getElementById(chessboard_id).appendChild(element);

        element = document.createElement('div');
        element.setAttribute("id", "highlight2");            
        element.setAttribute("style", pos_new); 
        document.getElementById(chessboard_id).appendChild(element);
       """, best_move[0], best_move[1], best_move[2], best_move[3], user_color)
    return

def play_game(driver, user_color, chessEngine):
    pgn = ""
    # Clear pgn.pgn file before use
    open('pgn.pgn', 'w').close()

    highlight_move(driver, user_color, "e2e4")
    '''
    auto_move(driver)

    for move_number in range(1, 500):
        pgn, move_notation = pgn_generator(driver, move_number, pgn, user_color)

        print(pgn)

        with open("pgn.pgn", "w") as text_file:
            text_file.write("%s" % pgn)

        best_move = get_best_move(chessEngine)

        highlight_move(driver, user_color, best_move)

        auto_move(driver)

        if game_end(user_color, move_notation) == 1:
            return
    '''
    return

#создаем драйвер
browser = webdriver.Chrome()
browser.implicitly_wait(3)

username = 'etspchess'
password = '121524'

chessEngine = ""

login(browser, username, password)

new_game(browser, username, chessEngine)

time.sleep(60000)

browser.quit()
