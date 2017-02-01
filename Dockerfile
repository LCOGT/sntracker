################################################################################
#
# Runs the LCOGT Asteroid Day app using nginx + uwsgi
#
# Build with
# docker build -t docker.lco.global/sntracker:dev .
#
# Push to docker registry with
# docker push docker.lco.global/sntracker:dev
#
################################################################################
FROM centos:centos7
MAINTAINER Edward Gomez <egomez@lco.global>

# nginx (http protocol) runs on port 80
EXPOSE 80
ENTRYPOINT [ "/init" ]

# Install package repositories
RUN yum -y install epel-release \
    && yum -y install http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-1.el7.nux.noarch.rpm \
    && yum -y install cronie ffmpeg ImageMagick postgresql-devel nginx python-pip python-psycopg2 supervisor uwsgi-plugin-python \
    && yum -y update \
    && yum -y clean all

# Copy the LCO Supernova Tracker requirements file
COPY app/requirements.pip /var/www/apps/sntracker/requirements.pip
RUN pip install -r /var/www/apps/sntracker/requirements.pip \
        && rm -rf ~/.cache/pip ~/.pip

# Setup the Python Django environment
ENV PYTHONPATH /var/www/apps
ENV DJANGO_SETTINGS_MODULE supernova.settings

# Ensure crond will run on all host operating systems
RUN sed -i -e 's/\(session\s*required\s*pam_loginuid.so\)/#\1/' /etc/pam.d/crond

# Copy configuration files
COPY config/uwsgi.ini /etc/uwsgi.ini
COPY config/nginx/* /etc/nginx/
COPY config/processes.ini /etc/supervisord.d/processes.ini
COPY config/crontab.root /var/spool/cron/root

# Copy configuration files
COPY config/init /init

# Copy the LCO Supernova Tracker files
COPY app /var/www/apps/sntracker
