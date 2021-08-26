from requests import get
from os import listdir, path, getcwd, mkdir
import zipfile
from os import path
from bs4 import BeautifulSoup as Soup
from shutil import copy
from random import randrange, choice, randint
from sys import byteorder

##                    full_bldgs.dat      full_spells.dat     half_spells.dat     no_spells_no_bldgs.dat
##5                   00                  fc                  fc                  00                  
##6                   00                  ff                  07                  00                  
##7                   00                  0b                  00                  00                  
##9                   f2                  00                  00                  00                  
##10                  a1                  00                  00                  00


##                    map02.hdr           spells_on.hdr       
##0                   00                  fc                  
##1                   00                  ff                  
##2                   00                  0b                  
##4                   00                  f2                  
##5                   00                  a1

##                    agreed.dat          all.dat             nothing.dat         
##5                   04                  fc                  00                  
##6                   10                  ff                  00                  
##7                   02                  0b                  00                  
##9                   02                  f2                  00                  
##10                  00                  a1                  00






MAPS_NEEDED = 32
MIN_SIZE = 0
IGNORE = ["final", "dat_bin_test"]

RES_MODS = {0:[0x04, 0xfc],
            1:[0x10, 0xff],
            2:[0x02, 0x0b],
            4:[0x02, 0xf2],
            5:[0x02, 0xa1]}

def download_map_packs():

    url = "https://www.popre.net/mappacks.php"
    download_stem = "https://www.popre.net/"
    pages = Soup(get(url).content, features="html.parser")
    map_pack_links = [download_stem+link['href'] for link in pages.findAll("a") if link['href'].endswith(".zip")]


    for link in map_pack_links:
        name = link.split("/")[-1]

        if path.exists(getcwd()+"/"+name):
            continue

        data = get(link).content
       
        with open(name, "wb") as f:
         
            f.write(data)


        print(f"Finished downloading {link}")

def unzip_map_packs():

    for file in listdir():
    
        if file.endswith(".zip"):
            folder = file.replace(".zip", "")
            if not path.exists(getcwd()+"/"+folder):
                zipfile.ZipFile(file).extractall(getcwd()+"/"+folder)
                print(f"Finished extracting {file}")

def pick_random_maps():

    packs = {}

    for folder in listdir():
        if path.isdir(folder) and folder not in IGNORE:

            this_pack = folder

            packs[this_pack] = {"levels":[], "extra":[]}

            with open(folder+"/mappack.txt") as f:
                pack_data = [line.strip() for line in f.readlines()]

                
                for i, line in enumerate(pack_data):
                    try:
                        next_line = pack_data[i+1]
                    except:
                        next_line = None
                    

                    if line.startswith("DAT"):
                        dat = line.split(":")[1].strip()
                        hdr = next_line.split(":")[1].strip()
                        packs[this_pack]['levels'].append([dat, hdr])

                    elif line.startswith("EXTRASRC"):
                        src = line.split(":")[1].strip()
                        dst = next_line.split(":")[1].strip()
                        packs[this_pack]['extra'].append([src, dst])

    
    count = 21

    while count < MAPS_NEEDED:
        try:
        
            pack_name = choice(list(packs.keys()))
            chosen_pack = packs[pack_name]
            chosen_map = choice(chosen_pack['levels'])
            extra = chosen_pack['extra']


            new_folder = getcwd()+"/final/map"+str(count).zfill(2)
            try:
                mkdir(new_folder)            
            except:
                pass


            copy(getcwd()+"/"+pack_name+"/"+chosen_map[0], new_folder+"/"+"levl2001.dat")
            if chosen_map[1] != "":
                copy(getcwd()+"/"+pack_name+"/"+chosen_map[1], new_folder+"/"+"levl2001.hdr")

            for extra_file in extra:
                src, dst = extra_file

                if src == "" or dst == "":
                    continue
                
                extra_folders = dst.split("\\")[:-1]

                if extra_folders[0] != "levels":
                    
                
                    try:
                        dst_path = ""
                        for folder in extra_folders:
                            dst_path += folder
                            mkdir(new_folder+"/"+dst_path)
                    except:
                        pass
                    extra_folder = "/".join(extra_folders) + "/"
                else:

                    extra_folder = ""

                

                copy(getcwd()+"/"+pack_name+"/"+src, new_folder+"/"+extra_folder+src)
        except:
            print("Problem choosing from", pack_name)
            continue

        print(f"Succeeded in porting level {chosen_map} from {pack_name}")

        count += 1

            
        

def randomise_restrictions(level):
    settings_start_byte = 5

    with open(level, "rb") as f:

        data = f.read()


    header = level.replace(".dat", ".hdr")
    
    if path.exists(header):
        level = header
        settings_start_byte = 0


    random_res_count = 0
    with open(level, "wb") as f:

        for i, b in enumerate(data):
            
            if i >= settings_start_byte:
                if random_res_count in RES_MODS.keys():
                
                    print(b)
                    b = randint(0, RES_MODS[random_res_count][1])
                    print("Changed to", b)


                    print("Remove unused")

                    b = b & RES_MODS[random_res_count][1]


                    

                    b = b | RES_MODS[random_res_count][0]
                    print("Adjusted to accomodate agreed res", b)

                random_res_count += 1

                

            

            
                

            f.write(b.to_bytes(1, byteorder))

def dat_bin_test():

    data = {}
    try:

        for fn in listdir("dat_bin_test"):
            if fn.endswith(".dat"):
                data[fn] = {"file_data":open("dat_bin_test/"+fn, "rb"), "binary":[]}

        
        print((" "*20) + "".join(["{:<20}".format(d) for d in data.keys()]))

        count = 0
        while True:
            
            b = [file["file_data"].read(1) for file in data.values()]

            if any(b[0] != other_b for other_b in b[1:]):
                print("{:<20}".format(count) + "".join(["{:<20}".format(byt.hex()) for byt in b]))

            count += 1

    except:
        pass
    
    for fn in data.keys():
        data[fn]["file_data"].close()
    print("Closed files")

        

#dat_bin_test()
pick_random_maps()
for i in range(21, 32):
    randomise_restrictions(f"final/map{str(i).zfill(2)}/levl2001.dat")
    
