# The Tracab Cookbook
Here is a collection of code snippets and functions that I have used to work with Tracab data. Thought I would share so I have a public record for my personal use later and to share for others. 

###### Caveats
This is based on parsing the raw .dat a pandas object, I call this object 'tdat'. Pandas isn't the most memory effective or speed effective data strcuture for tracking data, but whatever. All functions use the 'tdat' object name for the parsed tracking data, this is a default you can override. 

###### Contributions
If you want to contribute snippets to store here they will be warmly welcomed.  

### Parse Tracab Metadata 

```py
    
    def parse_tracking_metadata(filename):

    tree = ET.parse(filename)
    root = tree.getroot()

    period_startframe = []
    period_endframe = []

    gamexml = root.findall('match')[0]
    # gamexml.findall('period').get('iStartFrame')

    info_raw = []

    for i in gamexml.iter('period'):
            # get the info from the ball node main chunk
    #         print(int(i.get('iId')))
            info_raw.append( i.get('iStartFrame') )
            info_raw.append( i.get('iEndFrame') )

    # # Create empty dict Capitals
    game_info = dict()

    # # Fill it with some values
    game_info['period1_start'] = int(info_raw[0])
    game_info['period1_end'] = int(info_raw[1])
    game_info['period2_start'] = int(info_raw[2])
    game_info['period2_end'] = int(info_raw[3])
    game_info['period3_start'] = int(info_raw[4])
    game_info['period3_end'] = int(info_raw[5])
    game_info['period4_start'] = int(info_raw[6])
    game_info['period4_end'] = int(info_raw[7])


    for detail in root.iter('match'):
        game_info['pitch_x'] = int(float(detail.get('fPitchXSizeMeters')))
        game_info['pitch_y'] = int(float(detail.get('fPitchYSizeMeters')))

    return(game_info)
```
