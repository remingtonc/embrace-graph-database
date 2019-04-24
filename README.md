# embrace-graph-database
**Embrace the Graph Database**  
*DevNet Create 2019* | [Presentation](Embrace%20the%20Graph%20Database.pptx)

Learn about graph databases like ArangoDB and the powerful capabilities they provide. Apply them with IoT concepts and create useful visualizations and powerful queries to accomplish what is typically complex or computationally expensive with other domains of databases.

**Note**: This repository should not be taken as best practice example for code development or structure, but as an example PoC.

* [Objectives](#objectives)
* [Prerequisites](#prerequisites)
  * [Install Docker CE](#install-docker-ce)
  * [Get the code!](#get-the-code)
* [Help!](#help)

## Objectives

* Provide a quick introduction to graph algorithms
* Provide a quick introduction to graph databases
* Create a sample environment/application which exposes information to simulated IoT cloud
* Explore sample dashboards in Grafana
* Explore ArangoDB interface
* Create custom graph visualizations
* Express the power of graph database queries

## Prerequisites
In order to complete this lab you will need a development workstation with Docker, and other fundamental tools installed. :)

* [Docker [CE]](https://www.docker.com/community-edition)
  * Community Edition is fully capable.
* [Docker Compose](https://docs.docker.com/compose/install/)
  * Installed by default on MacOS and Windows Docker.
  * Linux requires separate installation of the component.
* Web browser
  * Latest versions of most browsers work.
  * [Firefox](https://www.mozilla.org/en-US/firefox/developer/) or [Chrome](https://www.google.com/chrome/) recommended.

### Install Docker CE

* [Mac OS[X]](https://docs.docker.com/docker-for-mac/install/)
* [Windows](https://docs.docker.com/docker-for-windows/install/)
* [Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/) / [Debian](https://docs.docker.com/install/linux/docker-ce/debian/)
* [CentOS](https://docs.docker.com/install/linux/docker-ce/centos/) / [Fedora](https://docs.docker.com/install/linux/docker-ce/fedora/)

### Get the code!
* If you have `git` installed...  
`git clone https://github.com/remingtonc/embrace-graph-database`
* Otherwise, [download](https://github.com/remingtonc/embrace-graph-database/archive/master.zip) from your web browser or other tool.  
https://github.com/remingtonc/embrace-graph-database/archive/master.zip

You're ready to workshop!

## Usage
This stack should work across any OS that supports the prerequisited Docker CE installation. All processes are containerized and deployable via Docker Compose. If you are running pre-existing Docker containers, ensure that there are no port conflicts in the `docker-compose.yml` file.

Explanation of the components is provided in the [Embrace the Graph Database](Embrace%20the%20Graph%20Database.pptx) PowerPoint.

### Get Started
The following expects you to utilize a terminal of some kind, also known as command prompt in Windows.

```bash
# Get the code!
git clone https://github.com/remingtonc/embrace-graph-database
cd embrace-graph-database
# If you have never run Docker Compose before...
./setup.sh # MacOS or Linux
.\setup.bat # Windows
# Start the stack!
./start.sh # MacOS or Linux
.\start.bat # Windows
# See what's running!
docker-compose ps
# Shut it down when you're done!
./stop.sh # MacOS or Linux
.\stop.bat # Windows
```

### Web Interfaces
The following listings detail ports made available over HTTP to explore the stack.

* ArangoDB
  * http://localhost:8529/
  * Credentials: `root/devnet`
* Python Application
  * http://localhost:8000/
* Grafana
  * http://localhost:3000/
  * Credentials: `admin/admin`

## Help!
If you require any assistance, please open an issue in this repository, or reach out to:
* [Remington Campbell](https://github.com/remingtonc) - [Email](mailto:remcampb@cisco.com)
