import os
import subprocess
import sys

def install_packages():
    # Update package list
    subprocess.run(["pkg", "update", "-y"])

    # Install dependencies
    dependencies = [
        "php",
        "mysql",
        "nginx",
        "git",
        "curl",
        "nodejs",
        "npm",
        "python"
    ]
    subprocess.run(["pkg", "install", "-y"] + dependencies)

def install_php_mysql_nginx():
    # Install and configure MySQL
    subprocess.run(["mysql", "--version"])
    subprocess.run(["mysql_secure_installation"])

    # Install and configure PHP with MySQL support
    subprocess.run(["pkg", "install", "php-mysqli", "php-fpm", "php-cli"])

    # Configure Nginx and PHP
    subprocess.run(["cp", "/data/data/com.termux/files/usr/etc/nginx/nginx.conf", "/data/data/com.termux/files/usr/etc/nginx/nginx.conf.backup"])

    nginx_conf = '''
    user  www-data;
    worker_processes  1;
    pid        /var/run/nginx.pid;
    events {
        worker_connections  1024;
    }
    http {
        include       mime.types;
        default_type  application/octet-stream;
        sendfile        on;
        tcp_nopush     on;
        tcp_nodelay    on;
        keepalive_timeout  65;
        types_hash_max_size 2048;
        server {
            listen       80;
            server_name  localhost;

            location / {
                root   /data/data/com.termux/files/home/your_directory;
                index  index.php index.html index.htm;
            }

            location ~ \.php$ {
                include        fastcgi_params;
                fastcgi_pass   127.0.0.1:9000;
                fastcgi_param  SCRIPT_FILENAME  /data/data/com.termux/files/home/your_directory$fastcgi_script_name;
                include        /data/data/com.termux/files/usr/etc/nginx/fastcgi_params;
            }
        }
    }
    '''

    # Write custom Nginx config
    with open("/data/data/com.termux/files/usr/etc/nginx/nginx.conf", "w") as file:
        file.write(nginx_conf)

    # Restart Nginx to apply changes
    subprocess.run(["nginx", "-s", "reload"])

def setup_react():
    # Install React dependencies
    subprocess.run(["npm", "install", "create-react-app"])

    # Create a simple React app
    subprocess.run(["npx", "create-react-app", "your-react-app"])

    # Change directory to React app folder
    os.chdir("your-react-app")

    # Start React development server
    subprocess.run(["npm", "start"])

def setup_mysql():
    # Start MySQL service
    subprocess.run(["mysqld_safe", "&"])

def main():
    print("Setting up Termux hosting environment...")
    install_packages()
    install_php_mysql_nginx()
    setup_react()
    setup_mysql()

    print("Hosting environment setup complete.")
    print("PHP is available at http://localhost, React app at http://localhost:3000.")

if __name__ == "__main__":
    main()
