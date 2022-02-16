from selenium import webdriver
import time
import random

website_url = "https://teame9.herokuapp.com/"
outputfile = open("selenium_test.txt", 'w')

#path = input('provide PATH for chromedriver.exe:\n')
#pathdriver = path
path = 'C:/Users/fluff/Downloads/chromedriver_win32/chromedriver.exe'
driver = webdriver.Chrome(path)

# v XPATH and URL information v#
nav_links = {
    'players':{'xpath': '/html/body/nav/ul/li[1]/a', 'url':'https://teame9.herokuapp.com/Players'},
    'teams':{'xpath':'/html/body/nav/ul/li[2]/a', 'url':'https://teame9.herokuapp.com/Teams'},
    'news':{'xpath':'/html/body/nav/ul/li[3]/a','url':'https://teame9.herokuapp.com/News'},
    'about':{'xpath':'/html/body/nav/ul/li[4]/a', 'url':'https://teame9.herokuapp.com/AboutPage'}
}
dropdown_links = {
        'dropdown':{'xpath':"/html/body/nav/ul/li[5]/a", 'url':'https://teame9.herokuapp.com/'},
        'fantasy':{'xpath':"/html/body/nav/ul/li[5]/div/a[1]", 'url':'https://teame9.herokuapp.com/Fantasy'},
        'fran_leaders':{'xpath':"/html/body/nav/ul/li[5]/div/a[2]", 'url':'https://teame9.herokuapp.com/Franchise_Leaders'},
        'coaches':{'xpath':"/html/body/nav/ul/li[5]/div/a[3]", 'url':'https://teame9.herokuapp.com/Coaches'},
        'archive':{'xpath':"/html/body/nav/ul/li[5]/div/a[4]", 'url':'https://teame9.herokuapp.com/Year'},
        'fav_team':{'xpath':"/html/body/nav/ul/li[5]/div/a[5]", 'url':'https://teame9.herokuapp.com/favteam'},
        'fav_players':{'xpath':"/html/body/nav/ul/li[5]/div/a[6]", 'url':'https://teame9.herokuapp.com/favplayer'},
        'compare':{'xpath':"/html/body/nav/ul/li[5]/div/a[7]", 'url':'https://teame9.herokuapp.com/comparison'},
        'settings':{'xpath':"/html/body/nav/ul/li[5]/div/a[8]", 'url':'https://teame9.herokuapp.com/Settings'}
}

page_urls = {
    'players':'https://teame9.herokuapp.com/Players',
    'teams':'https://teame9.herokuapp.com/Teams',
    'news':'https://teame9.herokuapp.com/News',
    'about':'https://teame9.herokuapp.com/AboutPage',
    'fantasy':'https://teame9.herokuapp.com/Fantasy',
    'fran_leaders':'https://teame9.herokuapp.com/Franchise_Leaders',
    'coaches':'https://teame9.herokuapp.com/Coaches',
    'archive':'https://teame9.herokuapp.com/Year',
    'fav_team':'https://teame9.herokuapp.com/favteam',
    'fav_player':'https://teame9.herokuapp.com/favplayer',
    'compare':'https://teame9.herokuapp.com/comparison',
    'settings':'https://teame9.herokuapp.com/Settings',
    'p_instance':'https://teame9.herokuapp.com/PlayerInstancePage',
    't_instance':'https://teame9.herokuapp.com/TeamInstancePage',
    'log_in':'https://teame9.herokuapp.com/account',
    'sign_up':'https://teame9.herokuapp.com/signup'
}

players_model_pages = {
    'player_go':{'xpath':'/html/body/form/input'},
    'player_page5':{'xpath':'//*[@id="page"]/option[5]', 'url':'https://teame9.herokuapp.com/Players?page=5&Status=None&Position=None&Team=None&Sort=None'},
    'player_page8':{'xpath':'//*[@id="page"]/option[8]', 'url':'https://teame9.herokuapp.com/Players?page=8&Status=None&Position=None&Team=None&Sort=None'},
    'player_page12':{'xpath':'//*[@id="page"]/option[12]', 'url':'https://teame9.herokuapp.com/Players?page=12&Status=None&Position=None&Team=None&Sort=None'}
}
team_model_pages = {
    'team_go':{'xpath':'/html/body/form/input'},
    'team_page3':{'xpath':'//*[@id="page"]/option[3]', 'url':'https://teame9.herokuapp.com/Teams?page=3&League=None&Conference=None&Division=None&Sort=None'}
}




## NAV BAR LINKS ##
def test_navbarLinks():
    outputfile.write("\n\nNow testing: Navbar links\n")
    #main
    navbar_list = list(nav_links.values())
    for i in range(len(nav_links)):
        driver.get(website_url)
        nav_button = driver.find_element_by_xpath(navbar_list[i]['xpath'])
        time.sleep(.25)
        nav_button.click()
        if driver.current_url == navbar_list[i]['url']:
            outputfile.write("URL " + navbar_list[i]['url'] + " has been reached.\n")
        else:
            outputfile.write("URL " + navbar_list[i]['url'] + " has NOT been reached.\n")

    #dropdown
    dd_list = list(dropdown_links.values())
    for i in range(len(dropdown_links)-1):
        driver.get(website_url)
        dd = driver.find_element_by_xpath(dd_list[0]['xpath'])
        dd.click()
        time.sleep(.25)
        dd_button = driver.find_element_by_xpath(dd_list[i+1]['xpath'])
        dd_button.click()
        if driver.current_url == dd_list[i+1]['url']:
            outputfile.write("URL " + driver.current_url + " has been reached.\n")
        else:
            outputfile.write("URL " + dd.current_url + " has not been reached.\n")
    return


## PAGINATION & SCROLL ##
# pagination on model pages. wll need to scroll too
# click to next page and compare URLs? ig
def test_scroll_pagination():
    outputfile.write("\n\nNow testing: Scroll and Pagination on Model pages\n")
    pm_list = list(players_model_pages.values())
    driver.get("https://teame9.herokuapp.com/Players")
    page_height = driver.execute_script("return document.body.scrollHeight")
    incr_count = page_height // 100
    for x in range(7):
        for i in range(incr_count):
            driver.execute_script("window.scrollTo(0,"+str(i*100)+")")
            time.sleep(.02)

        get_button = driver.find_element_by_xpath("/html/body/div[3]/div[2]/span/div/form[6]/input")
        get_button.click()
    if driver.current_url == "https://teame9.herokuapp.com/Players?page=17&Name=none&Status=none&Position=none&Team=none&Sort=None":
        outputfile.write("Was able to reach the last page: "+driver.current_url + ".\n")
    else:
        outputfile.write("Was NOT able to reach the last: "+ driver.current_url + ".\n")

    driver.get("https://teame9.herokuapp.com/Teams")
    tm_list = list(team_model_pages.values())
    for x in range(1):
        for i in range(incr_count):
            driver.execute_script("window.scrollTo(0,"+str(i*100)+")")
            time.sleep(.05)

        get_button = driver.find_element_by_xpath("/html/body/div[3]/div[2]/span/div/form[8]/input")
        get_button.click()
    if driver.current_url == "https://teame9.herokuapp.com/Teams?page=7&Name=None&League=None&Conference=None&Division=None&Sort=None":
        outputfile.write("Was able to reach the last page: "+driver.current_url + ".\n")
    else:
        outputfile.write("Was NOT able to reach the last: "+ driver.current_url + ".\n")

    return



## LOG-IN + FAVORITE TEAM/PLAYERS ##
# log in, go to favorite players/team, add fave, check contents of fave team/player page
def test_logInOut():
    outputfile.write("\n\nNow testing: Ability to log in and log out.\n")
    driver.get("https://teame9.herokuapp.com/account")
    #make an account
    email_in = driver.find_element_by_xpath("//*[@id='login_email']")
    email_in.send_keys('seleniumtest@gmail.com')
    pass_in = driver.find_element_by_xpath("//*[@id='login_pass']")
    pass_in.send_keys('password')
    sign_up_b = driver.find_element_by_xpath("/html/body/div/div/div/form/div[3]/button")
    sign_up_b.click()

    driver.get(website_url)
    logout_b = driver.find_element_by_xpath("//*[@id='logbutton']/a")
    logout_b.click()
    if driver.current_url == "https://teame9.herokuapp.com/loggedout":
        outputfile.write("SUCCESS: Can log-in with 'seleniumtest@gmail.com' + 'password' and log out.\n")
    else:
        outputfile.write("ERROR: Unable to log in and log out.\n")
    #check if logged out
    return

## ADDING AND REMOVING FAVORITE PLAYERS ##
def test_addremove():
    outputfile.write("\n\nNow Testing: Ability to add and remove a favorite player.\n")
    driver.get("https://teame9.herokuapp.com/account")
    email_in = driver.find_element_by_xpath("//*[@id='login_email']")
    email_in.send_keys('seleniumtest@gmail.com')
    pass_in = driver.find_element_by_xpath("//*[@id='login_pass']")
    pass_in.send_keys('password')
    sign_up_b = driver.find_element_by_xpath("/html/body/div/div/div/form/div[3]/button")
    sign_up_b.click()

    driver.get("https://teame9.herokuapp.com/Players")
    playerb = driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[6]/form/input")
    playerb.click()
    playerb = driver.find_element_by_xpath("/html/body/div/div/div[3]/div[2]/span[2]/form/button")
    playerb.click()
    driver.get("https://teame9.herokuapp.com/favplayer")
    try:
        playerb = driver.find_element_by_xpath("/html/body/div[3]/div/div[3]/div/form/button")
        playerb.click()
        outputfile.write("SUCCESS: Can add and remove a player.\n")
    except:
        outputfile.write("ERROR: Can NOT add and remove a player.\n")

    driver.get(website_url)
    logout_b = driver.find_element_by_xpath("//*[@id='logbutton']/a")
    logout_b.click()

    return



## RANDOM GAMES ON HOMEPAGE ##
# get first game on page. refresh. get first game and compare
def test_randomGamesOutput():
    outputfile.write("\n\nNow testing: Random Games shown on homepage.\n")
    driver.get(website_url)
    team1_prev = driver.find_element_by_xpath("//*[@id='box_score']/table/tbody/tr[2]/td[1]")
    team1_prev_text = team1_prev.text
    team2_prev = driver.find_element_by_xpath("//*[@id='box_score']/table/tbody/tr[2]/td[4]")
    team2_prev_text = team2_prev.text

    driver.refresh()
    team1_after = driver.find_element_by_xpath("//*[@id='box_score']/table/tbody/tr[2]/td[1]")
    team2_after = driver.find_element_by_xpath("//*[@id='box_score']/table/tbody/tr[2]/td[4]")

    if team1_prev_text != team1_after.text and team2_prev_text != team1_after.text:
        outputfile.write("SUCCESS: First game shown on homepage before refreshing: " + team1_prev_text + " vs " + team2_prev_text + ".\n" +
            " First game shown on homepage after refreshing: " + team1_after.text + " vs " + team2_after.text + ". " + 
            " Games shown on homepage are chosen at random.\n")
    else:
        outputfile.write("ERROR: First game shown on homepage before and after refreshing is the same. Games shown " +
            "on homepage are not random.\n")

    return

def test_search():
    outputfile.write("\n\nNow Testing: Search Function.\n")
    driver.get("https://teame9.herokuapp.com/Players")
    searchbar = driver.find_element_by_xpath("/html/body/div[2]/form[1]/input[1]")
    searchbar.send_keys("james")
    searchbutton = driver.find_element_by_xpath("/html/body/div[2]/form[1]/input[2]")
    searchbutton.click()

    element_one = driver.find_element_by_xpath("//*[@id='playerspage_m']/div[1]/div[1]/h4")
    element_two = driver.find_element_by_xpath("//*[@id='playerspage_m']/div[1]/div[2]/h4")
    element_three = driver.find_element_by_xpath("//*[@id='playerspage_m']/div[1]/div[3]/h4")

    if "James" in element_one.text and "James" in element_two.text and "James" in element_three.text:
        outputfile.write("SUCCESS: Searched James and found expected results.\n")
    else: 
        outputfile.write("ERROR: Searched James and did not find all expected results.\n")

    driver.get("https://teame9.herokuapp.com/Players")
    position = driver.find_element_by_xpath("//*[@id='Position']")
    position.click()
    position = driver.find_element_by_xpath("//*[@id='Position']/option[2]")
    position.click()
    pos_b = driver.find_element_by_xpath("/html/body/div[2]/form[2]/input")
    pos_b.click()

    for i in range(6):
        for x in range(6):
            get_player = driver.find_element_by_xpath("/html/body/div[3]/div[1]/div["+str(x+1)+"]/table/tbody/tr[3]/td[2]")
            if "Forward" not in get_player.text:
                outputfile.write("ERROR: Filtered by Position:Forward. Not all results fit the expected criteria.\n")
                return
        if i < 5:
            nextbutton = driver.find_element_by_xpath("/html/body/div[3]/div[2]/span/div/form[7]/input")
            nextbutton.click()

    outputfile.write("SUCCESS: Filtered by Position:Forward. All results fit the expected criteria.\n")

    return

## EXTRA BUTTONS ##
def test_buttons_franchiseLeader_Archive():
    outputfile.write("\n\nNow Testing: Buttons on Franchise Leaders and Archive page.\n")
    driver.get("https://teame9.herokuapp.com/Franchise_Leaders")

    for x in range(30):
        try:
            get_team = driver.find_element_by_xpath("/html/body/div[2]/form/table["+str(x+1)+"]/tbody/tr[1]/td/input")
            get_team.click()
        except:
            outputfile.write("ERROR: NOT able to traverse through each team, problem with picking team.\n")
            break;
        if x == 29:
            get_team = driver.find_element_by_xpath("/html/body/div[2]/div/h2/b")
            if "Washington Wizards" in get_team.text:
                outputfile.write("SUCCESS: Able to traverse through each team.\n")
            else:
                outputfile.write("ERROR: NOT able to traverse through each team, problem with last team.\n")
                break;
        else:
            try:
                go_back = driver.find_element_by_xpath("/html/body/div[1]/div/span/form/input")
                go_back.click()     
            except:
                outputfile.write("ERROR: NOT able to traverse through each team, problem with going back to all teams.\n")
                break;

    driver.get("https://teame9.herokuapp.com/Year")
    for i in range(7):
        get_decade = driver.find_element_by_xpath("/html/body/div[2]/div/div/div/span/div/form["+str(i+1)+"]/input")
        get_decade.click()
        for y in range(10):
            get_year = driver.find_element_by_xpath("/html/body/div[2]/div/div/ul/form["+str(y+1)+"]/input")
            get_year.click()

            if y == 9 and i == 6:
                if driver.current_url == "https://teame9.herokuapp.com/Year?page=7&year=1950":
                    outputfile.write("SUCCESS: Was able to traverse through the decades and years.\n")
                else:
                    outputfile.write("ERROR: Was NOT able to traverse through the decades and years.\n")
    return

    

## CSS ATTRIBUTES ##
def test_CSS():
    outputfile.write("\n\nNow Testing: CSS attributes.\n")
    driver.get(website_url)
    testelement = driver.find_element_by_css_selector("#logbutton")
    testvalue = testelement.get_attribute("style")
    if "position: absolute" in testvalue and "right: 10px" in testvalue:
        outputfile.write("SUCCESS: Log-In button is in correct position; absolute and 10px from right of screen.\n")
    else:
        outputfile.write("ERROR: Log-In button is not in correct position.\n")
    # TEST table on homepage
    table_element = driver.find_element_by_xpath("//*[@id='box_score']/table")
    table_class = table_element.get_attribute("class")
    if table_class == 'center':
        outputfile.write("SUCCESS: Homepage table class is centered.\n")
    else:
        outputfile.write("ERROR: Homepage table class is not centered.\n")
    table_style = table_element.get_attribute("style")
    if 'width: 80%' in table_style:
        outputfile.write("SUCCESS: Homepage table is correct width.\n")
    else:
        outputfile.write("ERROR: Homepage table is incorrect width.\n")
    if 'text-align: center' in table_style:
        outputfile.write("SUCCESS: Homepage table has centered text.\n")
    else:
        outputfile.write("ERROR: Homepage table does not have centered text.\n")
    # TEST num of instances on player ?
    driver.get("https://teame9.herokuapp.com/Players")
    player_element = driver.find_element_by_xpath("/html/body/div[3]/div[1]")
    player_class = player_element.get_attribute("class")
    if "card" in player_class:
        outputfile.write("SUCCESS: Player instance is a card.\n")
    else:
        outputfile.write("ERROR: Player instance is not a card.\n")
    player_status = driver.find_element_by_xpath("//*[@id='player_table']/tbody/tr[1]/td[1]")
    player_team = driver.find_element_by_xpath("//*[@id='player_table']/tbody/tr[2]/td[1]")
    player_position = driver.find_element_by_xpath("//*[@id='player_table']/tbody/tr[3]/td[1]")
    player_career = driver.find_element_by_xpath("//*[@id='player_table']/tbody/tr[4]/td[1]")
    if "Status" in player_status.text and "Team" in player_team.text and "Position" in player_position.text and "Career" in player_career.text:
        outputfile.write("SUCCESS: Player instance includes all necessary table information.\n")
    else:
        outputfile.write("ERROR: Player instance is missing table information.\n")

    # TEST carousel on player's instance page
    playerbutton = driver.find_element_by_xpath("//*[@id='playerspage_m']/div[1]/div[1]/form/input")
    playerbutton.click()
    carousel_element = driver.find_element_by_xpath("//*[@id='demo']")
    carousel_att = carousel_element.get_attribute("class")
    if "carousel slide pointer-event" in carousel_att:
        outputfile.write("SUCCESS: Images on Player Instance page are shown in a carousel.\n")
    else:
        outputfile.write("ERROR: Images on Player Instance page are not shown in a carousel.\n")
    firstimg_element = driver.find_element_by_xpath("//*[@id='demo']/div/div[1]/img")
    img_att = firstimg_element.get_attribute("src")
    if ".jpg" in img_att:
        outputfile.write("SUCCESS: An image is presented on the Player Instance page.\n")
    else:
        outputfile.write("ERROR: An image is not presented on the Player Instance page.\n")

    #TEST style consistency
    players_bg = driver.find_element_by_xpath("//*[@id='playerspage']")
    players_width = players_bg.value_of_css_property("width")
    players_bgcolor = players_bg.value_of_css_property("background-color")
    players_marginR = players_bg.value_of_css_property("margin-right")


    driver.get("https://teame9.herokuapp.com/Teams")
    teambutton = driver.find_element_by_xpath("//*[@id='teamspage_m']/div[1]/div[1]/form/input")
    teambutton.click()
    teams_bg = driver.find_element_by_xpath("//*[@id='teamspage']")
    teams_width = teams_bg.value_of_css_property("width")
    teams_bgcolor = teams_bg.value_of_css_property("background-color")
    teams_marginR = teams_bg.value_of_css_property("margin-right")

    driver.get("https://teame9.herokuapp.com/News")
    newsbutton = driver.find_element_by_xpath("//*[@id='newspage_m']/div[1]/div[1]/form/input")
    newsbutton.click()
    news_bg = driver.find_element_by_xpath("//*[@id='newspage']")
    news_width = news_bg.value_of_css_property("width")
    news_bgcolor = news_bg.value_of_css_property("background-color")
    news_marginR = news_bg.value_of_css_property("margin-right")

    if (players_width == teams_width) and (teams_width == news_width) and (players_bgcolor == teams_bgcolor) and (teams_bgcolor == news_bgcolor) and (players_marginR == teams_marginR) and (teams_marginR == news_marginR):
       outputfile.write("SUCCESS: Style amongst the players, teams, and news instance pages is consistent.\n")
    else:
       outputfile.write("ERROR: Style amongst the players, teams, and news instance pages is NOT consistent.\n")


    #TEST log in page 
    driver.get("https://teame9.herokuapp.com/account")
    logemail_element = driver.find_element_by_xpath("//*[@id='login_email']")
    email_att = logemail_element.get_attribute("type")
    logpass_element = driver.find_element_by_xpath("//*[@id='login_pass']")
    pass_att = logpass_element.get_attribute("type")
    if "password" in pass_att and "email" in email_att:
        outputfile.write("SUCCESS: Log-in page will take in input of type email and password.\n")
    else: 
        outputfile.write("ERROR Log-in page does not take in input of type email and/or password.\n")

    return

if __name__ == '__main__':
    print('GUI and front-end testing has begun, check selenium_test.txt for results')
    test_navbarLinks()
    test_scroll_pagination()
    test_logInOut()
    test_addremove()
    test_randomGamesOutput()
    test_buttons_franchiseLeader_Archive()
    test_CSS()
    test_search()
    driver.quit()
    outputfile.write("\n\nDone testing GUI and front end.")




