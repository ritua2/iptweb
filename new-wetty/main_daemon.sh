#!/bin/bash


# generates a random UUID for the current terminal, a set of 32 random characters
NEW_UUID=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)

printf "$NEW_UUID" > ./autokey

conductor=
orchestra_key=
# Must include http://----:port (no final / )
SLURM=

# Changes the user profile to update the line
sed -i '2s/.*/export MANAGER_NODE='"\"$conductor\""'/' /user_scripts/.profile

# Adds the first 12 characters of the UUID key to the profile as a check
# However, the full key is still required in order to remove individual ports
UUID_f10="${NEW_UUID:0:12}"
sed -i '3s/.*/export UUID_f10='"\"$UUID_f10\""'/' /user_scripts/.profile
sed -i '4s/.*/export SLURM='"\"$SLURM\""'/' /user_scripts/.profile


# Adds the needed commands to global profile and logout
cat /user_scripts/.profile >> /etc/profile
cat /user_scripts/.bash_logout >> /home/gib/.bash_logout

# Deletes the old and unnecessary scripts
rm /user_scripts/.profile /user_scripts/.bash_logout



# Sets up a listener API to check which port this is
{ echo -ne "HTTP/1.0 200 OK\r\nContent-Length: $(wc -c <./autokey)\r\n\r\n"; cat ./autokey; } | nc -l 3000 &

# Gets the IP of the current device
machine_ip=$(curl "http://$conductor:5000/api/instance/whatsmyip")


# Listens to available ports in the current machine, to check which one has the current API
current_port="NA"
for port in $(seq 7000 7010);
do
    # Stops when it finds itself
    NK=$(curl --max-time 10 "$machine_ip:$port") || true

    if [ "$NK" = "$NEW_UUID" ]; then
        current_port="$port"
        break
    fi
done


# Kill all listener APIs
if [ "$current_port" = "NA" ]; then

    # TODO: Message server about failed instance setup
    printf "Failed wetty setup. Instance could not find itself\n"
    exit
fi


# Calls the server to specify that a new instance is being created
curl -X POST -H "Content-Type: application/json" -d '{"key":"'$orchestra_key'", "sender":"'$NEW_UUID'", "port":"'$current_port'"}' \
    http://$conductor:5000/api/instance/attachme


mv ./autokey /root/autokey

# Kill all listener APIs
pkill nc

yarn start
