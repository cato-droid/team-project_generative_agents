-figure out how to look at the localhost of the ssh server


Task: try to understand the code and figure out where we can interact with agents
-> find the main code of the project, that the authors wrote themselves and inspect it.


all simulations are saved in environment/frontend_server.

-environment/frontend_server/frontend_server/urls.py has the urls,
that we can access in the browser and what functions in view they call.

-environment/frontend_server/translator/views.py
has all the functions that make the viewable simulation

-most of them call "render" at the end
-> function from django shortcuts, that combines a given template with a given context dictionary and returns a HttpResponse object with that rendered text

-update_environment sends the backend computation of the persona behavior to the frontend visual server. It does this by  reading the new movement information from "storage/movement.json" file.

-we find the main backend server of reverie under reverie/backend_server as the function start_server in the class ReverieServer




a persona's current state (memory) is saved (and loaded) into the files: spatial_memory.json, associative_memory, and scratch.json

-scratch.json contains the non-permanent data associated with the persona. It takes json form when saved and moves to python variables, when we load it.




In reverie/backend_server/persona/persona.py there is a function "plan", which conducts both the long term and short term planning for the persona

-> it's acutally a whole module under .../persona/cognitive_modules/plan.py,
separated into: generate and plan.

-in there are also the prompts for the llm

-long term planning (at beginning of day): generate the hourly schedule

-short term planning: _determine_action creates the next action sequence for the persona. As part of this, it may need to decompose the hourly schedule.


-If we want to ask someone to give instructions to an agent: how can we give those instructions to the agent? Where do we add them to their memory/schedule?


'''-> persona.scratch.f_daily_schedule is the daily schedule, an agent works on and that gets edited in plan.py
"# Based on the daily_req, we create an hourly schedule for the persona, 
# which is a list of todo items with a time duration (in minutes) that 
# add up to 24 hours"
-persona.scratch.add_new_action adds a new action to the personas queue
-> too specific, actions get added after beeing broken down, we won't be able to directly insert here'''


Giving instructions to an agent at the beginning of the simulation: try to edit the scratch.json of that persona in the newly created sim-folder
-> in reverie.py when the simulation gets set up, a new sim folder with a copy of the forked simulation gets created.
-In line 183 of scratch.py, the "currently" of the scratch.json gets loaded.
-> we can add stuff to do for the character here.


idea: command line prompts for orders to the personas:
see mindmap



AFTER EXAMS:


-self.name, .age, .innate, .learned, .currently, .lifestyle, and  .daily_plan_req are all strings we can theoretically just add stuff to.

added prompt for every person, so the user can give them tasks.
(inspired by prompts in plan.py)
The prompt and the current status of the person then gets fed to the llm for it to make a new entry for currently.
-> That doesn't totally work at the moment. The output the llm gives, doesn't match the previous style from entries in currently. It's somehow cut off and doesn't always include everything we want (maybe bc it's cut off). Sometimes it's also not only the stuff we asked for/not in 3rd person/ ...
-> see e.g. in tests_04_03_2024 - tests_6_3_24
-also: do we want to replace the currently from before, so the agent is only currently working on the task given by the user?

FIXME

trying to run the simulation on the remote server from haoyu:
-ssh -L gives: channel 3: open failed: connect failed: Connection refused
-> solution: add specific url after runserver that can be accessed from outside:
https://docs.djangoproject.com/en/1.11/ref/django-admin/#runserver
python manage.py runserver 134.2.56.203:8000
-that ip needs to be added to ALLOWED_HOSTS in the Django settings

-problem that still occurs: we can only load the simulator_home once. Refreshing the page after the simulation has started, gives us:
Please start the backend first. 
(which is already running)
-> backend gets somehow stopped by that request (doesn't terminate, but gets "stuck" -> no further computations/prompts)
-> also if we look at the output of the frontend server: a HTTP GET stops the HTTP POSTs:
[06/Mar/2024 16:01:26] "POST /update_environment/ HTTP/1.1" 200 14
[06/Mar/2024 16:01:26] "POST /update_environment/ HTTP/1.1" 200 14
[06/Mar/2024 16:01:26] "POST /update_environment/ HTTP/1.1" 200 14
[06/Mar/2024 16:01:26] "POST /update_environment/ HTTP/1.1" 200 14
[06/Mar/2024 16:01:26] "POST /update_environment/ HTTP/1.1" 200 14
[06/Mar/2024 16:01:26] "POST /update_environment/ HTTP/1.1" 200 14
[06/Mar/2024 16:01:26] "POST /update_environment/ HTTP/1.1" 200 14
[06/Mar/2024 16:01:26] "POST /update_environment/ HTTP/1.1" 200 14
[06/Mar/2024 16:01:26] "POST /update_environment/ HTTP/1.1" 200 14
[06/Mar/2024 16:01:26] "POST /update_environment/ HTTP/1.1" 200 14
[06/Mar/2024 16:01:26] "POST /update_environment/ HTTP/1.1" 200 14
[06/Mar/2024 16:01:26] "POST /update_environment/ HTTP/1.1" 200 14
[06/Mar/2024 16:01:26] "POST /update_environment/ HTTP/1.1" 200 14
[06/Mar/2024 16:01:27] "POST /update_environment/ HTTP/1.1" 200 14
[06/Mar/2024 16:01:27] "POST /update_environment/ HTTP/1.1" 200 14
[06/Mar/2024 16:01:27] "POST /update_environment/ HTTP/1.1" 200 14
[06/Mar/2024 16:01:27] "POST /update_environment/ HTTP/1.1" 200 14
[06/Mar/2024 16:01:27] "POST /update_environment/ HTTP/1.1" 200 14
[06/Mar/2024 16:01:27] "POST /update_environment/ HTTP/1.1" 200 14
[06/Mar/2024 16:01:27] "POST /update_environment/ HTTP/1.1" 200 14
[06/Mar/2024 16:01:27] "POST /update_environment/ HTTP/1.1" 200 14
[06/Mar/2024 16:01:27] "POST /update_environment/ HTTP/1.1" 200 14
[06/Mar/2024 16:01:27] "POST /update_environment/ HTTP/1.1" 200 14
[06/Mar/2024 16:01:27] "GET /simulator_home HTTP/1.1" 200 1374
-> here I refreshed the simulator_home
[06/Mar/2024 16:01:27] "POST /update_environment/ HTTP/1.1" 200 14
[06/Mar/2024 16:01:27] "POST /update_environment/ HTTP/1.1" 200 14
[06/Mar/2024 16:01:27] "POST /update_environment/ HTTP/1.1" 200 14
[06/Mar/2024 16:01:33] "GET /simulator_home HTTP/1.1" 200 1374
[06/Mar/2024 16:01:45] "GET /simulator_home HTTP/1.1" 200 1374
-> refreshing the simulator home again two times
-> no more POSTs

-> fixed by commenting out the line:
os.remove(f_curr_step) from views.py
-> now we can refresh the page, look at agents and go back to the
still viewable simulator_home


-with the updated currently, it got an error when trying to build the emojis for something Isabella is doing
-> stops there
-we haven't yet gotten to the point where the actual simulation started
-> try how far it runs with the old currently by running it overnight

-hundreds of post requests per second are empty?
->are maybe animation frames, but empty currently because animation hasn't started yet




Tasks for later

- split llm from the rest of the code and run it on the ssh server

- try a faster llm that uses CPU instead of GPT4all


