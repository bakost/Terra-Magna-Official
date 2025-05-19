#!/bin/bash
FILE=/root/tmbot/temp.file
cd /root/tmbot/
chmod 777 /root/tmbot/
echo "Start script..."
echo ""
sleep 1
screen -dmS tmbot_temp
runuser -l root -c "screen -S tmbot_temp -X screen /root/tmbot/tmbot_temp.sh"
echo "Script start complete!"
echo ""
while :
do
	while [ -f "$FILE" ];
	do
		runuser -l root -c 'screen -X -S tmbot_temp quit'
		sleep 1
		rm -r /root/tmbot/__pycache__
		rm -r /root/tmbot/temp.file
		echo "Restart script..."
		echo ""
		screen -dmS tmbot_temp
		runuser -l root -c "screen -S tmbot_temp -X screen /root/tmbot/tmbot_temp.sh"
	done	
done