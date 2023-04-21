import subprocess, os, time, shutil, colorama, json
import psutil

cubzh_directory = os.getenv('APPDATA')+'\\Voxowl\\Particubes\\bundle\\scripts\\'
cubzh_executable = 'D:/steam/steamapps/common/Cubzh/Cubzh.exe'
mods_directory = 'D:/projects/modzh/mods/'

colorama.init()

def log(log_message):
    print(colorama.Fore.MAGENTA+'[MODZH]: '+colorama.Fore.WHITE+log_message)

def script_combine(f1, f2):
    firstfile_lines = f1.split('\n')
    secondfile_lines = f2.split('\n')

    combined = []
    l1 = 0
    l2 = 0
    while True:
        if l1 > len(firstfile_lines)-1:
            break
        if l2 > len(secondfile_lines)-1:
            break
        if firstfile_lines[l1] == secondfile_lines[l2]:
            combined.append(firstfile_lines[l1])
        if secondfile_lines[l2] != firstfile_lines[l1]:
            combined.append(firstfile_lines[l1])
            combined.append(secondfile_lines[l2])
        l1 += 1
        l2 += 1
    return "\n".join(combined)

def launch_cubzh():
    log(f'Starting Cubzh..')
    cubzh = subprocess.Popen(cubzh_executable)
    time.sleep(1)
    psutil_cubzh = psutil.Process(cubzh.pid)
    psutil_cubzh.suspend()
    injected_scripts = []
    injected_scripts_data = {}
    log(f'Starting to inject..')
    for f in os.listdir(mods_directory):
        mod_file = mods_directory+f+"/mod.json"
        mod_config = json.loads(open(mod_file,'r').read())
        log(colorama.Back.BLUE+f'Injecting {mod_config["name"]} by {mod_config["author"]}:'+colorama.Back.RESET)
        for sc in mod_config["files"]:
            if sc in injected_scripts:
                f1 = injected_scripts_data[sc]
                f2 = open(mods_directory+f+"/"+sc, 'r').read()
                res = script_combine(f1, f2)
                open(cubzh_directory+sc,'w').write(res)
                injected_scripts_data[sc] = res
                log(f' - Combined and injected {sc}')
                continue
            shutil.copy(mods_directory+f+"/"+sc, cubzh_directory)
            injected_scripts.append(sc)
            injected_scripts_data[sc] = open(mods_directory+f+"/"+sc, 'r').read()
            log(f' - Injected {sc}')
    log(colorama.Back.GREEN+f'Successfully injected, unfreezing...'+colorama.Back.RESET)
    psutil_cubzh.resume()

launch_cubzh()