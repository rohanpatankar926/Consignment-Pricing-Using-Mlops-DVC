# import os
# dirs=[
#     os.path.join("data","raw"),
#     os.path.join("data","processed"),
#     os.path.join("data","transformed_data"),
#     "notebooks",
    
    
#     "saved_models"
#       ]

# for dir in dirs:
#     os.makedirs(dir,exist_ok=True)
    
# files=[
#     "dvc.yaml",
#     "params.yaml",
#     ".gitingnore",   
# ]

# for file_ in files:
#     with open(file_,"w") as write:
#         pass
import os

def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

list_files("H:\consignment pricing using mlops")