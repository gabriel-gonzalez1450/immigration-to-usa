import json
data, usa = {}, {}
years, countries = [], []

with open ("../data/ImmigrantsToUS.csv") as f:
	lines = f.readlines()
	years = [str(y.strip()) for y in lines[0].split(",")[1:]] # Initial parsing of years and countries
	for year in years: data[year] = {}
	for line in lines[1:]: countries.append(str(line.split(",")[0].strip()))
	for year in years: # Initial setup of empty JSON structure
		for country in countries:
			data[year][country] = { "emigrants": 0, "population": 0, "gdppc": 0.0, "unemployment": 0.0, "life_expectancy": 0.0 }
			usa[year] = {"gdppc": 0.0, "unemployment": 0.0, "life_expectancy": 0.0}

# Store filename, dictKeyName to iterate over populating all values in one go
data_pairs = [("ImmigrantsToUS", "emigrants"), ("Populations", "population"), ("GDPPerCapitaInUSD", "gdppc"),
			  ("Unemployment", "unemployment"), ("LifeExpectancy", "life_expectancy")]

# Fill in all the data with amazing code that avoids code duplication like a god-dang boss
for (filename, key) in data_pairs:
	with open ("../data/" + filename + ".csv") as f:
		lines = f.readlines()
		if filename == 'LifeExpectancy': lines = lines[0].split("\r")
		for line in lines[1:]:
			elems = [e.strip() for e in line.split(",")]
			country = elems[0]
			for i in range(len(elems[1:])):
				val, year = elems[1:][i], years[i]
				if key in ["unemployment", "life_expectancy", "gdppc"]: val = float(val)
				else: val = int(val)
				data[year][country][key] = val

# Write the data memory object out as a json file
with open('../static/data.json', 'w') as outfile:
	json.dump(data, outfile, indent=4, sort_keys=True)

# Build USA memory object
with open ("../data/UnitedStatesData.csv") as f:
	lines = f.readlines()
	for line in lines[1:]:
		elems = [e.strip() for e in line.split(",")]
		key = elems[0]
		for i in range(len(elems[1:])):
			val, year = float(elems[1:][i]), years[i]
			usa[year][key] = val

# Write the usa memory object out as a json file
with open('../static/usa.json', 'w') as outfile:
	json.dump(usa, outfile, indent=4, sort_keys=True)
