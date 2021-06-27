job('Spleeter Pipeline' ) {
    
   description('Processing Audiofiles with Spleeter and ffmpeg')

   scm {
            git('https://github.com/si3mshady/spleeter_jenkins_pipeline', 'main')
        }
    
    
    steps {       

        shell('''
                apt update && apt install git -y && apt install make -y 
                git clone https://github.com/awslabs/git-secrets.git && cd git-secrets/
                make install 
                git secrets --register-aws --global && cd ../
                if [  git secrets --scan ]; then exit; else true; fi                    
        ''')
    }

    
}

