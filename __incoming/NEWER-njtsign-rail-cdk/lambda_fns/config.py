# domain / subdomain
domain = "crowdr.org"
subdomain = "njtsign-rail"

# logging settings
LOG_FILE = 'app.log'
LEVEL = 'DEBUG'
MAX_BYTES = 50*1024
MAX_BACKUP_COUNT = 3

# home many arivals per route to show
num_arrivals_per_route=3

# how long ETA is before display is suppressed
cutoff = 90

# refresh rate in seconds
refresh_rate = 20

# station name lookup
station_names = {
    "HB" : {"station_name" : "HOBOKEN TERMINAL"},
    "NY" : {"station_name" : "NEW YORK PENN"},
    "MB" : {"station_name" : "MILLBURN"},

}

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
