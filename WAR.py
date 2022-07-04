'''
Using WAR data from https://public.tableau.com/app/profile/topdownhockey
'''

import csv
import statistics as stats
from toPercentile import *
import unicodedata


def WAR(NAME=None, decimals=1):
    global FMEAN
    global FSD

    global DMEAN
    global DSD

    global QFMEAN
    global QFSD

    global QDMEAN
    global QDSD

    global FDATAfiltered
    global DDATAfiltered

    global FDATA
    global DDATA

    global QFDATA
    global QDDATA

    global QFDATAfiltered
    global QDDATAfiltered

    global newteams

    newteams = get_new_teams()

    with open('Data/Aggregate_Skater_WAR_war_21_22_data.csv') as csvfile:
        csv_reader = csv.reader(csvfile)
        line_count = 0

        FDATA = []
        DDATA = []
        FDATAfiltered = []
        DDATAfiltered = []

        for row in csv_reader:
            line_count += 1
            if line_count == 1:
                continue

            DATA = ExtractData(row)
            DATAfiltered = ExtractData(row, EVTOIcutoff=200, PPTOIcutoff=20, SHTOIcutoff=20)

            if row[2] == 'F':
                FDATA.append(DATA)
            elif row[2] == 'D':
                DDATA.append(DATA)
            else:
                continue

            if DATAfiltered is None:
                continue

            if row[2] == 'F':
                FDATAfiltered.append(DATAfiltered)
            elif row[2] == 'D':
                DDATAfiltered.append(DATAfiltered)
            else:
                continue

    with open('Data/TOI.csv', encoding='utf-16') as csvfile:
        csv_reader = csv.reader(csvfile)
        line_count = 0
        QFDATA = []
        QDDATA = []
        QFDATAfiltered = []
        QDDATAfiltered = []

        for row in csv_reader:
            line_count += 1
            if line_count == 1:
                continue
            row = ''.join(row).split('\t')
            DATA = ExtractQData(row)
            DATAfiltered = ExtractQData(row, TOIcutoff=200)

            if DATA[1] == 'F':
                QFDATA.append(DATA)
            elif DATA[1] == 'D':
                QDDATA.append(DATA)
            else:
                continue

            if DATAfiltered is None:
                continue

            if DATA[1] == 'F':
                QFDATAfiltered.append(DATAfiltered)
            elif DATA[1] == 'D':
                QDDATAfiltered.append(DATAfiltered)
            else:
                continue


    FMEAN = getMean(FDATAfiltered)
    FSD = getSD(FDATAfiltered)

    DMEAN = getMean(DDATAfiltered)
    DSD = getSD(DDATAfiltered)

    QFMEAN = getQMean(QFDATAfiltered)
    QFSD = getQSD(QFDATAfiltered)

    QDMEAN = getQMean(QDDATAfiltered)
    QDSD = getQSD(QDDATAfiltered)

    if NAME is None:
        while True:
            NAME = input("Enter NHL Player Name:\n")
            if NAME == '':
                print("Exiting...")
                return

            NAME = NAME.upper()
            error = True
            for player in FDATA:
                if player[0] == NAME:
                    DATA = player
                    error = False
            for player in DDATA:
                if player[0] == NAME:
                    DATA = player
                    error = False

            if error:
                simname = FDATA[0][0]
                minLD, minlen = NameDifference(simname, NAME)

                for player in FDATA:
                    if NameDifference(player[0], NAME)[0] < minLD:
                        minLD, minlen = NameDifference(player[0], NAME)
                        simname = player[0]

                for player in DDATA:
                    if NameDifference(player[0], NAME)[0] < minLD:
                        minLD, minlen = NameDifference(player[0], NAME)
                        simname = player[0]

                if minLD > 2 + 0.5 * minlen:
                    print(f"\nError: No Player With The Name: {NAME} Has Been Found. (Difference Score: {minLD})\n")
                    continue
                else:
                    print(f"Did you mean: {simname}? (Difference Score: {minLD})\n")
                    NAME = simname

            P1 = PlayerCard(NAME, decimals)

            P1.displayZ()
            P1.displayPerc()

    else:
        NAME = NAME.upper()
        error = True
        for player in FDATA:
            if player[0] == NAME:
                DATA = player
                error = False
        for player in DDATA:
            if player[0] == NAME:
                DATA = player
                error = False

        if error:
            return None
        else:
            return PlayerCard(NAME)


def NameDifference(name1, name2):
    LD1 = LD(name1, name2)
    len1 = min(len(name1), len(name2))
    LD2 = LD(RemoveFirst(name1), name2)
    len2 = min(len(RemoveFirst(name1)), len(name2))

    if LD1 == LD2:
        if len1 < len2:
            return [LD2, len2]
        else:
            return [LD1, len1]
    elif LD1 < LD2:
        return [LD1, len1]
    else:
        return [LD2, len2]


def RemoveFirst(name):
    name = name.split()[1:]
    return ' '.join(name)


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


def LD(s, t, costs=(1, 1, 4)):
    """
        iterative_levenshtein(s, t) -> ldist
        ldist is the Levenshtein distance between the strings
        s and t.
        For all i and j, dist[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t

        costs: a tuple or a list with three integers (d, i, s)
               where d defines the costs for a deletion
                     i defines the costs for an insertion and
                     s defines the costs for a substitution
    """
    s = s.upper()
    t = t.upper()
    rows = len(s) + 1
    cols = len(t) + 1
    deletes, inserts, substitutes = costs

    dist = [[0 for x in range(cols)] for x in range(rows)]

    # source prefixes can be transformed into empty strings
    # by deletions:
    for row in range(1, rows):
        dist[row][0] = row * deletes

    # target prefixes can be created from an empty source string
    # by inserting the characters
    for col in range(1, cols):
        dist[0][col] = col * inserts

    for col in range(1, cols):
        for row in range(1, rows):
            if s[row - 1] == t[col - 1]:
                cost = 0
            else:
                cost = substitutes
            dist[row][col] = min(dist[row - 1][col] + deletes,
                                 dist[row][col - 1] + inserts,
                                 dist[row - 1][col - 1] + cost)  # substitution

    return dist[row][col]


def TeamAbbr(team):
    # If player has played for multiple teams this season, choose his most recent team
    team = team.split('/')[0]

    teams = ['ANA', 'ARI', 'BOS', 'BUF', 'CGY', 'CAR', 'CHI', 'COL', 'CBJ', 'DAL', 'DET', 'EDM',
             'FLA', 'L.A', 'MIN', 'MTL', 'NSH', 'N.J', 'NYI', 'NYR', 'OTT', 'PHI', 'PIT', 'S.J',
             'SEA', 'STL', 'T.B', 'TOR', 'VAN', 'VGK', 'WSH', 'WPG']

    teamabbrs = ['ANA', 'ARI', 'BOS', 'BUF', 'CGY', 'CAR', 'CHI', 'COL', 'CBJ', 'DAL', 'DET', 'EDM',
                 'FLA', 'LAK', 'MIN', 'MTL', 'NSH', 'NJD', 'NYI', 'NYR', 'OTT', 'PHI', 'PIT', 'SJS',
                 'SEA', 'STL', 'TBL', 'TOR', 'VAN', 'VGK', 'WSH', 'WPG']

    if team in teams:
        index = teams.index(team)
        return teamabbrs[index]
    else:
        return team


def ExtractData(row, EVTOIcutoff=0, PPTOIcutoff=20, SHTOIcutoff=20):
    NAME = row[1]
    POS = row[2]
    TEAM = row[4]
    EVTOI = float(row[7])
    PPTOI = float(row[12])
    SHTOI = float(row[16])
    TOI = float(row[19])
    WAR60 = float(row[20]) / TOI * 60
    EVO60 = float(row[9]) / EVTOI * 60
    EVD60 = float(row[8]) / EVTOI * 60
    PEN60 = float(row[10]) / TOI * 60
    SHOOT60 = (float(row[6]) + float(row[11]) + float(row[15])) / TOI * 60
    try:
        PPO60 = float(row[13]) / PPTOI * 60
    except:
        PPO60 = None

    try:
        SHD60 = float(row[17]) / SHTOI * 60
    except:
        SHD60 = None

    if EVTOI < EVTOIcutoff:
        return None

    if PPTOI < PPTOIcutoff:
        PPO60 = None
    if SHTOI < SHTOIcutoff:
        SHD60 = None

    return [NAME, POS, TEAM, WAR60, EVO60, EVD60, PEN60, SHOOT60, PPO60, SHD60, TOI]


def ExtractQData(row, TOIcutoff=0):
    NAME = strip_accents(row[1]).upper()
    POS = row[3]
    TOI = float(row[5])
    TOIperc = float(row[7].replace("%", ""))
    QoC = float(row[8].replace("%", ""))
    QoT = float(row[9].replace("%", ""))

    if TOI > TOIcutoff:
        return [NAME, POS, TOIperc, QoC, QoT]
    else:
        return None

def getMean(DATA):
    WAR60 = []
    EVO60 = []
    EVD60 = []
    PEN60 = []
    SHOOT60 = []
    PPO60 = []
    SHD60 = []
    for entry in DATA:
        WAR60.append(entry[3])
        EVO60.append(entry[4])
        EVD60.append(entry[5])
        PEN60.append(entry[6])
        SHOOT60.append(entry[7])
        if entry[8] is not None:
            PPO60.append(entry[8])
        if entry[9] is not None:
            SHD60.append(entry[9])

    return [stats.mean(WAR60), stats.mean(EVO60), stats.mean(EVD60), stats.mean(PEN60),
            stats.mean(SHOOT60), stats.mean(PPO60), stats.mean(SHD60)]

def getQMean(DATA):
    TOIperc = []
    QoC = []
    QoT = []

    for entry in DATA:
        TOIperc.append(entry[2])
        QoC.append(entry[3])
        QoT.append(entry[4])

    return [stats.mean(TOIperc), stats.mean(QoC), stats.mean(QoT)]


def getSD(DATA):
    WAR60 = []
    EVO60 = []
    EVD60 = []
    PEN60 = []
    SHOOT60 = []
    PPO60 = []
    SHD60 = []
    for entry in DATA:
        WAR60.append(entry[3])
        EVO60.append(entry[4])
        EVD60.append(entry[5])
        PEN60.append(entry[6])
        SHOOT60.append(entry[7])
        if entry[8] is not None:
            PPO60.append(entry[8])
        if entry[9] is not None:
            SHD60.append(entry[9])

    return [stats.stdev(WAR60), stats.stdev(EVO60), stats.stdev(EVD60), stats.stdev(PEN60),
            stats.stdev(SHOOT60), stats.stdev(PPO60), stats.stdev(SHD60)]

def getQSD(DATA):
    TOIperc = []
    QoC = []
    QoT = []

    for entry in DATA:
        TOIperc.append(entry[2])
        QoC.append(entry[3])
        QoT.append(entry[4])

    return [stats.stdev(TOIperc), stats.stdev(QoC), stats.stdev(QoT)]


def SelectFilteredData(DATAfiltered, col=None, stat=None, Q=False):
    if col is None and stat is None:
        return []

    if not Q:
        if col is None:
            # use stat string to determine what row were using
            # WAR60, EVO60, EVD60, PEN60, SHOOT60, PPO60, SHD60
            if stat in ['WAR60', 'WAR']:
                col = 0
            elif stat in ['EVO60', 'EVO']:
                col = 1
            elif stat in ['EVD60', 'EVD']:
                col = 2
            elif stat in ['PEN60', 'PEN']:
                col = 3
            elif stat in ['SHOOT60', 'SHOOT']:
                col = 4
            elif stat in ['PPO60', 'PPO']:
                col = 5
            elif stat in ['SHD60', 'SHD']:
                col = 6
            else:
                return []

        # need to account for the 'NAME', 'POS', and 'TEAM' columns
        col += 3

        data = []
        for row in DATAfiltered:
            if row[col] is None:
                continue
            else:
                data.append(row[col])

        return data

    else:
        if col is None:
            # use stat string to determine what row were using
            # WAR60, EVO60, EVD60, PEN60, SHOOT60, PPO60, SHD60
            if stat in ['TOIperc']:
                col = 0
            elif stat in ['QoC']:
                col = 1
            elif stat in ['QoT']:
                col = 2
            else:
                return []

        # need to account for the 'NAME', 'POS' columns
        col += 2

        data = []
        for row in DATAfiltered:
            if row[col] is None:
                continue
            else:
                data.append(row[col])

        return data


def formatperc(val):
    if val is None:
        return 'N/A'
    # elif type(val) == str:
    #     return val
    else:
        return val


def formatz(val):
    if val is None:
        return 'N/A'
    elif type(val) == str:
        return val
    else:
        return round(val, 4)


def get_new_teams():
    newteams = {}
    with open('Data/newteams.csv') as csvfile:
        csv_teams = csv.reader(csvfile)
        for row in csv_teams:

            newteams[row[0]] = row[1]

    return newteams


def getNames():
    names = []

    with open('Data/Aggregate_Skater_WAR_war_21_22_data.csv') as csvfile:
        line_count = 0
        csv_reader = csv.reader(csvfile)

        for row in csv_reader:
            line_count += 1
            if line_count == 1:
                continue

            names.append(row[1])

    return sorted(names)


class PlayerCard:
    def __init__(self, NAME, decimals=1):
        global newteams
        NAME = NAME.upper()
        error = True
        for player in FDATA:
            if player[0] == NAME:
                DATA = player
                error = False
        for player in DDATA:
            if player[0] == NAME:
                DATA = player
                error = False

        if error:
            raise Exception(f"No Player With The Name: {NAME} Has Been Found.")

        self.decimals = decimals
        self.pos = DATA[1]
        if NAME in newteams:
            self.team = TeamAbbr(newteams[NAME])
        else:
            self.team = TeamAbbr(DATA[2])
        self.WAR60 = DATA[3]
        self.EVO60 = DATA[4]
        self.EVD60 = DATA[5]
        self.PEN60 = DATA[6]
        self.SHOOT60 = DATA[7]
        self.PPO60 = DATA[8]
        self.SHD60 = DATA[9]
        self.TOI = DATA[10]
        # change name of second sebastian aho - idk why im doing it here but whatever
        if NAME == 'SEBASTIAN AHO SWE':
            NAME = 'SEBASTIAN AHO'
        self.name = NAME

        PP = True
        if self.PPO60 is None:
            PP = False

        PK = True
        if self.SHD60 is None:
            PK = False

        if self.pos == 'F':
            self.WAR60z = (self.WAR60 - FMEAN[0]) / FSD[0]
            self.EVO60z = (self.EVO60 - FMEAN[1]) / FSD[1]
            self.EVD60z = (self.EVD60 - FMEAN[2]) / FSD[2]
            self.PEN60z = (self.PEN60 - FMEAN[3]) / FSD[3]
            self.SHOOT60z = (self.SHOOT60 - FMEAN[4]) / FSD[4]
            self.WAR60perc = toPercentile(self.WAR60, SelectFilteredData(FDATAfiltered, col=0))
            self.EVO60perc = toPercentile(self.EVO60, SelectFilteredData(FDATAfiltered, col=1))
            self.EVD60perc = toPercentile(self.EVD60, SelectFilteredData(FDATAfiltered, col=2))
            self.PEN60perc = toPercentile(self.PEN60, SelectFilteredData(FDATAfiltered, col=3))
            self.SHOOT60perc = toPercentile(self.SHOOT60, SelectFilteredData(FDATAfiltered, col=4))

            for row in QFDATA:
                if self.name == row[0]:
                    self.QoC = row[3]
                    self.QoT = row[4]

                    self.QoCz = (self.QoC - QFMEAN[1]) / QFSD[1]
                    self.QoTz = (self.QoT - QFMEAN[2]) / QFSD[2]

                    self.QoCperc = toPercentile(self.QoC, SelectFilteredData(QFDATAfiltered, stat='QoC', Q=True))
                    self.QoTperc = toPercentile(self.QoT, SelectFilteredData(QFDATAfiltered, stat='QoT', Q=True))
                    break

        elif self.pos == 'D':
            self.WAR60z = (self.WAR60 - DMEAN[0]) / DSD[0]
            self.EVO60z = (self.EVO60 - DMEAN[1]) / DSD[1]
            self.EVD60z = (self.EVD60 - DMEAN[2]) / DSD[2]
            self.PEN60z = (self.PEN60 - DMEAN[3]) / DSD[3]
            self.SHOOT60z = (self.SHOOT60 - DMEAN[4]) / DSD[4]
            self.WAR60perc = toPercentile(self.WAR60, SelectFilteredData(DDATAfiltered, col=0))
            self.EVO60perc = toPercentile(self.EVO60, SelectFilteredData(DDATAfiltered, col=1))
            self.EVD60perc = toPercentile(self.EVD60, SelectFilteredData(DDATAfiltered, col=2))
            self.PEN60perc = toPercentile(self.PEN60, SelectFilteredData(DDATAfiltered, col=3))
            self.SHOOT60perc = toPercentile(self.SHOOT60, SelectFilteredData(DDATAfiltered, col=4))

            for row in QDDATA:
                if self.name == row[0]:
                    self.QoC = row[3]
                    self.QoT = row[4]

                    self.QoCz = (self.QoC - QDMEAN[1]) / QDSD[1]
                    self.QoTz = (self.QoT - QDMEAN[2]) / QDSD[2]

                    self.QoCperc = toPercentile(self.QoC, SelectFilteredData(QDDATAfiltered, stat='QoC', Q=True))
                    self.QoTperc = toPercentile(self.QoT, SelectFilteredData(QDDATAfiltered, stat='QoT', Q=True))
                    break

        # self.WAR60perc = round(stats.NormalDist().cdf(self.WAR60z) * 100, decimals)
        # self.EVO60perc = round(stats.NormalDist().cdf(self.EVO60z) * 100, decimals)
        # self.EVD60perc = round(stats.NormalDist().cdf(self.EVD60z) * 100, decimals)
        # self.PEN60perc = round(stats.NormalDist().cdf(self.PEN60z) * 100, decimals)
        # self.SHOOT60perc = round(stats.NormalDist().cdf(self.SHOOT60z) * 100, decimals)

        if PP:
            if self.pos == 'F':
                self.PPO60z = (self.PPO60 - FMEAN[5]) / FSD[5]
                self.PPO60perc = toPercentile(self.PPO60, SelectFilteredData(FDATAfiltered, col=5))
            elif self.pos == 'D':
                self.PPO60z = (self.PPO60 - DMEAN[5]) / DSD[5]
                self.PPO60perc = toPercentile(self.PPO60, SelectFilteredData(DDATAfiltered, col=5))

        else:
            self.PPO60z = 'N/A'
            self.PPO60perc = 'N/A'

        if PK:
            if self.pos == 'F':
                self.SHD60z = (self.SHD60 - FMEAN[6]) / FSD[6]
                self.SHD60perc = toPercentile(self.SHD60, SelectFilteredData(FDATAfiltered, col=6))
            elif self.pos == 'D':
                self.SHD60z = (self.SHD60 - DMEAN[6]) / DSD[6]
                self.SHD60perc = toPercentile(self.SHD60, SelectFilteredData(DDATAfiltered, col=6))

        else:
            self.SHD60z = 'N/A'
            self.SHD60perc = 'N/A'

    def displayZ(self):
        print(f'{self.name}\nPOS: {self.pos} , TEAM: {self.team} , Z-Scores:\n'
              f'WAR: {formatz(self.WAR60z)} , EVO: {formatz(self.EVO60z)}'
              f' , EVD: {formatz(self.EVD60z)}'
              f' , SHOOT: {formatz(self.SHOOT60z)}\nPP: {formatz(self.PPO60z)}'
              f' , PK: {formatz(self.SHD60z)} , PEN: {formatz(self.PEN60z)}\n')

    def displayPerc(self):
        print(f'{self.name}\nPOS: {self.pos} , TEAM: {self.team} , Percentiles:\n'
              f'WAR: {formatperc(self.WAR60perc)} , EVO: {formatperc(self.EVO60perc)}'
              f' , EVD: {formatperc(self.EVD60perc)}'
              f' , SHOOT: {formatperc(self.SHOOT60perc)}\nPP: {formatperc(self.PPO60perc)}'
              f' , PK: {formatperc(self.SHD60perc)} , PEN: {formatperc(self.PEN60perc)}\n')

    def ZString(self):
        string = f'{self.name}\nPOS: {self.pos} , TEAM: {self.team} , Z-Scores:\n' \
                 f'WAR: {formatz(self.WAR60z)} , EVO: {formatz(self.EVO60z)}' \
                 f' , EVD: {formatz(self.EVD60z)}' \
                 f' , SHOOT: {formatz(self.SHOOT60z)}\nPP: {formatz(self.PPO60z)}' \
                 f' , PK: {formatz(self.SHD60z)} , PEN: {formatz(self.PEN60z)}\n'

        return string

    def PercString(self):
        string = f'{self.name}\nPOS: {self.pos} , TEAM: {self.team} , Percentiles:\n' \
                 f'WAR: {formatperc(self.WAR60perc)} , EVO: {formatperc(self.EVO60perc)}' \
                 f' , EVD: {formatperc(self.EVD60perc)}' \
                 f' , SHOOT: {formatperc(self.SHOOT60perc)}\nPP: {formatperc(self.PPO60perc)}' \
                 f' , PK: {formatperc(self.SHD60perc)} , PEN: {formatperc(self.PEN60perc)}\n'

        return string


class FDataset:
    def __init__(self):
        self.WAR60 = SelectFilteredData(FDATAfiltered, stat='WAR60')
        self.EVO60 = SelectFilteredData(FDATAfiltered, stat='EVO60')
        self.EVD60 = SelectFilteredData(FDATAfiltered, stat='EVD60')
        self.PEN60 = SelectFilteredData(FDATAfiltered, stat='PEN60')
        self.SHOOT60 = SelectFilteredData(FDATAfiltered, stat='SHOOT60')
        self.PPO60 = SelectFilteredData(FDATAfiltered, stat='PPO60')
        self.SHD60 = SelectFilteredData(FDATAfiltered, stat='SHD60')


class DDataset:
    def __init__(self):
        self.WAR60 = SelectFilteredData(DDATAfiltered, stat='WAR60')
        self.EVO60 = SelectFilteredData(DDATAfiltered, stat='EVO60')
        self.EVD60 = SelectFilteredData(DDATAfiltered, stat='EVD60')
        self.PEN60 = SelectFilteredData(DDATAfiltered, stat='PEN60')
        self.SHOOT60 = SelectFilteredData(DDATAfiltered, stat='SHOOT60')
        self.PPO60 = SelectFilteredData(DDATAfiltered, stat='PPO60')
        self.SHD60 = SelectFilteredData(DDATAfiltered, stat='SHD60')


if __name__ == '__main__':
    names = getNames()
    for name in names:
        player = WAR(name)
        if player.EVO60z >= 0.5 and player.EVD60z >= 0.5 and player.pos == 'D':
            player.displayZ()

