Name:           rust-hypervisor-firmware-bin
Version:        0.4.1
Release:        1%{?dist}
Summary:        A simple firmware that is designed to be launched from anything that supports loading ELF binaries and running them with the PVH booting standard
# FIXME: Select a correct license from https://github.com/openSUSE/spec-cleaner#spdx-licenses
License:        Apache-2.0
URL:            https://github.com/cloud-hypervisor/rust-hypervisor-firmware
Source0:         https://github.com/cloud-hypervisor/rust-hypervisor-firmware/releases/download/%{version}/hypervisor-fw
ExclusiveArch:  x86_64

%description
A simple firmware that is designed to be launched from anything that supports loading ELF binaries and running them with the PVH booting standard.

The purpose is to be able to use this firmware to be able to load a bootloader from within a disk image without requiring the use of a complex firmware such as TianoCore/edk2 and without requiring the VMM to reuse functionality used for booting the Linux kernel.

%prep

%build

%install
D=%{buildroot}%{_datadir}/cloud-hypervisor
install -D -m 644 %{SOURCE0} $D/hypervisor-fw

%files
%defattr(-,root,root,-)
%{_datadir}/cloud-hypervisor/hypervisor-fw
%dir %{_datadir}/cloud-hypervisor

%changelog
* Sun Sep 25 2022 Anatol Belski <anbelski@linux.microsoft.com> - 0.4.1-1
- Initial SPEC 

* Sat Jul 30 2022 Anatol Belski <anbelski@linux.microsoft.com> - 0.4.0-1
- Initial SPEC 
