#!/usr/bin/python3.8
import subprocess, sys

def checkFileNameArgExist():
    #audio file can be broken into chunks in order to be processed by spleeter and avoid OOM errors 
    #this fn will only fire when at least when  argv[1]  exists = filename
    # argv[2] is the number of seconds to break up the audio file with ffmpeg  
    try:
        #check if argv[1] is .mp3 if so continue        
        if sys.argv[1].endswith('.mp3'):
            fileName = sys.argv[1]
        try:
            segment_size = sys.argv[2]    
        except IndexError:
            segment_size=90  
        cmd0 = 'rm -rf out*mp3 || true'
        cmd1 = 'rm -rf pretrained_models/ || true '
        cmd2 = 'rm output/ || true'    
        cmd3 = f"bash splitclip.sh {fileName} 90"
        for cmd in [cmd0,cmd1,cmd2,cmd3]:
            try:
              result = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
              (out, err) = result.communicate()
              
              
            except Exception as e:
                print(e)          
        return   
    except IndexError:
        print("Filename argument not present")              
 

def init_spleeter():            
    # sub_cmd = 'sudo docker run  -it  -v $(pwd):/output researchdeezer/spleeter:gpu \
    # separate -p spleeter:2stems -o output -i /output/'
    sub_cmd = 'spleeter separate -p spleeter:2stems -o output'

    cmd = f"for file in $(ls | egrep 'out*.*?mp3' | grep -v yt); do  {sub_cmd} $file; done"

    result = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (out, err) = result.communicate()
    return

def concatenate_files():
    cmd0 = '> beastMode.txt'
    cmd1 = "for path in $(find  output/out* | grep acc); do echo file $path >> beastMode.txt; done"     
    cmd2 = 'ffmpeg -f concat -safe 0 -i  beastMode.txt -c copy beastMode_"`date +"%m_%d_%Y_%M:%S"`".wav'
    cmd3 =  f'{cmd0} && {cmd1} && {cmd2}'
    
    for cmd in [cmd3]:
        result = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (out, err) = result.communicate()
    return
    
     

if __name__ == "__main__":
    if sys.argv[1].endswith('.mp3'):
        checkFileNameArgExist()
    try:
        print('start init spleeter')
        init_spleeter()
        print('end init spleeter')
    except Exception as e:
        print(e)
    try:
        print('start concat files')
        concatenate_files()
        print('end concat files')
    except Exception as e:
        print(e)

    
# sudo docker run  -ti  -v $(pwd):/output researchdeezer/spleeter:gpu separate -p spleeter:2stems -o output -i /output/bigdaddy.mp3
