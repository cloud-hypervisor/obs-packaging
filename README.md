# cloud-hypervisor-obs

This repository contains specifications to package [Cloud Hypervisor](https://github.com/cloud-hypervisor/cloud-hypervisor) and accompanying software for various formats and Linux distributions. The packages built on [Open Build Service](https://build.opensuse.org/) are available through the [package repositories](https://download.opensuse.org/repositories/home:/weltling:/cloud-hypervisor/).

# Available Packages

| Package | Architecture |
|         | AMD64 | AARCH64 |
| cloud-hypervisor | yes | yes |
| edk2-cloud-hypervisor | yes | yes |
| rust-hyperisor-firmware | yes | no |

# Package Repository Usage
In order to use the pre-built Cloud Hypervisor binaries, the repository for the corresponding distribution needs to be imported on your system. For example, to install on OpenSUSE Tumbleweed, the series of commands below needs to be executed:
```bash
zypper ar https://download.opensuse.org/repositories/home:/weltling:/cloud-hypervisor/openSUSE_Tumbleweed/home:weltling:cloud-hypervisor.repo
zypper ref
zypper in cloud-hypervisor edk2-cloud-hypervisor
```

For an Ubuntu based system, the following commands are to be executed:
```bash
sudo add-apt-repository 'deb https://download.opensuse.org/repositories/home:/weltling:/cloud-hypervisor/xUbuntu_20.04/ ./' 
wget -q https://download.opensuse.org/repositories/home:/weltling:/cloud-hypervisor/xUbuntu_20.04/Release.key -O- | sudo apt-key add - 
sudo apt-get install cloud-hypervisor edk2-cloud-hypervisor
``` 

