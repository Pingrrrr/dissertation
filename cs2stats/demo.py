from awpy import Demo


#parser = DemoParser(demofile=r"C:\Users\laura\Downloads\9-pandas-fearless-vs-nip-fe-overpass.dem")
#parser = DemoParser(demofile=r"C:\Users\laura\Downloads\9-pandas-fearless-vs-nip-fe-overpass.dem")
#parser = DemoParser(demofile=r"C:\Users\laura\Downloads\natus-vincere-vs-virtus-pro-m1-overpass.dem")
dem = Demo(r"C:\Users\laura\Downloads\natus-vincere-vs-virtus-pro-m1-overpass.dem")


#dem = parser.parse()

# Available properties (all demos)
print(f"Kills: \n{dem.kills.head(n=10)}")
print(f"\nDamages: \n{dem.damages.head(n=3)}")
print(f"\nBomb: \n{dem.bomb.head(n=3)}")
print(f"\nSmokes: \n{dem.smokes.head(n=3)}")
print(f"\nInfernos: \n{dem.infernos.head(n=3)}")
print(f"\nWeapon Fires: \n{dem.weapon_fires.head(n=3)}")
print(f"\nRounds: \n{dem.rounds.head(n=3)}")
print(f"\nGrenades: \n{dem.grenades.head(n=3)}")
print(f"\nTicks: \n{dem.ticks.head(n=3)}")

print(f"\nHeader: \n{dem.header}")