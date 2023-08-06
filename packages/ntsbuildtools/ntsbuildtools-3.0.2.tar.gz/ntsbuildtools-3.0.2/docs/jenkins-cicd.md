# BuildTools Jenkins CICD Solution

The BuildTools project is deployed using Jenkins.

Jenkins Solutions & Practices
-----------------------------

There is general documentation for how NTS uses Jenkins -- this is especially helpful for folks who are unfamiliar with Jenkins as a 'continous deployment solution.'
You may want to open ["NTS Jenkins Solutions & Practices"](https://confluence.uoregon.edu/x/awxHGQ) confluence page for reference as you read this documentation.

Jenkins Server Configuration
============================

There are several pieces of configuration in Jenkins that are required to support this solution. In particular, there are the following prerequisites for a Jenkins server to run this solution:

1. There needs to be an 'NTS' Jenkins Agent configured with the 'nts' label.
2. Several secrets need to be available (uploaded to 'Jenkins Credentials' store).
3. The actual Jenkins Jobs need to be set up ('Multibranch Pipelines' and 'Pipelines').

NTS Jenkins Agent
-----------------

This is documented in detail [in our internal documentation](https://confluence.uoregon.edu/display/NTS/NTS+Jenkins).

In particular, this project relies on Python being available on the Jenkins Agent.
Additionally, the Agent must be on the appropriate UO subnet so that it won't be blocked by access control lists (ACLs) on the targeted network gear.

Jenkins Credentials
-------------------

There are several secrets that must be uploaded to 'Jenkins Credentials' for this solution to have any chance of working.

|           Credential ID           | Type                          | Where to find the secret value?|
|-----------------------------------|-------------------------------|--------------------------------|
| nts_git_jenkins_rsa               | SSH Username with private key | KeePass -> PKI Keys -> nts_git_jenkins_rsa |
-------


Jenkins Job
------------

**Basic setup details**

| Jenkinsfile | Job Name        | Type                 | 
|-------------|-----------------|----------------------|
| Jenkinsfile | BuildTools-CICD | Multibranch Pipeline |

**Full configuration details**

* Branch Sources
    * Git
        * *Project Repository*: This project 
        * *Credentials*: nts_git_jenkins_rsa
        * *Behaviors*: 
            - Discover Branches
            - Clean before checkout
* Build Configuration
    * by Jenkinsfile
        *  *Script Path*: `Jenkinsfile`
* Orphaned Item Strategy
    * Discard old items
        * *Days to keep old items*: 90
    
### "Parameterized build for Jenkins" plugin configuration

Now that the Jenkins Job is in place, we would like to trigger it based on events from our source control management service, BitBucket (as opposed to polling). 
We need a Jenkins API Token (via a service account) so that BitBucket can interact with Jenkins. 
This is done following the ["Define a server (in a project)" instructions](https://github.com/ParameterizedBuilds/parameterized-builds#define-a-server).

> How to use this "server definition" yourself is discussed in [our internal Confluence documentation on 'Jenkins Practices'](https://confluence.uoregon.edu/pages/viewpage.action?pageId=424086635#NTSJenkinsSolutions&Practices-FromBitbuckettoJenkins)

Additionally, we need to configure the plugin so that it knows when to trigger a build and which Jenkins Jobs should be triggered.
This is done by configuring the "Parameterized Builds for Jenkins" Hook in the `repository settings`.
The required settings are enumerated below -- each has a **Comment** that indicates the purpose of the particular Hook. 

> Before looking at the block of configuration details enumerated below, it is worth understanding one detail of how "Multibranch Pipelines" work: A multibranch pipeline contains a seperate Pipeline-per-branch. 
> So, Multibranch Pipelines must occasionally 'scan' the git repository in order to detect any new branches -- otherwise Jenkins won't actually instantiate a 'Pipeline' for that branch.
> The implication is that we need Bitbucket to trigger a 'scan' whenever a new branch is 'pushed' by a developer/engineer.
> This behavior is actually discussed in the ["Parameterized build for Jenkins" plugin documentation](https://github.com/ParameterizedBuilds/parameterized-builds#multibranch-pipeline-setup).

**Repository Settings -> Hooks -> Parameterized Builds for Jenkins**
* BuildTools-CICD
    * *Job Name*: BuildTools-CICD
    * *Jenkins Server*: IS Jenkins (project)
    * *Multibranch Pipeline*: yes
    * *Triggers*: 
        * REF CREATED
        * MANUAL
        * PR OPENED
        * PR REOPENED
        * PR SOURCE RESCOPED
        * PR MERGED
    * *Build Parameters*: 
      
            BITBUCKET_PROJECT=$PROJECT
            BITBUCKET_REPO=$REPOSITORY
            PR_ID=$PRID
            PR_AUTHOR=$PRAUTHOR
            PR_DESTINATION=$PRDESTINATION
            PR_TITLE=$PRTITLE
            PR_DESCRIPTION=$PRDESCRIPTION
            PR_MERGE_COMMIT=$MERGECOMMIT
      
    * *Required Build Permission*: Write
