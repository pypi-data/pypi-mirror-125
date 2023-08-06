function echov() {
  [ "$VERBOSE" = true ] && echo "$*"
} # echov

#-----------------------------------------------------------------------------------------------------------------------
function getConfig() {
  local PNAME=$1
  local CONFIG_FNAME=$CONF_DIR/wm.config
  if [ ! -f "$CONFIG_FNAME" ]; then echo "ERROR - config file '$CONFIG_FNAME' not found"; return 1; fi

  if [[ ! "${PYTHONPATH/$PF_ROOT/PF-LIB-IN-PATH}" =~ PF-LIB-IN-PATH ]]; then export PYTHONPATH="$PYTHONPATH:$PF_ROOT/lib"; fi
  /usr/bin/env python <<EOF
import configparser
import pi3dpf_owm_weather.common.pf_common as pfc
config         = configparser.ConfigParser(inline_comment_prefixes=';',
  empty_lines_in_values=False,
  converters={'list': lambda x: [i.strip() for i in x.split(',')]}) # cannot use interpolation=None, need to escape % (as %%) in values!
config.read('$CONFIG_FNAME')
print (pfc.get_config_param(config, '$PNAME'))
EOF
} # getConfig

#-----------------------------------------------------------------------------------------------------------------------
function getMainColorRGB() {
  local IMG_FNAME="$1"
  local PROP_FNAME="$2"
  /usr/bin/env python <<EO_PYTHON_PROG
import operator
from PIL import Image
image = Image.open('$IMG_FNAME')
count = {}
# count pixels per RGB color
for i in image.getdata():
  count[i] = count[i] + 1 if i in count.keys() else 1
maincolor = max(count.items(), key=operator.itemgetter(1))[0]
try:
  print("maincolor=rgb({},{},{})".format(maincolor[0], maincolor[1], maincolor[2]))
except IndexError as e:
  print('INFO - probably using this function on a transparent image $IMG_FNAME')
  exit(1)

# From: https://stackoverflow.com/a/44923761
# get first and last pixel not equal background 
rgb = image.convert('RGB')
x_min = image.size[0] + 1
x_max = -1
y_min = image.size[1] + 1
y_max = -1
r_min = maincolor[0] - 5
r_max = maincolor[0] + 5
g_min = maincolor[1] - 5
g_max = maincolor[1] + 5
b_min = maincolor[2] - 5
b_max = maincolor[2] + 5

for y in range(image.size[1]):
  for x in range(image.size[0]):
    rgb_pix = rgb.getpixel((x, y))
    if r_min <= rgb_pix[0] <= r_max and g_min <= rgb_pix[1] <= g_max and b_min <= rgb_pix[2] <= b_max:
      pass
    else:
      x_min = x if x < x_min else x_min
      x_max = x if x > x_max else x_max
      y_min = y if y < y_min else y_min
      y_max = y if y > y_max else y_max

print("x_min: {:4d} x_max: {:4d} y_min: {:4d} y_max: {:4d}\n".format(x_min, x_max, y_min, y_max))
#print("imagemagick_crop={}x{}+{}+{}".format(x_min, y_min, x_max - x_min, y_max - y_min))    
with open('$PROP_FNAME', 'w') as of:
  of.write("maincolor=rgb({},{},{})\n".format(maincolor[0], maincolor[1], maincolor[2]))
  of.write("imagemagick_crop={}x{}+{}+{}\n".format(x_max - x_min, y_max - y_min, x_min, y_min))
  of.write("x_min={}\n".format(x_min))
  of.write("x_max={}\n".format(x_max))
  of.write("y_min={}\n".format(y_min))
  of.write("y_max={}\n".format(y_max))
  
exit(0)
EO_PYTHON_PROG
#import pdb; pdb.set_trace()
} # getMainColorRGB

#-----------------------------------------------------------------------------------------------------------------------
# From: https://superuser.com/a/576980
# libre calc actually prints A2 page, which is mostly white. So, getMainColorRGB is of no use.
# function to display the most used color in given image
function imagemagick_2nd_most_color() {
  local FNAME="$1"
  local COLOR_RAW="$(convert "$FNAME" -format %c -depth 8 histogram:info:- | sort -n | tail -2 | head -1)"
  # extract RGB code and print like 'rgb(238,238,238)'
  perl -se 'print "rgb($1)\n" if $color_raw =~ /\s+\d+: \((\s*\d+,\s*\d+,\s*\d+).*/;' -- -color_raw="$COLOR_RAW"
} # imagemagick_2nd_most_color
#-----------------------------------------------------------------------------------------------------------------------
function updateTemplateWithOWMdata() {
  local CONFIG_FNAME=$CONF_DIR/wm.config
  if [ ! -f "$CONFIG_FNAME" ]; then echo "ERROR - config file '$CONFIG_FNAME' not found"; return 1; fi
  /usr/bin/env python <<EO_PROGRAM
import pi3dpf.openweathermapToerikflowers_wi as owm
import libreoff2img as lofi

import configparser #, logger
import pi3dpf_owm_weather.common.pf_common as pfc
from pi3d import Log
logging = Log(level='INFO', format="%(asctime)s %(levelname)s: %(message)s") # name='a.py', 

config         = configparser.ConfigParser(inline_comment_prefixes=';',
                                           empty_lines_in_values=False,
                                           converters={'list': lambda x: [i.strip() for i in x.split(',')]}) # cannot use interpolation=None, need to escape % (as %%) in values!
config.read('$CONFIG_FNAME')

OWM_API_KEY          = pfc.get_config_param(config, 'OWM_API_KEY')
OWM_UNITS            = pfc.get_config_param(config, 'OWM_UNITS')
OWM_CITY_IDS         = pfc.get_config_param(config, 'OWM_CITY_IDS')
OWM_NOW_BASE_URL= pfc.get_config_param(config, 'OWM_NOW_BASE_URL')
OWM_NOW_BASE_URL+=OWM_API_KEY
logging.info('OWM_NOW_BASE_URL={}'.format(OWM_NOW_BASE_URL))

x = lofi.loff2img(config, logging)
x.addWeatherToTemplate()
EO_PROGRAM
} # updateTemplateWithOWMdata
#-----------------------------------------------------------------------------------------------------------------------
function open_and_save_ods() {
  local ODS_PATH="$1" # mandatory. Path to local Libre Calc document, e.g. /home/pi/.pf/owm/5d_001_02657896_CH.Zürich/owm-weather-5d3h.ods
  if [ ! -f "$ODS_PATH" ]; then echo "ERROR - config file '$ODS_PATH' not found"; return 1; fi
  /usr/bin/env python <<EO_PROGRAM
import pyoo
desktop = pyoo.Desktop('localhost', 8052)
doc = desktop.open_spreadsheet('$ODS_PATH')
EO_PROGRAM
} # open_and_save_ods
#-----------------------------------------------------------------------------------------------------------------------
# extract min and max parameters from properties files generated by getMainColorRGB()
# example property file (supplied to PROP_FNAME as pathname to property file):
#      maincolor=rgb(255,255,255)
#      imagemagick_crop=1803x947+220+1
#      x_min=220
#      x_max=2023
#      y_min=1
#      y_max=948
# this functions output is such that it can be used in an eval expression to set the variables X_MIN X_MAX Y_MIN Y_MAX
function get_png_props() {
  local PROP_FNAME="$1"
  unset X_MIN X_MAX Y_MIN Y_MAX
  perl -wne '$x_min=$1 if /^x_min=(\d+)/;
  $x_max=$1 if /^x_max=(\d+)/;
  $y_min=$1 if /^y_min=(\d+)/;
  $y_max=$1 if /^y_max=(\d+)/;
  END { printf "X_MIN=%d; X_MAX=%d; Y_MIN=%d; Y_MAX=%d", $x_min, $x_max, $y_min, $y_max; }
  ' "$PROP_FNAME"
} # get_png_props

#-----------------------------------------------------------------------------------------------------------------------
function check_city_id_dir() {
  local CITYID="$(printf "%08d" "$1")"    # mandatory. OWM city ID, e.g. 2657896 for Zurich.
  local BASE_DIR="${2:-/home/pi/.pf/owm}" # mandatory. Typically OWM_DATA_DIR (/home/pi/.pf/owm)
  local DIR_COUNT="$(cd "$BASE_DIR" && ls -ld 5d_*_${CITYID}_* |grep ^d|wc -l)"
  # echo "DIR_COUNT=$DIR_COUNT" >&2
  if [ "$DIR_COUNT" -ne 1 ]; then
    echo "ERROR - check_city_id_dir() - The number of city directories with '$CITYID' in '$BASE_DIR' is $DIR_COUNT, expected 1." >&2
    echo "invalid_city_id_$CITYID"
    return 1
  fi
  (cd "$BASE_DIR" && ls -d 5d_*_${CITYID}_*)
} # check_city_id_dir
