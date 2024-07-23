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
		stage('Deploy') {
			agent any
				steps {
					sh "chmod +x -R ${env.WORKSPACE}"
					sh './jenkins/scripts/deploy.sh'
					input message: 'Finished using the web site? (Click "Proceed" to continue)'
					sh './jenkins/scripts/kill.sh'
				}
			}
		stage('Headless Browser Test') {
			agent {
				docker {
					image 'maven:3-alpine' 
					args '-v /root/.m2:/root/.m2' 
				}
			}
			steps {
				sh 'mvn -B -DskipTests clean package'
				sh 'mvn test'
			}
			post {
				always {
					junit 'target/surefire-reports/*.xml'
				}
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