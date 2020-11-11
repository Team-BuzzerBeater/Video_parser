import os, json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR,'./json/')
def reader(year = 9, round = 1, team = 0):
    print("read round {} team number {}".format(round, team))
    textround = '0' + str(round) if round < 10 else str(round)
    with open(os.path.join(JSON_PATH, 'shoot_info_{}1{}{}.json'.format(year,textround,team)), 'r', encoding='UTF-8-sig') as f:
        json_data = json.load(f)
    return json_data

def showjson(year = 9, round = 1, team = 0):
    rdjson = reader(year,round,team)
    print(json.dumps(rdjson, indent ='\t',ensure_ascii=False))

def showfirstshoot(year = 9, round = 1, team = 0):
    rdjson = reader(year,round,team)

    rdjson1 = [play for play in rdjson if play['PERIOD_ID'] == 1]
    rdjson1.sort(key = lambda play : (play['MIN_TIME'], play['SEC_TIME']))
    print(rdjson1[0]['MIN_TIME'])
    print(rdjson1[0]['SEC_TIME'])
    print(rdjson1[0]['PLAYER_NAME'])
    print('--')

    rdjson2 = [play for play in rdjson if play['PERIOD_ID'] == 2]
    rdjson2.sort(key = lambda play : (play['MIN_TIME'], play['SEC_TIME']))
    print(rdjson2[0]['MIN_TIME'])
    print(rdjson2[0]['SEC_TIME'])
    print(rdjson2[0]['PLAYER_NAME'])

def showtimejson(year = 9, round = 1, team = 0):
    rdjson = reader(year,round,team)
    rdjson.sort(key = lambda play : (play['PERIOD_ID'],play['MIN_TIME'], play['SEC_TIME']))
    for play in rdjson:
        print(play['MIN_TIME'],' ',play['SEC_TIME'],' ',play['PLAYER_NAME'])


showtimejson(9,12,5)#showfirstshoot(9,12,5)