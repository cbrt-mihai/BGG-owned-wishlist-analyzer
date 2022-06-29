import json
import timeit
import urllib.request

import xlsxwriter
from bs4 import BeautifulSoup
from tqdm import tqdm


def printGameDataFromUrl(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()

    copyStr = mybytes.decode("utf8")
    arr = copyStr.split("GEEK.geekitemPreload =")
    arr2 = arr[1].split("GEEK.geekitemSettings =")
    jsonStr = arr2[0]
    goodJson = jsonStr[:-3]
    # print(goodJson)
    # jsonFile.write(goodJson)

    jsonParser = json.loads(goodJson)
    itemLinks = jsonParser["item"]["links"]
    itemRankinfo = jsonParser["item"]["rankinfo"]
    try:
        type = itemRankinfo[1]["veryshortprettyname"]
    except IndexError:
        type = "Uncategorized"

    gameName = jsonParser["item"]["name"]

    print("Game: " + gameName)
    print("Type: " + type)
    # print(list(itemLinks))
    for title in itemLinks:
        if (title == "boardgamecategory") or (title == "boardgamemechanic") or (title == "boardgamefamily"):
            tag = title.split("boardgame")[1]
            print(tag.capitalize() + ": ")
            for elem in itemLinks[title]:
                print("\t" + elem["name"])

    mystr = mybytes.decode("utf8")
    fp.close()

def writeGameDataFromUrl(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()

    fileName = url.split("/").pop() + ".txt"
    file = open(fileName, "w")

    copyStr = mybytes.decode("utf8")
    arr = copyStr.split("GEEK.geekitemPreload =")
    arr2 = arr[1].split("GEEK.geekitemSettings =")
    jsonStr = arr2[0]
    goodJson = jsonStr[:-3]
    # print(goodJson)
    # jsonFile.write(goodJson)

    jsonParser = json.loads(goodJson)
    itemLinks = jsonParser["item"]["links"]
    itemRankinfo = jsonParser["item"]["rankinfo"]
    try:
        type = itemRankinfo[1]["veryshortprettyname"]
    except IndexError:
        type = "Uncategorized"
    gameName = jsonParser["item"]["name"]

    file.write("Game: " + gameName + "\n")
    file.write("Type: " + type + "\n")
    # print(list(itemLinks))
    for title in itemLinks:
        if (title == "boardgamecategory") or (title == "boardgamemechanic") or (title == "boardgamefamily"):
            tag = title.split("boardgame")[1]
            file.write(tag.capitalize() + ": "  + "\n")
            for elem in itemLinks[title]:
                file.write("\t" + elem["name"]  + "\n")

    fp.close()
    file.close()

def writeToFileGameDataFromUrl(url, file):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()

    fileName = url.split("/").pop() + ".txt"

    copyStr = mybytes.decode("utf8")
    arr = copyStr.split("GEEK.geekitemPreload =")
    arr2 = arr[1].split("GEEK.geekitemSettings =")
    jsonStr = arr2[0]
    goodJson = jsonStr[:-3]
    # print(goodJson)
    # jsonFile.write(goodJson)

    jsonParser = json.loads(goodJson)
    itemLinks = jsonParser["item"]["links"]
    itemRankinfo = jsonParser["item"]["rankinfo"]
    try:
        type = itemRankinfo[1]["veryshortprettyname"]
    except IndexError:
        type = "Uncategorized"
    gameName = jsonParser["item"]["name"]

    try:
        file.write(f"Game: " + gameName + "\n")
    except UnicodeEncodeError:
        file.write(f"Game: " + str(gameName.encode('utf8')) + "\n")
    file.write("Type: " + type + "\n")
    # print(list(itemLinks))
    for title in itemLinks:
        if (title == "boardgamecategory") or (title == "boardgamemechanic") or (title == "boardgamefamily"):
            tag = title.split("boardgame")[1]
            file.write(tag.capitalize() + ": "  + "\n")
            for elem in itemLinks[title]:
                file.write("\t" + elem["name"]  + "\n")

    file.write("-----------\n\n")
    fp.close()

def getUrlList(url):
    baseUrl = url.split("/collection")[0]
    # print(baseUrl)

    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    # print(mystr)

    urlList = []
    soup = BeautifulSoup(mystr, features="lxml")
    for a in soup.find_all('a', {'class': 'primary'}, href=True):
        urlSuffix = a["href"]
        fullUrl = baseUrl + urlSuffix
        urlList.append(fullUrl)
        # print("Found the URL:", urlSuffix)
        # print("fullUrl: " + baseUrl + urlSuffix)

    return urlList

def printDataForAllGamesByUrlList(urlList):
    for url in urlList:
        # print(url)
        printGameDataFromUrl(url)

def writeDataForAllGamesByUrlList(urlList, file):
    count = 1
    urlListLength = len(urlList)
    for url in urlList:
        if count % 10 == 0:
            print(f"{count} / {urlListLength} done.")
        writeToFileGameDataFromUrl(url,file)
        count += 1

def writeToFileGameDataFromBoardgame(game, file):
    try:
        file.write(f"Game: " + game.name + "\n")
    except UnicodeEncodeError:
        file.write(f"Game: " + str(game.name.encode('utf8')) + "\n")

    file.write("Type: " + game.type + "\n")

    file.write("Categories:\n")
    for category in game.categories:
        file.write("\t" + category + "\n")

    file.write("Mechanics:\n")
    for mechanic in game.mechanics:
        file.write("\t" + mechanic + "\n")

    file.write("Families:\n")
    for family in game.families:
        file.write("\t" + family + "\n")

    file.write("-----------\n\n")

def writeDataForAllGamesByBoardgameList(gameList, file):
    count = 1
    listLength = len(gameList)
    for i in tqdm(range(len(gameList))):
        writeToFileGameDataFromBoardgame(gameList[i], file)
        count += 1

def getUsernameFromUrlOfLinks(url):
    questionMarkSplit = url.split("?")
    slashSplit = questionMarkSplit[0].split("/")
    username = slashSplit.pop()
    return username

class Boardgame:
    def __init__(self, name, type, categories, mechanics, families):
        self.name = name
        self.type = type
        self.categories = categories
        self.mechanics = mechanics
        self.families = families

class Category:
    def __init__(self, name, games):
        self.name = name
        self.games = games

class Type:
    def __init__(self, name, games):
        self.name = name
        self.games = games

class Mechanic:
    def __init__(self, name, games):
        self.name = name
        self.games = games

class Family:
    def __init__(self, name, games):
        self.name = name
        self.games = games

def createBoardgameFromUrl(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()

    copyStr = mybytes.decode("utf8")
    arr = copyStr.split("GEEK.geekitemPreload =")
    arr2 = arr[1].split("GEEK.geekitemSettings =")
    jsonStr = arr2[0]
    goodJson = jsonStr[:-3]
    # print(goodJson)
    # jsonFile.write(goodJson)

    jsonParser = json.loads(goodJson)
    itemLinks = jsonParser["item"]["links"]
    itemRankinfo = jsonParser["item"]["rankinfo"]
    try:
        type = itemRankinfo[1]["veryshortprettyname"]
    except IndexError:
        type = "Uncategorized"

    gameName = jsonParser["item"]["name"]

    # print("Game: " + gameName)
    # print("Type: " + type)
    # print(list(itemLinks))
    categories = []
    mechanics = []
    families = []
    categs = itemLinks["boardgamecategory"]
    mechs = itemLinks["boardgamemechanic"]
    fams = itemLinks["boardgamefamily"]
    # print(f"{gameName} - {categs}")

    for categ in categs:
        category = categ["name"]
        categories.append(category)

    for mech in mechs:
        mechanic = mech["name"]
        mechanics.append(mechanic)

    for fam in fams:
        family = fam["name"]
        families.append(family)

    boardgame = Boardgame(gameName, type, categories, mechanics, families)
    fp.close()

    return boardgame

def createBoardgameListFromUrlList(listOfUrls):
    print("Started createBoardgameListFromUrlLists")
    boardgames = []
    urlList = getUrlList(listOfUrls)
    urlListLength = len(urlList)
    for i in tqdm(range(len(urlList))):
        boardgames.append(createBoardgameFromUrl(urlList[i]))

    print("Finished createBoardgameListFromUrlLists")
    return boardgames

def elemExists(x, list):
    for elem in list:
        if( x == elem.name ):
            return True

    return False

def addInClass(bgName, x, list):
    for i, elem in enumerate(list):
        if(x == elem.name):
            list[i].games.append(bgName)

def printPercentageDone(current, max):
    print(f"{100*current/max}% done: {int(10*current/max)*chr(255)}{int(10*current/max)*chr(219)}")

def createCategoriesTypesMechanicsFamiliesFromBoardgameList(boardgameList):
    print("Started createCategoriesTypesMechanicsFamiliesFromBoardgameList")
    categoriesList = []
    typesList = []
    mechanicsList = []
    familiesList = []

    for boardgame in boardgameList:
        bgName = boardgame.name
        categories = boardgame.categories
        type = boardgame.type
        mechanics = boardgame.mechanics
        families = boardgame.families

        for category in categories:
            newCategory = Category(category, [bgName])
            if ( not elemExists(category, categoriesList) ):
                categoriesList.append(newCategory)
            else:
                addInClass(bgName, category, categoriesList)

        newType = Type(type, [bgName])
        if ( not elemExists(type, typesList) ):
            typesList.append(newType)
        else:
            addInClass(bgName, type, typesList)

        for mechanic in mechanics:
            newMechanic = Mechanic(mechanic, [bgName])
            if ( not elemExists(mechanic, mechanicsList) ):
                mechanicsList.append(newMechanic)
            else:
                addInClass(bgName, mechanic, mechanicsList)

        for family in families:
            newFamily = Family(family, [bgName])
            if ( not elemExists(family, familiesList) ):
                familiesList.append(newFamily)
            else:
                addInClass(bgName, family, familiesList)

    print("Finished createCategoriesTypesMechanicsFamiliesFromBoardgameList")
    return categoriesList, typesList, mechanicsList, familiesList

def printClassNameAndGameCountFromList(message, list):
    print(message)
    for elem in list:
        print("\t " + elem.name + " - " + str(len(elem.games)))

    print("\n")

def printGamesFromClassList(message, list):
    print(message)
    for elem in list:
        print("\t " + elem.name + " - " + str(len(elem.games)) + " - [" + ', '.join(map(str,elem.games)) + "] ")

    print("\n")

def writeGamesFromClassList(message, list, file):
    file.write(message + "\n")
    for elem in list:
        try:
            file.write("\t " + elem.name + " - " + str(len(elem.games)) + " - [" + ', '.join(map(str,elem.games)) + "] " + "\n")
        except UnicodeEncodeError:
            print(elem.name)
            print(elem.name.encode('utf8'))
            print(str(elem.name.encode('utf8')))
            file.write("\t " + str(elem.name.encode('utf8')) + " - " + str(len(elem.games)) + " - [" + ', '.join(map(str, elem.games)) + "] " + "\n")

    file.write("\n\n")

def excel_style(row, col):
    """ Convert given row and column number to an Excel-style cell name. """
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = []
    while col:
        col, rem = divmod(col-1, 26)
        result[:0] = LETTERS[rem]
    return ''.join(result) + str(row)

def createExcelGamesFromClassList(fileName, list):
    workbook = xlsxwriter.Workbook(f"{fileName[0]}.xlsx")

    BOLD_FORMAT = workbook.add_format({"bold": True})
    BOLD_FORMAT.set_align("center")

    CELL_FORMAT = workbook.add_format()
    CELL_FORMAT.set_align("center")

    for k in range(0, 4):
        worksheet = workbook.add_worksheet(fileName[k+1])

        for i, elem in enumerate(list[k]):
            header = f"{elem.name} {len(elem.games)}"
            address = f"{excel_style(1, i+1)}"
            worksheet.write(address, header, BOLD_FORMAT)
            maxLenGame = len(elem.name)
            for j, gameName in enumerate(elem.games):
                if len(gameName) > maxLenGame:
                    maxLenGame = len(gameName)
                addressEntry = f"{excel_style(j+2, i+1)}"
                worksheet.write(addressEntry, gameName, CELL_FORMAT)
            # print(f"{elem.name} {maxLenGame}")
            worksheet.set_column(i, i, width=maxLenGame + int(10*maxLenGame/100))
    workbook.close()

def elementNameInClassList(elemName, classList):
    for elem in classList:
        if elemName == elem.name:
            return elem

    return None

def createBuyList(wishlist, ownedLists):
    buyList = []
    buyListSplit = []

    for game in wishlist:
        gameName = game.name
        gameType = game.type
        gameCategories = game.categories
        gameMechanics = game.mechanics
        gameFamilies = game.families

        score = 0
        scoreType = 0
        scoreCategories = 0
        scoreMechanics = 0
        scoreFamilies = 0
        element = elementNameInClassList(gameType, ownedLists[1])
        if element is not None:
            score += len(element.games)
            scoreType += len(element.games)

        for category in gameCategories:
            element = elementNameInClassList(category, ownedLists[0])
            if element is not None:
                score += len(element.games)
                scoreCategories += len(element.games)

        for mechanic in gameMechanics:
            element = elementNameInClassList(mechanic, ownedLists[2])
            if element is not None:
                score += len(element.games)
                scoreMechanics += len(element.games)

        for family in gameFamilies:
            element = elementNameInClassList(family, ownedLists[3])
            if element is not None:
                score += len(element.games)
                scoreFamilies += len(element.games)

        buyList.append((gameName, score - scoreType, score))
        scoreAvg = (scoreCategories + scoreType + scoreMechanics + scoreFamilies)/4
        scoreNZAvg = (scoreCategories * int(bool(scoreCategories)) + scoreType * int(bool(scoreType)) +
                      scoreMechanics * int(bool(scoreMechanics)) + scoreFamilies * int(bool(scoreFamilies))) / (int(bool(scoreCategories)) + int(bool(scoreType)) + int(bool(scoreMechanics)) + int(bool(scoreFamilies)))
        score2Avg = (scoreAvg + scoreNZAvg)/2
        buyListSplit.append((gameName, score - scoreType, score, scoreAvg, scoreNZAvg, score2Avg, scoreCategories, scoreType, scoreMechanics, scoreFamilies))

    return buyList, buyListSplit

def printBuyListSplit(gameList):
    count = 0
    for game in gameList:
        count += 1
        gameName = game[0]
        scoreNoType = game[1]
        score = game[2]
        scoreAvg = game[3]
        scoreCategories = game[4]
        scoreType = game[5]
        scoreMechanics = game[6]
        scoreFamilies = game[7]

        print(f"{count}. {gameName}:")
        print(f"\t\tScore without Type: {scoreNoType}")
        print(f"\t\tScore with Type: {score}")
        print(f"\t\tScore Average: {scoreAvg}")
        print(f"\t\tScore by Categories: {scoreCategories}")
        print(f"\t\tScore by Type: {scoreType}")
        print(f"\t\tScore by Mechanics: {scoreMechanics}")
        print(f"\t\tScore by Families: {scoreFamilies}\n")

def writeBuyListSplit(fileName, gameList):
    file = open(fileName, "w", encoding='utf-8')
    count = 0
    for game in gameList:
        count += 1
        gameName = game[0]
        scoreNoType = game[1]
        score = game[2]
        scoreAvg = game[3]
        scoreNZAvg = game[4]
        score2Avg = game[5]
        scoreCategories = game[6]
        scoreType = game[7]
        scoreMechanics = game[8]
        scoreFamilies = game[9]

        file.write(f"{count}. {gameName}:\n")
        file.write(f"\tScore without Type: {scoreNoType}\n")
        file.write(f"\tScore with Type: {score}\n")
        file.write(f"\tScore Average: {scoreAvg}\n")
        file.write(f"\tScore !0 Average: {scoreNZAvg}\n")
        file.write(f"\tScore 2xAverage: {score2Avg}\n")
        file.write(f"\tScore by Categories: {scoreCategories}\n")
        file.write(f"\tScore by Type: {scoreType}\n")
        file.write(f"\tScore by Mechanics: {scoreMechanics}\n")
        file.write(f"\tScore by Families: {scoreFamilies}\n\n")

    file.close()

def writeBuyListIndexed(fileName, gameList):
    file = open(fileName, "w", encoding='utf-8')
    count = 0
    length = len(gameList)
    for i, game in enumerate(gameList):
        count += 1
        gameName = game
        # index1 = indexes[i][0]
        # index2 = indexes[i][1]
        # index3 = indexes[i][2]
        #
        # indexAvg = (index1 + index2 + index3)/3

        file.write(f"{count}. {gameName}\n")
        if( (i+1) == int(length/2)):
            file.write("===========\n")
        elif ( (i+1) % int(length/4) == 0):
            file.write("-----------\n")

    file.close()

def createAvgIndexList(lists):
    auxList = []
    # indexes = []
    for i, elem in enumerate(lists[0]):
        index1 = i + 1
        index2 = lists[1].index(elem) + 1
        index3 = lists[2].index(elem) + 1

        avgIndex = (index1 + index2 + index3)/3
        # print(f"{elem[0]} - {index1}, {index2}, {index3}, {avgIndex}, {int(avgIndex)}")

        auxList.append((elem, int(avgIndex)))
        # indexes.append((index1, index2, index3))

    auxList.sort(key=takeSecond)

    newList = []
    for elem in auxList:
        newList.append(elem[0][0])

    return newList



def writeFullPackage(ownedTxtName, ownedTxtNameSplit, wishlistTxtName, wishlistTxtNameSplit, ownedExcelName, wishExcelName, buyTxtName, ownedListLink, wishlistLink):
    # ownedList = getUrlList(ownedListLink)
    # wishList = getUrlList(wishlistLink)

    boardgameList = createBoardgameListFromUrlList(ownedListLink)
    wishlistBoardgamesList = createBoardgameListFromUrlList(wishlistLink)
    categoryList, typeList, mechanicList, familyList = createCategoriesTypesMechanicsFamiliesFromBoardgameList(boardgameList)
    wCategoryList, wTypeList, wMechanicList, wFamilyList = createCategoriesTypesMechanicsFamiliesFromBoardgameList(wishlistBoardgamesList)

    fileName = "output/" + ownedTxtName + ".txt"
    file = open(fileName, "w", encoding='utf-8')
    # writeDataForAllGamesByUrlList(ownedList, file)
    writeDataForAllGamesByBoardgameList(boardgameList, file)
    file.close()

    fileName = "output/" + wishlistTxtName + ".txt"
    file = open(fileName, "w", encoding='utf-8')
    # writeDataForAllGamesByUrlList(wishList, file)
    writeDataForAllGamesByBoardgameList(wishlistBoardgamesList, file)
    file.close()

    fileName = "output/" + ownedTxtNameSplit + ".txt"
    file = open(fileName, "w", encoding='utf-8')
    writeGamesFromClassList("Categories: ", categoryList, file)
    writeGamesFromClassList("Types: ", typeList, file)
    writeGamesFromClassList("Mechanics: ", mechanicList, file)
    writeGamesFromClassList("Families: ", familyList, file)
    file.close()

    fileName = "output/" + wishlistTxtNameSplit + ".txt"
    file = open(fileName, "w", encoding='utf-8')
    writeGamesFromClassList("Categories: ", wCategoryList, file)
    writeGamesFromClassList("Types: ", wTypeList, file)
    writeGamesFromClassList("Mechanics: ", wMechanicList, file)
    writeGamesFromClassList("Families: ", wFamilyList, file)
    file.close()

    excelNames = [f"output/{ownedExcelName}", "Categories", "Types", "Mechanics", "Families"]
    lists = [categoryList, typeList, mechanicList, familyList]
    createExcelGamesFromClassList(excelNames, lists)

    wExcelNames = [f"output/{wishExcelName}", "Categories", "Types", "Mechanics", "Families"]
    wLists = [wCategoryList, wTypeList, wMechanicList, wFamilyList]
    createExcelGamesFromClassList(wExcelNames, wLists)

    sortedLists = []

    gamesToBuyList, gamesToBuyListSplit = createBuyList(wishlistBoardgamesList, lists)
    sorted1 = sorted(gamesToBuyListSplit, key=lambda x: (x[5], x[3], x[1]))
    # gamesToBuyListSplit.sort(key=lambda x: (x[5], x[3], x[1]))
    wishTxt = "output/" + buyTxtName + "_2AvgToAvgToScore.txt"
    writeBuyListSplit(wishTxt, sorted1)

    gamesToBuyList, gamesToBuyListSplit = createBuyList(wishlistBoardgamesList, lists)
    sorted2 = sorted(gamesToBuyListSplit, key=lambda x: (x[3], x[1]))
    # gamesToBuyListSplit.sort(key=lambda x: (x[3], x[1]))
    wishTxt = "output/" + buyTxtName + "_AvgToScore.txt"
    writeBuyListSplit(wishTxt, sorted2)

    gamesToBuyList, gamesToBuyListSplit = createBuyList(wishlistBoardgamesList, lists)
    sorted3 = sorted(gamesToBuyListSplit, key=lambda x: (x[1]))
    # gamesToBuyListSplit.sort(key=lambda x: (x[1]))
    wishTxt = "output/" + buyTxtName + "_Normal.txt"
    writeBuyListSplit(wishTxt, sorted3)

    sortedLists.append(sorted1)
    sortedLists.append(sorted2)
    sortedLists.append(sorted3)

    avgIndexList = createAvgIndexList(sortedLists)
    wishTxt = "output/" + buyTxtName + "_Indexed.txt"
    writeBuyListIndexed(wishTxt, avgIndexList)

def takeSecond(elem):
    return elem[1]

def takeThird(elem):
    return elem[2]

def takeFourth(elem):
    return elem[3]
