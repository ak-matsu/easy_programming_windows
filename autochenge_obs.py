import obspython as obs
import time

def switch_scene(sec, scene_name):
    time.sleep(sec)
    obs.obs_frontend_set_current_scene(scene_name)

# start with Scene A
obs.obs_frontend_set_current_scene('Scene A')
# switch to Scene B after 5 seconds
switch_scene(5, 'Scene B')
# switch to Scene C and start streaming after 10 seconds
switch_scene(10, 'Scene C')
obs.obs_frontend_streaming_start()
