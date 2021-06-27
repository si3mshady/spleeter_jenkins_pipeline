job('Spleeter Pipeline' ) {
    
   description('Processing Audiofiles with Spleeter and ffmpeg')

   scm {
            git('https://github.com/si3mshady/spleeter_jenkins_pipeline', 'main')
        }
    
    
    steps {       

        shell('''
                echo "testing for aws credentials in repo!"
                apt update && apt install git -y && apt install make -y 
                rm -rf git-secrets/ || true && echo "1"
                git clone https://github.com/awslabs/git-secrets.git && cd git-secrets/
                make install 
                git secrets --register-aws --global && cd ../
                git secrets --scan
                if [ $? -eq 0 ]; then exit -1; fi           
                 
                  
        ''')

          shell('''
                apt install python3-pip &&  pip3 install awscli  
                for wav in $(ls | grep wav); do  aws s3 cp $wav s3://spleeter-si3mshady; done && \\
                for wav in $(ls | grep wav); do  rm -rf $wav; done                 

        ''')


    }

    
}

