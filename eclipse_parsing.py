# Source: https://eclipse.gsfc.nasa.gov/SEdecade/SEdecade2021.html

def parseEclipseData(eclipseList: list) -> list:
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