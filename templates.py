import os
dirs=[
    os.path.join("data","raw"),
    os.path.join("data","processed"),
    os.path.join("data","transformed_data"),
    "notebooks",
    
    
    "saved_models"
      ]

for dir in dirs:
    os.makedirs(dir,exist_ok=True)
    
files=[
    "dvc.yaml",
    "params.yaml",
    ".gitingnore",   
]

for file_ in files:
    with open(file_,"w") as write:
        pass