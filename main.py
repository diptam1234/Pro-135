import csv
from re import T
from turtle import distance
import plotly.express as pe

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

rows=[]

with open("data.csv","r") as f:
    data = csv.reader(f)

    for row in data:
        rows.append(row)

headers = rows[0]    

planet_data_rows = rows[1:]

# print(headers)
# print(planet_data_rows)

headers[0] = "row_num"

solar_system_planet_count ={}

for planet_data in planet_data_rows:
    
    if solar_system_planet_count.get(planet_data[11]):
        solar_system_planet_count[planet_data[11]] += 1

    else:
        solar_system_planet_count[planet_data[11]] = 1


max_solar_system = max(solar_system_planet_count, key = solar_system_planet_count.get)

print("Solar System That Has The Maximum Number Of The Planets-->",max_solar_system)
print("The Maximum Number Of The Planets-->",solar_system_planet_count[max_solar_system])



temp_planet_data_rows = list(planet_data_rows)

for planet_data in temp_planet_data_rows :
    
    # 1 Jupiter Mass = 317.8 Earth Mass
    # 1 Jupiter Radius = 11.2 Earth Radius

    planet_mass = planet_data[3]

    if planet_mass.lower() == "unknown" :
        planet_data_rows.remove(planet_data)
        continue

    else:
        planet_mass_value = planet_mass.split(" ")[0]  
        planet_mass_ref = planet_mass.split(" ")[1]

        if planet_mass_ref == "Jupiters":
            planet_mass_value = float(planet_mass_value)*317.8

            planet_data[3] = planet_mass_value
            
    planet_radius = planet_data[7]
    if planet_radius.lower() == "unknown" :
        planet_data_rows.remove(planet_data)
        continue
    
    else:
        planet_radius_value = planet_radius.split(" ")[0]
        planet_radius_ref = planet_radius.split(" ")[2]

        if planet_radius_ref == "Jupiters":
            planet_radius_value = float(planet_radius_value)*11.2

            planet_data[7] = planet_radius_value

print(len(planet_data_rows))


hd_10180_planets = []
  
for planet_data in planet_data_rows:
    if max_solar_system == planet_data[11]:
        hd_10180_planets.append(planet_data)


# print(hd_10180_planets)
# print(len(hd_10180_planets))

#------------------- BAR GRAPH ------------------------------

hd_10180_planets_mass =[]
hd_10180_planets_name =[]

for planet_data in hd_10180_planets:
    hd_10180_planets_mass.append(planet_data[3])
    hd_10180_planets_name.append(planet_data[1])


# fig = pe.bar(x=hd_10180_planets_mass , y = hd_10180_planets_name )    

# fig.show()

#------------------------------------------------------------------------------------

# g = (G + mass of Earth) / d2
 
#  G is a gravitational constant, which means that it will always be the same.

# M(earth) is the mass of Earth (or any other planet if we are calculating it for another planet)

# d is the radius of the planet!

# Our Earth’s gravity(g) is 9.8 m/s, and we as humans are accustomed to it

# Mars has a gravity of 3.711 m/s and Moon has a gravity of 1.62 m/s.



temp_planet_data_rows = list(planet_data_rows)

for planet_data in temp_planet_data_rows:
    if planet_data[1].lower() == "hd 100546 b":
        planet_data_rows.remove(planet_data)

planet_masses = []
planet_radiuses = []
planet_names = []

for planet_data in planet_data_rows:
    planet_masses.append(planet_data[3])
    planet_radiuses.append(planet_data[7])
    planet_names.append(planet_data[1])

planet_gravity = []

for index, name in enumerate(planet_names):
    gravity = (float(planet_masses[index])*5.972e+24) / (float(planet_radiuses[index])*float(planet_radiuses[index])*6371000*6371000) * 6.674e-11
    planet_gravity.append(gravity)

# fig = pe.scatter(x=planet_radiuses, y=planet_masses, size=planet_gravity, hover_data=[planet_names])
# fig.show()

# Mass of Earth = 5.972e+24  
# Radius of Earth = 6371000

# The value of G (Gravitational Constant) is 6.674e-11

low_gravity_planets = []
 
for index , gravity in enumerate(planet_gravity):
    if gravity < 10:
        low_gravity_planets.append(planet_data_rows[index])

print(len(low_gravity_planets))

low_gravity_planets = []
for index, gravity in enumerate(planet_gravity):
  if gravity < 100:
    low_gravity_planets.append(planet_data_rows[index])

print(len(low_gravity_planets))

print(headers)
planet_types_values = []
for planet_data in planet_data_rows:
  planet_types_values.append(planet_data[6])
print(list(set(planet_types_values)))

planet_masses =[]
planet_radiuses = []

for planet_data in planet_data_rows:
  planet_masses.append(planet_data[3])
  planet_radiuses.append(planet_data[7])

fig = pe.scatter(x=planet_radiuses,y = planet_masses)
fig.show()

X = []

for index, planet_mass in enumerate(planet_masses):
  temp_list = [
                  planet_radiuses[index],
                  planet_mass
              ]
  X.append(temp_list)


wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state = 42)
    kmeans.fit(X)
    # inertia method returns wcss for that model
    wcss.append(kmeans.inertia_)

plt.figure(figsize=(10,5))
sns.lineplot(range(1, 11), wcss, marker='o', color='red')
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

planet_masses = []
planet_radiuses = []
planet_types = []

for planet_data in low_gravity_planets:
  planet_masses.append(planet_data[3])
  planet_radiuses.append(planet_data[7])
  planet_types.append(planet_data[6])

fig = pe.scatter(x = planet_radiuses,y = planet_masses , color = planet_types )
fig.show()

suitable_planets = []
for planet_data in low_gravity_planets:
  if planet_data[6].lower() == "terrestrial" or planet_data[6].lower() == "super earth":
    suitable_planets.append(planet_data)

print(len(suitable_planets))



# ---------------------------- c 133 --------------------------------------------------------------

# AU is short for Astronomical Unit which is roughly the distance between the Sun and the Earth.

# 1 AU = 1.496e+8

temp_suitable_planets = list(suitable_planets)

for planet_data in temp_suitable_planets:
    if planet_data[8].lower() == "unknown":
        suitable_planets.remove(planet_data)

for planet_data in suitable_planets:
    if planet_data[9].split(" ")[1].lower() == "days":
        planet_data[9] = float(planet_data[9].split(" ")[0])  #removing the word "days"

    else:
        planet_data[9] = float(planet_data[9].split(" ")[0]) * 365

    planet_data[8] = float(planet_data[8].split(" ")[0])

orbital_radiuses = []  
orbital_period = []

for planet_data in suitable_planets:
    orbital_radiuses.append(planet_data[8])
    orbital_period.append(planet_data[9])
    
fig = pe.scatter(x = orbital_radiuses , y = orbital_period)
fig.show()


# If a planet is too close to its sun, we can say that the planet will be too hot for us to survive.

# If a planet is too far away from its sun, we can say that the planet will be too cold for us to survive.

# Goldilock Zone is the habitable zone where the planet is more likely to have just the right conditions to sustain life.

# planet that lies within 0.38 - 2 AU is likely to be habitable
    
# Earth is 1AU from the Sun and Mars is 1.5AU from the Sun.

goldilock_planets = list(suitable_planets)     

temp_goldilock_planets = list(suitable_planets)

for planet_data in temp_goldilock_planets:
    if planet_data[8] < 0.38 or planet_data[8] > 2:
        goldilock_planets.remove(planet_data)

print(len(suitable_planets))
print(len(goldilock_planets))

# Our Earth revolves around the sun at 30km/s. Similarly, our solar system revolves around the center of the Milky Way galaxy at the speed of 200km/s.

planet_speeds = []

for planet_data in suitable_planets:
    distance = 2 * 3.14  * (planet_data[8]*1.496e+9)
    time = planet_data[9] * 86400
    speed = distance/time
    planet_speeds.append(speed)

speed_suporting_planets = list(suitable_planets)

temp_supporting_planets = list(suitable_planets)

for index,planet_data in enumerate(temp_supporting_planets):
    if planet_speeds[index] > 200 :
        speed_suporting_planets.remove(planet_data)
    
print(len(speed_suporting_planets))

# ---------------------------------- class 134 ---------------------------------------

habitable_planets = []

for planet in speed_suporting_planets:
    if planet in goldilock_planets:
        habitable_planets.append(planet)

print(len(habitable_planets))        

# ---------------- gravity fior 4 terrestrial planets --------------------
# Mercury - 3.7 m/s
# Venus - 8.87 m/s
# Earth - 9.8 m/s
# Mars - 3.8 m/s


# --------------- based on AU ------------------
# Mercury - 0.4AU
# Venus - 0.7AU
# Earth - 1AU
# Mars - 1.5AU

# ------------------ based on speed -----------

# Mercury - 47km/s
# Venus - 35km/s
# Earth - 30km/s
# Mars - 24km/s


# Mercury -- Mercury is not habitable since it does not have an atmosphere and its temperature varies from 100 Degree Celsius to 700 Degree Celsius.

# Venus is an extreme planet and it’s
# very hot. It’s atmosphere traps the
# heat on the surface and its
# temperature is a whopping 700
# Degree Celsius. There are also rains
# of sulphuric acid.

# Mars -
# Mars has some atmosphere and it
# also has water on its surface. The
# temperatures are a bit extreme (20
# Degree to -150 degree) but it is still
# manageable compared to others

# ----------------------------------------------------------
final_dict = {}

for index,planet_data in enumerate(planet_data_rows):
    features_list = []
    
    # -------------------- gravity -------------------
    gravity = (float(planet_data[3])*5.972e+24) / (float(planet_data[7])*float(planet_data[7])*6371000*6371000) * 6.674e-11

    try:
        if gravity < 100:
            features_list.append("gravity")
    except: pass

    # ------------------- planet type ------------------
    try:
        if (planet_data[6].lower() == "terrestrial" or
        planet_data[6].lower() == "super earth"):
            
            features_list.append("planet_type")
          
    except: pass   

    # -------------------- goldilock ---------------------

    try:
        if planet_data[8] > 0.38 or planet_data[8] < 2:
            features_list.append("goldilock")


    except: pass      

    # ---------------------- speed ------------------------
    
    try:
        distance = 2 * 3.14  * (planet_data[8]*1.496e+9)
        time = planet_data[9] * 86400
        speed = distance/time

        if speed < 200:
            features_list.append("speed")

    except: pass      

    final_dict[index] = features_list


print(final_dict)

# ---------------------------------- class 135 ------------------------------------

gravity_planet_count = 0
 
for key,value in final_dict.items():
    if "gravity" in value:
        gravity_planet_count = gravity_planet_count+1

print(gravity_planet_count)    

# ---------------------------------------------------------
planet_type_count = 0
 
for key,value in final_dict.items():
    if "planet_type" in value:
        planet_type_count = planet_type_count+1

print(planet_type_count)    

# ---------------------------------------------------------------------

gravity_not_planetType = []

for planet_data in planet_data_rows:
    if planet_data not in low_gravity_planets:
        gravity_not_planetType.append(planet_data)

# ----------------------------------------
planet_type_not_gravity = 0

for planet_data in gravity_not_planetType:
    if planet_data[6].lower() == "terrestrial" or planet_data[6].lower() == "super earth" :
        planet_type_not_gravity = planet_type_not_gravity + 1

print(gravity_not_planetType) 

print(planet_type_count - planet_type_not_gravity)        
  

#-------------------------------------------------------------------    

# ------------------------------ goldilock -----------------
goldilock_planet_count = 0

for key,value in final_dict.items():
    if "goldilock" in value:
        goldilock_planet_count+= 1

print(goldilock_planet_count)

# ------------------------------ speed ----------------------

speed_planet_count = 0

for key,value in final_dict.items():
    if "speed" in value:
        speed_planet_count+= 1

print(speed_planet_count)

# --------------------------------------------------------------------------------------

final_dict = {}

for index, planet_data in enumerate(planet_data_rows):
  features_list = []
  gravity = (float(planet_data[3])*5.972e+24) / (float(planet_data[7])*float(planet_data[7])*6371000*6371000) * 6.674e-11
  try:
    if gravity < 100:
      features_list.append("gravity")
  except: pass
  try:
    if planet_data[6].lower() == "terrestrial" or planet_data[6].lower() == "super earth":
      features_list.append("planet_type")
  except: pass
  try:
    if float(planet_data[8].split(" ")[0]) > 0.38 and float(planet_data[8].split(" ")[0]) < 2:
      features_list.append("goldilock")
  except: 
    try:
      if planet_data[8] > 0.38 and planet_data[8] < 2:
        features_list.append("goldilock")
    except: pass
  try:
    try:
      distance = 2 * 3.14 * (float(planet_data[8].split(" ")[0]) * 1.496e+9)
    except:
      try:
        distance = 2 * 3.14 * (float(planet_data[8]) * 1.496e+9)
      except: pass
    try:
      time, unit = planet_data[9].split(" ")[0], planet_data[9].split(" ")[1]
      if unit.lower() == "days":
        time = float(time)
      else:
        time = float(time) * 365
    except:
      time = planet_data[9]
    time = time * 86400
    speed = distance / time
    if speed < 200:
      features_list.append("speed")
  except: pass
  final_dict[planet_data[1]] = features_list

print(final_dict)

# ---------------------- will find out goldilock planet count based on new final_dict ------------------------------

goldilock_planet_count = 0

for key,value in final_dict.items():
    if "goldilock" in value:
        goldilock_planet_count+= 1

print(goldilock_planet_count)

# -------------------------------------

goldilock_gravity_type_planet_count = 0

for key,value in final_dict.items():
    if "goldilock" in value and "planet_type" in value and "gravity" in value:
        goldilock_gravity_type_planet_count += 1

print(goldilock_gravity_type_planet_count)


# -------------------------------------------------------------------------------------

speed_planet_count = 0

for key,value in final_dict.items():
    if "speed" in value:
        speed_planet_count+= 1

print(speed_planet_count)

# -------------------------------------

speed_goldilock_gravity_type_planet_count = 0

for key,value in final_dict.items():
    if "goldilock" in value and "planet_type" in value and "gravity" in value and "speed" in value:
        speed_goldilock_gravity_type_planet_count += 1

print(speed_goldilock_gravity_type_planet_count)


