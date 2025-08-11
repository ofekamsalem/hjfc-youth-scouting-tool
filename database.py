from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import pandas as pd
from team_selection import choose_team
from team_selection import load_config



def get_team_url() -> str:
    config = load_config()
    team = choose_team(config)

    base_url = config['base url']
    team_url = base_url.format(team_id=team['team id'])
    return team_url


def scratch_names_and_minutes():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 20)
    driver.get(get_team_url())

    # wait for container to appear
    container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "section.players-statistics-container")))
    print(type(container))

    # scroll into view 
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)

    # wait for tale rows - allow both <a> and <div> elements
    rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "section.players-statistics-container .table_row.link_url")))

    print(type(rows))

    players_data = []  # will store [name, minutes]

    for row in rows:
        cols = row.find_elements(By.CSS_SELECTOR, "div.table_col")
        name = None
        minutes = None

        for col in cols:
            labels = [el.text.strip() for el in col.find_elements(By.CSS_SELECTOR, "span.sr-only")]

            # find player name
            if any(lbl in ("שם השחקן") for lbl in labels):
                txt = col.text.strip()
                for lbl in ("שם השחקן", "שם שחקן"):
                    txt = txt.replace(lbl, "")
                name = txt.strip().strip('"')  

            # find minutes he played in leauge and cups
            if any(lbl == "דקות משחק" for lbl in labels):
                txt = col.text.replace("דקות משחק", "").strip()
                minutes = int("".join(ch for ch in txt if ch.isdigit()) or "0")
            # if we already have both - no need to check more columns
            if name is not None and minutes is not None:
                break
        if name is not None and minutes is not None:
            players_data.append([minutes,name])
    driver.quit()
    return players_data



def put_db_in_table():
    df = pd.DataFrame(scratch_names_and_minutes(), columns=["דקות משחק", "שם השחקן"])
    df.to_excel("players_minutes.xlsx", index=False)

put_db_in_table()









