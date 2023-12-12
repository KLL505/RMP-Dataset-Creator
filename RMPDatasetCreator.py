from API.RateMyProfApi import RateMyProfApi
import pickle

RMP = RateMyProfApi()

#Loads all prfessor data from university into the Profs list
with open('Professors_1273.pk1', 'rb') as inp:
    Profs = pickle.load(inp)


school = RMP.get_school_by_name("The University of Texas at Dallas")

print(school)

#Prompt = "Is {Prof} a good professor"


