import boto3, time, uuid

# sts=boto3.client('sts')

# assumed_role_object=sts.assume_role(
#     RoleArn="arn:aws:iam::674406573293:role/EC2-Kratos",
#     RoleSessionName="AssumeRoleSession1"
# )
# creds=assumed_role_object.get('Credentials')
# print(creds.keys())
# print(creds)


class InspectorGadget():
    rule_packages = {
        "CVE": "arn:aws:inspector:us-east-1:316112463485:rulespackage/0-R01qwB5Q",
        "OSSecConfigBenchmarks": "arn:aws:inspector:us-east-1:316112463485:rulespackage/0-rExsr2X8",
        "NetworkReachability": "arn:aws:inspector:us-east-1:316112463485:rulespackage/0-PmNV0Tcd",
        "SecurityBestPractices": "arn:aws:inspector:us-east-1:316112463485:rulespackage/0-R01qwB5Q"
    }

    def __init__(self, targetAssessmentName, rules=rule_packages):
       

        self.inspector = boto3.client('inspector', 
              
        region_name='us-east-1')
        self.rule_arns = list(map(lambda x: x, rules.values()))
        self.targetAssessmentName = targetAssessmentName

        super().__init__()

    def checkForVulns(self):
        '''start sequence to check for vuls on EC2 instances'''
        resource_group_arn = self.create_resource_group()
        assessment_target_arn = self.create_assessment_target(resource_group_arn)
        assessment_template_arn = self.create_assessment_template(assessment_target_arn)
        assessment_run_arn = self.start_assesment_run(assessment_template_arn)
        time.sleep(600)
        self.stop_assessment_run(assessment_run_arn)
        result = self.get_assessment_report(assessment_run_arn)

        if result['status'] == 'FAILED':
            return 'ASSESSMENT FAILED'
        while result['status'] != 'COMPLETED':
            time.sleep(10)
            result = self.get_assessment_report(assessment_run_arn)
        return result['url']

    def create_resource_group(self):
        '''params 'key', 'value' '''
        resp = self.inspector.create_resource_group(
            resourceGroupTags=[
                {
                    'key': str(uuid.uuid4()),
                    'value': 'shady'
                },
            ]
        )

        return resp['resourceGroupArn']

    def create_assessment_target(self, resourceGroupArn: str):
        '''2nd step'''
        resp = self.inspector.create_assessment_target(assessmentTargetName=self.targetAssessmentName,
                                                       resourceGroupArn=resourceGroupArn)
        return resp['assessmentTargetArn']

    def create_assessment_template(self, assessmentTargetArn: str, durationInSeconds=300, assessmentTemplateName="Default_Template_Name"):
        '''3rd step'''
        resp = self.inspector.create_assessment_template(
            assessmentTargetArn=assessmentTargetArn,
            assessmentTemplateName=assessmentTemplateName,
            durationInSeconds=durationInSeconds,
            rulesPackageArns=self.rule_arns)
        return resp['assessmentTemplateArn']

    def start_assesment_run(self, assessmentTemplateArn: str, unique_assesment_name=str(uuid.uuid4())):
        '''4th step'''
        resp = self.inspector.start_assessment_run(assessmentTemplateArn=assessmentTemplateArn,
                                                   assessmentRunName=unique_assesment_name)
        return resp['assessmentRunArn']

    def stop_assessment_run(self, assessmentRunArn: str):
        '''5th step'''
        resp = self.inspector.stop_assessment_run(
            assessmentRunArn=assessmentRunArn,
            stopAction='START_EVALUATION')

    def get_assessment_report(self, assessmentRunArn):
        '''6th step'''
        resp = self.inspector.get_assessment_report(
            assessmentRunArn=assessmentRunArn,
            reportFileFormat='HTML',
            reportType='FULL'
        )

        return resp

if __name__ == "__main__":
    ig = InspectorGadget(str(uuid.uuid4()))
    response  = ig.checkForVulns()
    print(response)


#AWS Inspector Practice - using AWS Inspector to create vuln scans on EC2 instances
#Elliott Arnold 10-19-19
#si3mshady

#modified 6-27-21


#https://docs.aws.amazon.com/inspector/latest/userguide/inspector_rules-arns.html#us-east-1


