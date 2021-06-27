job('Spleeter Pipeline' ) {
    
   description('Processing Audiofiles with Spleeter and ffmpeg')

   scm {
            git('https://github.com/si3mshady/spleeter_jenkins_pipeline', 'main')
        }
    
    
    steps {       

        shell('''
        ls -lrth
        pip3  install aws-sam-cli        
        apt update -y
        
        ''')
    }

    
}

