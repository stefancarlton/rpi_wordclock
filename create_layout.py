import ast
import ConfigParser
import getopt
import os
import svgwrite
import sys
import wordclock_tools.wiring as wiring

def searchInWCA(wcl, index):
    for i in range(wcl.WCA_WIDTH):
        for j in range(wcl.WCA_HEIGHT):
            if wcl.getStripIndexFrom2D(i,j) == index:
                return (i,j)
    return None

def searchInMinutes(wcl, index):
    for i in [1, 2, 3, 4]:
        if wcl.mapMinutes(i) == index:
            return i
    print('Mapping error for minute: Index: ' + str(index))
    return None

def get_letter_coords(wca_top_left,x,x_spacing,y,y_spacing, side, col_num):
    if(side=='front'):
        return wca_top_left[0]+x*x_spacing, wca_top_left[1]+y*y_spacing
    elif(side=='back'):
        return wca_top_left[0]+(col_num-x-1)*x_spacing, wca_top_left[1]+y*y_spacing

    
def get_min_coords(width, height, minute_margin, min_num, side):
    if (side=='front' and min_num == 1) or (side=='back' and min_num == 2):
        return (minute_margin, minute_margin)
    elif (side=='front' and min_num == 2) or (side=='back' and min_num == 1):
        return (width-minute_margin,minute_margin)
    elif (side=='front' and min_num == 3) or (side=='back' and min_num == 4):
        return (minute_margin,height-minute_margin)
    elif (side=='front' and min_num == 4) or (side=='back' and min_num == 3):
        return (width-minute_margin,height-minute_margin)
    else:
        print('ERROR: Invalid ' + str(min_num))

def create_svg(lang, config, side='front', mode='stancil'):
    #height = word array height + margin + minute row
    #width  = word array width + margin
    
    if not mode == 'stancil':
        wiring_type='_' + config.get('wordclock_display','wiring_layout')
    else:
        wiring_type=''
    outpt_file =  'rects.svg'
    print('Rendering ' + outpt_file + '...')
    print('  Side .........: ' + side)
    print('  Mode .........: ' + mode)
    content = ast.literal_eval(config.get('language_options', lang))
    print('  Language .....: ' + lang)
    font_type = config.get('stancil_parameter', 'font_type')
    print('  Font-type.....: ' + font_type)
    font_size = config.get('stancil_parameter', 'font_size')
    print('  Font-size.....: ' + font_size)
    
    #wca_height=float(config.get('stancil_parameter', 'wca_height'))

    
    row_num=len(content)
    print('  Wca rows .....: ' + str(row_num))
    col_num=len(content[0].decode('utf-8'))
    print('  Wca columns ..: ' + str(col_num))
    minute_margin=float(config.get('stancil_parameter', 'minute_margin'))
    minute_diameter=float(config.get('stancil_parameter', 'minute_diameter'))
    
    wca_height = float(config.get('stancil_parameter', 'wca_height'))
    print('  Wca height ...: ' + str(wca_height) + 'mm')
    wca_width =float(config.get('stancil_parameter', 'wca_width'))
    print('  Wca width ....: ' + str(wca_width) + 'mm')
    
    wca_margin=float(config.get('stancil_parameter', 'wca_margin'))
    print('  Wca margin ..: ' + str(wca_margin))
    
    wcbr_height = wca_height/row_num
    
    height=wca_height + (wca_margin*2)
    print('  Height .......: ' + str(height) + 'mm')
    
    width =wca_width + (wca_margin*2)
    print('  Width ........: ' + str(width) + 'mm')
    
    rm=minute_diameter/2


    # Create directory to store layout
    file_dir = os.path.join('wordclock_layouts', lang + '_' + str(col_num) + 'x' + str(row_num))
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    full_path=os.path.join(file_dir, outpt_file)

    fg='rgb(255,255,255)'
    st='rgb(0,0,0)'
    bg='rgb(255,255,255)'
    wc_style='fill:none;fill-opacity:1;'\
          'stroke:'+st+';stroke-width:0.2822222222;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;'\
          'text-anchor:middle;'\
          'font-family:'+font_type+';'\
          'font-size:'+str(font_size)
          
    wc_style_small='fill:none;fill-opacity:1;'\
          'stroke:'+st+';stroke-width:0.282222222;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;'\
          'text-anchor:middle;'\
          'font-family:'+font_type+';'\
          'font-size:11;'
    
    # Generate header
    layout = svgwrite.Drawing(full_path, \
            size = (str(width)+'mm', str(height)+'mm'), \
            viewBox=('0 0 ' + str(width) + ' ' + str(height)))
    # Assure set background-color to bg

    # Create layout-group for text
    text_layout=layout.g(style=str(wc_style))

    # top 
    layout.add( layout.line(start=(0,0), end=(width, 0), stroke='rgb(0,0,0)'))
    # left
    layout.add( layout.line(start=(0,0), end=(0, height), stroke='rgb(0,0,0)'))
    #right
    layout.add( layout.line(start=(width,0), end=(width, height), stroke='rgb(0,0,0)'))
    #bottom
    layout.add( layout.line(start=(0, height), end=(width,height), stroke='rgb(0,0,0)')) 
            
    # top 
    #text_layout.add( layout.line(start=(4,4), end=(width-4, 4), stroke='rgb(0,0,0)'))
    # left
    #text_layout.add( layout.line(start=(4,4), end=(4, height-4), stroke='rgb(0,0,0)'))
    #right
    #text_layout.add( layout.line(start=(width-4,4), end=(width-4, height-4), stroke='rgb(0,0,0)'))
    #bottom
    #text_layout.add( layout.line(start=(4, height-4), end=(width-4,height-4), stroke='rgb(0,0,0)')) 
            
    # Process letters
    #wca_top_left = [ wca_margin, (height-wca_margin)]
    wca_top_left = [(width-wca_width)/2, (height-wca_height)/2]
    x_coords = range(0,col_num,1)
    y_coords = range(0,row_num,1)
    x_spacing =  wca_width/(col_num-1)
    y_spacing = wca_height/(row_num-1)

    # Additional steps to prepare the plotting of the wiring layout
    x_sub_spacing = x_spacing/5.0
    y_sub_spacing = y_spacing/5.0
    wca_index_1d = 0

    wca_top_left=(30, 35)
    
    # Draw characters
    for y in y_coords:
        for x in x_coords:
            coords=(wca_top_left[0]+(x*30), wca_top_left[1]+(y*33))
            #coords=get_letter_coords(wca_top_left,x,x_spacing,y,y_spacing, side, col_num)
           
            # Write only characters
            #text_layout.add(layout.text((content[y].decode('utf-8')[x]), insert = (coords[0],coords[1]+float(font_size)/2.0)))
            loc_x = coords[0] - 3
            loc_y = coords[1] -3
            
            text_layout.add( layout.rect( insert=(loc_x, loc_y ), rx=None, ry=None, stroke='rgb(0,0,0)', size=(6,6) ))
            
            wca_index_1d +=1

            
#def get_letter_coords(wca_top_left,x,x_spacing,y,y_spacing, side, col_num):
#    if(side=='front'):
#        return wca_top_left[0]+x*x_spacing, wca_top_left[1]+y*y_spacing
#    elif(side=='back'):
#        return wca_top_left[0]+(col_num-x-1)*x_spacing, wca_top_left[1]+y*y_spacing
            
    # Process minutes

    #min_coords = get_letter_coords(wca_top_left, 8, x_spacing, row_num, y_spacing, side, col_num)
    #min_coords = (wca_top_left[0]+wca_width-48.655, min_coords[1])
    
    
    
    #layout.add(layout.text('O\' CLOCK', insert=('281.96655','355.26889'), style=str(wc_style)) )
            
    # Fuse layouts
    layout.add(text_layout)

    # Saving svg-file
    layout.save()
    print('Saved ' + full_path + '.')

def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'ahc:', ['all', 'help', 'config='])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)
    configFile = 'wordclock_config/wordclock_config.cfg'
    process_all = False
    for o, a in opts:
        if o in ('-a', '--all'):
            process_all = True
        elif o in ('-c', '--config'):
            configFile = a
        elif o in ('-h'):
            print('Provide config-file using -c option')
        else:
            assert False, 'unhandled option'

    print('Using ' + configFile + ' to parse configuration.')
    print('Use\n\t' + str(sys.argv[0]) + ' -c "config-file"\nto change')
    cfg = ConfigParser.ConfigParser()
    cfg.read(configFile)

    if process_all:
        all_languages=cfg.options('language_options')
    else:
        all_languages=[cfg.get('stancil_parameter', 'language')]

    for lang in all_languages:
        print('Processing layouts for ' +str(lang) + '.')
        create_svg(lang, cfg, side='front', mode='stancil')

if __name__ == '__main__':
    main()

