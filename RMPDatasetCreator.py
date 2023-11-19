from ratemyprof_api.ratemyprof_api import RateMyProfApi as RMP

school  = RMP(1273) 

Prompt = "Is {Prof} a good professor"

Profs = RMP.search_professor("Jason Smith")
print(Profs)