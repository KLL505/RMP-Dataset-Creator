from API.RateMyProfApi import RateMyProfApi

RMP = RateMyProfApi()



school = RMP.get_school_by_name("The University of Texas at Dallas")

Prompt = "Is {Prof} a good professor"



school = RMP.get_school_by_name("The University of Texas at Dallas")
Profs = RMP.get_professor_by_school_and_name(school, "Jason Smith") 
print(Profs.name)