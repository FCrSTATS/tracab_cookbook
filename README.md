# The Tracab Cookbook
Here is a collection of code snippets and functions that I have used to work with Tracab data. Thought I would share so I have a public record for my personal use later and to share for others. 

###### Caveats
This is based on parsing the raw .dat a pandas object, I call this object 'tdat'. Pandas isn't the most memory effective or speed effective data strcuture for tracking data, but whatever. All functions use the 'tdat' object name for the parsed tracking data, this is a default you can override. 

###### Contributions
If you want to contribute snippets to store here they will be warmly welcomed.  

### Parse Tracab Metadata 
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


### Get One Frame of Tracking Data
Select one frame in time of tracking data, with options to select just one team (1 = home, 0 = away, 10 = ball).

```p
def get_frame(frame_select, trackingdata = tdat, a_team = False, team_select = 1):
    
    if a_team:
        return(trackingdata[(trackingdata['frameID'] == frame_select) & 
                            (trackingdata['team'] == team_select)].reset_index(drop=True))    
    else:
        return(trackingdata[trackingdata['frameID'] == frame_select].reset_index(drop=True))
```

### Get a Segment of Tracking Data
Select a period of time within the tracking data, with options to select just one team (1 = home, 0 = away, 10 = ball).

```p
def get_segment(frame_select_start, frame_select_end, trackingdata = tdat, a_team = False, team_select = 1):
    
    if a_team:
        return(trackingdata[(trackingdata['frameID'].between(frame_select_start, frame_select_end)) & 
                            (trackingdata['team'] == team_select)].reset_index(drop=True))    
    else:
        return(trackingdata[trackingdata['frameID'].between(frame_select_start, frame_select_end)].reset_index(drop=True))
```

### Add False/True Column if a Player's Team is in Possession
Althougth tracab data has the information regarding which team is in possession in a particular frame there isn't a easy way of determining if a player's team is in possession of the ball.

```p
def add_team_in_possession(trackingdata = tdat):
    
    trackingdata['team_in_possession'] = [(x == 1 and y == "H") or 
                                     (x == 0 and y == "A") 
                                     for x,y in zip(trackingdata.team, 
                                     trackingdata.ball_owning_team )]  
    return( trackingdata )
```

### Create a Pitch 
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

### Add the Ball x & y Coordinates
Create two new columns for the ball's x and y coorindates that frame in time. 

```p
def add_ball_xy(trackingdata = tdat):
    
    ball_df = trackingdata[trackingdata['team'] == 10].reset_index(drop=True)[['frameID', 'x', 'y']]    
    ball_df.columns = ['frameID', 'ball_x', 'ball_y']
    
    trackingdata = trackingdata.merge(ball_df, on = "frameID")
    
    return(trackingdata)

```

### Calculate the Distance to the Ball
Creates a new column of the distance the player is from the ball. 

```p
def add_distance_to_ball(trackingdata = tdat):
    trackingdata['distance_to_ball'] = trackingdata[['x', 'y']].sub(np.array( trackingdata[['ball_x', 'ball_y']] )).pow(2).sum(1).pow(0.5)
    trackingdata.distance_to_ball = trackingdata.distance_to_ball.round(2)
    return(trackingdata)
```

### Calculate the Distance to the Goals
Creates two new columns for the distance from a player to each goal, goal1 (-x) and goal2 (x)

```p
def add_distance_to_goals(trackingdata = tdat, x = 5250):

    trackingdata['distance_to_goal1'] = trackingdata[['x', 'y']].sub(np.array( -x, 0 )).pow(2).sum(1).pow(0.5)
    trackingdata['distance_to_goal2'] = trackingdata[['x', 'y']].sub(np.array( x, 0 )).pow(2).sum(1).pow(0.5)

    trackingdata.distance_to_goal1 = trackingdata.distance_to_goal1.round(2)
    trackingdata.distance_to_goal2 = trackingdata.distance_to_goal2.round(2)

    return(trackingdata)
```

### Calculate Distance Between 2 Points
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

### Add Attacking Direction
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

### Switch the Pitch
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
