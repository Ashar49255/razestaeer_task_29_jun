**SIMPLE DEPLOYMENT STEPS**

**1. ON YOUR AWS EC2 (Ubuntu)**:
Install everything:
sudo apt update
sudo apt install python3-pip nginx mysql-server -y
Setup MySQL:
sudo mysql
Then run these commands in MySQL:
CREATE DATABASE userdb;
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';
FLUSH PRIVILEGES;
EXIT;
**2. UPLOAD YOUR FILES TO SERVER:**
Put these 3 files in /home/ubuntu/:
•	main.py
•	requirements.txt       fastapi             uvicorn              mysql-connector-python
•	index.html
**3. INSTALL PYTHON PACKAGES:**
cd /home/ubuntu
pip3 install -r requirements.txt
**4. EDIT main.py:**
DB_PASSWORD = ""  # Put your MySQL password here
**5. RUN BACKEND:**
python3 main.py
Backend will run on port 8000.


**6. SETUP NGINX:**
Edit nginx config:
sudo nano /etc/nginx/sites-available/default
Delete everything and paste this:
server {
    listen 80;
    servername _;
    
    location / {
        root /home/ubuntu;
        index index.html;
    }
    
    location /users {
        proxy_pass http://localhost:8000/users;
    }
}
Save and restart:
sudo systemctl restart nginx
**7. EDIT index.html:**
const API = 'http://YOUR_EC2_IP';  // Put your EC2 public IP
**8. DONE!**


**Visit: http://YOUR_EC2_IP**
________________________________________
**LOCAL TESTING (On your computer):
1.	Install MySQL and Python
2.	Create database: CREATE DATABASE userdb;
3.	Edit main.py - add your MySQL password
4.	Run: pip install -r requirements.txt
5.	Run: python main.py
6.	Open index.html in browser
Done!**

