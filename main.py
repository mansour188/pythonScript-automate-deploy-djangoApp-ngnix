
import os
import subprocess
import requests
import time
import platform



#install ngnix server
def install_loadBalancer():
    print("\033[32mInstall Loadbalancer ngnix\033[0m")

    """Install necessary dependencies."""
    # Check the operating system
    os_type = platform.system()

    if os_type == "Linux":
        # Check if it's a Debian-based system (like Ubuntu) or a Red Hat-based system
        debian_based = subprocess.run(["which", "apt-get"], capture_output=True).returncode == 0
        redhat_based = subprocess.run(["which", "yum"], capture_output=True).returncode == 0

        if debian_based:
            subprocess.run(["apt-get", "update"])
            subprocess.run(["apt-get", "install", "-y", "nginx"])
        elif redhat_based:
            subprocess.run(["yum", "install", "-y", "nginx"])
        else:
            print("Unsupported Linux distribution")
    elif os_type == "Darwin":  # macOS
        subprocess.run(["brew", "update"]) 
        subprocess.run(["brew", "install", "nginx"])
    else:
        print("Unsupported operating system")



# Nginx configuration for load balancing applications and configuring health checks for Prometheus.

def configure_load_balancer():
    print("\033[32mConfigure Nginx as a load balancer\033[0m")

    """Configure Nginx as a load balancer."""
    nginx_config = """
events {}

http {

    upstream backend {
        server localhost:8000;
        server localhost:8001;
    }

    server {
        listen 80;
        location / {
            proxy_pass http://backend;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $host;
        }
    }

    server {
        listen 8080;
        # Optionally: allow access only from localhost
        # listen 127.0.0.1:8080;
        server_name _;

        location /status {
            stub_status;
        }

        location /metrics {
            stub_status on;
            access_log off;
            allow 127.0.0.1;
            deny all;
        }
    }
}
    """

    # Determine the Nginx configuration file path based on the operating system
    if platform.system() == "Darwin":
        nginx_conf_path = "/usr/local/etc/nginx/nginx.conf"  # macOS
    elif platform.system() == "Linux":
        nginx_conf_path = "/etc/nginx/nginx.conf"  # Linux
    else:
        print("Unsupported operating system")
        return

    # Write the Nginx configuration to the configuration file
    with open(nginx_conf_path, "w") as f:
        f.write(nginx_config)

    # Restart Nginx to apply the new configuration
    restart_command = ["sudo", "nginx", "-s", "reload"]
    subprocess.run(restart_command)

def find_django_app_dir():
    print("\033[32mfind name of django applcation\033[0m")

    """Find the directory containing wsgi.py."""
    current_dir = os.getcwd()
    for root, dirs, files in os.walk(current_dir):
        if 'wsgi.py' in files:
            return os.path.basename(root)
    return None
def install_python3_venv():
    print("\033[32mInstall python3-venv package if not available\033[0m")
    """Install python3-venv package if not available."""
    os_type = platform.system()
    if os_type == "Linux":
        # Check if python3-venv package is installed
        if subprocess.run(["which", "apt-get"]).returncode == 0:
            # Debian-based (like Ubuntu)
            install_cmd = ["sudo", "apt-get", "install", "-y", "python3-venv"]
            update_cmd = ["sudo", "apt-get", "update"]
        elif subprocess.run(["which", "yum"]).returncode == 0:
            # Red Hat-based (like Fedora, CentOS)
            install_cmd = ["sudo", "yum", "install", "-y", "python3-venv"]
            update_cmd = ["sudo", "yum", "update", "-y"]
        elif subprocess.run(["which", "dnf"]).returncode == 0:
            # Red Hat-based
            install_cmd = ["sudo", "dnf", "install", "-y", "python3-venv"]
            update_cmd = ["sudo", "dnf", "update", "-y"]
        else:
            print("Unsupported Linux distribution")
            return
        subprocess.run(update_cmd)
        subprocess.run(install_cmd)
    elif os_type == "Darwin":  # macOS
        # Check if Homebrew is installed
        if subprocess.run(["which", "brew"]).returncode == 0:
            # Install python3-venv using Homebrew
            subprocess.run(["brew", "install", "python3"])
        else:
            print("Homebrew is not installed. Please install Homebrew to continue.")
            return
    else:
        print("Unsupported operating system")
        return
def create_virtualenv():
    print("\033[32mCreate a virtual environment\033[0m")
    """Create a virtual environment."""
    venv_dir = os.path.join(os.getcwd(), 'venv')
    subprocess.run(['python3', '-m', 'venv', venv_dir])





# install a package manager for Python
def install_pip():
    
    """Install python3-pip package if not available."""
    print("\033[32mInstall python3-pip package if not available\033[0m")
    
    os_type = platform.system()
    if os_type == "Linux":
        # Check if python3-pip package is installed
        if subprocess.run(["which", "pip3"]).returncode != 0:
            # Install python3-pip package
            if subprocess.run(["which", "apt-get"]).returncode == 0:
                # Debian-based (like Ubuntu)
                install_cmd = ["sudo", "apt-get", "install", "-y", "python3-pip"]
            elif subprocess.run(["which", "yum"]).returncode == 0:
                # Red Hat-based (like Fedora, CentOS)
                install_cmd = ["sudo", "yum", "install", "-y", "python3-pip"]
            elif subprocess.run(["which", "dnf"]).returncode == 0:
                # Red Hat-based 
                install_cmd = ["sudo", "dnf", "install", "-y", "python3-pip"]
            else:
                print("Unsupported Linux distribution")
        
                return
            
            subprocess.run(install_cmd)
            print("pip installed ...........")
        else:
            print("python3-pip is already installed.")
    elif os_type == "Darwin":  # macOS
        # Check if Homebrew is installed
        if subprocess.run(["which", "brew"]).returncode == 0:
            
            subprocess.run(["brew", "install", "python3-pip"])
        else:
            print("Homebrew is not installed. Please install Homebrew to continue.")
            return
    else:
        print("Unsupported operating system")
#activate my virtueal envirement 


def activate_virtualenv():
    print("\033[32mActivate the virtual environment\033[0m")
    """Activate the virtual environment."""
    venv_bin_dir = os.path.join(os.getcwd(), 'venv', 'bin')
    activate_script = os.path.join(venv_bin_dir, 'activate')
    activate_cmd = f"source {activate_script}"
    env = os.environ.copy()
    env['PATH'] = f"{venv_bin_dir}:{env['PATH']}"
    subprocess.run(activate_cmd, shell=True, env=env)
def deploy_web_app(port):
    print("\033[32mDeploy  django Application\033[0m")

    """Automatically install Django, collect static files, and run Gunicorn on the specified port."""
    # Create virtual environment for Linux and macOS
    if platform.system() in ['Linux', 'Darwin']:
        install_python3_venv()
        create_virtualenv()
        activate_virtualenv()
        install_pip()

    # Find the directory containing wsgi.py
    django_app_name = find_django_app_dir()
    
    if django_app_name is None:
        print("Error: Django application directory not found.")
        return
    
  
    
    # Install Django and gunicorn server
    subprocess.run(["pip", "install", "django", "gunicorn"])

    
    if not os.path.exists("requirements.txt"):
        print("\033[35mWarning: This project does not have a requirements.txt file.\033[0m")
    else:
        # Install dependencies from requirements.txt
        subprocess.run(["pip", "install", "-r", "requirements.txt"])
    
    subprocess.run(["python3", "manage.py", "makemigrations", "--noinput"])
    subprocess.run(["python3", "manage.py", "migrate", "--noinput"])
    # Collect static files

    subprocess.run(["python3", "manage.py", "collectstatic", "--noinput"])
    
   
    
    # Run Gunicorn on the specified port
    gunicorn_command = ["gunicorn", "--bind", f"localhost:{port}", f"{django_app_name}.wsgi:application"]
    subprocess.Popen(gunicorn_command)


#Verify the application's availability by sending HTTP requests, and if it's not running, redeploy it.
def health_check():
    print("\033[32mCheck the health of web applications securely\033[0m")
    
    """Check the health of web applications securely."""
    while True:
        for port in [8000, 8001]:
            try:
                response = requests.get(f"http://localhost:{port}" , verify=True, timeout=3)

                print(f"This app runs on port {port} and the status code is \033[32m{response.status_code}\033[0m") 
                
                
               
                if response.status_code != 200  :
                    # Web application failed health check, redeploy it
                   deploy_web_app(port)
                   print(f"\033[31mWeb application on port {port} failed health check. Status code: {response.status_code}\033[0m")
            except requests.exceptions.RequestException:
                print(" Web application is down")
                print(f"\033[31mWeb application on port {port} Web application is down\033[0m")
                # Web application is down, redeploy it
                deploy_web_app(port)

        time.sleep(30)

#clone the repo from github
def download_from_github(repo_url):
    print("\033[32mDownload Django application from GitHub\033[0m")
    
    """Download Django application from GitHub."""
    
    subprocess.run(["git", "clone", repo_url])
    repo_name = repo_url.split("/")[-1].replace(".git", "")

    # Change the current working directory to the downloaded repository
    os.chdir(repo_name)

    # Return the path to the downloaded directory
    return os.getcwd()



def download_from_s3(bucket_name, object_key, aws_access_key_id, aws_secret_access_key):
    """Download Django application from AWS S3."""
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    try:
        target_dir = os.getcwd()
        os.makedirs(target_dir, exist_ok=True)
        local_file_path = os.path.join(target_dir, object_key.split('/')[-1])
        s3.download_file(bucket_name, object_key, local_file_path)
        # Extract if it's a compressed file, adjust this based on your object_key pattern
        if local_file_path.endswith('.zip'):
            shutil.unpack_archive(local_file_path, target_dir)
            os.remove(local_file_path)
    except ClientError as e:
        print("Error downloading from S3:", e)
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    try:
        os.makedirs(target_dir, exist_ok=True)
        local_file_path = os.path.join(target_dir, object_key.split('/')[-1])
        s3.download_file(bucket_name, object_key, local_file_path)
        # Extract if it's a compressed file, adjust this based on your object_key pattern
        if local_file_path.endswith('.zip'):
            shutil.unpack_archive(local_file_path, target_dir)
            os.remove(local_file_path)
    except ClientError as e:
        print("Error downloading from S3:", e)







##########################################################################################

def main():
    source = input("Choose download source (github/s3): ").lower()
    
    if source == 'github':
        repo_url = input("Enter GitHub repository URL: ")
        downloaded_dir =download_from_github(repo_url)
    elif source == 's3':
        bucket_name = input("Enter S3 bucket name: ")
        object_key = input("Enter S3 object key (path to the zip file): ")
        aws_access_key_id = input("Enter AWS access key ID: ")
        aws_secret_access_key = input("Enter AWS secret access key: ")
        download_from_s3(bucket_name, object_key, aws_access_key_id, aws_secret_access_key)
    else:
        print("Invalid source selection.")
        return
    os.chdir(downloaded_dir)
    
    deploy_web_app(8000)
    deploy_web_app(8001)
    install_loadBalancer()
    configure_load_balancer()
    time.sleep(30)
    health_check()

    
   

if __name__ == "__main__":
    main()










   