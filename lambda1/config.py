# domain / subdomain
domain = "crowdr.org"
subdomain = "mydeparturevision"

# logging settings
LOG_FILE = 'app.log'
LEVEL = 'DEBUG'
MAX_BYTES = 50*1024
MAX_BACKUP_COUNT = 3

# home many arivals to show
num_arrivals=10

# default font size
font_size = 3

# how long ETA is before display is suppressed
cutoff = 90

# refresh rate in seconds
refresh_rate = 60

# # lookup dict of headsign (fd) and replacement text
# headsign_replacements = {
#     "HOBOKEN": "HOBOKEN",
#     "NEW YORK": "NEW YORK",
#     "HOBOKEN TERMINAL": "HOBOKEN",
#     "HOBOKEN-PATH VIA JOURNAL SQ":"HOBOKEN",
#     "NEWPORT MALL ":"GROVE ST",
#     "NEWPORT MALL  VIA EXCHANGE PLACE":"GROVE ST",
#     "NEWPORT MALL EXCHANGE PL VIA PARK AV":"GROVE ST",
#     "NEWPORT MALL EXCHANGE PL VIA PARK AVE":"GROVE ST"
#     }

# used to rewrite messages for better display
message_replacements = {
    "APPROACHING": "NOW",
    "DELAYED": "DELAY",
    "Less than 1 MIN": "NOW"
}
