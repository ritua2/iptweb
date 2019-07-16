"""
BASICS

Redirects a user, doing all the necessary actions
Checks that a user is valid after login into wetty
"""


from flask import Flask, redirect, request, send_file
import os
import random
import redis
import requests
import signal
import subprocess




URL_BASE = os.environ["URL_BASE"]
REDIS_AUTH = os.environ["REDIS_AUTH"]
orchestra_key = os.environ["orchestra_key"]
PROJECT = os.environ["PROJECT"]
GREYFISH_URL = URL_BASE
GREYFISH_REDIS_KEY = REDIS_AUTH




# Adds to the list of available containers
def change_container_availability(a1):
    misc = redis.Redis(host=URL_BASE, port=6379, password=REDIS_AUTH, db=4)
    misc.incrby("Available containers", a1)


def l2_contains_l1(l1, l2):
    return[elem for elem in l1 if elem not in l2]


def valid_adm_passwd(apass):
    if apass == orchestra_key:
        return True
    else:
        return False


# Gets the keys in a certain redis database
# rdb (Redis connection object)
def redkeys(rdb):
    return [x.decode("UTF-8") for x in rdb.keys()]


# Checks if a particular key exists in a redis DB
# tested_key (str): Key to be checked
def red_key_check(rdb, tested_key):
    if rdb.get(tested_key) == None:
        return False
    else:
        return True


def available_instances():
    r_occupied = redis.Redis(host=URL_BASE, port=6379, password=REDIS_AUTH, db=0)
    instances_av = []
    for insip in redkeys(r_occupied):
        abav = r_occupied.hget(insip, "Available").decode("UTF-8")
        if abav == "Yes":
            instances_av.append(insip)

    return instances_av



# Finds the list of occupied ports for certain instance, each port is a string
# instance (str)
def ports_occupied(instance):

    r_occupied = redis.Redis(host=URL_BASE, port=6379, password=REDIS_AUTH, db=0)
    redports = int(r_occupied.hget(instance, "Ports").decode("UTF-8"))
    # Shows the ports in binary: 0b100 = 4, and reverses it
    portsn = bin(redports)[2:][::-1]
    pav = []

    for loc, port_used in zip(range(0, len(portsn)), portsn):
        if port_used == "1":
            pav.append(str(7000+loc))

    return pav



# vmip (str): VM IP
def empty_ports(vmip):

    r_occupied = redis.Redis(host=URL_BASE, port=6379, password=REDIS_AUTH, db=0)
    ep = []
    abav = r_occupied.hget(vmip, "Available").decode("UTF-8")
    if abav == "No":
        return ep

    for pn in ports_occupied(vmip):
        ava = r_occupied.hget(vmip, "Available_"+pn).decode("UTF-8")
        if ava == "Yes":
            ep.append(pn)

    return ep



# Gets the long key of a wetty container
# vmip (str): VM IPv4
# port_used (str)
def PK_32(vmip, port_used):
    r_occupied = redis.Redis(host=URL_BASE, port=6379, password=REDIS_AUTH, db=0)
    return r_occupied.hget(vmip, "id_"+port_used).decode("UTF-8")


# Verifies that a port key key is valid
# vmip (str): VM IPv4
# kk (str): key
# port_used (str)
def Valid_PK(vmip, kk, port_used):
    r_occupied = redis.Redis(host=URL_BASE, port=6379, password=REDIS_AUTH, db=0)
    expected_key = r_occupied.hget(vmip, "id_"+port_used).decode("UTF-8")
    if expected_key == kk:
        return True
    else:
        return False



# Checks the port of a 10 character hash
# If the port is not associated with anything, it returns ["NA", 1]
def Porter10(vmip, kk):

    r_occupied = redis.Redis(host=URL_BASE, port=6379, password=REDIS_AUTH, db=0)
    for pn in ports_occupied(vmip):
        expected_key = r_occupied.hget(vmip, "id_"+pn).decode("UTF-8")
        if kk in expected_key:
            return [pn, 0]
    else:
        return ["NA", 1]




# Creates a random string of fixed length
# n (int): length
def random_string(n):

    A = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
        "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    random.shuffle(A)

    return "".join(A)[:n]



# Synchronizes an user local directory and a VM using rsync
# Note: The synchronization is only with the VM, individual containers need to read this data at a later date
# vm_ip (str): VM IP or URL without http:// or ending '/'
def remote_synchronization(vm_ip):

    cron_step = "*/5 * * * * " # Every 5 minutes

    manager_node_to_wetty = "rsync -rvz -e 'ssh -o StrictHostKeyChecking=no -p 4646 -i /conductor/rsync_wetty.key' /greyfish/sandbox/ rsync_user@"+vm_ip+":/home/rsync_user/data"
    wetty_to_manager_node = "rsync -rvz -e 'ssh -o StrictHostKeyChecking=no -p 4646 -i /conductor/rsync_wetty.key' rsync_user@"+vm_ip+":/home/rsync_user/data/ /greyfish/sandbox"

    with open("/var/spool/cron/crontabs/root", "a") as cronfile:
        cronfile.write("\n# VM: "+vm_ip+"\n")
        cronfile.write(cron_step+manager_node_to_wetty+"\n")
        cronfile.write(cron_step+wetty_to_manager_node)




app = Flask(__name__)



####################
# WETTY ACTIONS
####################


# Returns the startup script
@app.route("/api/scripts/startup", methods=['GET'])
def startup_supplier():
    return send_file("/scripts/startup.sh")



# Returns the project name
@app.route("/api/project/name", methods=['GET'])
def project_name():
    return PROJECT



# Returns a string of available docker containers
@app.route("/api/status/containers/available", methods=['GET'])
def AvCon_API():
    misc = redis.Redis(host=URL_BASE, port=6379, password=REDIS_AUTH, db=4)
    return misc.get("Available containers").decode("UTF-8")



@app.route("/api/active", methods=['GET'])
def active():
    return "Orchestration node is active"



# Requests an available container for a user
@app.route("/api/assign/users/<user_id>", methods=['POST'])
def assigner(user_id):

    r_redirect_cache = redis.Redis(host=URL_BASE, port=6379, password=REDIS_AUTH, db=1)

    if not request.is_json:
        return "POST parameters could not be parsed"

    ppr = request.get_json()
    check = l2_contains_l1(ppr.keys(), ["key", "sender"])

    if check:
        return "INVALID: Lacking the following json fields to be read: "+",".join([str(a) for a in check])

    key = ppr["key"]

    if not valid_adm_passwd(key):
        return "INVALID key"

    # Checks all instances with at least one port open
    for instance in available_instances():

        # Adds '_' at the end
        instance_ = instance+"_"

        # Checks only ports not assigned yet
        for emp in empty_ports(instance):
            if red_key_check(r_redirect_cache, instance_+emp):
                # Ignores ports in cache
                continue

            # Sets the instance as occupied, the server now has 20 s to redirect the user
            r_redirect_cache.setex(instance_+emp, 20, user_id)
            return instance+":"+emp

    # All instances are occupied
    else:
        return "False"



# Redirects a user after an available IP has been provided to him
@app.route("/api/redirect/users/<user_id>/<target_ip>", methods=['GET'])
def redirect_to_wetty(user_id, target_ip):

    r_redirect_cache = redis.Redis(host=URL_BASE, port=6379, password=REDIS_AUTH, db=1)

    # Finds if the user is attached to any instance
    available_redirect = [x.decode("UTF-8") for x in r_redirect_cache.keys(target_ip+"_*")]
    for avred in available_redirect:

        expected_user = r_redirect_cache.get(avred)
        if expected_user == None:
            # Avoids race conditions
            continue

        if expected_user.decode("UTF-8") == user_id:
            user_instance = avred
            break
    else:
        return "INVALID: "+target_ip+" has already been assigned to another user"

    # Deletes the copy in Redis
    r_redirect_cache.delete(user_instance)
    # Gets the port number
    user_instance = user_instance.replace("_", ":")
    # 20 s to complete redirect
    r_redirect_cache.setex(user_instance, 20, user_id)

    return redirect("http://"+user_instance+"/wetty", code=302)



# Adds a new container by port and IP
@app.route("/api/instance/attachme", methods=['POST'])
def attachme():

    r_occupied = redis.Redis(host=URL_BASE, port=6379, password=REDIS_AUTH, db=0)

    if not request.is_json:
        return "POST parameters could not be parsed"

    ppr = request.get_json()
    check = l2_contains_l1(ppr.keys(), ["key", "sender", "port"])

    if check:
        return "INVALID: Lacking the following json fields to be read: "+",".join([str(a) for a in check])

    key = ppr["key"]
    # There may be multiple containers per instance
    iport = ppr["port"]
    sender_ID = ppr["sender"]
    reqip = request.environ['REMOTE_ADDR']

    if not valid_adm_passwd(key):
        return "INVALID key"

    instances = redkeys(r_occupied)
    port_number = int(iport)

    # Instance IP has already been added
    if reqip in instances:
        occports = ports_occupied(reqip)
        if not (iport in occports):
            r_occupied.hincrby(reqip, "Ports", 2**((port_number-7000)%10))
            r_occupied.hset(reqip, "Available", "Yes")
            r_occupied.hset(reqip, "Available_"+iport, "Yes")
            r_occupied.hset(reqip, "current_user_"+iport, "Empty")
            r_occupied.hset(reqip, "id_"+iport, sender_ID)
            change_container_availability(1)
            return "Added port "+iport

        else:
            return "Port has already been added"

    else:

        # All IPs are stored in Redis with the following data:
        # Available, id, current_user, whoami_count, address
        new_instance = {
                        "address":reqip,
                        "Available":"Yes",
                        "Ports":str(int(2**((port_number-7000)%10))),

                        # Varies per instance
                        "id_"+iport:sender_ID,
                        "current_user_"+iport:"Empty",
                        "Available_"+iport:"Yes"
        }

        r_occupied.hmset(reqip, new_instance)
        change_container_availability(1)
        remote_synchronization(reqip)
        return "Instance correctly attached"



# Removes the current IP as a wetty instance
@app.route("/api/instance/removeme", methods=['POST'])
def removeme():

    r_occupied = redis.Redis(host=URL_BASE, port=6379, password=REDIS_AUTH, db=0)

    if not request.is_json:
        return "POST parameters could not be parsed"

    ppr = request.get_json()
    check = l2_contains_l1(ppr.keys(), ["key"])

    if check:
        return "INVALID: Lacking the following json fields to be read: "+",".join([str(a) for a in check])

    key = ppr["key"]
    reqip = request.environ['REMOTE_ADDR']

    if not valid_adm_passwd(key):
        return "INVALID key"

    if not (reqip in redkeys(r_occupied)):
        return "INVALID, instance is not associated with the project"

    change_container_availability(-1)
    r_occupied.delete(reqip)
    return "Instance removed"



# Removes a port from an instance
# If the instance has no more ports, it deletes it
# This is an instantaneous action and it does not matter if there is a user already in the instance
@app.route("/api/instance/remove_my_port", methods=['POST'])
def remove_my_port():

    r_occupied = redis.Redis(host=URL_BASE, port=6379, password=REDIS_AUTH, db=0)

    if not request.is_json:
        return "POST parameters could not be parsed"

    ppr = request.get_json()
    check = l2_contains_l1(ppr.keys(), ["key", "sender", "port"])

    if check:
        return "INVALID: Lacking the following json fields to be read: "+",".join([str(a) for a in check])

    key = ppr["key"]
    # There may be multiple containers per instance
    iport = ppr["port"]
    sender_ID = ppr["sender"]
    reqip = request.environ['REMOTE_ADDR']

    if not valid_adm_passwd(key):
        return "INVALID key"

    instances = redkeys(r_occupied)
    port_number = int(iport)
    if not (reqip in redkeys(r_occupied)):
        return "INVALID, instance is not associated with the project"

    # Port must be added
    occports = ports_occupied(reqip)
    if not (iport in occports):
        return "Port is not associated with the instance"

    if (len(occports) == 1) and (Valid_PK(reqip, sender_ID, iport)):
        # If last port, delete the instance from database
        change_container_availability(-1)
        r_occupied.delete(reqip)
        return "Instance removed"

    else:
        # Check for valid key
        if Valid_PK(reqip, sender_ID, iport):
            # Removes all the provided characteristics
            r_occupied.hdel(reqip, "Available_"+iport, "current_user_"+iport, "id_"+iport)
            # Changes the port number
            r_occupied.hincrby(reqip, "Ports", -1*2**((port_number-7000)%10))
            change_container_availability(-1)
            return "Removed port from instance"



# Frees an instance
# Must be called from springIPT
@app.route("/api/instance/free", methods=['POST'])
def free_instance():

    r_occupied = redis.Redis(host=URL_BASE, port=6379, password=REDIS_AUTH, db=0)
    greyfish_server = redis.Redis(host=GREYFISH_URL, port=6379, password=GREYFISH_REDIS_KEY, db=3)
    r_user_to_ = redis.Redis(host=URL_BASE, port=6379, password=REDIS_AUTH, db=4)

    if not request.is_json:
        return "POST parameters could not be parsed"

    ppr = request.get_json()
    check = l2_contains_l1(ppr.keys(), ["key", "IP", "Port"])

    if check:
        return "INVALID: Lacking the following json fields to be read: "+",".join([str(a) for a in check])

    key = ppr["key"]
    reqip = ppr["IP"]
    port = str(ppr["Port"])

    if not valid_adm_passwd(key):
        return "INVALID key"

    if not r_occupied.hexists(reqip, "Available_"+port):
        return "INVALID, port not attached"

    if r_occupied.hget(reqip, "Available_"+port).decode("UTF-8") != "No":
        return "INVALID, wetty instance is empty at the moment"

    current_wetty_user = r_occupied.hget(reqip, "current_user_"+port).decode("UTF-8")
    miniserver_port = str(int(port) + 100)

    # Generates a single-use greyfish token
    new_token = random_string(24)
    greyfish_server.setex(new_token, 60, current_wetty_user)

    wetty_key = PK_32(reqip, port)

    # Issues a call to the wetty miniserver
    # The miniserver will then prepare the instance for a new user
    req = requests.post("http://"+reqip+":"+miniserver_port+"/user/purge", data={"key": wetty_key, "username":current_wetty_user,
                                                                                "greyfish_url":URL_BASE, "gk":new_token})

    # Frees the instance
    r_occupied.hset(reqip, "Available_"+port, "Yes")
    r_occupied.hset(reqip, "current_user_"+port, "Empty")
    # Sets the instance as globaly available
    r_occupied.hset(reqip, "Available", "Yes")
    change_container_availability(1)

    # Removes the user as occupying a VM
    r_user_to_.delete(current_wetty_user)

    return "Correctly freed instance"



# Returns the current user
# Sets up the Redis table with the instance as occupied
@app.route("/api/instance/whoami/<uf10>", methods=['GET'])
def whoami(uf10):


    r_occupied = redis.Redis(host=URL_BASE, port=6379, password=REDIS_AUTH, db=0)
    r_redirect_cache = redis.Redis(host=URL_BASE, port=6379, password=REDIS_AUTH, db=1)

    reqip = request.environ['REMOTE_ADDR']
    user_port, err = Porter10(reqip, uf10)

    if err:
        # If it does not exist, the user is either already there or the VM is not attached
        return "Empty"

    proper_location = reqip+":"+user_port
    expected_user = r_redirect_cache.get(proper_location)

    if expected_user == None:
        return "Empty"

    # Deletes the cache
    r_redirect_cache.delete(proper_location)
    # Sets the port as occupied
    r_occupied.hset(reqip, "Available_"+user_port, "No")
    r_occupied.hset(reqip, "current_user_"+user_port, expected_user.decode("UTF-8"))

    # If all ports are occupied, it sets the available tag as no
    if len(empty_ports(reqip)) == 0:
        r_occupied.hset(reqip, "Available", "No")
    
    # Sets the user as already occupying a container
    r_user_to_ = redis.Redis(host=URL_BASE, port=6379, password=REDIS_AUTH, db=4)
    r_user_to_.hset(expected_user.decode("UTF-8"), "IP:port", proper_location)


    change_container_availability(-1)
    return expected_user.decode("UTF-8")



# Checks if a user is logged in 
# Returns 'False' if not, and the IP:port if yes
@app.route("/api/users/logged_in", methods=['POST'])
def logged_in():

    r_user_to_ = redis.Redis(host=URL_BASE, port=6379, password=REDIS_AUTH, db=4)

    if not request.is_json:
        return "POST parameters could not be parsed"

    ppr = request.get_json()
    check = l2_contains_l1(ppr.keys(), ["key", "username"])

    if check:
        return "INVALID: Lacking the following json fields to be read: "+",".join([str(a) for a in check])

    key = ppr["key"]
    username = ppr["username"]

    if not valid_adm_passwd(key):
        return "INVALID key"


    # Checks all instances with at least one port open
    if r_user_to_.exists(username) == 0:
        return "False"
    else:
        return r_user_to_.hget(username, "IP:port").decode("UTF-8")



# Sets the container assigned to user X as waiting
@app.route("/api/users/container_wait", methods=['POST'])
def container_wait():

    r_user_to_ = redis.Redis(host=URL_BASE, port=6379, password=REDIS_AUTH, db=4)

    if not request.is_json:
        return "POST parameters could not be parsed"

    ppr = request.get_json()
    check = l2_contains_l1(ppr.keys(), ["key", "username"])

    if check:
        return "INVALID: Lacking the following json fields to be read: "+",".join([str(a) for a in check])

    key = ppr["key"]
    username = ppr["username"]

    if not valid_adm_passwd(key):
        return "INVALID key"

    # Finds if the user is logged in
    if r_user_to_.exists(username) == 0:
        return "User is not available at any container"

    user_ip_port_container = r_user_to_.hget(username, "IP:port").decode("UTF-8")
    [ip_used, port_used] = user_ip_port_container.split(":")

    wetty_key = PK_32(ip_used, port_used)

    miniserver_port = str(int(port_used) + 100)

    # Calls the miniserver
    req = requests.post("http://"+ip_used+":"+miniserver_port+"/wait", data={"key": wetty_key, "username":username})
    
    if req.text == "INVALID key":
        return "Could not set wetty terminal as WAIT"

    r_user_to_.hset(username, "WAIT key", req.text)
    return "Set wetty at "+user_ip_port_container+" as WAIT"



# Returns the WAIT key for a user
# Returns false if not
@app.route("/api/users/wetty_wait_key", methods=['POST'])
def wetty_wait_key():

    r_user_to_ = redis.Redis(host=URL_BASE, port=6379, password=REDIS_AUTH, db=4)

    if not request.is_json:
        return "POST parameters could not be parsed"

    ppr = request.get_json()
    check = l2_contains_l1(ppr.keys(), ["key", "username"])

    if check:
        return "INVALID: Lacking the following json fields to be read: "+",".join([str(a) for a in check])

    key = ppr["key"]
    username = ppr["username"]

    if not valid_adm_passwd(key):
        return "INVALID key"

    # Checks all instances with at least one port open
    if r_user_to_.exists(username) == 0:
        return "False"
    else:

        if r_user_to_.hexists(username, "WAIT key"):
            return r_user_to_.hget(username, "WAIT key").decode("UTF-8")
        else:
            return "User is logged in, no waiting containers"





@app.route("/api/instance/whatsmyip", methods=['GET'])
def whatsmyip():
    return request.environ['REMOTE_ADDR']



# Returns the server public key
@app.route("/api/manager_node/public_key", methods=['GET'])
def public_key():

    with open("rsync_wetty.key.pub", "r") as rsync_pub:
        pkey = rsync_pub.readline()

    return pkey




####################
# GREYFISH ACTIONS
####################



# Returns the location of the greyfish server (without 'http://')
@app.route("/api/greyfish/location", methods=['GET'])
def grey_locator():
    return GREYFISH_URL



# Creates a new key for the user located at the present instance
# Simply returns the key
# Cannot be called from outside the instance
@app.route("/api/greyfish/new/single_use_token/<uf10>", methods=['GET'])
def grey_stoken(uf10):

    r_occupied = redis.Redis(host=URL_BASE, port=6379, password=REDIS_AUTH, db=0)
    greyfish_server = redis.Redis(host=GREYFISH_URL, port=6379, password=GREYFISH_REDIS_KEY, db=3)

    reqip = request.environ['REMOTE_ADDR']
    instances = redkeys(r_occupied)

    if not (reqip in redkeys(r_occupied)):
        return "INVALID: instance not attached"

    pnn, err = Porter10(reqip, uf10)
    if err:
        return "INVALID: port not attached"

    curuser = r_occupied.hget(reqip, "current_user_"+pnn).decode("UTF-8")
    if curuser != "Empty":
        # Creates a random string of characters (24 length), sets it as a token, and returns it
        # Each token will last a maximum of 2 hours
        new_token = random_string(24)
        greyfish_server.setex(new_token, 7200, curuser)
        return new_token

    else:
        return "INVALID user"



# Creates a new key for the user 'commonuser', used to store the job information
# Simply returns the key
# Cannot be called from outside the instance
@app.route("/api/greyfish/new/commonuser_token/<uf10>", methods=['GET'])
def grey_commonuser_token(uf10):

    r_occupied = redis.Redis(host=URL_BASE, port=6379, password=REDIS_AUTH, db=0)
    greyfish_server = redis.Redis(host=GREYFISH_URL, port=6379, password=GREYFISH_REDIS_KEY, db=3)

    reqip = request.environ['REMOTE_ADDR']
    instances = redkeys(r_occupied)

    if not (reqip in redkeys(r_occupied)):
        return "INVALID: instance not attached"

    pnn, err = Porter10(reqip, uf10)
    if err:
        return "INVALID: port not attached"

    curuser = r_occupied.hget(reqip, "current_user_"+pnn).decode("UTF-8")
    if curuser != "Empty":
        # Creates a random string of characters (24 length), sets it as a token, and returns it
        # Each token will last a maximum of 2 hours
        new_token = random_string(24)
        greyfish_server.setex(new_token, 7200, "commonuser")
        return new_token

    else:
        return "INVALID user"



# Creates a temporary key for a greyfish user
@app.route("/api/greyfish/users/<user_id>/create_greyfish_key", methods=['POST'])
def tmp_greyfish_key_for_user(user_id):

    greyfish_server = redis.Redis(host=GREYFISH_URL, port=6379, password=GREYFISH_REDIS_KEY, db=3)

    if not request.is_json:
        return "POST parameters could not be parsed"

    ppr = request.get_json()
    check = l2_contains_l1(ppr.keys(), ["key", "user"])

    if check:
        return "INVALID: Lacking the following json fields to be read: "+",".join([str(a) for a in check])

    key = ppr["key"]

    if not valid_adm_passwd(key):
        return "INVALID key"

    # Sets a greyfish key for the user for a maximum of 120 s
    new_token = random_string(24)
    greyfish_server.setex(new_token, 120, user_id)

    return new_token





if __name__ == '__main__':
    app.run()
