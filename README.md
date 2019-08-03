# The Tracab Cookbook
Here is a collection of code snippets and functions that I have used to work with Tracab data. Thought I would share so I have a public record for my personal use later and to share for others. 

###### Caveats
This is based on parsing the raw .dat a pandas object, I call this object 'tdat'. Pandas isn't the most memory effective or speed effective data strcuture for tracking data, but whatever. All functions use the 'tdat' object name for the parsed tracking data, this is a default you can override. 

###### Contributions
If you want to contribute snippets to store here they will be warmly welcomed.  

### 1. Parse Tracab Metadata 
Each tracab file comes with a xml file holding all meta data for the period start and ends as well as the pitch dimensions. This function parses it into a dict for easier access for later analysis. 

```py
    
    def parse_tracking_metadata(filename):

    tree = ET.parse(filename)       # parse the raw xml 
    root = tree.getroot()           # get the root object to access the information 

    gamexml = root.findall('match')[0]      # get all of the nodes called 'match'

    info_raw = []       # create an empty list for storing the data 

    # for each period node get the start and end, appending them to the infa_raw list
    for i in gamexml.iter('period'):
            info_raw.append( i.get('iStartFrame') )
            info_raw.append( i.get('iEndFrame') )

    game_info = dict()      # Create empty dict for storing the information 

    # get all the information for each period and add the info to the dictionary 
    game_info['period1_start'] = int(info_raw[0])
    game_info['period1_end'] = int(info_raw[1])
    game_info['period2_start'] = int(info_raw[2])
    game_info['period2_end'] = int(info_raw[3])
    game_info['period3_start'] = int(info_raw[4])
    game_info['period3_end'] = int(info_raw[5])
    game_info['period4_start'] = int(info_raw[6])
    game_info['period4_end'] = int(info_raw[7])

    # get all the information for the pitch sizes and add the info to the dictionary 
    for detail in root.iter('match'):
        game_info['pitch_x'] = int(float(detail.get('fPitchXSizeMeters')))
        game_info['pitch_y'] = int(float(detail.get('fPitchYSizeMeters')))

    # return the dictionary of information 
    return(game_info)
```


### 2. Get One Frame of Tracking Data
Select one frame in time of tracking data, with options to select just one team (1 = home, 0 = away, 10 = ball).

```p
def get_frame(frame_select, trackingdata = tdat, a_team = False, team_select = 1):
    
    if a_team:
        return(trackingdata[(trackingdata['frameID'] == frame_select) & 
                            (trackingdata['team'] == team_select)].reset_index(drop=True))    
    else:
        return(trackingdata[trackingdata['frameID'] == frame_select].reset_index(drop=True))
```

### 3. Get a Segment of Tracking Data
Select a period of time within the tracking data, with options to select just one team (1 = home, 0 = away, 10 = ball).

```p
def get_segment(frame_select_start, frame_select_end, trackingdata = tdat, a_team = False, team_select = 1):
    
    if a_team:
        return(trackingdata[(trackingdata['frameID'].between(frame_select_start, frame_select_end)) & 
                            (trackingdata['team'] == team_select)].reset_index(drop=True))    
    else:
        return(trackingdata[trackingdata['frameID'].between(frame_select_start, frame_select_end)].reset_index(drop=True))
```

### 4. Add False/True Column if a Player's Team is in Possession
Althougth tracab data has the information regarding which team is in possession in a particular frame there isn't a easy way of determining if a player's team is in possession of the ball.

```p
def add_team_in_possession(trackingdata = tdat):
    
    trackingdata['team_in_possession'] = [(x == 1 and y == "H") or 
                                     (x == 0 and y == "A") 
                                     for x,y in zip(trackingdata.team, 
                                     trackingdata.ball_owning_team )]  
    return( trackingdata )
```

### 5. Create a Pitch 
A flexible pitch function that's customisable but with fixed defaults. 

```p
def create_pitch(fig_width = 9, 
                 fig_height = 6, 
                 x = 5600, 
                 y = 3600, 
                 border = 400, 
                 line_colour = 'black', 
                 jp_alpha = 0.2, 
                 jp_colour = 'r', 
                 middle_thirds = False, 
                 basic_features = False,
                 JdeP = False, 
                 add_axis = False):

    plt.figure(figsize=(fig_width, fig_height))
    plt.axis([-x-border,x+border,-y-border, y+border])

    ## create each half 
    plt.plot([ -x, -x, 0, 0, -x ] , [ -y, y, y, -y, -y], color = line_colour, linewidth = 1)
    plt.plot([ x, x, 0, 0, x ] , [ -y, y, y, -y, -y], color = line_colour, linewidth = 1)

    ## create the 18 yard boxes 
    w_of_18 = 2015
    h_of_18 = x-1660
    
    plt.plot([ -x, -x, -h_of_18, -h_of_18, -x ] , 
    [ -w_of_18, w_of_18, w_of_18, -w_of_18, -w_of_18], 
    color = 'black', 
    linewidth = 1)
    
    plt.plot([ x, x, h_of_18, h_of_18, x ] , 
    [ -w_of_18, w_of_18, w_of_18, -w_of_18, -w_of_18], 
    color = 'black', l
    inewidth = 1)

    ## create the goals     
    plt.plot([ -x, -x] , [ -366, 366], color = 'black', linewidth = 3)
    plt.plot([ x, x] , [ -366, 366], color = 'black', linewidth = 3)
    
    ## Add middle thirds 
    if middle_thirds:
        middle_third_w = (x/2) - (x/6)
        plt.fill([-middle_third_w,middle_third_w,middle_third_w,-middle_third_w,-middle_third_w], 
                 [y,y,-y,-y,y], 
                 "black",
                 alpha = 0.05)

    if basic_features:
        print("")
    else:
        ## add centre circle     
        circle1=plt.Circle((0,0),(915),edgecolor=line_colour, fill = None)
        plt.gcf().gca().add_artist(circle1)

        ## add spots 
        plt.scatter([x-1100, -x+1100, 0], [0,0,0], color = line_colour, s=(x/500))
        
        ## create the 6 yard boxes 
        w_of_6 = 1015 
        h_of_6 = x-550 
        
        plt.plot([ -x, -x, -h_of_6, -h_of_6, -x ] , 
        [ -w_of_6, w_of_6, w_of_6, -w_of_6, -w_of_6], 
        color = 'black', 
        linewidth = 1)
        
        plt.plot([ x, x, h_of_6, h_of_6, x ] , 
        [ -w_of_6, w_of_6, w_of_6, -w_of_6, -w_of_6], 
        color = 'black', linewidth = 1)


    ## add Juego de Posicion
    if JdeP:
        middle_third_w = (x/2) - (x/6)

        plt.plot([ -h_of_18, h_of_18 ] , 
        [ w_of_18, w_of_18], 
        color = jp_colour, 
        linewidth = 1, 
        alpha = jp_alpha)
        
        plt.plot([ -h_of_18, h_of_18 ] , 
        [ -w_of_18, -w_of_18], 
        color = jp_colour, 
        linewidth = 1, 
        alpha = jp_alpha)

        plt.plot([ -h_of_18, h_of_18 ] , 
        [ 915, 915], 
        color = jp_colour, 
        linewidth = 1, 
        alpha = jp_alpha)
        
        plt.plot([ -h_of_18, h_of_18 ] , 
        [ -915, -915], 
        color = jp_colour, 
        linewidth = 1, 
        alpha = jp_alpha)

        plt.plot([ h_of_18, h_of_18 ] , 
        [ -y, y], 
        color = jp_colour, 
        linewidth = 1, 
        alpha = jp_alpha)
        
        plt.plot([ -h_of_18, -h_of_18 ] , 
        [ -y, y], 
        color = jp_colour, 
        linewidth = 1, 
        alpha = jp_alpha)

        jp_third = (h_of_18) / 2

        plt.plot([ -middle_third_w, -middle_third_w ] , 
        [ w_of_18, y], 
        color = jp_colour, 
        linewidth = 1, 
        alpha = jp_alpha)
        
        plt.plot([ -middle_third_w, -middle_third_w ] , 
        [ -w_of_18, -y], 
        color = jp_colour, 
        linewidth = 1, 
        alpha = jp_alpha)

        plt.plot([ middle_third_w, middle_third_w ] , 
        [ w_of_18, y], 
        color = jp_colour, 
        linewidth = 1, 
        alpha = jp_alpha)
        
        plt.plot([ middle_third_w, middle_third_w ] , 
        [ -w_of_18, -y], 
        color = jp_colour, 
        linewidth = 1, 
        alpha = jp_alpha)

    ## add axis 
    if add_axis:
        print("")
    else:
        plt.axis('off')
    
    return(plt)

```

### 6. Add the Ball x & y Coordinates
Create two new columns for the ball's x and y coorindates that frame in time. 

```p
def add_ball_xy(trackingdata = tdat):
    
    ball_df = trackingdata[trackingdata['team'] == 10].reset_index(drop=True)[['frameID', 'x', 'y']]    
    ball_df.columns = ['frameID', 'ball_x', 'ball_y']
    
    trackingdata = trackingdata.merge(ball_df, on = "frameID")
    
    return(trackingdata)

```

### 7. Calculate the Distance to the Ball
Creates a new column of the distance the player is from the ball. 

```p
def add_distance_to_ball(trackingdata = tdat):
    
    if 'ball_x' in trackingdata.columns: 
        trackingdata['distance_to_ball'] = trackingdata[['x', 'y']].sub(np.array( trackingdata[['ball_x', 'ball_y']] )).pow(2).sum(1).pow(0.5)
        trackingdata.distance_to_ball = trackingdata.distance_to_ball.round(2)
        return(trackingdata)

    else: 
        print("x||----------------")
        print("Ball x and y coordinates missing - 'add_distance_to_ball' function failed")
        print("Use 'add_ball_xy' to add the missing coordinates")
        print("----------------||x")

        
add_distance_to_ball(tdat2)
```

### 8. Calculate the Distance to the Goals
Creates two new columns for the distance from a player to each goal, goal1 (-x) and goal2 (x)

```p
def add_distance_to_goals(trackingdata = tdat, x = 5250):

    trackingdata['distance_to_goal1'] = trackingdata[['x', 'y']].sub(np.array( -x, 0 )).pow(2).sum(1).pow(0.5)
    trackingdata['distance_to_goal2'] = trackingdata[['x', 'y']].sub(np.array( x, 0 )).pow(2).sum(1).pow(0.5)

    trackingdata.distance_to_goal1 = trackingdata.distance_to_goal1.round(2)
    trackingdata.distance_to_goal2 = trackingdata.distance_to_goal2.round(2)

    return(trackingdata)
```

### 9. Calculate Distance Between 2 Points
Calculate the distance between 2 points 

```p
def calc_distance(x,y):   
    return np.sqrt(np.sum((x-y)**2))

# test
a = np.array((0,100))
b = np.array((0,400))
calc_distance(a,b)
"300"
```

### 10. Add Attacking Direction
For many analyses with tracking data you need to know the direction of play. Adding an attacking direction column helps with this. Attcking direction of 1 means the team is defending the goal -x and attacking the goal +x. An attacking direction of 1 means the team is defending the goal +x and attacking the goal -x.

```p
def add_attacking_direction(trackingdata=tdat, metadata = meta):
    
    period1_start_frame = trackingdata[trackingdata['frameID'] == metadata['period1_start']].reset_index(drop=True)

    avg_starting_x_attack = period1_start_frame[period1_start_frame['team'] == 1]['x'].mean()
    avg_starting_x_defence = period1_start_frame[period1_start_frame['team'] == 0]['x'].mean()

    ## lists of attacking direction
    periods_list = []
    direction_list = []

    if avg_starting_x_attack < avg_starting_x_defence:
        periods_list.append(1)
        periods_list.append(1)
        direction_list.append(1)
        direction_list.append(-1)
    else:
        periods_list.append(2)
        periods_list.append(2)
        direction_list.append(-1)
        direction_list.append(1)

    attacking_direction_ref = pd.DataFrame(
    {'period_id': periods_list,
    'attacking_direction': direction_list, 
    'team': [1,0]})

    trackingdata = pd.merge(trackingdata, attacking_direction_ref, on = ["team", "period_id"])
    
    return(trackingdata)
```

### 11. Switch the Pitch
For some analysis there is a need to orientate the pitch towards a standardised direction from -x -> x. This function switches the x,y coordinates to face -x -> x if the team in possession has an attacking direction of -1. Returns the tracking data segment and if the switch occured as a false/true. 

```p
def switch_the_pitch(frame_seg):

    if frame_seg.attacking_direction[0] == 1:
        if frame_seg.ball_owning_team[0] == "H":
            switch = False
        else:
            switch = True
    else:
        if frame_seg.ball_owning_team[0] == "H":
            switch = True
        else:
            switch = False
    if switch:
        frame_seg['x'] = frame_seg.x * -1
        frame_seg['y'] = frame_seg.y * -1
    else:
        frame_seg['x'] = frame_seg.x
        frame_seg['y'] = frame_seg.y
    return([frame_seg, switch])
```

### 12. Calculate the Slope between 2 Points
For some analysis it is helpful to calculate the slope between two points. 

```p

def slope(x1, y1, x2, y2):
    m = (y2-y1)/(x2-x1)
    return(m)
    
```

### 13. Convert a Tracab Location into Opta Coordinates
There will be the need to convert a location in tracab coordinate space (-x:x and -y:y) into the equivilent Opta coordinates (0-100 for both x and y)

```p
def to_opta_coords(att_dir, X, Y, pitch_x = meta['pitch_x'], pitch_y = meta['pitch_y']):

    if att_dir == 1:

        tracab_x = (pitch_x / 2) * 100
        opta_x_temp = 0.5 + (X / tracab_x) / 2
        opta_x = int(round(opta_x_temp,2)*100)

        tracab_y = (pitch_y / 2) * 100
        opta_y_temp = 0.5 + (Y / tracab_y) / 2
        opta_y = int(round(opta_y_temp,2)*100)

        return([opta_x, opta_y])

    else:

        X = X*-1
        tracab_x = (pitch_x / 2) * 100
        opta_x_temp = 0.5 + (X / tracab_x) / 2
        opta_x = int(round(opta_x_temp,2)*100)

        Y = Y*-1
        tracab_y = (pitch_y / 2) * 100
        opta_y_temp = 0.5 + (Y / tracab_y) / 2
        opta_y = int(round(opta_y_temp,2)*100)

        return([opta_x, opta_y])
```

### 14. Convert a Opta Location into Tracab Coordinates
There will be the need to convert a location in opta coordinate space (0-100 for both x and y) into the equivilent tracab coordinates (-x:x and -y:y).

```p
def to_tracab_coords(att_dir, opta_x, opta_y, pitch_x = meta['pitch_x'], pitch_y = meta['pitch_y']):
    
    if att_dir == 1:

        tracab_x = (opta_x - 50) * pitch_x
        tracab_y = (opta_y - 50) * pitch_y

        return([tracab_x, tracab_y])

    else:

        tracab_x = ((opta_x - 50) * pitch_x) * -1
        tracab_y = ((opta_y - 50) * pitch_y) * -1

        return([tracab_x, tracab_y])
```
### 15. Parse f7 Files to Player Database
Convert the f7 xml file into a player info dataframe 
```p
def parse_f7(file_name):

    # parse the xml and convert to a tree and root
    tree = ET.parse(file_name)
    root = tree.getroot()

    match_id = int(root.find('SoccerDocument').get('uID')[1:])

    # ## get the main game info from the single 'Game' node
    gameinfo = root.findall('SoccerDocument')
    gameinfo = gameinfo[0]
    # # gameinfo.get('Country')
    # gameinfo = gameinfo.iter('MatchData')
    # gameinfo = gameinfo[0]



    # gameinfo.iter('MatchInfo')
    # root.iter('MatchData').iter('MatchInfo').get('Period')

    formation_place = []
    player_id = []
    position = []
    jersey_no = []
    status = []

    for neighbor in gameinfo.iter('MatchPlayer'):
        formation_place.append(neighbor.get('Formation_Place')) 
        player_id.append(neighbor.get('PlayerRef'))
        position.append(neighbor.get('Position'))
        jersey_no.append(neighbor.get('ShirtNumber')) 
        status.append(neighbor.get('Status')) 


    players1 = pd.DataFrame(
        {'formation_place': formation_place,
         'player_id': player_id,
         'position': position,
         'jersey_no': jersey_no,
         'status': status})


    p_id = []
    first_name = []
    last_name = []

    for neighbor in gameinfo.iter('Player'):
        p_id.append(neighbor.get('uID')) 
        first_name.append(neighbor.find('PersonName').find('First').text)
        last_name.append(neighbor.find('PersonName').find('Last').text)


    players2 = pd.DataFrame(
        {'first_name': first_name,
         'player_id': p_id,
         'last_name': last_name})


    players1['player_id'] = players1['player_id'].str[1:]
    players2['player_id'] = players2['player_id'].str[1:]

    playersDB = players1.merge(players2, on='player_id', how='inner')
    playersDB["player_name"] = playersDB["first_name"].map(str) + " " + playersDB["last_name"]


    minute = []
    period_id = []
    player_off = []
    player_on = []


    for neighbor in gameinfo.iter('Substitution'):
        minute.append(neighbor.get('Time')) 
        period_id.append(neighbor.get('Period')) 
        player_off.append(neighbor.get('SubOff')) 
        player_on.append(neighbor.get('SubOn')) 


    subs = pd.DataFrame(
        {'minute': minute,
         'period_id': period_id,
         'player_off': player_off,
         'player_on': player_on
        })


    subs['player_off'] = subs['player_off'].str[1:]
    subs['player_on'] = subs['player_on'].str[1:]

    playersDB['start_min'] = 0 
    playersDB['end_min'] = 0 

    match_length = 90
    for neighbor in gameinfo.iter('Stat'):
        if neighbor.get('Type') == "match_time":
            match_length = int(neighbor.text)

    for i in range(0,len(playersDB)):

        player_2_test = playersDB.iloc[i]

        if player_2_test['status'] == "Start":

            if player_2_test['player_id'] in subs.player_off.get_values():
                playersDB.at[i, 'end_min'] = subs.loc[subs['player_off'] == player_2_test['player_id']]['minute'].get_values()[0]

            else:
                playersDB.at[i, 'end_min'] = match_length

        if player_2_test['status'] == "Sub":

            if player_2_test['player_id'] in subs.player_on.get_values():
                playersDB.at[i, 'start_min'] = subs.loc[subs['player_on'] == player_2_test['player_id']]['minute'].get_values()[0]
                playersDB.at[i, 'end_min'] = match_length
            else:
                playersDB.at[i, 'end_min'] = player_2_test['end_min']

            if player_2_test['player_id'] in subs.player_off.get_values():
                playersDB.at[i, 'end_min'] = subs.loc[subs['player_off'] == player_2_test['player_id']]['minute'].get_values()[0]

    playersDB['mins_played'] = playersDB["end_min"] - playersDB["start_min"] 

    playersDB['match_id'] = match_id

    teams = []
    for team in gameinfo.findall('Team'):
        teams.append(team.get('uID')[1:])

    playersDB['team_id'] = ""
    playersDB['team'] = ""


    for i in range(0,36):
        if i <= 17:
            playersDB.at[i, 'team_id'] = teams[0]
            playersDB.at[i, 'team'] = 1
        else:
            playersDB.at[i, 'team_id'] = teams[1]
            playersDB.at[i, 'team'] = 0

    return(playersDB)
```

### 17. Add the Player Name and Opta player_id 
Useful in order to link tracking data to players 

```p
def add_player_id(f7_filename = f7_file, tracking_data = tdat):
    
    playerDB_ = parse_f7(f7_filename)[['jersey_no','player_id', 'team', 'player_name']]

    ballDB = pd.Series(['999.0', '000000', '10.0', 'ball'], index=['jersey_no','player_id', 'team', 'player_name'])
    playerDB_ = playerDB_.append(ballDB, ignore_index=True)

    playerDB_['jersey_no'] = playerDB_['jersey_no'].transform(float)
    playerDB_['team'] = playerDB_['team'].transform(float)
    
    tracking_data = tracking_data.merge(playerDB_, on = ['jersey_no', 'team'])
    
    return(tracking_data)
```
