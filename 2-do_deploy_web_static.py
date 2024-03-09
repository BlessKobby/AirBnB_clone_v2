#!/usr/bin/python3
from fabric.api import local, env, put, run
from os.path import exists
from datetime import datetime

env.hosts = ['34.204.81.159', '52.73.255.61']
env.user = 'ubuntu'  # Update with your SSH username
env.key_filename = '~/.ssh/school'  # Update with the path to your SSH private key

def do_pack():
    """ A script that generates archive the contents of web_static folder"""

    filename = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -czvf versions/web_static_{}.tgz web_static/".format(filename))
        filepath = "versions/web_static_{}.tgz".format(filename)
        filesize = os.path.getsize(filepath)
        print("web_static packed: {} -> {} Bytes".format(filepath, filesize))

        return filepath
    except Exception as e:
        return None

def do_deploy(archive_path):
    """Deploy the archive to web servers"""

    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Extract the archive to /data/web_static/releases/<archive filename without extension>
        archive_filename = archive_path.split('/')[-1].split('.')[0]
        run("mkdir -p /data/web_static/releases/{}/".format(archive_filename))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(archive_path.split('/')[-1], archive_filename))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(archive_path.split('/')[-1]))

        # Move files to the proper location
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/"
            .format(archive_filename, archive_filename))

        # Remove unnecessary directory
        run("rm -rf /data/web_static/releases/{}/web_static".format(archive_filename))

        # Delete the symbolic link /data/web_static/current
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(archive_filename))

        print("New version deployed!")

        return True
    except Exception as e:
        return False

