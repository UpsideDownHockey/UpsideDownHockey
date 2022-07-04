'''
This code is shit but it works
'''


import urllib.parse
import cv2
import streamlit as st
import pandas as pd
from WAR import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import os
import datetime
import pyimgur
from streamlit_option_menu import option_menu

lastupdatedWAR = "Date: May 2, 2022"
lastupdatedMONEYPUCK = "Date: May 2, 2022"
lastupdatedprospects = "Date: June 29, 2022"
KeyUnlock = False
calcNHLe = False


@st.cache
def loadFWAR():
    FData = FDataset()
    return FData


@st.cache
def loadDWAR():
    DData = DDataset()
    return DData


def Player_Cards():
    UDHlogo = Image.open("UDH_logo.png")
    st.set_page_config(page_title="UpsideDownHockey", page_icon=UDHlogo, layout="centered",
                       initial_sidebar_state="auto",
                       menu_items={
                           "Get help": None,
                           "Report a Bug": None,
                           "About": None}
                       )

    st.markdown(
        '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" '
        'integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">',
        unsafe_allow_html=True)

    st.markdown("""
    <nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #09875B;">
      <a class="navbar-brand" target="_blank"> <img src="https://i.ibb.co/Qv5WwGW/UDH-blackwhite.png" alt="UDH_logo" 
      style="width:95px;height:40px;> </a>
      <a class="navbar-brand" target="_blank"> <b><font size="5", color='black'>UpsideDownHockey</font></b> </a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" 
      aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <a class="nav-link" href="https://www.patreon.com/UpsideDownHockey" target="_blank"><font color="black"></font></a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="https://twitter.com/UpsideDownHky" target="_blank"><font color="black">Twitter</font></a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="https://public.tableau.com/app/profile/topdownhockey" target="_blank"><font color="black"></font></a>
          </li>
        </ul>
      </div>
    </nav>
    """, unsafe_allow_html=True)

    # timeline = st.slider("Years", 2010, 2022, (2010, 2022))

    global newteams
    global comp1
    global comp2

    newteams = get_new_teams()
    names = getNames()

    goalienames = getGoalieNames()

    prospectnames = getProspectNames()

    if 'KeyUnlock' not in st.session_state:
        st.session_state.KeyUnlock = False
    if 'count' not in st.session_state:
        st.session_state.count = 0
    if 'gindex' not in st.session_state:
        st.session_state.gindex = goalienames.index("IGOR SHESTERKIN")
    if 'index' not in st.session_state:
        st.session_state.index = names.index("DEVON TOEWS")
    if 'pindex' not in st.session_state:
        st.session_state.pindex = prospectnames.index("SHANE WRIGHT")

    prev = st.session_state.count
    query = st.experimental_get_query_params()

    password = ['udh1234']
    KeyUnlock = False
    if 'admin' in query:
        key = urllib.parse.unquote(query['admin'][0])
        if key in password:
            KeyUnlock = password[0]
            st.session_state.KeyUnlock = password[0]
        else:
            KeyUnlock = False


    if KeyUnlock in password:
        selectedoptions = ["WAR", "Skaters", "Lines", 'Goalies', 'Prospects']
        defaultview = "WAR"
        defaultindex = 0
    else:
        selectedoptions = ["Skaters", "Lines", 'Goalies', 'Prospects']
        defaultview = "Skaters"
        defaultindex = 0

    if 'player' in query:
        playername = urllib.parse.unquote(query['player'][0])
        st.session_state.player = playername
        if playername in names:
            st.session_state.index = names.index(playername)
        elif playername in goalienames:
            st.session_state.gindex = goalienames.index(playername)
        elif playername in prospectnames:
            st.session_state.pindex = prospectnames.index(playername)

        if 'view' in query:
            selected = urllib.parse.unquote((query['view'][0]))

            if selected in selectedoptions:

                if selected != "Lines":
                    comp1 = ""
                    comp2 = ""
                    st.session_state.comp1 = ""
                    st.session_state.comp2 = ""

                st.session_state.view = selected
                st.session_state.selectedindex = selectedoptions.index(selected)

                if 'comp1' in query:
                    comp1 = urllib.parse.unquote((query['comp1'][0]))
                    st.session_state.comp1 = comp1
                else:
                    comp1 = ""
                if 'comp2' in query:
                    comp2 = urllib.parse.unquote((query['comp2'][0]))
                    st.session_state.comp2 = comp2
                else:
                    comp2 = ""

            else:
                st.session_state.view = defaultview
                st.session_state.selectedindex = defaultindex
                comp1 = ""
                comp2 = ""
        else:
            st.session_state.view = defaultview
            st.session_state.selectedindex = defaultindex
            comp1 = ""
            comp2 = ""

    else:
        st.session_state.player = "DEVON TOEWS"
        st.session_state.index = names.index(st.session_state.player)

        st.session_state.gindex = goalienames.index("IGOR SHESTERKIN")
        st.session_state.pindex = prospectnames.index("SHANE WRIGHT")

        st.session_state.view = defaultview
        st.session_state.selectedindex = defaultindex
        comp1 = ""
        comp2 = ""


    selected = option_menu(
        menu_title=None,
        options=selectedoptions,
        menu_icon="cast",
        default_index=st.session_state.selectedindex,
        orientation="horizontal",
    )
    # this should be called every time "selected" is manually changed
    if selected != selectedoptions[st.session_state.selectedindex]:
        playerselected()


    if selected == "Goalies":
        playername = st.selectbox("Choose Player", goalienames, index=st.session_state.gindex, on_change=playerselected)
    elif selected == "Prospects" or selected == "ProspectsHidden":
        playername = st.selectbox("Choose Player", prospectnames, index=st.session_state.pindex, on_change=playerselected)
        ''
    else:
        playername = st.selectbox("Choose Player", names, index=st.session_state.index, on_change=playerselected)
        player_selected = WAR(playername)

    if selected == "Lines":
        compcol1, compcol2 = st.columns(2)

        with compcol1:
            st.text("")
            lastupdatedMONEYPUCK

            curteam = st.checkbox("Only Current Team", value=True, on_change=setnewcomp())

        with compcol2:
            if curteam:
                teams = player_selected.team
            else:
                teams = 'All'


            names_blank = getNames(addblank=True, team=teams, pos=player_selected.pos, exc=[player_selected.name, comp2])
            player_comp1 = WAR(comp1)
            player_comp2 = WAR(comp2)
            if comp1 != "" and (player_comp1.team != player_selected.team or player_comp1.pos != player_selected.pos or player_selected.name == player_comp1.name):
                comp1 = ""
                comp2 = ""
                st.session_state.comp1 = ""
                st.session_state.comp2 = ""
            st.session_state.comp1index = names_blank.index(comp1)
            comp1 = st.selectbox("Choose Teammate #1", names_blank, index=st.session_state.comp1index, on_change=playerselected,
                                       key='comp1selectbox')
            st.session_state.comp1 = comp1

            if player_selected.pos == 'F':
                if comp2 != "" and (player_comp2.team != player_selected.team or player_comp2.pos != player_selected.pos  or player_selected.name == player_comp2.name):
                    comp1 = ""
                    comp2 = ""
                    st.session_state.comp1 = ""
                    st.session_state.comp2 = ""
                names_blank2 = getNames(addblank=True, team=teams, pos=player_selected.pos, exc=[player_selected.name, comp1])
                st.session_state.comp2index = names_blank2.index(comp2)
                comp2 = st.selectbox("Choose Teammate #2", names_blank2, index=st.session_state.comp2index, on_change=playerselected,
                                     key='comp2selectbox')
                st.session_state.comp2 = comp2
    else:
        comp1 = ""
        comp2 = ""
        st.session_state.comp1 = ""
        st.session_state.comp2 = ""


    st.session_state.player = playername

    if selected == "Goalies":
        st.session_state.gindex = goalienames.index(playername)
    elif selected == "Prospects" or selected == "ProspectsHidden":
        st.session_state.pindex = prospectnames.index(playername)
        ''
    else:
        st.session_state.index = names.index(playername)


    st.session_state.view = selected
    st.session_state.selectedindex = selectedoptions.index(selected)

    st.session_state.comp1 = comp1
    st.session_state.comp2 = comp2

    st.experimental_set_query_params(
        player=playername,
        view=selected,
        comp1=comp1,
        comp2=comp2,
        admin=KeyUnlock
    )

    # this is super sketchy but refreshing every other time stops the drop down menu from getting stuck on 1 player
    # otherwise the drop down player select would require 2 inputs to change each player
    if st.session_state.count % 2 == 0:
        st.session_state.count += 1
        st.experimental_rerun()

    m = st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #09B97C;
            height: 4em;
            width: 10em;
        }
        </style>""", unsafe_allow_html=True)

    if selected == "WAR":
        displayCompactWAR(playername)
        #st.write("This section has been removed as requested by Patrick Bacon (Top Down Hockey)")
    if selected == "Skaters":
        displaySkaterImpact(playername)
    if selected == "Lines":
        displayLinemates(playername, comp1, comp2, curteam)
    if selected == "Goalies":
        displayGoalieImpact(playername)
    if selected == "Prospects":
        if key in password:
            displayProspects(playername)
        else:
            st.write("The prospect cards have been removed as requested by Patrick Bacon (Top Down Hockey).")

            st.write("\n\nFor now, here is an NHLe calculator which converts P/GP in other leagues to the equivalent NHL P/GP")

            #Making NHLe converter for temporary prospect tab
            #multipliers found experimentally from https://frozenpool.dobbersports.com/frozenpool_nhle.php
            leagues = ["KHL (Kontinental Hockey League)",
                       "SHL (Swedish Hockey League)",
                       "AHL (American Hockey League)",
                       "Czech Extraliga",
                       "NLA (Switzerland National League)",
                       "Liiga (Finland)",
                       "DEL (Deutsche Eishockey Liga)"
                       "NCHC (National Collegiate Hockey Conference)",
                       "WCHA (Western Collegiate Hockey Association)",
                       "Hockey-East (College)",
                       "Big-10 (College)",
                       "CCHA (Central Collegiate Hockey Association)"
                       "ECAC (Eastern College Athletic Conference)",
                       "OHL (Ontario Hockey League)",
                       "WHL (Western Hockey League)",
                       "QMJHL (Quebec Major Junior Hockey League)"]
            multipliers = [0.8, 0.6, 0.49, 0.47, 0.47, 0.45, 0.44, 0.44, 0.39, 0.35, 0.33, 0.32, 0.28, 0.32, 0.30, 0.28]
            col1, col2, col3 = st.columns(3)
            with col1:
                lg = st.selectbox("Choose League", leagues, index=0, on_change=updateNHLe)

            with col2:
                gp = st.number_input("Games Played:", min_value=1, step=1, on_change=updateNHLe)
                pts = st.number_input("Points:", min_value=0, step=1, on_change=updateNHLe)

            with col3:
                st.metric("NHLe (82 Games)", round(multipliers[leagues.index(lg)]*pts/gp*82, 0))




def updateNHLe():
    calcNHLe = True


def TeamAbbrs(team):
    # If player has played for multiple teams this season, choose his most recent team
    team = team.split('/')[0]

    teams = ['ANA', 'ARI', 'BOS', 'BUF', 'CGY', 'CAR', 'CHI', 'COL', 'CBJ', 'DAL', 'DET', 'EDM',
             'FLA', 'L.A', 'MIN', 'MTL', 'NSH', 'N.J', 'NYI', 'NYR', 'OTT', 'PHI', 'PIT', 'S.J',
             'SEA', 'STL', 'T.B', 'TOR', 'VAN', 'VGK', 'WSH', 'WPG']

    fullteams = ['Anaheim Ducks', 'Arizona Coyotes', 'Boston Bruins', 'Buffalo Sabres', 'Calgary Flames', 'Carolina Hurricanes',
                 'Chicago Blackhawks', 'Colorado Avalanche', 'Columbus Blue Jackets', 'Dallas Stars', 'Detroit Red Wings',
                 'Edmonton Oilers', 'Florida Panthers', 'Los Angeles Kings', 'Minnesota Wild', 'Montreal Canadiens',
                 'Nashville Predators', 'New Jersey Devils', 'New York Islanders', 'New York Rangers', 'Ottawa Senators',
                 'Philadelphia Flyers', 'Pittsburgh Penguins', 'San Jose Sharks', 'Seattle Kraken', 'St. Louis Blues',
                 'Tampa Bay Lightning', 'Toronto Maple Leafs', 'Vancouver Canucks', 'Vegas Golden Knights',
                 'Washington Capitals', 'Winnipeg Jets']

    teamabbrs = ['ANA', 'ARI', 'BOS', 'BUF', 'CGY', 'CAR', 'CHI', 'COL', 'CBJ', 'DAL', 'DET', 'EDM',
                 'FLA', 'LAK', 'MIN', 'MTL', 'NSH', 'NJD', 'NYI', 'NYR', 'OTT', 'PHI', 'PIT', 'SJS',
                 'SEA', 'STL', 'TBL', 'TOR', 'VAN', 'VGK', 'WSH', 'WPG']

    if team in teams:
        index = teams.index(team)
        return [team, teamabbrs[index]]
    elif team in fullteams:
        index = fullteams.index(team)
        return [team, teamabbrs[index]]
    elif team in teamabbrs:
        index = teamabbrs.index(team)
        return [team, teams[index]]


def setnewcomp():
    st.session_state.comp1 = ""
    st.session_state.comp2 = ""

def playerselected():
    global comp1
    global comp2
    st.session_state.count += 1
    comp1 = ""
    comp2 = ""
    st.session_state.comp1 = ""
    st.session_state.comp2 = ""
    st.session_state.comp1index = 0
    st.session_state.comp2index = 0
    # st.session_state.index = None
    # st.session_state.player = None


@st.cache
def setindex(names, goalienames):
    query = st.experimental_get_query_params()
    if 'player' in query:
        playername = urllib.parse.unquote(query['player'][0])

        if playername in names:
            return names.index(playername)
        elif playername in goalienames:
            return goalienames.index(playername)
    else:
        return st.session_state.index


@st.cache
def getLogo(team):
    # logo = Image.open('Teamlogos/' + team + '.png')
    # return logo
    # swap RBG and BGR by opening with cv2
    logo = cv2.imread('Teamlogos/' + team + '.png')

    # Comment this out to use the troll OTT logo
    if team == 'OTT':
        logo = cv2.imread('Teamlogos/' + team + '2.png')

    logo = cv2.cvtColor(logo, cv2.COLOR_BGR2RGB)

    # st.write(logo)
    background = np.where((logo[:, :, 0] == 71) & (logo[:, :, 1] == 112) & (logo[:, :, 2] == 76))
    logo[background] = (255, 255, 255)

    if team == 'SEA':
        background = np.where((logo[:, :, 0] == 0) & (logo[:, :, 1] == 0) & (logo[:, :, 2] == 0))
        logo[background] = (255, 255, 255)

    return logo


@st.cache
def getLastModified():
    file = 'Data/Aggregate_Skater_WAR_war_21_22_data.csv'
    statbuf = os.stat(file)
    date = datetime.datetime.fromtimestamp(statbuf.st_mtime).strftime('%b %d %Y')
    return date

@st.cache
def rgb2hex(val):
    r = int(val[0]*256)
    g = int(val[1]*256)
    b = int(val[2]*256)
    return "#{:02x}{:02x}{:02x}".format(r,g,b)


#THIS IS NOT BEING USED CURRENTLY
def displayWAR(playername, decimals=1):
    global lastupdatedWAR
    player = WAR(playername, decimals)
    logo = getLogo(player.team)

    if player.pos == 'F':
        DATA = loadFWAR()
    else:
        DATA = loadDWAR()

    with st.container():
        col1, blank, col2, blank, col3, col4 = st.columns([3, 1, 4, 1, 2, 2])

        with col1:
            st.subheader(player.name)
            'Team: ' + player.team
            'Pos: ' + player.pos
            'TOI: ' + str(round(player.TOI, 1))
            if player.TOI <= 200:
                st.write("Warning: small sample size")
            st.image(logo, width=100)
            # st.write("Data Last Updated: {}".format(getLastModified()))
            lastupdatedWAR

        with col2:
            st.metric(label="WAR", value=player.WAR60perc, delta=round(player.WAR60z, 2))

            # #plotly
            # labels = ['WAR/60']
            # data = DATA.WAR60
            # playerdata = player.WAR60
            # binsize = (max(data)-min(data))/(len(data))*10
            #
            # #normalize data
            # scale = float(binsize/len(data));
            # # data = [x/scale for x in data]
            #
            #
            #
            #
            # fig = ff.create_distplot([data], group_labels=[''], bin_size=binsize, show_rug=False, show_hist=False)
            # fig.update_layout(width=400, height=400)
            # fig.add_vline(x=playerdata)
            #
            #
            # st.plotly_chart(fig)

            # seaborn
            data = DATA.WAR60
            playerdata = player.WAR60

            dens = sm.nonparametric.KDEUnivariate(data)
            dens.fit()
            x = np.linspace(min(data), max(data), 100)
            y = dens.evaluate(x)

            y_at_player = dens.evaluate(playerdata)

            fig = plt.figure(figsize=(4, 4))
            plt.hist(data, bins=int(len(data) / 10), density=True, alpha=0.2)
            ax = sns.kdeplot(data=data, fill=True, alpha=0.2, palette="crest")

            plt.title("League WAR/60 Distribution")
            plt.xlabel("WAR/60")
            plt.ylabel("Density")
            plt.ylim([0, max(y) + 1.5])
            plt.grid(False)
            plt.yticks([])
            plt.vlines(playerdata, 0, max(y_at_player, (max(y) + 1.5) / 20), colors=(1, 0.5, 0.5), linewidth=2)

            plt.legend(["League Distribution", player.name])
            st.pyplot(fig)

            # fig = px.scatter(x=x, y=y)
            # st.plotly_chart(fig)

        with col3:
            st.metric(label='EV Offense', value=player.EVO60perc, delta=round(player.EVO60z, 2))
            st.metric(label='EV Defense', value=player.EVD60perc, delta=round(player.EVD60z, 2))
            st.metric(label='Shooting', value=player.SHOOT60perc, delta=round(player.SHOOT60z, 2))
            st.metric(label="QoC", value=player.QoCperc, delta=round(player.QoCz, 2))

        with col4:
            if player.PPO60 is None:
                st.metric(label='PP', value=player.PPO60perc, delta=player.PPO60perc, delta_color='off')
            else:
                st.metric(label='PP', value=player.PPO60perc, delta=round(player.PPO60z, 2))
            if player.SHD60 is None:
                st.metric(label='PK', value=player.SHD60perc, delta=player.SHD60perc, delta_color='off')
            else:
                st.metric(label='PK', value=player.SHD60perc, delta=round(player.SHD60z, 2))
            st.metric(label='Penalties', value=player.PEN60perc, delta=round(player.PEN60z, 2))
            st.metric(label="QoT", value=player.QoTperc, delta=round(player.QoTz, 2))

    ''
    ''
    ''
    ''
    st.write(f'All values in black/white are percentiles among Forwards/Defensemen in WAR/60 for the 2021-2022 NHL'
             f' season. All values in green/red are Z-scores (standard deviations above/below the mean).\n'
             f'Only players with 100+ mins of EV TOI are included in the dataset used for determining percentiles '
             f'to prevent the league WAR/60 distribution from being skewed by players with a small sample size, however percentiles '
             f'will still be shown for players with under 100 mins of EV TOI.')
    st.write(f'\nQoC and QoT may not be accurate for players who have recently changed teams.')

    st.markdown('''---\n---''')


def displayCompactWAR(playername):
    global lastupdatedWAR

    with st.container():
        player = WAR(playername)
        if player.TOI <= 200:
            st.write("Warning: small sample size")

        logo = getLogo(player.team)

        logoheight = 100
        logowidth = int(logo.shape[1] * logoheight / logo.shape[0])

        logo = cv2.resize(logo, (logowidth, logoheight))

        UDHlogo = Image.open('UDH_logo.png')
        UDHlogo = UDHlogo.resize((200, 200))

        squaresidelength = 100
        sqrcol = set_palette([player.WAR60perc], scale=[0,100])

        square = Image.new('RGB', (squaresidelength,squaresidelength), color=rgb2hex(sqrcol[0]))

        fnt = ImageFont.truetype('arial.ttf', size=50)
        d = ImageDraw.Draw(square)
        val = str(int(round(player.WAR60perc, 0)))
        if len(val)>2:
            loc = (7,23)
        elif len(val)>1:
            loc = (23,23)
        else:
            loc = (36,23)
        d.text(loc, val, fill=(0,0,0), font=fnt)

        # square = Image.open('sqr.png')
        # squaresidelength = 100
        # square = square.resize((squaresidelength, squaresidelength))

        if player.pos == 'F':
            DATA = loadFWAR()
        else:
            DATA = loadDWAR()

        fig = make_subplots(rows=2, cols=1, shared_yaxes=True)

        labels = ['EVO', 'EVD', 'SHOOT', 'PEN', 'PP', 'PK']
        values = [player.EVO60z, player.EVD60z, player.SHOOT60z, player.PEN60z]
        percentiles = [player.EVO60perc, player.EVD60perc, player.SHOOT60perc, player.PEN60perc]

        if player.PPO60 == None:
            labels.remove('PP')
        else:
            values.append(player.PPO60z)
            percentiles.append(player.PPO60perc)
        if player.SHD60 == None:
            labels.remove('PK')
        else:
            values.append(player.SHD60z)
            percentiles.append(player.SHD60perc)

        data = DATA.WAR60
        playerdata = player.WAR60

        ### Make figure to be saved as image

        fig, ax = plt.subplots(2, 1, gridspec_kw={'height_ratios': [4, 3]})

        fig.suptitle(playername)

        plt.figimage(UDHlogo, xo=1075 - UDHlogo.width / 2, yo=0)
        plt.figimage(logo, xo=1100 - logowidth / 2, yo=980)
        plt.figimage(square, xo= 230 - squaresidelength/2, yo=980)

        # fig.set_size_inches(7.,7.)
        sns.set(style='whitegrid', color_codes=True)

        p1 = ax[0].bar(x=labels, height=values, color=set_palette(values), edgecolor='k', linewidth=0.4)
        p2 = ax[0].bar(x=labels, height=invertbarvals(values), alpha=0)
        ax[0].bar_label(p2, labels=[str(perc) + '%' for perc in percentiles], label_type='center', padding=0)
        ax[0].grid(which='minor', color='black', axis='y')
        ax[0].xaxis.grid(False)

        # ax[0].set_title("WAR/60 = " + str(player.WAR60perc) + "%         TOI: " + str(round(
        #     player.TOI)) + "         POS: " + player.pos + "         TEAM: " + player.team + "                   ",
        #                 fontsize=10)

        ax[0].set_title("TOI: " + str(round(
            player.TOI)) + "     POS: " + player.pos + "     TEAM: " + player.team,
                        fontsize=10)





        ax[0].set_ylabel("z-score")
        # ax[0].set_xlabel("WAR/60")
        ax[0].set(ylim=(-3, 3))

        dens = sm.nonparametric.KDEUnivariate(data)
        dens.fit()
        x = np.linspace(min(data), max(data), 100)
        y = dens.evaluate(x)

        y_at_player = dens.evaluate(playerdata)

        sns.kdeplot(ax=ax[1], data=data, fill=True, alpha=0.2, palette="crest")
        ax[1].hist(x=data, bins=int(len(data) / 10), density=True, alpha=0.2)

        ax[1].set_xlabel("WAR/60")
        ax[1].set_ylabel("density\n")

        plt.ylim([0, max(y) + 3])
        ax[1].vlines(playerdata, 0, max(y_at_player, (max(y) + 3) / 20), colors=(1, 0.5, 0.5), linewidth=2)

        ax[1].legend(["League WAR/60 Distribution", player.name], prop={'size': 8.5})
        ax[1].grid(False)
        ax[1].axes.yaxis.set_ticks([])

        plt.figtext(x=0, y=-0.1, fontsize=10,
                    s="21-22 NHL Season\nWAR/60 shown as percentiles split by position (F/D)\nMade by UpsideDownHockey (upsidedownhockey.herokuapp.com)\nWAR data from Patrick Bacon (Top Down Hockey)")
        st.pyplot(fig)

        if st.button("Upload to Imgur"):
            CLIENT_ID = "53b192dd3aef148"
            CLIENT_SECRET = "0cdb64420ad4889d5d07a53570bbbab2cd487883"
            PATH = playername.replace(" ", "") + "WAR.png"
            plt.savefig(PATH, bbox_inches='tight', dpi=200)

            im = pyimgur.Imgur(CLIENT_ID)
            uploaded_image = im.upload_image(PATH, title=playername + " WAR")

            st.code(uploaded_image.link_large_thumbnail)

        ''
        '---\n---'
        'Legend:'
        f'EVO: Even Strength Offensive WAR/60'
        f'EVD: Even Strength Defensive WAR/60'
        f'SHOOT: Shooting WAR/60'
        f'PEN: Penalty Differential WAR/60'
        f'PP: Powerplay Offensive WAR/60'
        f'PK: Penalty Kill Defensive WAR/60'

    st.markdown('''---\n---''')


def invertbarvals(values, scale=1):
    newvals = []
    for val in values:
        if val == 0:
            newvals.append(0)
        else:
            newvals.append(-scale * val / abs(val))
    return newvals


@st.cache
def set_palette(values, palette='vlag', scale=[-3, 3], cmap='RdYlGn'):
    # palette = sns.diverging_palette(230,10,as_cmap=True)
    palette = plt.get_cmap(cmap)
    cmap = plt.get_cmap(palette)

    pal = []
    for val in values:

        val = (val-scale[0])*6/(scale[1]-scale[0])-3

        normval = val / 4 + 0.5
        if normval >= 1:
            normval = 0.99
        if normval <= 0:
            normval = 0.01

        # if normval>0.5:
        #     normval+=0.3
        # else:
        #     normval-=0.3

        pal.append(cmap(normval))

    return pal


def displayLinemates(playername, playercomp1, playercomp2, curteam):
    global lastupdatedMONEYPUCK

    player = WAR(playername)
    skaterid = getSkaterID(playername)
    lastname = playername.split(" ")[-1]

    if skaterid == 999999:
        "Error: Skater ID Not Found"

    comp1id = getSkaterID(playercomp1)
    comp1lastname = playercomp1.split(" ")[-1]

    if comp1id == 999999 and playercomp1 != "":
        "Error: Teammate #1 ID Not Found"

    comp2id = getSkaterID(playercomp2)
    comp2lastname = playercomp2.split(" ")[-1]

    if comp2id == 999999 and playercomp2 != "":
        "Error: Teammate #2 ID Not Found"

    hide_table_row_index = """
                <style>
                tbody th {display:none}
                .blank {display:none}
                </style>
                """
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    df = pd.read_csv('Data/lines_moneypuck_2021-2022.csv',
                     usecols=['lineId', 'name', 'team', 'position', 'situation', 'icetime', 'xGoalsFor',
                              'xGoalsAgainst',
                              'goalsFor', 'goalsAgainst'], index_col=False)

    cols = df.select_dtypes(include=[np.object]).columns
    df[cols] = df[cols].apply(
        lambda x: x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8'))

    if curteam:
        df = df[(df['team'].str.contains(player.team)) & (df['name'].str.contains(lastname, case=False))]

    playerdf = df[(df['lineId'].str.contains(str(skaterid)))]

    with1df = df[(df['name'].str.contains(lastname, case=False)) &
                    (df['lineId'].str.contains(str(skaterid))) & (df['lineId'].str.contains(str(comp1id)))]

    without1df = df[(df['name'].str.contains(lastname, case=False)) &
                       (df['lineId'].str.contains(str(skaterid))) & (~df['lineId'].str.contains(str(comp1id)))]

    with2df = df[(df['name'].str.contains(lastname, case=False)) &
                 (df['lineId'].str.contains(str(skaterid))) & (df['lineId'].str.contains(str(comp2id)))]

    without2df = df[(df['name'].str.contains(lastname, case=False)) &
                    (df['lineId'].str.contains(str(skaterid))) & (~df['lineId'].str.contains(str(comp2id)))]

    with1a2df = df[(df['name'].str.contains(lastname, case=False)) &
                 (df['lineId'].str.contains(str(skaterid))) & (df['lineId'].str.contains(str(comp1id))) & (df['lineId'].str.contains(str(comp2id)))]

    with1o2df = df[(df['name'].str.contains(lastname, case=False)) &
                   (df['lineId'].str.contains(str(skaterid))) & ((df['lineId'].str.contains(str(comp1id))) | (
                       df['lineId'].str.contains(str(comp2id))))]

    without1o2df = df[(df['name'].str.contains(lastname, case=False)) &
                 (df['lineId'].str.contains(str(skaterid))) & (~df['lineId'].str.contains(str(comp1id))) & (~df['lineId'].str.contains(str(comp2id)))]

    TOI, w1TOIperc, w2TOIperc, w1a2TOIperc, w1o2TOIperc = WOWYperc(playerdf, skaterid, comp1id, comp2id, 'icetime')
    xGF60, xGA60, xGFperc, w1xGF60, w1xGA60, w1xGFperc, wo1xGF60, wo1xGA60, wo1xGFperc = WOWYperc(playerdf, skaterid, comp1id, comp2id, 'xG')
    GF60, GA60, GFperc, w1GF60, w1GA60, w1GFperc, wo1GF60, wo1GA60, wo1GFperc = WOWYperc(playerdf, skaterid, comp1id, comp2id, 'G')


    with st.container():
        if playercomp1 != "":
            displaywith1df = with1df
            if displaywith1df.shape[0]>=1:
                displaywith1df['TOI'] = displaywith1df.apply(
                    lambda row: round(row.icetime / 60,1), axis=1
                )
                displaywith1df['xGF%'] = displaywith1df.apply(
                    lambda row: round(100*row.xGoalsFor / max(row.xGoalsFor + row.xGoalsAgainst, 0.00001),1), axis=1
                )
                displaywith1df['GF%'] = displaywith1df.apply(
                    lambda row: round(100*row.goalsFor / max(row.goalsFor + row.goalsAgainst, 0.00001),1), axis=1
                )
            displaywith1df = displaywith1df.drop(labels=['lineId', 'icetime', 'position', 'xGoalsFor', 'xGoalsAgainst', 'goalsFor', 'goalsAgainst'], axis=1)

            displaywithout1df = without1df
            if displaywithout1df.shape[0] >= 1:
                displaywithout1df['TOI'] = displaywithout1df.apply(
                    lambda row: round(row.icetime / 60,1), axis=1
                )
                displaywithout1df['xGF%'] = displaywithout1df.apply(
                    lambda row: round(100*row.xGoalsFor / max(row.xGoalsFor + row.xGoalsAgainst, 0.00001),1), axis=1
                )
                displaywithout1df['GF%'] = displaywithout1df.apply(
                    lambda row: round(100*row.goalsFor / max(row.goalsFor + row.goalsAgainst, 0.00001),1), axis=1
                )
            displaywithout1df = displaywithout1df.drop(labels=['lineId', 'icetime', 'position', 'xGoalsFor', 'xGoalsAgainst', 'goalsFor', 'goalsAgainst'], axis=1)

        if playercomp2 != "":
            displaywith2df = with2df
            if displaywith2df.shape[0] >= 1:
                displaywith2df['TOI'] = displaywith2df.apply(
                    lambda row: round(row.icetime / 60, 1), axis=1
                )
                displaywith2df['xGF%'] = displaywith2df.apply(
                    lambda row: round(100 * row.xGoalsFor / max(row.xGoalsFor + row.xGoalsAgainst, 0.00001), 1), axis=1
                )
                displaywith2df['GF%'] = displaywith2df.apply(
                    lambda row: round(100 * row.goalsFor / max(row.goalsFor + row.goalsAgainst, 0.00001), 1), axis=1
                )
            displaywith2df = displaywith2df.drop(
                labels=['lineId', 'icetime', 'position', 'xGoalsFor', 'xGoalsAgainst', 'goalsFor', 'goalsAgainst'],
                axis=1)

            displaywithout2df = without2df
            if displaywithout2df.shape[0] >= 1:
                displaywithout2df['TOI'] = displaywithout2df.apply(
                    lambda row: round(row.icetime / 60, 1), axis=1
                )
                displaywithout2df['xGF%'] = displaywithout2df.apply(
                    lambda row: round(100 * row.xGoalsFor / max(row.xGoalsFor + row.xGoalsAgainst, 0.00001), 1), axis=1
                )
                displaywithout2df['GF%'] = displaywithout2df.apply(
                    lambda row: round(100 * row.goalsFor / max(row.goalsFor + row.goalsAgainst, 0.00001), 1), axis=1
                )
            displaywithout2df = displaywithout2df.drop(
                labels=['lineId', 'icetime', 'position', 'xGoalsFor', 'xGoalsAgainst', 'goalsFor', 'goalsAgainst'],
                axis=1)




        if playercomp1 != "" and playercomp2 != "":
            displaywith1a2df = with1a2df
            if displaywith1a2df.shape[0] >= 1:
                displaywith1a2df['TOI'] = displaywith1a2df.apply(
                    lambda row: round(row.icetime / 60, 1), axis=1
                )
                displaywith1a2df['xGF%'] = displaywith1a2df.apply(
                    lambda row: round(100 * row.xGoalsFor / max(row.xGoalsFor + row.xGoalsAgainst, 0.00001), 1), axis=1
                )
                displaywith1a2df['GF%'] = displaywith1a2df.apply(
                    lambda row: round(100 * row.goalsFor / max(row.goalsFor + row.goalsAgainst, 0.00001), 1), axis=1
                )
            displaywith1a2df = displaywith1a2df.drop(
                labels=['lineId', 'icetime', 'position', 'xGoalsFor', 'xGoalsAgainst', 'goalsFor', 'goalsAgainst'],
                axis=1)

            displaywith1o2df = with1o2df
            if displaywith1o2df.shape[0] >= 1:
                displaywith1o2df['TOI'] = displaywith1o2df.apply(
                    lambda row: round(row.icetime / 60, 1), axis=1
                )
                displaywith1o2df['xGF%'] = displaywith1o2df.apply(
                    lambda row: round(100 * row.xGoalsFor / max(row.xGoalsFor + row.xGoalsAgainst, 0.00001), 1), axis=1
                )
                displaywith1o2df['GF%'] = displaywith1o2df.apply(
                    lambda row: round(100 * row.goalsFor / max(row.goalsFor + row.goalsAgainst, 0.00001), 1), axis=1
                )
            displaywith1o2df = displaywith1o2df.drop(
                labels=['lineId', 'icetime', 'position', 'xGoalsFor', 'xGoalsAgainst', 'goalsFor', 'goalsAgainst'],
                axis=1)

            displaywithout1o2df = without1o2df
            if displaywithout1o2df.shape[0] >= 1:
                displaywithout1o2df['TOI'] = displaywithout1o2df.apply(
                    lambda row: round(row.icetime / 60, 1), axis=1
                )
                displaywithout1o2df['xGF%'] = displaywithout1o2df.apply(
                    lambda row: round(100 * row.xGoalsFor / max(row.xGoalsFor + row.xGoalsAgainst, 0.00001), 1), axis=1
                )
                displaywithout1o2df['GF%'] = displaywithout1o2df.apply(
                    lambda row: round(100 * row.goalsFor / max(row.goalsFor + row.goalsAgainst, 0.00001), 1), axis=1
                )
            displaywithout1o2df = displaywithout1o2df.drop(
                labels=['lineId', 'icetime', 'position', 'xGoalsFor', 'xGoalsAgainst', 'goalsFor', 'goalsAgainst'],
                axis=1)

            st.write(playername.title() + " plays with " + playercomp1.title() + " " + str(w1TOIperc) + "% of the time at 5v5")
            st.write(playername.title() + " plays with " + playercomp2.title() + " " + str(w2TOIperc) + "% of the time at 5v5")
            st.write(playername.title() + " plays with " + playercomp1.title() + " and " + playercomp2.title() + " " + str(w1a2TOIperc) + "% of the time at 5v5")
            st.write(playername.title() + " plays with " + playercomp1.title() + " or " + playercomp2.title() + " " + str(w1o2TOIperc) + "% of the time at 5v5")
            st.markdown('''---\n---''')
            st.write(playername.title() + " with " + playercomp1.title() + " and " + playercomp2.title() + ":")
            st.table(displaywith1a2df)
            st.write(playername.title() + " with " + playercomp1.title() + " or " + playercomp2.title() + ":")
            st.table(displaywith1o2df)
            st.write(playername.title() + " without " + playercomp1.title() + " or " + playercomp2.title() + ":")
            st.table(displaywithout1o2df)
        elif playercomp1 != "" and playercomp2 == "":
            st.write(playername.title() + " plays with " + playercomp1.title() + " " + str(w1TOIperc) + "% of the time at 5v5")
            st.markdown('''---\n---''')
            st.write(playername.title() + " with " + playercomp1.title() + ":")
            st.table(displaywith1df.style.hide_index())
            st.write(playername.title() + " without " + playercomp1.title() + ":")
            st.table(displaywithout1df)
        elif playercomp1 == "" and playercomp2 != "":
            st.write(playername.title() + " plays with " + playercomp2.title() + " " + str(w2TOIperc) + "% of the time at 5v5")
            st.markdown('''---\n---''')
            st.write(playername.title() + " with " + playercomp2.title() + ":")
            st.table(displaywith2df)
            st.write(playername.title() + " without " + playercomp2.title() + ":")
            st.table(displaywithout2df)
        elif playercomp1 == "" and playercomp2 == "":
            st.markdown('''---\n---''')
            displayplayerdf = playerdf
            if displayplayerdf.shape[0] >= 1:
                displayplayerdf['TOI'] = displayplayerdf.apply(
                    lambda row: round(row.icetime / 60, 1), axis=1
                )
                displayplayerdf['xGF%'] = displayplayerdf.apply(
                    lambda row: round(100 * row.xGoalsFor / max(row.xGoalsFor + row.xGoalsAgainst, 0.00001), 1), axis=1
                )
                displayplayerdf['GF%'] = displayplayerdf.apply(
                    lambda row: round(100 * row.goalsFor / max(row.goalsFor + row.goalsAgainst, 0.00001), 1), axis=1
                )
            displayplayerdf = displayplayerdf.drop(
                labels=['lineId', 'icetime', 'position', 'xGoalsFor', 'xGoalsAgainst', 'goalsFor', 'goalsAgainst'],
                axis=1)

            st.write(playername.title() + " line combinations:")
            st.table(displayplayerdf)

    #WOWY BAR PLOTS
    # with st.container():
    #     perclabels = ['\u0394 GF%', '\u0394 xGF%']
    #     ratelabels = ['\u0394 GF/60', '\u0394 xGF/60', '\u0394 GA/60', '\u0394 xGA/60']
    #
    #     totalpercvalues = [GFperc, xGFperc]
    #     totalratevalues = [GF60, xGF60, GA60, xGA60]
    #
    #     withpercvalues = [wGFperc-GFperc, wxGFperc-xGFperc]
    #     withratevalues = [wGF60-GF60, wxGF60-xGF60, wGA60-GA60, wxGA60-xGA60]
    #
    #     withoutpercvalues = [woGFperc-GFperc, woxGFperc-xGFperc]
    #     withoutratevalues = [woGF60-GF60, woxGF60-xGF60, woGA60-GA60, woxGA60-xGA60]
    #
    #     fig, ax = plt.subplots(2, 2, gridspec_kw={'height_ratios': [3, 3],
    #                                               'width_ratios': [2,4]})
    #
    #     fig.suptitle(playername+"\nWith Or Without "+playercomp1)
    #
    #
    #     ax[0, 0].bar(x=perclabels, height=withpercvalues, color=set_palette(withpercvalues, scale=[-25, 25]), edgecolor='k')
    #     ax[0, 0].set(ylim=(-25, 25))
    #     ax[0, 0].set_ylabel("WITH\n\nRelative GF%")
    #     ax[0, 0].axes.yaxis.set_ticks(range(-30, 31, 10))
    #
    #     ax[1, 0].bar(x=perclabels, height=withoutpercvalues, color=set_palette(withoutpercvalues, scale=[-25, 25]), edgecolor='k')
    #     ax[1, 0].set(ylim=(-25, 25))
    #     ax[1, 0].set_ylabel("WITHOUT\n\nRelative GF%")
    #     ax[1, 0].axes.yaxis.set_ticks(range(-30, 31, 10))
    #
    #     vals = setzeros(withratevalues, [2, 3])
    #     ax[0, 1].bar(x=ratelabels, height=vals, color=set_palette(vals, scale=[-2, 2]), edgecolor='k')
    #     vals = setzeros(withratevalues, [0, 1])
    #     ax[0, 1].bar(x=ratelabels, height=vals, color=set_palette(invertbarvals(vals), scale=[-2, 2]), edgecolor='k')
    #     ax[0, 1].set(ylim=(-1, 1))
    #     ax[0, 1].set_ylabel("Relative G/60")
    #
    #     vals = setzeros(withoutratevalues, [2, 3])
    #     ax[1, 1].bar(x=ratelabels, height=vals, color=set_palette(vals, scale=[-2, 2]), edgecolor='k')
    #     vals = setzeros(withoutratevalues, [0, 1])
    #     ax[1, 1].bar(x=ratelabels, height=vals, color=set_palette(invertbarvals(vals), scale=[-2, 2]), edgecolor='k')
    #     ax[1, 1].set(ylim=(-1, 1))
    #     ax[1, 1].set_ylabel("Relative G/60")
    #     plt.tight_layout()
    #
    #     if playercomp1 != "":
    #         st.pyplot(fig)


    st.markdown('''---\n---''')
    st.write("Lines and TOI Data from MoneyPuck.com")


def setzeros(list, indexes):
    newlist = []
    for i in range(len(list)):
        if i in indexes:
            newlist.append(0)
        else:
            newlist.append(list[i])
    return newlist


@st.cache
def getNames(addblank=False, team='All', pos='All', exc=[]):
    global newteams

    if team != 'All':
        team = TeamAbbrs(team)

    names = []

    if addblank == True:
        names.append("")

    with open('Data/Aggregate_Skater_WAR_war_21_22_data.csv') as csvfile:
        line_count = 0
        csv_reader = csv.reader(csvfile)

        for row in csv_reader:
            line_count += 1
            if line_count == 1:
                continue

            readpos = row[2]
            readteam = row[4]


            if row[1] in newteams:
                readteam = TeamAbbr(newteams[row[1]])
            if (readteam in team or team == 'All') and (readpos == pos or pos == 'All') and (row[1] not in exc):
                names.append(row[1])

    return sorted(names)


def getProspectNames():
    #some sketchy stuff to change csv file encoding
    # names = ['SHANE WRIGHT']
    # ff_name = 'Data/Full Year NHLe.csv'
    # target_file_name = 'Data/FullYearNHLe.csv'
    # with open(ff_name, 'rb') as source_file:
    #     with open(target_file_name, 'w+b') as dest_file:
    #         contents = source_file.read()
    #         dest_file.write(contents.decode('utf-16').encode('utf-8'))

    df = pd.read_csv('Data/FullYearNHLe.csv', encoding='utf-8',
                     usecols=['Player + Season', 'Player', 'Rights', 'Position', 'Teams', 'Leagues', 'Draft Year', 'Age', 'NHLe', 'Star %', 'Make %'])
    df['Player'] = df.apply(lambda row: row.Player.upper(), axis=1)

    duplicate = df.duplicated('Player').tolist()
    df['Duplicate'] = duplicate

    df['Name'] = df.apply(
        lambda row: str(row['Player']) + row.Duplicate * (" " + str(row['Player + Season'].split("/")[4])), axis=1)

    namelist = df['Name'].tolist()
    # namelist = sorted(namelist)

    return namelist



def WOWYperc(df, skaterid, comp1id, comp2id, col, decimals=1):
    with1df = df[(df['lineId'].str.contains(str(skaterid))) & (df['lineId'].str.contains(str(comp1id)))]
    without1df = df[(df['lineId'].str.contains(str(skaterid))) & (~df['lineId'].str.contains(str(comp1id)))]

    with2df = df[(df['lineId'].str.contains(str(skaterid))) & (df['lineId'].str.contains(str(comp2id)))]
    without2df = df[(df['lineId'].str.contains(str(skaterid))) & (~df['lineId'].str.contains(str(comp2id)))]

    with1a2df = df[(df['lineId'].str.contains(str(skaterid))) & (df['lineId'].str.contains(str(comp1id))) & (df['lineId'].str.contains(str(comp2id)))]
    with1o2df = df[(df['lineId'].str.contains(str(skaterid))) & ((df['lineId'].str.contains(str(comp1id))) | (df['lineId'].str.contains(str(comp2id))))]

    toi = df['icetime'].sum()
    w1toi = with1df['icetime'].sum()
    wo1toi = without1df['icetime'].sum()

    w2toi = with2df['icetime'].sum()
    wo2toi = without2df['icetime'].sum()

    w1a2toi = with1a2df['icetime'].sum()
    w1o2toi = with1o2df['icetime'].sum()

    if col == 'xG' or col == 'G':
        if col == 'xG':
            pref = 'xG'
        else:
            pref = 'g'
        gf = pref+"oalsFor"
        ga = pref+"oalsAgainst"

        gftotal = df[gf].sum()
        gatotal = df[ga].sum()
        wgftotal = with1df[gf].sum()
        wgatotal = with1df[ga].sum()
        wogftotal = without1df[gf].sum()
        wogatotal = without1df[ga].sum()

        totalgfperc = round(gftotal / (gftotal + gatotal)*100, decimals)
        wgfperc = round(wgftotal / (wgftotal + wgatotal)*100, decimals)
        wogfperc = round(wogftotal / (wogftotal + wogatotal)*100, decimals)

        gftotal60 = gftotal / (toi) * 60 * 60
        wgftotal60 = wgftotal / (w1toi) * 60 * 60
        wogftotal60 = wogftotal / (wo1toi) * 60 * 60

        gatotal60 = gatotal / (toi) * 60 * 60
        wgatotal60 = wgatotal / (w1toi) * 60 * 60
        wogatotal60 = wogatotal / (wo1toi) * 60 * 60
                # xGF60,   xGA60,     xGFperc,    wxGF60,      wxGA60,    wxGFperc,   woxGF60,   woxGA60,    woxGFperc
        return gftotal60, gatotal60, totalgfperc, wgftotal60, wgatotal60, wgfperc, wogftotal60, wogatotal60, wogfperc
    else:

        with1perc = round(w1toi/toi*100, decimals)
        without1perc = round(wo1toi/toi*100, decimals)

        with2perc = round(w2toi / toi * 100, decimals)
        without2perc = round(wo2toi / toi * 100, decimals)

        with1a2perc = round(w1a2toi/toi*100, decimals)
        with1o2perc = round(w1o2toi/toi*100, decimals)

        return toi, with1perc, with2perc, with1a2perc, with1o2perc



def getSkaterID(playername):

    player = WAR(playername)

    firstname = playername.split(" ")[0]
    lastname = playername.split(" ")[-1]

    dfskaterid = pd.read_csv('Data/skaters_moneypuck_2021-2022.csv', usecols=['playerId', 'name', 'situation'])
    dfskaterid = dfskaterid[(dfskaterid['situation'] == 'all') & (dfskaterid['name'].str.contains(lastname, case=False))]

    if dfskaterid.shape[0] > 1:
        dfskaterid = dfskaterid[dfskaterid['name'].str.contains(firstname, case=False)]

    if dfskaterid.shape[0] > 1:
        return 999999
    else:
        return dfskaterid['playerId'].values[0]

def teamcolorcode(team):
    teamabbrs = {'ANA':(252, 76, 2),
                 'ARI':(140,38,51),
                 'BOS':(252, 181, 20),
                 'BUF':(0,38,84),
                 'CGY':(200,16,46),
                 'CAR':(226,24,54),
                 'CHI':(207,10,44),
                 'COL':(35, 97, 146),
                 'CBJ':(0,38,84),
                 'DAL':(0, 104, 71),
                 'DET':(206,17,38),
                 'EDM':(252, 76, 0),
                 'FLA':(200,16,46),
                 'LAK':(87,42,132),
                 'MIN':(2, 73, 48),
                 'MTL':(175, 30, 45),
                 'NSH':(255,184,28),
                 'NJD':(206, 17, 38),
                 'NYI':(244, 125, 48),
                 'NYR':(0,56,168),
                 'OTT':(197, 32, 50),
                 'PHI':(247, 73, 2),
                 'PIT':(252,181,20),
                 'SJS':(0, 109, 117),
                 'SEA':(153, 217, 217),
                 'STL':(0, 47, 135),
                 'TBL':(0, 40, 104),
                 'TOR':(0, 32, 91),
                 'VAN':(0, 32, 91),
                 'VGK':(185,151,91),
                 'WSH':(200, 16, 46),
                 'WPG':(4,30,66)
    }

    col = teamabbrs[team]
    col = [val/255 for val in col]
    col.append(1)

    return col


def getGoalieNames():
    names = []

    with open('Data/goalies_moneypuck_2021-2022.csv') as csvfile:
        line_count = 0
        csv_reader = csv.reader(csvfile)

        for row in csv_reader:
            line_count += 1
            if line_count == 1:
                continue
            elif (line_count - 1) % 5 == 0:
                names.append(row[2].upper())

    return sorted(names)


@st.cache
def loadGoalieData(minGP=10):

    df = pd.read_csv('Data/goalies_moneypuck_2021-2022.csv',
                     usecols=['name', 'team', 'games_played', 'position', 'situation', 'icetime', 'xGoals', 'goals',
                              'lowDangerxGoals', 'mediumDangerxGoals', 'highDangerxGoals',
                              'lowDangerGoals', 'mediumDangerGoals', 'highDangerGoals',
                              'lowDangerShots', 'mediumDangerShots', 'highDangerShots',
                              'xRebounds', 'rebounds', 'xFreeze', 'freeze'],
                     index_col=False)

    cols = df.select_dtypes(include=[np.object]).columns
    df[cols] = df[cols].apply(
        lambda x: x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8'))

    df = df[(df['situation'] == 'all') & (df['games_played'] >= minGP)]
    df['icetime'] = df['icetime'].div(60).round(2)
    df['GSAx'] = df.apply(lambda row: row.xGoals - row.goals, axis=1)
    df['GSAx/60'] = df.apply(lambda row: row.GSAx / row.icetime * 60, axis=1)
    df['LDGSAx/shot'] = df.apply(lambda row: (row.lowDangerxGoals - row.lowDangerGoals) / row.lowDangerShots,axis=1)
    df['MDGSAx/shot'] = df.apply(lambda row: (row.mediumDangerxGoals - row.mediumDangerGoals) / row.mediumDangerShots, axis=1)
    df['HDGSAx/shot'] = df.apply(lambda row: (row.highDangerxGoals - row.highDangerGoals) / row.highDangerShots,axis=1)
    df['freezeAx/60'] = df.apply(lambda row: (row.freeze - row.xFreeze) / row.icetime * 60, axis=1)
    df['reboundsBx/60'] = df.apply(lambda row: (row.xRebounds - row.rebounds) / row.icetime * 60, axis=1)

    gmean = df.mean()
    gstd = df.std()

    return df, gmean, gstd


def getGoalieZscore(goalie, mean, std, stat):
    zscore = (goalie[stat].iloc[0] - mean[stat]) / std[stat]
    return zscore


def displayGoalieImpact(playername):
    global lastupdatedMONEYPUCK

    goaliedata, gmean, gstd = loadGoalieData()

    df = pd.read_csv('Data/goalies_moneypuck_2021-2022.csv',
                     usecols=['name', 'team', 'games_played', 'position', 'situation', 'icetime', 'xGoals', 'goals',
                              'lowDangerxGoals', 'mediumDangerxGoals', 'highDangerxGoals',
                              'lowDangerGoals', 'mediumDangerGoals', 'highDangerGoals',
                              'lowDangerShots', 'mediumDangerShots', 'highDangerShots',
                              'xRebounds', 'rebounds', 'xFreeze', 'freeze', 'ongoal'],
                     index_col=False)

    cols = df.select_dtypes(include=[np.object]).columns
    df[cols] = df[cols].apply(
        lambda x: x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8'))

    goalie = df[(df['situation'] == 'all') & (df['name'].str.contains(playername, case=False))]

    goalie['icetime'] = goalie['icetime'].div(60).round(2)
    goalie['GSAx'] = goalie.apply(lambda row: row.xGoals - row.goals, axis=1)
    goalie['GSAx/60'] = goalie.apply(lambda row: row.GSAx / row.icetime * 60, axis=1)
    goalie['LDGSAx/shot'] = goalie.apply(lambda row: (row.lowDangerxGoals - row.lowDangerGoals) / row.lowDangerShots, axis=1)
    goalie['MDGSAx/shot'] = goalie.apply(lambda row: (row.mediumDangerxGoals - row.mediumDangerGoals) / row.mediumDangerShots, axis=1)
    goalie['HDGSAx/shot'] = goalie.apply(lambda row: (row.highDangerxGoals - row.highDangerGoals) / row.highDangerShots, axis=1)
    goalie['freezeAx/60'] = goalie.apply(lambda row: (row.freeze - row.xFreeze) / row.icetime * 60, axis=1)
    goalie['reboundsBx/60'] = goalie.apply(lambda row: (row.xRebounds - row.rebounds) / row.icetime * 60, axis=1)

    GSAx = round(goalie['xGoals'].iloc[0]-goalie['goals'].iloc[0], 1)

    SA = goalie['ongoal'].iloc[0]
    GA = goalie['goals'].iloc[0]

    SVperc = round((SA-GA)/SA, 3)
    GAA = round(GA/goalie['icetime'].iloc[0] * 60, 2)

    pos = goalie['position'].iloc[0]
    team = goalie['team'].iloc[0]

    icetime = goalie['icetime'].iloc[0]
    GP = goalie['games_played'].iloc[0]
    GSAx60 = goalie['GSAx/60'].iloc[0]
    LDGSAxshot = goalie['LDGSAx/shot'].iloc[0]
    MDGSAxshot = goalie['MDGSAx/shot'].iloc[0]
    HDGSAxshot = goalie['HDGSAx/shot'].iloc[0]
    ReboundsBx60 = goalie['reboundsBx/60'].iloc[0]
    FreezeAx60 = goalie['freezeAx/60'].iloc[0]

    zGSAx60 = getGoalieZscore(goalie, gmean, gstd, 'GSAx/60')
    zLDGSAxshot = getGoalieZscore(goalie, gmean, gstd, 'LDGSAx/shot')
    zMDGSAxshot = getGoalieZscore(goalie, gmean, gstd, 'MDGSAx/shot')
    zHDGSAxshot = getGoalieZscore(goalie, gmean, gstd, 'HDGSAx/shot')
    zReboundsBx60 = getGoalieZscore(goalie, gmean, gstd, 'reboundsBx/60')
    zFreezeAx60 = getGoalieZscore(goalie, gmean, gstd, 'freezeAx/60')

    GSAx60perc = toPercentile(GSAx60, goaliedata['GSAx/60'].tolist())
    LDGSAxshotperc = toPercentile(LDGSAxshot, goaliedata['LDGSAx/shot'].tolist())
    MDGSAxshotperc = toPercentile(MDGSAxshot, goaliedata['MDGSAx/shot'].tolist())
    HDGSAxshotperc = toPercentile(HDGSAxshot, goaliedata['HDGSAx/shot'].tolist())
    ReboundsBx60perc = toPercentile(ReboundsBx60, goaliedata['reboundsBx/60'].tolist())
    FreezeAx60perc = toPercentile(FreezeAx60, goaliedata['freezeAx/60'].tolist())

    with st.container():

        if icetime <= 600:
            st.write("Warning: small sample size")

        logo = getLogo(team)

        logoheight = 100
        logowidth = int(logo.shape[1] * logoheight / logo.shape[0])

        logo = cv2.resize(logo, (logowidth, logoheight))

        UDHlogo = Image.open('UDH_logo.png')
        UDHlogo = UDHlogo.resize((200, 200))


        labels1 = ['Low\nDanger', 'Medium\nDanger', 'High\nDanger', 'Rebound\nControl']
        # values1 = [GSAx60, LDGSAxshot, MDGSAxshot, HDGSAxshot, ReboundsBx60, FreezeAx60]
        values1 = [zLDGSAxshot, zMDGSAxshot, zHDGSAxshot, zReboundsBx60]

        percentiles = [LDGSAxshotperc, MDGSAxshotperc, HDGSAxshotperc, ReboundsBx60perc]

        squaresidelength = 100
        sqrcol = set_palette([GSAx60perc], scale=[0, 100])

        square = Image.new('RGB', (squaresidelength, squaresidelength), color=rgb2hex(sqrcol[0]))

        fnt = ImageFont.truetype('arial.ttf', size=50)
        d = ImageDraw.Draw(square)
        val = str(int(round(GSAx60perc, 0)))
        if len(val) > 2:
            loc = (7, 23)
        elif len(val) > 1:
            loc = (23, 23)
        else:
            loc = (36, 23)
        d.text(loc, val, fill=(0, 0, 0), font=fnt)

        fig = make_subplots(rows=2, cols=1, shared_yaxes=True)

        ### Make figure to be saved as image

        fig, ax = plt.subplots(2, 1, figsize=(6.4,4.8), gridspec_kw={'height_ratios': [2, 1]})

        fig.suptitle(playername, x=0.5)

        plt.figimage(UDHlogo, xo= 1075 - UDHlogo.width / 2, yo=-15)
        plt.figimage(logo, xo=1100 - logowidth / 2, yo=690)
        plt.figimage(square, xo=230 - squaresidelength / 2, yo=690)

        # fig.set_size_inches(7.,7.)
        sns.set(style='whitegrid', color_codes=True)

        # colorvals = values1.copy()
        # colorvals[1] = -colorvals[1]

        p1 = ax[0].bar(x=labels1, height=values1, color=set_palette(values1, scale=(-3,3)), edgecolor='k', linewidth=0.4)
        p2 = ax[0].bar(x=labels1, height=invertbarvals(values1), alpha=0)
        ax[0].bar_label(p2, labels=[str(perc) + '%' for perc in percentiles], label_type='center', padding=0)
        ax[0].grid(which='minor', color='black', axis='y')
        ax[0].xaxis.grid(False)

        # ax.bar(x=labels1, height=values1, color=set_palette(values1, scale=(-3, 3)), edgecolor='k', linewidth=0.4)
        # ax.grid(which='minor', color='black', axis='y')
        # ax.xaxis.grid(False)


        ax[0].set_title("GP: " + str(GP) + "     SV%: " + str(SVperc) + "     GAA: " + str(GAA) + "     GSAx: " + str(GSAx), fontsize=10, x=.5)

        ax[0].set_ylabel("z-score")
        # ax[0].set_xlabel("WAR/60")
        ax[0].set(ylim=(-3, 3))

        ax[1].set_visible(False)
        #
        # # color_thief = ColorThief('Teamlogos/' + player.team + '.png')
        # # dominant_color = color_thief.get_color(quality=1)
        # #
        # # dominant_color = list(dominant_color)
        # #
        # # dominant_color = [val/255 for val in dominant_color]
        # # dominant_color.append(1)
        #
        # ax[2].bar(x=labels2, height=np.r_[values2]-50, color=teamcolorcode(player.team), edgecolor='k', linewidth=0.4, bottom=50)
        # # ax[2].yaxis.tick_right()
        # # ax[2].yaxis.set_label_position("right")
        # ax[2].set_ylabel("5v5 xGF%")
        # ax[2].set(ylim=(30, 70))


        plt.figtext(x=0, y=0.2, fontsize=9,
                    s="21-22 NHL Season\n" + lastupdatedMONEYPUCK + "\nMade by UpsideDownHockey (upsidedownhockey.herokuapp.com)\nGoalie data from Moneypuck.com")
        # fig.tight_layout()
        st.pyplot(fig)


        if st.button("Upload to Imgur"):
            CLIENT_ID = "53b192dd3aef148"
            CLIENT_SECRET = "0cdb64420ad4889d5d07a53570bbbab2cd487883"
            PATH = playername.replace(" ", "") + "goalie.png"
            plt.savefig(PATH, bbox_inches='tight', dpi=200)

            im = pyimgur.Imgur(CLIENT_ID)
            uploaded_image = im.upload_image(PATH, title=playername + " goalie")

            st.code(uploaded_image.link_large_thumbnail)

        ''
        '---\n---'
        'Legend:'
        f'relTM xGF/60: expected goals for per 60 minutes relative to teammates (higher/positive is better)'
        f'relTM xGA/60: expected goals against per 60 minutes relative to teammates (lower/negative is better)'
        f'On Ice xGF%: percentage of expected goals for while the player is on the ice'
        f'Off Ice xGF%: percentage of expected goals for while the player is on the bench'

    st.markdown('''---\n---''')






def displaySkaterImpact(playername):
    global lastupdatedMONEYPUCK

    player = WAR(playername)
    skaterid = getSkaterID(playername)
    lastname = playername.split(" ")[-1]

    if skaterid == 999999:
        "Error: Skater ID Not Found"

    df = pd.read_csv('Data/skaters_moneypuck_2021-2022.csv',
                     usecols=['playerId', 'games_played', 'name', 'team', 'position', 'situation', 'I_F_goals',
                              'I_F_primaryAssists', 'I_F_secondaryAssists', 'gameScore', 'icetime', 'timeOnBench',
                              'OnIce_F_xGoals', 'OnIce_A_xGoals', 'OffIce_F_xGoals', 'OffIce_A_xGoals'], index_col=False)

    cols = df.select_dtypes(include=[np.object]).columns
    df[cols] = df[cols].apply(
        lambda x: x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8'))

    skater = df[(df['situation'] == '5on5') & (df['playerId'] == getSkaterID(playername))]

    statline = df[(df['situation'] == 'all') & (df['playerId'] == getSkaterID(playername))]


    icetime = skater['icetime'].iloc[0]
    benchtime = skater['timeOnBench'].iloc[0]
    onicexgf = skater['OnIce_F_xGoals'].iloc[0]
    onicexga = skater['OnIce_A_xGoals'].iloc[0]
    officexgf = skater['OffIce_F_xGoals'].iloc[0]
    officexga = skater['OffIce_A_xGoals'].iloc[0]

    gamesplayed = statline['games_played'].iloc[0]
    gamescore = statline['gameScore'].iloc[0] / gamesplayed
    goals = statline['I_F_goals'].iloc[0]
    assists1 = statline['I_F_primaryAssists'].iloc[0]
    assists2 = statline['I_F_secondaryAssists'].iloc[0]


    xGF60relTM = (onicexgf / icetime - officexgf / benchtime) * 60 * 60
    xGA60relTM = (onicexga / icetime - officexga / benchtime) * 60 * 60

    onicexGFperc = onicexgf / (onicexgf + onicexga)
    officexGFperc = officexgf / (officexgf + officexga)

    xGFpercrelTM = onicexGFperc - officexGFperc

    with st.container():

        if player.TOI <= 200:
            st.write("Warning: small sample size")

        logo = getLogo(player.team)

        logoheight = 100
        logowidth = int(logo.shape[1] * logoheight / logo.shape[0])

        logo = cv2.resize(logo, (logowidth, logoheight))

        UDHlogo = Image.open('UDH_logo.png')
        UDHlogo = UDHlogo.resize((200, 200))


        fig = make_subplots(rows=1, cols=1, shared_yaxes=True)

        labels1 = ['relTM\nxGF/60', 'relTM\nxGA/60']
        labels2 = ['On Ice\nxGF%', 'Off Ice\n xGF%']
        values1 = [xGF60relTM, xGA60relTM]
        values2 = [onicexGFperc*100, officexGFperc*100]


        ### Make figure to be saved as image

        fig, ax = plt.subplots(1, 5, gridspec_kw={'width_ratios': [2, 0.7, 1, 0.7, 2]})

        fig.suptitle(playername, x=0.5)

        plt.figimage(UDHlogo, xo=1075 - UDHlogo.width / 2, yo=-15)
        plt.figimage(logo, xo=1100 - logowidth / 2, yo=980)

        # fig.set_size_inches(7.,7.)
        sns.set(style='whitegrid', color_codes=True)

        colorvals = values1.copy()
        colorvals[1] = -colorvals[1]

        ax[0].bar(x=labels1, height=values1, color=set_palette(colorvals, scale=(-1, 1)), edgecolor='k', linewidth=0.4)
        ax[0].grid(which='minor', color='black', axis='y')
        ax[0].xaxis.grid(False)


        ax[2].set_title("GP: " + str(gamesplayed) + "   G: " + str(int(goals)) + "   A1: "+ str(int(assists1)) +
                        "   A2: "+ str(int(assists2))+"   Pts: "+str(int(goals+assists1+assists2))+
                            "   POS: " + player.pos, fontsize=10, x=.4, y=1.02)

        ax[0].set_ylabel("5v5 \u0394 xG/60")
        # ax[0].set_xlabel("WAR/60")
        ax[0].set(ylim=(-1.5, 1.5))

        ax[1].set_visible(False)

        # color_thief = ColorThief('Teamlogos/' + player.team + '.png')
        # dominant_color = color_thief.get_color(quality=1)
        #
        # dominant_color = list(dominant_color)
        #
        # dominant_color = [val/255 for val in dominant_color]
        # dominant_color.append(1)

        ax[2].bar(x=['Avg Game Score'], height=[gamescore], color=set_palette([gamescore], scale=(-1, 2)), edgecolor='k', linewidth=0.4, bottom=0)
        ax[2].set_ylabel("Avg Game Score")
        ax[2].set(ylim=(-2, 2))
        ax[2].grid(which='minor', color='black', axis='y')
        ax[2].xaxis.grid(False)

        ax[3].set_visible(False)

        ax[4].bar(x=labels2, height=np.r_[values2]-50, color=teamcolorcode(player.team), edgecolor='k', linewidth=0.4, bottom=50)
        # ax[4].yaxis.tick_right()
        # ax[4].yaxis.set_label_position("right")
        ax[4].set_ylabel("5v5 xGF%")
        ax[4].set(ylim=(30, 70))
        ax[4].grid(which='minor', color='black', axis='y')
        ax[4].xaxis.grid(False)


        plt.figtext(x=0, y=-0.1, fontsize=9,
                    s="21-22 NHL Season\n" + lastupdatedMONEYPUCK + "\nMade by UpsideDownHockey (upsidedownhockey.herokuapp.com)\n5v5 xG data from Moneypuck.com")
        #fig.tight_layout()
        st.pyplot(fig)


        if st.button("Upload to Imgur"):
            CLIENT_ID = "53b192dd3aef148"
            CLIENT_SECRET = "0cdb64420ad4889d5d07a53570bbbab2cd487883"
            PATH = playername.replace(" ", "") + "xG.png"
            plt.savefig(PATH, bbox_inches='tight', dpi=200)

            im = pyimgur.Imgur(CLIENT_ID)
            uploaded_image = im.upload_image(PATH, title=playername + " xG")

            st.code(uploaded_image.link_large_thumbnail)

        ''
        '---\n---'
        'Legend:'
        f'relTM xGF/60: expected goals for per 60 minutes relative to teammates (higher/positive is better)'
        f'relTM xGA/60: expected goals against per 60 minutes relative to teammates (lower/negative is better)'
        f'On Ice xGF%: percentage of expected goals for while the player is on the ice'
        f'Off Ice xGF%: percentage of expected goals for while the player is on the bench'

    st.markdown('''---\n---''')

def displayProspects(playername):
    global lastupdatedprospects
    df = pd.read_csv('Data/FullYearNHLe.csv',
                     usecols=['Player + Season', 'Player', 'Rights', 'Position', 'Teams', 'Leagues', 'Draft Year', 'Age', 'NHLe', 'Star %', 'Make %'],
                     index_col=False)

    cols = df.select_dtypes(include=[np.object]).columns
    df[cols] = df[cols].apply(
        lambda x: x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8'))

    df['Player'] = df.apply(lambda row: row.Player.upper(), axis=1)

    duplicate = df.duplicated('Player').tolist()
    df['Duplicate'] = duplicate

    df['Name'] = df.apply(lambda row: str(row['Player']) + row.Duplicate*(" " + str(row['Player + Season'].split("/")[4])), axis=1)

    prospect = df[(df['Name'] == playername)]

    rights = prospect['Rights'].iloc[0]
    teams = prospect['Teams'].iloc[0]
    leagues = prospect['Leagues'].iloc[0]
    pos = prospect['Position'].iloc[0]
    draftyear = 2022 - prospect['Draft Year'].iloc[0]
    age = prospect['Age'].iloc[0]
    NHLe = prospect['NHLe'].iloc[0]
    Star = float(prospect['Star %'].iloc[0].rstrip("%"))
    Make = float(prospect['Make %'].iloc[0].rstrip("%"))

    with st.container():

        if rights != "Unsigned":
            logo = getLogo(TeamAbbrs(rights)[1])
        else:
            logo = getLogo('NHL')

        logoheight = 100
        logowidth = int(logo.shape[1] * logoheight / logo.shape[0])

        logo = cv2.resize(logo, (logowidth, logoheight))

        UDHlogo = Image.open('UDH_logo.png')
        UDHlogo = UDHlogo.resize((150, 150))


        labels1 = []
        values1 = []
        percentiles = []

        squaresidelength = 200
        NHLecol = set_palette([NHLe], scale=[-50, 150], cmap='Blues') #cmap='BuGn'
        NHLesquare = Image.new('RGB', (squaresidelength, squaresidelength), color=rgb2hex(NHLecol[0]))

        fnt = ImageFont.truetype('arial.ttf', size=100)
        d = ImageDraw.Draw(NHLesquare)
        val = str(int(round(NHLe, 0)))
        if len(val) > 2:
            loc = (14, 45)
        elif len(val) > 1:
            loc = (40, 45)
        else:
            loc = (72, 45)
        d.text(loc, val, fill=(0, 0, 0), font=fnt)

        makecol = set_palette([Make], scale=[-50, 150], cmap='RdYlBu')  # cmap='BuGn'
        makesquare = Image.new('RGB', (squaresidelength, squaresidelength), color=rgb2hex(makecol[0]))

        fnt = ImageFont.truetype('arial.ttf', size=70)
        d = ImageDraw.Draw(makesquare)
        val = str(int(round(Make, 0)))+"%"
        if len(val) > 3:
            loc = (10, 60)
        elif len(val) > 2:
            loc = (36, 60)
        else:
            loc = (57, 60)
        d.text(loc, val, fill=(0, 0, 0), font=fnt)

        starcol = set_palette([Star], scale=[-50, 150], cmap='RdYlBu')  # cmap='BuGn'
        starsquare = Image.new('RGB', (squaresidelength, squaresidelength), color=rgb2hex(starcol[0]))

        fnt = ImageFont.truetype('arial.ttf', size=70)
        d = ImageDraw.Draw(starsquare)
        val = str(int(round(Star, 0)))+"%"
        if len(val) > 3:
            loc = (10, 60)
        elif len(val) > 2:
            loc = (36, 60)
        else:
            loc = (57, 60)
        d.text(loc, val, fill=(0, 0, 0), font=fnt)




        fig = make_subplots(rows=2, cols=1, shared_yaxes=True)

        ### Make figure to be saved as image

        fig, ax = plt.subplots(2, 1, figsize=(6.4,4.8), gridspec_kw={'height_ratios': [2, 1]})

        fig.suptitle(''.join([i for i in playername if not i.isdigit()]), x=0.5)
        #x range from 0-1030 roughly
        #figure range from 120 to 910 with sqr side length of 200
        #20 to 930
        plt.figimage(UDHlogo, xo= 932 - UDHlogo.width / 2, yo=0)
        plt.figimage(logo, xo=950 - logowidth / 2, yo=475)
        plt.figimage(NHLesquare, xo=1030/4 - squaresidelength / 2, yo=150)
        plt.figimage(starsquare, xo=2*1030/4 - squaresidelength / 2, yo=150)
        plt.figimage(makesquare, xo=3*1030/4 - squaresidelength / 2, yo=150)

        plt.figtext(x=0.255, y=0.77, fontsize=20, s="NHLe")
        plt.figtext(x=0.445, y=0.77, fontsize=20, s="Star %")
        plt.figtext(x=0.635, y=0.77, fontsize=20, s="Make %")

        # fig.set_size_inches(7.,7.)
        sns.set(style='whitegrid', color_codes=True)

        # colorvals = values1.copy()
        # colorvals[1] = -colorvals[1]

        # p1 = ax[0].bar(x=labels1, height=values1, color=set_palette(values1, scale=(-3,3)), edgecolor='k', linewidth=0.4)
        # p2 = ax[0].bar(x=labels1, height=invertbarvals(values1), alpha=0)
        # ax[0].bar_label(p2, labels=[str(perc) + '%' for perc in percentiles], label_type='center', padding=0)

        # ax[0].bar(x=[], height=[])
        ax[0].grid(which='minor', color='black', axis='y')
        ax[0].xaxis.grid(False)
        ax[0].yaxis.grid(False)
        ax[0].get_yaxis().set_visible(False)
        ax[0].get_xaxis().set_visible(False)

        # ax.bar(x=labels1, height=values1, color=set_palette(values1, scale=(-3, 3)), edgecolor='k', linewidth=0.4)
        # ax.grid(which='minor', color='black', axis='y')
        # ax.xaxis.grid(False)


        ax[0].set_title("Age: " + str(age) + "     POS: " + pos + "     Draft Year: " + str(draftyear) +
                        "\nLeagues: " + leagues.upper() + "     Teams: " + teams, fontsize=8, x=.5)

        # ax[0].set_ylabel("z-score")
        # ax[0].set_xlabel("WAR/60")
        # ax[0].set(ylim=(-3, 3))
        # ax[0].set_visible(False)

        ax[1].set_visible(False)
        #
        # # color_thief = ColorThief('Teamlogos/' + player.team + '.png')
        # # dominant_color = color_thief.get_color(quality=1)
        # #
        # # dominant_color = list(dominant_color)
        # #
        # # dominant_color = [val/255 for val in dominant_color]
        # # dominant_color.append(1)
        #
        # ax[2].bar(x=labels2, height=np.r_[values2]-50, color=teamcolorcode(player.team), edgecolor='k', linewidth=0.4, bottom=50)
        # # ax[2].yaxis.tick_right()
        # # ax[2].yaxis.set_label_position("right")
        # ax[2].set_ylabel("5v5 xGF%")
        # ax[2].set(ylim=(30, 70))


        plt.figtext(x=0.13, y=0.42, fontsize=7,
                    s="21-22 Season\n" + lastupdatedprospects + "\nMade by UpsideDownHockey (upsidedownhockey.herokuapp.com)\nData from Patrick Bacon (Top Down Hockey)")
        # fig.tight_layout()
        st.pyplot(fig)

        url = prospect['Player + Season'].iloc[0].split(" ")[0]
        st.write(url)

        if st.button("Upload to Imgur"):
            CLIENT_ID = "53b192dd3aef148"
            CLIENT_SECRET = "0cdb64420ad4889d5d07a53570bbbab2cd487883"
            PATH = playername.replace(" ", "") + "prospect.png"
            plt.savefig(PATH, bbox_inches='tight', dpi=200)

            im = pyimgur.Imgur(CLIENT_ID)
            uploaded_image = im.upload_image(PATH, title=playername + " prospect")

            st.code(uploaded_image.link_large_thumbnail)


    st.markdown('''---\n---''')

if __name__ == '__main__':
    Player_Cards()

# git add .
# git commit -m "message"
##git push heroku master        OR      git push heroku HEAD:master
# heroku ps:scale web=1
