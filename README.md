# Clearml Workshops
## Content
| Topic  | Description |
| ------------- | ------------- |
| [Preparing for the workshops](#Preparing-your-machine-for-the-workshops) | One time steps to setup your computer for the workshops   |
| [Workshop agendas](#Workshop-agendas)  | Details on each session |

<h4 id="Preparing-your-machine-for-the-workshops)">
Preparing your machine for the workshops
</h4>

1. Make sure python3 is installed
2. Create a virtual environment with clearml support
```
$ python3 -m venv venv

$ source venv/bin/activate

(venv)$

(venv)$ pip install -U --extra-index-url https://shared:HF6w0RbukY@packages.allegro.ai/repository/allegroai/simple allegroai
ooking in indexes: https://pypi.org/simple, https://shared:****@packages.allegro.ai/repository/allegroai/simple
Collecting allegroai
  Using cached https://packages.allegro.ai/repository/allegroai/packages/allegroai/3.5.6/allegroai-3.5.6-45-py2.py3-none-any.whl (1.6 MB)
...
Collecting certifi>=2017.4.17
  Using cached certifi-2022.6.15-py3-none-any.whl (160 kB)
Building wheels for collected packages: future
  Building wheel for future (setup.py) ... error
Installing collected packages: six, pathlib2, pyparsing, numpy, pyjwt, ply, luqum, humanfriendly, urllib3, attrs, pyrsistent, jsonschema, python-dateutil, orderedmultidict, furl, future, idna, charset-normalizer, certifi, requests, PyYAML, Pillow, psutil, clearml, jmespath, botocore, s3transfer, boto3, allegroai
    Running setup.py install for future ... done
Successfully installed Pillow-9.2.0 PyYAML-6.0 allegroai-3.5.6 attrs-20.3.0 boto3-1.24.29 botocore-1.27.29 certifi-2022.6.15 charset-normalizer-2.1.0 clearml-1.6.2 furl-2.1.3 future-0.18.2 humanfriendly-9.2 idna-3.3 jmespath-1.0.1 jsonschema-3.2.0 luqum-0.11.0 numpy-1.23.1 orderedmultidict-1.0.1 pathlib2-2.3.7.post1 ply-3.11 psutil-5.9.1 pyjwt-2.4.0 pyparsing-2.4.7 pyrsistent-0.18.1 python-dateutil-2.8.2 requests-2.28.1 s3transfer-0.6.0 six-1.16.0 urllib3-1.26.10


(venv)$ allegroai-init
Allegro.AI SDK setup process

Please create new Allegro.AI credentials through the profile page in your Allegro.AI web app
In the profile page, press "Create new credentials", then press "Copy to clipboard".

Paste copied configuration here:
```
3. To get the copied configuration;
    - Browse and log into https://app.clear.ml/ 
    - Navigate to settings/workspace by clicking on the profile icon on top right.
    - Click 'Create new credentials' and copy the entire credentials configuration.
    - Paste the copied credentials back into the command line above as requested.
    - You should see following;
```
api { 
    # Kah Siong Tan's workspace
    web_server: https://app.clear.ml
    api_server: https://api.clear.ml
    files_server: https://files.clear.ml
    credentials {
        "access_key" = "RJJC4*********"
        "secret_key" = "sgmmxo*********************"
    }
}
Detected credentials key="RJJC4F*********" secret="sgmm***"
API Host configured to: [https://api.clear.ml] 
Web Application Host configured to: [https://app.clear.ml] 
File Store Host configured to: [https://files.clear.ml] 
api.clear.ml is the api server, we need the web server. Replacing 'api.' with 'app.'

Allegro.AI Hosts configuration:
Web App: https://app.clear.ml
API: https://api.clear.ml
File Store: https://files.clear.ml

Verifying credentials ...
Credentials verified!

New configuration stored in /home/tkahsion/clearml.conf
Allegro.AI setup completed successfully.
```
4. Test it out. 
- Create a python script with following content and name it `runme.py`.
```
from allegroai import Task
task = Task.init(project_name="ClearML Workshop", task_name="my test test task")
```
- Execute the task
```
(venv)$ python runme.py
ClearML Task: created new task id=12cb8ea42ba34dc09514f285a6946f43
2022-07-14 15:30:48,954 - clearml.Task - INFO - No repository found, storing script code instead
ClearML results page: https://app.clear.ml/projects/bfd5a961df5546a0a419e2c641b7f901/experiments/12cb8ea42ba34dc09514f285a6946f43/output/log
2022-07-14 15:30:57,413 - clearml.Task - INFO - Waiting for repository detection and full package requirement analysis
2022-07-14 15:31:01,612 - clearml.Task - INFO - Finished repository detection and package analysis

```
- You should see a new project and task named as indicated in the script on https://app.clear.ml/
