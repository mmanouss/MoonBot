# Source: https://eclipse.gsfc.nasa.gov/SEdecade/SEdecade2021.html

def fileToList(fileName: str) -> list:
    """Converts a given file into a list"""
    with open(fileName, "r") as file:
        return file.readlines()

def parseEclipseFile(eclipseList: list) -> list:
    """Parses the eclipse data into a list of dictionaries."""
    eclipse_list = []
    lines = eclipseList
    for line in lines:
        parts = line.split('\t')
        date = parts[0]
        time_of_greatest_eclipse = parts[1]
        eclipse_type = parts[2]
        saros_series = int(parts[3])
        eclipse_magnitude = float(parts[4])
        central_duration = parts[5] if parts[5] != '-' else "N/A"
        geographic_region_parts = parts[6].split('[')
        geographic_region = geographic_region_parts[0].strip()
        
        # Parse the most apparent locations from the part in brackets
        if len(geographic_region_parts) > 1:
            most_apparent_locations = geographic_region_parts[1].split(':')[-1].strip().rstrip(']\n')
            geographic_region = geographic_region+", but most apparent in "+most_apparent_locations
        
        eclipse_info = {
            "date": date,
            "time_of_greatest_eclipse": time_of_greatest_eclipse,
            "eclipse_type": eclipse_type,
            "saros_series": saros_series,
            "eclipse_magnitude": eclipse_magnitude,
            "central_duration": central_duration,
            "geographic_region": geographic_region,
        }
        eclipse_list.append(eclipse_info)
    return eclipse_list

def parseEclipse(next_eclipse: dict) -> str:
    eclipse_magnitude_calculation = f"* The moon's apparent diameter will be **{next_eclipse['eclipse_magnitude']*100:.1f}% of the Sun's apparent diameter**, so "
    eclipse_magnitude_specifics = {"Total": eclipse_magnitude_calculation + "the Sun will be completely covered. ", 
                                "Partial": eclipse_magnitude_calculation + "a portion of the Sun will be visible. ", 
                                "Annular": eclipse_magnitude_calculation + "the outer edge of the Sun will still be visible. "}
    
    eclipse_info = f"solar eclipse will be **{next_eclipse['eclipse_type']} on {next_eclipse['date']} at {next_eclipse['time_of_greatest_eclipse']} UTC**, with a central duration of {next_eclipse['central_duration']}.\n"
    eclipse_info_p2 = f"{eclipse_magnitude_specifics[next_eclipse['eclipse_type']]}\n* It will be visible in {next_eclipse['geographic_region']}."
    
    # Eclipse countdown logic
    import datetime
    eclipse_datetime = datetime.datetime.strptime(next_eclipse["date"] + " " + next_eclipse["time_of_greatest_eclipse"], "%Y %b %d %H:%M:%S")
    time_remaining = eclipse_datetime - datetime.datetime.utcnow()
    days_remaining = time_remaining.days
    hours_remaining, remainder = divmod(time_remaining.seconds, 3600)
    minutes_remaining, seconds_remaining = divmod(remainder, 60)
    countdown = f"**Countdown: {days_remaining} days, {hours_remaining} hours, {minutes_remaining} minutes, and {seconds_remaining} seconds.**"
    
    return [eclipse_info, eclipse_info_p2 + "\n\n" + countdown]

# eclipseData = parseEclipseFile(fileToList("future_eclipses.txt"))
# print(parseEclipse(eclipseData[0]))