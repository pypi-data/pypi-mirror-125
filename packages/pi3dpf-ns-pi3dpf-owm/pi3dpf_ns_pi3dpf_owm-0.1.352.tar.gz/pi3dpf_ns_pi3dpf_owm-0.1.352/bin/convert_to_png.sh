#!/bin/bash
# tiny wrapper to make sure all pre-requisites to convert a libreoffice .odt file (aka template) to a bitmap image (jpg/png) are in place
THIS_FILE="$(basename "$0")"
THIS_DIR="$(dirname "$0")"
FONT_DIR="$(cd "$THIS_DIR"; cd ../lib/python*/site-packages/pi3dpf_owm_weather/common/cfg/fonts; pwd)"
CONF_DIR="$(cd "$THIS_DIR"; cd ../lib/python*/site-packages/pi3dpf_owm_weather/common/cfg; pwd)"
LIBR_DIR="$(cd "$THIS_DIR"; cd ../lib/python*/site-packages/pi3dpf_owm_weather/common; pwd)"
export PYTHONPATH=$LIBR_DIR
source $THIS_DIR/activate
source $LIBR_DIR/pf.functions.sh

#-----------------------------------------------------------------------------------------------------------------------
function usage() {
  cat <<EO_USAGE
  usage: $THIS_FILE -t template [-c city_id] [-vh] [-l log_file]

  Mandatory Command Line Switches:
    -t template. For template, use one of 'NOW' or '5D3H'
    -c city_id. Only mandatory for -t 5D3H. OWM city id as specified in OWM_CITY_IDS
       the following cities are currently available: $(show_city_ids "$OWM_DATA_DIR")

  Optional Command Line Switches:
    -f force copying 5D3H template to CITY directory even there is already a template
    -l log_file. Append log output to log_file instead of stdout
    -h print this page
    -v be more verbose. Use up to 3 -v options to increase verbosity.

EO_USAGE
# Deprecated options:
#   -r only for '-t now'. Refresh weather information before generating png. (obsolete, not working)
  exit 0
} # usage
#-----------------------------------------------------------------------------------------------------------------------
function log() {
  local PREFIX=""
  [ "$REDIRECT_OUTPUT" = true ] && PREFIX="$(date '+%Y-%m-%d %H:%M:%S,%N')" && PREFIX="${PREFIX:0:23} "
  echo "${PREFIX}$*" >&2
} # log
#-----------------------------------------------------------------------------------------------------------------------
function echov() {
  [ "$VERBOSE" = true ] && log "$*"
} # echov
#-----------------------------------------------------------------------------------------------------------------------
function echoe() {
  log "$*"
  log "INFO - script $THIS_FILE failed"
} # echoe
#-----------------------------------------------------------------------------------------------------------------------
function show_city_ids() {
  local OWM_DIR="${1:-/home/pi/.pf/owm}" # optional
  local A D ID REST
  while read D; do IFS=_ read A A ID REST <<< "$D"; printf "%d " "${ID##0}"; done < <(cd "$OWM_DIR"; ls -d 5d_???_????????_*)
}
#-----------------------------------------------------------------------------------------------------------------------

function mk_new_city_soft_link() {
  local OWM_DATA_DIR="$1"
  local CITY_DIR="$2"
  if [ -f "$OWM_DATA_DIR/5d_000_current_city" -o -L "$OWM_DATA_DIR/5d_000_current_city" ]; then
    log "+ rm '$OWM_DATA_DIR/5d_000_current_city'"
           rm "$OWM_DATA_DIR/5d_000_current_city"
  fi
  log "+ cd '$OWM_DATA_DIR'"
         cd "$OWM_DATA_DIR"
  log "+ ln -s '$CITY_DIR' 5d_000_current_city"
         ln -s "$CITY_DIR" 5d_000_current_city
  log "+ ls -l '$OWM_DATA_DIR/5d_000_current_city' '$OWM_DATA_DIR/5d_000_current_city/consolidated.csv'"
         ls -l "$OWM_DATA_DIR/5d_000_current_city" "$OWM_DATA_DIR/5d_000_current_city/consolidated.csv"
  log "+ grep 'City Names:' $OWM_DATA_DIR/5d_000_current_city/consolidated.csv"
         grep 'City Names:' $OWM_DATA_DIR/5d_000_current_city/consolidated.csv
} # mk_new_city_soft_link
#-----------------------------------------------------------------------------------------------------------------------
function change_simple_ods_link() {
  local ODS_PATH="$1"   # mandatory. Path to LibreCalc file containing a link to consolidated.csv, typically owm-weather-5d3h.ods
  local NEW_SOURCE="$2" # mandatory. Path to insert into content.xml. E.g. /home/pi/.pf/owm/5d_001_02657896_CH.Zürich/consolidated.csv

  if [ ! -f "$ODS_PATH"   ]; then echoe "ERROR - Libre Calc file '$ODS_PATH' does not exist"; return 1; fi
  if [ ! -f "$NEW_SOURCE" ]; then echoe "ERROR - requested data source '$NEW_SOURCE' does not exist"; return 1; fi

  # check if requested path is already in content.xml
  local LINK="$(unzip -p "$ODS_PATH" content.xml|grep -oP "xlink:type=.simple. xlink:href=.*?$NEW_SOURCE")"
  if [ -n "$LINK" ]; then
    echo "INFO - the source '$NEW_SOURCE' is already in content.xml"
    echo "LINK='$LINK'"
    return 0
  fi

  local CONTENT_ORIG="$(dirname "$ODS_PATH")"/CONTENT.XML
  local CONTENT_NEW="$( dirname "$ODS_PATH")"/content.xml
  unzip -p "$ODS_PATH" content.xml | xmllint --format - > "$CONTENT_ORIG"
  perl -wspe 's/(xlink:type=.simple. xlink:href=.)(.*?consolidated.csv)/$1$new_src/;' -- -new_src="$NEW_SOURCE" "$CONTENT_ORIG" > "$CONTENT_NEW"
  grep -o -P 'xlink:type=.simple. xlink:href=.*?consolidated.csv' "$CONTENT_ORIG" "$CONTENT_NEW"
  # zip -f /home/pi/.pf/owm-n/5d_001_02657896_CH.Zürich/owm-weather-5d3h.ods /home/pi/.pf/owm-n/5d_001_02657896_CH.Zürich/content.xml
  cd "$(dirname "$ODS_PATH")"
  zip -f "$(basename "$ODS_PATH")" "$(basename "$CONTENT_NEW")"
  unzip -p "$ODS_PATH" content.xml|grep -oP 'xlink:type=.simple. xlink:href=.*?consolidated.csv'
  cd -
} # change_simple_ods_link
#-----------------------------------------------------------------------------------------------------------------------
#     #     #
#     ##   ##   ##   # #    #
#     # # # #  #  #  # ##   #
#     #  #  # #    # # # #  #
#     #     # ###### # #  # #
#     #     # #    # # #   ##
#     #     # #    # # #    #

OWM_DATA_DIR="$(getConfig OWM_DATA_DIR)"
VERBOSE=false
REDIRECT_OUTPUT=false
LF=uninitialized
TEMPLATE=uninitialized
CITY_ID=uninitialized
FORCE_5D3H_TEMPLATE_COPY=false
while getopts c:l:ht:v ARG; do
  case "$ARG" in
    c) CITY_ID="$OPTARG"                                ;;
    f) FORCE_5D3H_TEMPLATE_COPY=true                    ;;
    l) REDIRECT_OUTPUT=true; LF="$OPTARG"               ;;
    h) usage; exit 0                                    ;;
    t) TEMPLATE="${OPTARG^^}"                           ;;
    v) VERBOSE=true;V_LEVEL=$((V_LEVEL + 1))            ;;
    *) echoe "ERROR - invalid option encountered"; exit 1;;
  esac
done
shift $((OPTIND-1))

if [ "$REDIRECT_OUTPUT" = true ]; then
  exec >>"$LF"
  exec 2>&1
fi

case "$TEMPLATE" in
  NOW)  OWM_LIBREOFFICE_TEMPLATE_IN="$(getConfig OWM_NOW_LIBREOFFICE_TEMPLATE_IN)"
        OWM_LIBREOFFICE_PRINT_READY="$(getConfig OWM_NOW_LIBREOFFICE_PRINT_READY)"
        OWM_LIBREOFFICE_BITMAP_OUT="$( getConfig OWM_NOW_LIBREOFFICE_BITMAP_OUT)"
        OWM_DATA_DIR="$OWM_DATA_DIR/now"
    ;;
  5D3H)
    if [ "$CITY_ID" = uninitialized ]; then
      log "ERROR - option '-c city_id' mandatory with '-t 5D3H'"
      log "INFO - available cities: $(show_city_ids "$OWM_DATA_DIR")"
      exit 1
    fi
    CITY_DIR="$(check_city_id_dir "${CITY_ID##0}" "$OWM_DATA_DIR")"
    if [ "${CITY_DIR:0:15}" = invalid_city_id ]; then
      log "ERROR - city id '$CITY_ID' invalid"
      log "INFO - check directories for '-c $CITY_ID' in $OWM_DATA_DIR"
      log "INFO - available city_ids: $(show_city_ids "$OWM_DATA_DIR")"
      exit 1
    fi

    # handle soft link pointing to the weather data (contained in consolidated.csv)
    # CAVEAT: this softlink is used inside the Libre Calc to refer to the external data source consolidated.csv
    if [ -L "$OWM_DATA_DIR/5d_000_current_city" ]; then
      SL_TARGET="$(readlink "$OWM_DATA_DIR/5d_000_current_city")"
      if [ "${SL_TARGET%%/}" != "$CITY_DIR" ]; then
        mk_new_city_soft_link "$OWM_DATA_DIR" "$CITY_DIR"
      fi
    else
      mk_new_city_soft_link "$OWM_DATA_DIR" "$CITY_DIR"
    fi

    OWM_DATA_DIR="$OWM_DATA_DIR/$CITY_DIR"
    OWM_LIBREOFFICE_TEMPLATE_IN="$(getConfig OWM_5D3H_LIBREOFFICE_TEMPLATE_IN)"
    OWM_LIBREOFFICE_PRINT_READY="${OWM_DATA_DIR}/$(getConfig OWM_5D3H_LIBREOFFICE_PRINT_READY)"
    OWM_LIBREOFFICE_BITMAP_OUT="${OWM_DATA_DIR}/$( getConfig OWM_5D3H_LIBREOFFICE_BITMAP_OUT)"
    ;;
  uninitialized) "ERROR - option -t is mandatory"; exit 1;;
  *) echoe "ERROR - option '-t $TEMPLATE is invalid"; exit 1;
esac

log "OWM_LIBREOFFICE_TEMPLATE_IN=$OWM_LIBREOFFICE_TEMPLATE_IN"
if [ ! -f "$OWM_LIBREOFFICE_TEMPLATE_IN" ]; then
  echoe "ERROR - input template '$OWM_LIBREOFFICE_TEMPLATE_IN' does not exist"
  exit 1
fi

log "OWM_LIBREOFFICE_PRINT_READY=$OWM_LIBREOFFICE_PRINT_READY"
## if [ ! -f "$OWM_LIBREOFFICE_PRINT_READY" -a "$TEMPLATE" = NOW ]; then
##   # openweathermapToerikflowers_wi.update_weather_info() enriched OWM_NOW_LIBREOFFICE_TEMPLATE_IN with weather data
##   # so OWM_LIBREOFFICE_PRINT_READY must exist when -t NOW
##   log "ERROR - output template '$OWM_LIBREOFFICE_PRINT_READY' does not exist"
##   exit 1
## else
##   #
##   if [ ! -f "$OWM_LIBREOFFICE_PRINT_READY" -o "$FORCE_5D3H_TEMPLATE_COPY" = true ]; then
##     # copy OWM_5D3H_LIBREOFFICE_TEMPLATE_IN to OWM_LIBREOFFICE_PRINT_READY just to keep algorythm consistent with '-t now'
##     log "+ cp '$OWM_LIBREOFFICE_TEMPLATE_IN' '$OWM_LIBREOFFICE_PRINT_READY' # FORCE_5D3H_TEMPLATE_COPY=$FORCE_5D3H_TEMPLATE_COPY"
##            cp "$OWM_LIBREOFFICE_TEMPLATE_IN" "$OWM_LIBREOFFICE_PRINT_READY"
##   fi
## fi
if [ ! -f "$OWM_LIBREOFFICE_PRINT_READY" -a "$TEMPLATE" = NOW ]; then
  # templates are always copied from within the owm python library
  log "ERROR - output template '$OWM_LIBREOFFICE_PRINT_READY' does not exist"
  exit 1
fi


# check required packages on RPi
MISSING_LIST=""
while read STATUS PKG REST; do
  OPENJDK=$PKG
  OPENJDK=${OPENJDK%:*}
  break
done < <(dpkg-query -l openjdk*|grep '^.i..openjdk.*jre[ :]')

# check libreoffice packages depending on the libreoffice format (specified in OWM_LIBREOFFICE_TEMPLATE_IN)
case "${OWM_LIBREOFFICE_TEMPLATE_IN##*.}" in
  odt) LIBREOFFICE_RPM="libreoffice-writer" ;;
  odg) LIBREOFFICE_RPM="libreoffice-draw"   ;;
  odp) LIBREOFFICE_RPM="libreoffice-impress";;
  ods) LIBREOFFICE_RPM="libreoffice-calc"   ;;
  *) echoe "ERROR - unexpected libreoffice template extension '${OWM_LIBREOFFICE_TEMPLATE_IN##*.}'"; exit 1;;
esac

for P in $OPENJDK $LIBREOFFICE_RPM libreoffice-java-common imagemagick; do # openjdk-9-jre
  dpkg-query --status "$P" > /dev/null 2>&1
  RC=$?
  if [ "$RC" -ne 0 ]; then MISSING_LIST+=" $P"; fi
done
if [ -n "$MISSING_LIST" ]; then echoe "ERROR - packages $MISSING_LIST missing"; exit 1; fi

# check font is installed
OWM_FT_FONT="$(getConfig OWM_FT_FONT)"
log "OWM_FT_FONT=$OWM_FT_FONT"
if [ ! -f $OWM_FT_FONT ]; then echoe "ERROR - font '$OWM_FT_FONT' not found. (Defined as OWM_FT_FONT in $CONF_DIR/wm.config)"; exit 1; fi
FONT_TEST="$(find /usr/share/fonts/ -type f -name "$(basename "$OWM_FT_FONT")")"
MUST_COPY_FONT=false
if [ -z "$FONT_TEST" ]; then 
  log "INFO - required font '$OWM_FT_FONT' not found in /usr/share/fonts"
  MUST_COPY_FONT=true
elif [ "$(stat --format='%Y' "$FONT_TEST")" -lt "$(stat --format='%Y' "$OWM_FT_FONT")" -o "$(stat --format='%s' "$FONT_TEST")" -ne "$(stat --format='%s' "$OWM_FT_FONT")" ]; then
  log "INFO - font '$FONT_TEST' is not identical to '$OWM_FT_FONT'"
  MUST_COPY_FONT=true
fi

FONT_SPEC="$(basename "$OWM_FT_FONT")"
FONT_FAMILY="$(fc-list "${FONT_SPEC%.*}" : family)"
FONT_FAMILY="${FONT_FAMILY#*,}"

# check if font configured in wm.config OWM_FT_FONT parameter is referenced in libreoffice's content.xml and/or styles.xml files.
# unzip -p weather.odp styles.xml | grep -c 'Weather Icons'
#        log "+ fc-list | grep '$(basename "$OWM_FT_FONT")' # get font family name of font currently configured in OWM_FT_FONT"
# FONT_FAMILY="$(fc-list | grep "$(basename "$OWM_FT_FONT")" )"
# FONT_FAMILY="${FONT_FAMILY#*: }" # cut leading clutter
# FONT_FAMILY="${FONT_FAMILY%:*}"  # cut trailing clutter
             log "+ unzip -p '$OWM_LIBREOFFICE_TEMPLATE_IN' styles.xml  | grep -c '$FONT_FAMILY') # determine number of occurances in style.xml"
REF_IN_STYLE_CNT="$(unzip -p "$OWM_LIBREOFFICE_TEMPLATE_IN" styles.xml  | grep -c "$FONT_FAMILY")"
             log "+ unzip -p '$OWM_LIBREOFFICE_TEMPLATE_IN' content.xml | grep -c '$FONT_FAMILY') # determine number of occurances in content.xml"
REF_IN_CONT_CNT="$( unzip -p "$OWM_LIBREOFFICE_TEMPLATE_IN" content.xml | grep -c "$FONT_FAMILY")"
if [ "$REF_IN_STYLE_CNT" -lt 1 -a "$REF_IN_CONT_CNT" -lt 1 ];then 
  log "WARNING - font '$(basename "$OWM_FT_FONT")' referenced by wm.config parameter OWM_FT_FONT seems not to be used in '$OWM_LIBREOFFICE_TEMPLATE_IN'"
fi

if [ "$MUST_COPY_FONT" = true ]; then
  if [ "$(whoami)" = root ]; then SUDO=""; else SUDO="sudo "; fi
  log "+ ${SUDO}cp '$OWM_FT_FONT' /usr/share/fonts"
         ${SUDO}cp "$OWM_FT_FONT" /usr/share/fonts
fi

IMAGEMAGICK_CONVERT="$(type convert)"
if [ -z "$IMAGEMAGICK_CONVERT" ]; then echoe "ERROR - ImageMagick not installed"; exit 1; fi

if [ "$TEMPLATE" = 5D3H ]; then
  LO_PROP_FILE="$(find ~/.config/libreoffice/ -name registrymodifications.xcu)"
  if [ ! -f "$LO_PROP_FILE" ]; then
    log "WARNING - libre office configuration not found in ~/.config/libreoffice"
  else
    CHECK_EXTERNAL_LINK="$(grep -ri "SecureURL.*/opt/venvs/pi3d-owm-weather" "$LO_PROP_FILE")"
    SEC_URL_LIST="$(perl -ne 'if (m{SecureURL.*?<it>(.*)</it>}) {@e = split(m{</it><it>}, $1); foreach $f (@e) {print "$f\n";} }' "$LO_PROP_FILE")"
    SEC_URL_CHECK_PASSED=false
    AUTO_INPUT_CHECK_PASSED=false
    for F in $SEC_URL_LIST; do
      F="${F#file://}"; F="${F/\$\(home\)/$HOME}"
      if [[ "$OWM_LIBREOFFICE_PRINT_READY" =~ $F ]]; then SEC_URL_CHECK_PASSED=true; fi
    done
    AUTO_INPUT="$(perl -nwe 'print "$1\n" if m{AutoInput.*<value>(.*)</value>};' "$LO_PROP_FILE")"
    if [ "$AUTO_INPUT" = true ]; then SEC_URL_CHECK_PASSED=true; fi
    if [ "$SEC_URL_CHECK_PASSED" != true -o "$SEC_URL_CHECK_PASSED" != true ]; then
      cat <<EO_HINTS
To set trusted locations: Use Tools > Options > LibreOffice > Security > Button: Macro Security >
 Tab: «Trusted Sources» > Category: Trusted File Locations >
   Button: Add to add the directory of your file(s) which you want to trust to automatically update external links.
EO_HINTS
    else
      log "INFO - Libre Calc config: fonts and user settings: ok"
    fi
  fi
fi

LIBOFF_CONVERT_TO_NOTRANS_BMP=$OWM_DATA_DIR/"$(basename "$OWM_LIBREOFFICE_PRINT_READY")"
LIBOFF_CONVERT_TO_NOTRANS_BMP=${LIBOFF_CONVERT_TO_NOTRANS_BMP%.???}.png
LIBOFF_CONVERT_TO_NOTRANS_PRP="${LIBOFF_CONVERT_TO_NOTRANS_BMP%.???}-png-props.txt"

# if [ "$TEMPLATE" = 5D3H ]; then
#   echo "+ change_simple_ods_link '$OWM_LIBREOFFICE_PRINT_READY' '$(dirname "$OWM_LIBREOFFICE_PRINT_READY")/consolidated.csv'"
#           change_simple_ods_link "$OWM_LIBREOFFICE_PRINT_READY" "$(dirname "$OWM_LIBREOFFICE_PRINT_READY")/consolidated.csv"
#   RC=$?
# fi

if [ -f "$LIBOFF_CONVERT_TO_NOTRANS_BMP" ]; then rm "$LIBOFF_CONVERT_TO_NOTRANS_BMP"; fi
# Libreoffice filters for draw (graphic filters): https://help.libreoffice.org/latest/he/text/shared/guide/convertfilters.html
log "+ soffice --headless --convert-to png --outdir '$(dirname "$LIBOFF_CONVERT_TO_NOTRANS_BMP")' '$OWM_LIBREOFFICE_PRINT_READY'"
       soffice --headless --convert-to png --outdir "$(dirname "$LIBOFF_CONVERT_TO_NOTRANS_BMP")" "$OWM_LIBREOFFICE_PRINT_READY" &>> "$LF"
RC=$?
if [ $RC -ne 0 -o ! -f "$LIBOFF_CONVERT_TO_NOTRANS_BMP" ]; then 
  echoe "ERROR - something went wrong"
  echoe "INFO - make sure the relevant libreoffice packages are installed"
  exit 1
fi

log "+ getMainColorRGB '$LIBOFF_CONVERT_TO_NOTRANS_BMP' '$LIBOFF_CONVERT_TO_NOTRANS_PRP'"
       getMainColorRGB "$LIBOFF_CONVERT_TO_NOTRANS_BMP" "$LIBOFF_CONVERT_TO_NOTRANS_PRP"

# get cached results from last getMainColorRGB run
case "$TEMPLATE" in
  NOW)  MAIN_COLOR="$(grep ^maincolor=rgb "$LIBOFF_CONVERT_TO_NOTRANS_PRP")"
        MAIN_COLOR=${MAIN_COLOR:10}
        ;;
  5D3H) MAIN_COLOR="$(imagemagick_2nd_most_color "$LIBOFF_CONVERT_TO_NOTRANS_BMP")";;
esac

log "MAIN_COLOR=$MAIN_COLOR # TEMPLATE='$TEMPLATE'"
CROP_RANGE="$(grep ^imagemagick_crop= "$LIBOFF_CONVERT_TO_NOTRANS_PRP")"
CROP_RANGE=${CROP_RANGE:17}
# extract all values from 394x143+303+61 and assign to variables, e.g. WIDTH=394; HEIGHT=143; X_OFF=303; Y_OFF=61;
eval $(perl -se 'print "WIDTH=$1; HEIGHT=$2; X_OFF=$3; Y_OFF=$4;\n" if $expr =~ /(\d+)x(\d+)\+(\d+)\+(\d+)/' -- -expr="$CROP_RANGE")

RESIZE_INSTR=""
if [ "$TEMPLATE" = 5D3H ]; then
  # The Libre Calc template prints the chart with a lite gray background on a white A2 page.
  # The light gray area is first used to determine the crop area.
  # Then, we need to replace the left and right white borders with light gray so that it will transformed to transparent
  # log "+ cp ${LIBOFF_CONVERT_TO_NOTRANS_BMP} ${LIBOFF_CONVERT_TO_NOTRANS_BMP%.png}-page.png # just temporary"
  #         cp ${LIBOFF_CONVERT_TO_NOTRANS_BMP} ${LIBOFF_CONVERT_TO_NOTRANS_BMP%.png}-page.png
  eval $(get_png_props "$LIBOFF_CONVERT_TO_NOTRANS_PRP") # setting variables X_MIN X_MAX Y_MIN Y_MAX
  # get_png_props example output: X_MIN=220; X_MAX=2023; Y_MIN=1; Y_MAX=948

  # +---------------------------+-------------+-----------+----------+-----------+-----------+
  # | -draw rectangle syntax => |             |  x_offset | y_offset |     width |    height |
  # +---------------------------+-------------+-----------+----------+-----------+-----------+
  # | Comments/Usage            |      Symbol |           |          |           |           |
  # +---------------------------+-------------+-----------+----------+-----------+-----------+
  # | left fill geometry        | RECTANGLE_L |         0 |        0 | X_MIN - 1 | Y_MAX - 1 |
  # | right fill geometry       | RECTANGLE_R | X_MAX + 1 |        0 |     10000 |     Y_MAX |
  # +---------------------------+-------------+-----------+----------+-----------+-----------+
  RECTANGLE_L="rectangle 0, 0, $((X_MIN - 1)), $((Y_MAX - 1))"
  RECTANGLE_R="rectangle $((X_MAX + 1)), 0, 10000, $Y_MAX"
  log "RECTANGLE_L='$RECTANGLE_L' RECTANGLE_R='$RECTANGLE_R'"
  log "+ convert '${LIBOFF_CONVERT_TO_NOTRANS_BMP}' -fill '$MAIN_COLOR' -draw '$RECTANGLE_L' -draw '$RECTANGLE_R' '${LIBOFF_CONVERT_TO_NOTRANS_BMP}~'"
         convert "${LIBOFF_CONVERT_TO_NOTRANS_BMP}" -fill "$MAIN_COLOR" -draw "$RECTANGLE_L" -draw "$RECTANGLE_R" "${LIBOFF_CONVERT_TO_NOTRANS_BMP}~"
  log "+ mv '${LIBOFF_CONVERT_TO_NOTRANS_BMP}~' '${LIBOFF_CONVERT_TO_NOTRANS_BMP}'"
         mv "${LIBOFF_CONVERT_TO_NOTRANS_BMP}~" "${LIBOFF_CONVERT_TO_NOTRANS_BMP}"

  # calculating '-resize geometry' to resize the image in next convert operation
  OWM_5D3H_LIBREOFFICE_BITMAP_MAX_WIDTH="$(getConfig OWM_5D3H_LIBREOFFICE_BITMAP_MAX_WIDTH)"
  log "OWM_5D3H_LIBREOFFICE_BITMAP_MAX_WIDTH=$OWM_5D3H_LIBREOFFICE_BITMAP_MAX_WIDTH, WIDTH=$WIDTH"
  if [ "$WIDTH" -gt "$OWM_5D3H_LIBREOFFICE_BITMAP_MAX_WIDTH" ]; then
    RESIZE_INSTR="-resize ${OWM_5D3H_LIBREOFFICE_BITMAP_MAX_WIDTH}x$((HEIGHT * OWM_5D3H_LIBREOFFICE_BITMAP_MAX_WIDTH / WIDTH))"
  fi
fi

log "RESIZE_INSTR='$RESIZE_INSTR'"

# From: http://pi3d.github.io/html/pi3d.html#pi3d.Texture.Texture
#    NB images loaded as textures can cause distortion effects unless they are certain sizes (below). 
#    If the image width is a value not in this list then it will be rescaled with a resulting loss of clarity
#    Allowed widths 4, 8, 16, 32, 48, 64, 72, 96, 128, 144, 192, 256, 288, 384, 512, 576, 640, 720, 768, 800, 960, 1024, 1080, 1920
# Extend the crop range to fit to the next size of allowed withs to prevent odd distortion
ALLOWED_WIDTHS="4 8 16 32 48 64 72 96 128 144 192 256 288 384 512 576 640 720 768 800 960 1024 1080 1920"
IMG_WIDTH="${CROP_RANGE%x*}"
TEX_WITDH=uninitialized
for W in $(echo $ALLOWED_WIDTHS); do if [ "$W" -gt "$IMG_WIDTH" ]; then TEX_WITDH="$W"; break; fi; done
if [ "$TEX_WITDH" = uninitialized ]; then log "WARNING - detected image width $IMG_WIDTH larger than max allowed width 1920"; TEX_WITDH=1920; fi
DIFF=$((TEX_WITDH - IMG_WIDTH))
# # extract all values from 394x143+303+61 and assign to variables, e.g. WIDTH=394; HEIGHT=143; X_OFF=303; Y_OFF=61;
# eval $(perl -se 'print "WIDTH=$1; HEIGHT=$2; X_OFF=$3; Y_OFF=$4;\n" if $expr =~ /(\d+)x(\d+)\+(\d+)\+(\d+)/' -- -expr="$CROP_RANGE")
log "CROP_RANGE=$CROP_RANGE; WIDTH=$WIDTH; HEIGHT=$HEIGHT; X_OFF=$X_OFF; Y_OFF=$Y_OFF; TEX_WITDH=$TEX_WITDH; DIFF=$DIFF"

log "+ convert '$LIBOFF_CONVERT_TO_NOTRANS_BMP' -crop $CROP_RANGE -fuzz 2% -transparent '$MAIN_COLOR' $RESIZE_INSTR '${OWM_LIBREOFFICE_BITMAP_OUT}~'"
       convert "$LIBOFF_CONVERT_TO_NOTRANS_BMP" -crop $CROP_RANGE -fuzz 2% -transparent "$MAIN_COLOR" $RESIZE_INSTR "${OWM_LIBREOFFICE_BITMAP_OUT}~"

CROP_RANGE_RALIGNED="${TEX_WITDH}x${HEIGHT}+$((X_OFF-DIFF))+${Y_OFF}"
log "+ convert '$LIBOFF_CONVERT_TO_NOTRANS_BMP' -crop $CROP_RANGE_RALIGNED -fuzz 2% -transparent '$MAIN_COLOR' $RESIZE_INSTR '${OWM_LIBREOFFICE_BITMAP_OUT%.png}-right-aligned.png~'"
        convert "$LIBOFF_CONVERT_TO_NOTRANS_BMP" -crop $CROP_RANGE_RALIGNED -fuzz 2% -transparent "$MAIN_COLOR" $RESIZE_INSTR "${OWM_LIBREOFFICE_BITMAP_OUT%.png}-right-aligned.png~"

CROP_RANGE_LALIGNED="${TEX_WITDH}x${HEIGHT}+${X_OFF}+${Y_OFF}"
log "+ convert '$LIBOFF_CONVERT_TO_NOTRANS_BMP' -crop $CROP_RANGE_LALIGNED -fuzz 2% -transparent '$MAIN_COLOR' $RESIZE_INSTR '${OWM_LIBREOFFICE_BITMAP_OUT%.png}-left-aligned.png~'"
       convert "$LIBOFF_CONVERT_TO_NOTRANS_BMP" -crop $CROP_RANGE_LALIGNED -fuzz 2% -transparent "$MAIN_COLOR" $RESIZE_INSTR "${OWM_LIBREOFFICE_BITMAP_OUT%.png}-left-aligned.png~"

log "+ mv '${OWM_LIBREOFFICE_BITMAP_OUT}~' '${OWM_LIBREOFFICE_BITMAP_OUT}'"
       mv "${OWM_LIBREOFFICE_BITMAP_OUT}~" "${OWM_LIBREOFFICE_BITMAP_OUT}"

log "+ mv '${OWM_LIBREOFFICE_BITMAP_OUT%.png}-right-aligned.png~' '${OWM_LIBREOFFICE_BITMAP_OUT%.png}-right-aligned.png'"
       mv "${OWM_LIBREOFFICE_BITMAP_OUT%.png}-right-aligned.png~" "${OWM_LIBREOFFICE_BITMAP_OUT%.png}-right-aligned.png"

log "+ mv '${OWM_LIBREOFFICE_BITMAP_OUT%.png}-left-aligned.png~' '${OWM_LIBREOFFICE_BITMAP_OUT%.png}-left-aligned.png'"
       mv "${OWM_LIBREOFFICE_BITMAP_OUT%.png}-left-aligned.png~" "${OWM_LIBREOFFICE_BITMAP_OUT%.png}-left-aligned.png"

# From: https://stackoverflow.com/a/44542839
# My Comment: does not work well as floodfill (by definition?) is not catching enclosed background.
# color=$( convert x.png -format "%[pixel:p{0,0}]" info:- )
# convert x.png -alpha off -bordercolor $color -border 1 \
#     \( +clone -fuzz 30% -fill none -floodfill +0+0 $color \
#        -alpha extract -geometry 200% -blur 0x0.5 \
#        -morphology erode square:1 -geometry 50% \) \
#     -compose CopyOpacity -composite -shave 1 weather-out.png

