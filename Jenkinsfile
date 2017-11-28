#!groovy

// Use "node {...}" to use any Jenkins server, or "node('master') {...}" to
// only run on the master node.
node('master') {
    // You can hardcode the settings here, or have it dynamically figured out
    // in the build step.
    def djangoSettings = null
    def curDir = pwd()
    def envDir = "${curDir}/../env"

    stage ("Build") {
        def installed = fileExists "${envDir}/bin/activate"

        checkout scm

        // Hard way of determining the Django settings path.
        if (!djangoSettings) {
            djangoSettings = sh(
                script: 'projectFolder=`cd src; ls -d */`; echo "${projectFolder%?}.conf.test"',
                returnStdout: true
            )
        }

        if (!installed) {
            sh "virtualenv ${envDir} --no-site-packages -p python3"
        }
    }

    stage ("Install backend requirements") {
        sh """
            . ${envDir}/bin/activate
            pip install pip --upgrade
            pip install -r requirements/test.txt
            deactivate
          """
    }

    stage ("Install frontend requirements") {
        sh """
            npm install
            gulp sass
           """

        sh """
            . ${envDir}/bin/activate
            python src/manage.py collectstatic \
                --link \
                --noinput \
                --settings=${djangoSettings}
            deactivate
           """
    }

    stage ("Test backend") {
        def testsError = null
        def keepDbOption = ""

        if (!env.CHANGE_TARGET) {
            keepDbOption = "--keepdb"
        }

        try {
            sh """
                . ${envDir}/bin/activate
                python src/manage.py jenkins \
                    --project-apps-tests \
                    --verbosity 2 \
                    --noinput \
                    ${keepDbOption} \
                    --enable-coverage \
                    --pep8-rcfile=pep8.rc \
                    --pylint-rcfile=pylint.rc \
                    --coverage-rcfile=.coveragerc \
                    --settings=${djangoSettings}
                deactivate
               """
        }
        catch(err) {
            testsError = err
            currentBuild.result = "FAILURE"
        }
        finally {
            dir("media") {
                deleteDir()
            }
            junit "reports/junit.xml"

            if (testsError) {
                throw testsError
            }
        }
    }

    stage ("Test frontend") {
        def testsError = null

        // TODO: Should be gulp test, but Sven made a booboo
        try {
            sh "xvfb-run --server-args='-screen 0, 1920x1200x16' gulp build"
        }
        catch(err) {
            testsError = err
            currentBuild.result = "FAILURE"
        }
        finally {
            // Maybe do stuff
            if (testsError) {
                throw testsError
            }
        }
    }

    stage ("Quality") {
        step(
            [
                $class: "CoberturaPublisher",
                coberturaReportFile: "reports/coverage.xml"
            ]
        )
        step(
            [
                $class: "WarningsPublisher",
                parserConfigurations: [
                    [
                        parserName: "PyLint",
                        pattern: "reports/pylint.report",
                        unstableTotalAll: "10",
                        usePreviousBuildAsReference: true,
                    ],
                    [
                        parserName: "Pep8",
                        pattern: "reports/pep8.report",
                        unstableTotalAll: "50",
                        usePreviousBuildAsReference: true,
                    ],
                ]
            ]
        )
    }

// Enable for SonarQube
//  stage("Analysis") {
//    def scannerHome = tool "SonarQube Scanner 2.8";
//    withSonarQubeEnv("Jenkins Scanner") {
//      sh "${scannerHome}/bin/sonar-scanner"
//    }
//  }

//    post {
//        always {
//            cleanWs()
//        }
//        failure {
//            slackSend color: 'danger', message: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})"
//        }
//        success {
//            slackSend color: 'good', message: "SUCCESS: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})"
//        }
//        unstable {
//            slackSend color: 'warning', message: "UNSTABLE: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})"
//        }
//    }

}
