from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

year = input("년도(2015년부터): ")
innings = int(input("이닝(100이닝 이상): "))

columns = ['이름', '출장', '완투', '완봉', '선발', '승', '패', '세', '홀드', '이닝', '실점', '자책', '타자', '안타', '2타', '3타', '홈런', '볼넷', '고4', '사구', '삼진', '보크', '폭투', 'ERA', 'FIP', 'WHIP', 'ERA+', 'FIP+', 'WAR', 'WPA']
data = []
html = urlopen("http://www.statiz.co.kr/stat.php?re=1&ys=" + year + "&ye=" + year + "&o1=OutCount&de=1&sn=100")
bsObject = BeautifulSoup(html, "html.parser")

players = []
for i, x in enumerate(bsObject.select("td a")):
   if i % 21 == 1 and float(x.get_text()) < innings:
      tmp = i // 21
      break
   if i % 21 != 1:
      players.append(x.get_text().strip())

np_players = np.array(players[:20 * tmp])
np_players = np.reshape(np_players, (tmp, 20))

players2 = []
players3 = []
players4 = []
players5 = []
players6 = []
for i, x in enumerate(bsObject.select("td span")):
   if i % 33 == 3 and float(x.get_text()) < innings:
      break
   if i % 33 > 26:
      players2.append(x.get_text().strip())
   if i % 33 == 13:
      players3.append(x.get_text().strip())
   if i % 33 == 14:
      players4.append(x.get_text().strip())
   if i % 33 == 24:
      players5.append(x.get_text().strip())
   if i % 33 == 25:
      players6.append(x.get_text().strip())

np_players2 = np.array(players2[:6 * tmp])
np_players2 = np.reshape(np_players2, (tmp, 6))

np_players = np.insert(np_players, 10, players3, axis=1)
np_players = np.insert(np_players, 11, players4, axis=1)
np_players = np.insert(np_players, 21, players5, axis=1)
np_players = np.insert(np_players, 22, players6, axis=1)
np_players = np.append(np_players, np_players2, axis=1)
df = pd.DataFrame(np_players, columns = columns)
df.set_index('이름', inplace=True)

df.to_csv('baseball.csv', encoding='euc-kr')