from src.Container.build import Build

print(Build(
    processorPlans=1,
    processor="cpu",
    projectName="asdfmrieu", 
    containerOS="ubuntu",
    password="test",
    databaseContainer=["mongo", "mysql"]).database())