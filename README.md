# Cat Feeder Raspberry Pi W

This project uses a Servo motor to release the food, takes a picture and send it over to my Pushbullet account, it runs on a pre-defined Schedule, also has Manual relese button, the amount of food is adjusted by the opening time

![operating](https://user-images.githubusercontent.com/24723/128587800-42998588-a0e9-42b3-a32b-a37479aa53d4.gif)
<img src="https://user-images.githubusercontent.com/24723/128587874-78ab8928-73b7-4b73-9cdb-705764648c58.jpg" alt="drawing" width="320"/>


The first version had a SG90 Servo Motor which did not performed well with full load, I had to upgrade it to a MG996R with independent power supply.


----------------------------------------------------------------------------------------------------------------

<img src="https://user-images.githubusercontent.com/24723/128587860-e4c27864-7290-4f21-9178-2ce7a89d9cc0.jpg" alt="drawing" width="320" align="left"/>
<img src="https://user-images.githubusercontent.com/24723/128587850-9db1cd02-26af-41cf-a092-f5a051f0179c.gif" alt="drawing" width="320" align="left"/>
<img src="https://user-images.githubusercontent.com/24723/128587868-6d0b0829-2939-4250-b223-4c0307e3e458.jpg" alt="drawing" width="320"/>

----------------------------------------------------------------------------------------------------------------


To start it automatically on boot, I added the following lines to the end of `/home/pi/.bashrc`

```Python
push_bullet_token = "YOUR-PUSHBULLET-TOKEN-HERE"

echo Running at boot
sudo PUSH_BULLET="$push_bullet_token" python /home/pi/Desktop/feeder.py
```
