sudo dpkg --configure -a
sudo apt update
sudo apt upgrade
# Then choose install maintainer's version on screen
sudo apt install python3-pip


# master
pip install pyspark

# install neo4j on EC2
wget --no-check-certificate -O - https://debian.neo4j.org/neotechnology.gpg.key | sudo apt-key add -
echo 'deb http://debian.neo4j.org/repo stable/' | sudo tee /etc/apt/sources.list.d/neo4j.list
sudo apt update
sudo apt install neo4j
