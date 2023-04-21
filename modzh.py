import subprocess, os, time, shutil, colorama, json
import psutil
import config

colorama.init()

def log(log_message):
    print(colorama.Fore.MAGENTA+'[MODZH]: '+colorama.Fore.WHITE+log_message+colorama.Back.RESET)

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

def inject_mods_into(pid):
    psutil_cubzh = psutil.Process(pid)
    psutil_cubzh.suspend()
    injected_scripts = []
    injected_scripts_data = {}
    log(f'Starting to inject..')
    for f in os.listdir(config.mods_directory):
        f_dir = config.mods_directory+f
        mod_file = f_dir+"/mod.json"
        mod_config = json.loads(open(mod_file,'r').read())
        log(f'{colorama.Back.BLUE}Injecting {mod_config["name"]} by {mod_config["author"]}:')
        for script in mod_config["files"]:
            if script in injected_scripts:
                f1 = injected_scripts_data[script]
                f2 = open(f_dir+"/"+script, 'r').read()
                res = script_combine(f1, f2)
                open(config.cubzh_directory+script,'w').write(res)
                injected_scripts_data[script] = res
                log(f' - Combined and injected {script}')
                continue
            shutil.copy(f_dir+"/"+script, config.cubzh_directory)
            injected_scripts.append(script)
            injected_scripts_data[script] = open(f_dir+"/"+script, 'r').read()
            log(f' - Injected {script}')
    log(f'{colorama.Back.GREEN} Successfully injected, unfreezing...')
    psutil_cubzh.resume()

def launch_cubzh():
    log(f'Starting Cubzh..')
    cubzh = subprocess.Popen(config.cubzh_executable)
    time.sleep(1)
    inject_mods_into(cubzh.pid)

launch_cubzh()