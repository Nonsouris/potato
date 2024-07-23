pipeline {
	agent any
	stages {
		stage('Checkout SCM') {
			steps {
                checkout([$class: 'GitSCM', 
						branches: [[name: '*/master']], 
						userRemoteConfigs: [[
							url: 'https://github.com/Nonsouris/potato' 
							]]
						])
			}
		}

		stage('OWASP DependencyCheck') {
			steps {
				dependencyCheck additionalArguments: '--format HTML --format XML --noupdate --nvdApiKey 4314dcc0-a7e3-44eb-a1be-423b66d4f4b1', odcInstallation: 'OWASP Dependency-Check Vulnerabilities'
			}
		}
		stage('Code Quality Check via SonarQube') {
			steps {
			script {
				def scannerHome = tool 'SonarQube';
					withSonarQubeEnv('SonarQube') {
						sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=SSD -Dsonar.sources=."
					}
				}
			}
		}
	}	
	post {
		always {
			recordIssues enabledForFailure: true, tool: sonarQube()
		}
		success {
			dependencyCheckPublisher pattern: 'dependency-check-report.xml'
		}
	}
}