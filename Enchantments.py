applications = {}
awarded = {}

def isDate(token):
    return "2020" in token

def sanitizeZone(zone):
    zone.replace(" (stock)", "")
    if zone == "Stuart Zone":
        zone = "Stuart"

    return zone

f = open("2020_data.csv")
for line in f.readlines()[2:]: # skip header rows
    line = line.split(",")
    if line[0] != "Overnight Permit": # skip the page numbers
        continue

    award = []
    for i in range(len(line)):
        token = line[i]
        if token == "":
            continue

        # Done here
        if token == "Unsuccessful" or token == "Cancelled":
            break

        # Track awarded permits and exit
        if token == "Awarded":
            award_date = line[i+2]
            award_zone = line[i+3]

            award_zone = sanitizeZone(award_zone)

            try:
                award_size = int(line[-1][0])
            except:
                award_size = int(line[-2])

            if award_date not in awarded:
                awarded[award_date] = {}

            if award_zone not in awarded[award_date]:
                awarded[award_date][award_zone] = [0, 0] # groups, people
            
            awarded[award_date][award_zone][0] += 1
            awarded[award_date][award_zone][1] += award_size

            break

        # Track applied permits by date and zone
        if isDate(token):
            date = token
            zone = line[i+1]

            # Sanitize
            zone = sanitizeZone(zone)

            if date not in applications:
                applications[date] = {}
            
            if zone not in applications[date]:
                applications[date][zone] = 0

            applications[date][zone] += 1

all_zones = ["Colchuck Zone", "Core Enchantment Zone", "Eightmile/Caroline Zone", "Snow Zone", "Stuart"]

date = "7/22/2020"
print(date)
for zone in all_zones:
    app_num = applications[date][zone]

    try:
        award_num = awarded[date][zone][0] # number of groups winning the lotto
    except KeyError:
        award_num = 0 # No permits awarded for this zone on this date

    percent = round(100 * int(award_num) / int(app_num), 2)

    print(f"{zone}: {award_num} / {app_num} ({percent}%)")
