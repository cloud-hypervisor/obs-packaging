# Cloud Hypervisor OBS Packaging

This repository contains specifications to package [Cloud Hypervisor](https://github.com/cloud-hypervisor/cloud-hypervisor) and accompanying software for various formats and Linux distributions. The packages built on [Open Build Service](https://build.opensuse.org/project/show/home:cloud-hypervisor) are available through the [package repositories](https://download.opensuse.org/repositories/home:/cloud-hypervisor/).

# Available Packages

| Package | AMD64 | AARCH64 |
| ------- | ----- | ------- |
| cloud-hypervisor | yes | yes |
| edk2-cloud-hypervisor | yes | yes |
| rust-hyperisor-firmware | yes | no |
| kernel-cloud-hypervisor-guest | yes | yes |

# Package Repository Usage
In order to use the pre-built Cloud Hypervisor binaries, the repository for the corresponding distribution needs to be imported on your system.

Installing with `zypper`:
```bash
$ zypper ar https://download.opensuse.org/repositories/home:/cloud-hypervisor/openSUSE_Tumbleweed/home:cloud-hypervisor.repo
$ zypper ref
$ zypper in cloud-hypervisor edk2-cloud-hypervisor
```

Installing with `yum`:
```bash
$ yum install yum-utils
$ yum-config-manager --add-repo https://download.opensuse.org/repositories/home:/cloud-hypervisor/Fedora_36/home:cloud-hypervisor.repo
$ yum-config-manager --enable home_cloud-hypervisor
$ yum install cloud-hypervisor edk2-cloud-hypervisor
```

Installing with `apt`:
```bash
$ echo 'deb http://download.opensuse.org/repositories/home:/cloud-hypervisor/xUbuntu_22.04/ /' | sudo tee /etc/apt/sources.list.d/home:cloud-hypervisor.list
$ curl -fsSL https://download.opensuse.org/repositories/home:cloud-hypervisor/xUbuntu_22.04/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/home_cloud-hypervisor.gpg > /dev/null
$ sudo apt update
$ sudo apt install cloud-hypervisor
``` 

See also instructions for [specific distribution versions](https://software.opensuse.org//download.html?project=home%3Acloud-hypervisor&package=cloud-hypervisor).

