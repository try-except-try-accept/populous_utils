from os import getcwd, path, listdir, system, rename
from shutil import copy


source = r"C:\Users\chris\Programming\populous\random_restrictions\final"

def install_random_maps():

    while True:





        # fix textures etc.

        data_folder_path = getcwd() + "/data"
        backup_path = data_folder_path + "_backup"
        cmd = f'Xcopy /E /I "{backup_path}" "{data_folder_path}"'

        print(cmd)
        try:
            system(cmd)
        except Exception as e:
            print(e)
            input()
            


        x = input("What random map to use?")

        source = source + "\\map" + x


        for fn in listdir(source):

            if path.isdir(source+"/"+fn):
                for fn2 in listdir(source+"/"+fn):
                    copy(source+"/"+fn+"/"+fn2, getcwd()+"/"+fn+"/"+fn2)

            else:
                copy(source+"/"+fn, getcwd()+"/levels/"+fn)


        if input("success?") == "no":

            cmd = 'rmdir /Q /S "' + source + '"'
            print(cmd)
            system(cmd)
                
                


for folder in listdir(source):
    for fn in listdir(source+"/"+folder):
        if fn.startswith("levl"):
            rename(source+"/"+folder+"/"+fn, source+"/"+folder+"/"+fn.replace("2001", "2128"))
