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

    return the dictionary of information 
    return(game_info)
```
