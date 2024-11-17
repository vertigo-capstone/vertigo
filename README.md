# vertigo

vertigo test
pull test


On Linux, you can use cron (the scheduler) or systemd to run a Python script at startup.
Method 1: Using cron

The easiest way to run a script at startup in Linux is to use the cron daemon. Specifically, you can use @reboot, which runs the script every time the system reboots.
Steps:

1. Open your terminal and type:

crontab -e

2. In the crontab file, add the following line at the end (replacing /path/to/your/script.py with the full path to your Python script):

    @reboot /usr/bin/python3 /path/to/your/script.py

    Explanation:
        @reboot: Tells cron to run the script at system boot.
        /usr/bin/python3: This is the path to the Python interpreter (you can find it by running which python3).
        /path/to/your/script.py: This is the full path to the Python script you want to run.

    Save and exit the editor (Ctrl + X to exit, then Y to confirm changes).

    The Python script should now run automatically every time your computer restarts.

Method 2: Using systemd (for more control)

For more control over the startup process, you can create a systemd service that starts your script at boot.
Steps:

1. Create a systemd service file, for example: my_script.service. Create it in /etc/systemd/system/.

sudo nano /etc/systemd/system/my_script.service

2. Add the following contents to the file:

[Unit]
Description=Run My Python Script at Startup
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/your/script.py
WorkingDirectory=/path/to/your/
StandardOutput=journal
StandardError=journal
Restart=always

[Install]
WantedBy=multi-user.target

3. Save and close the file (Ctrl + X, then Y).

4. Enable the service to start automatically at boot:

sudo systemctl enable my_script.service

5. You can start the service immediately by running:

sudo systemctl start my_script.service

6. To check the status of your service:

sudo systemctl status my_script.service
