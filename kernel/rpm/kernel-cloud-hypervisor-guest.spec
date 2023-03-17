
%global gitver 6.2.0
%global gitrev g9a1660e8

Name:           kernel-cloud-hypervisor-guest
Version:        %{gitver}
Release:        1.%{gitrev}%{?dist}
Summary:        Cloud Hypervisor Linux Fork
License:        GPL-2.0-only
Group:          System/Kernel
URL:            https://github.com/cloud-hypervisor/linux
Source0:        ch-%{gitver}-%{gitrev}.tar.gz
%ifarch x86_64
Source1:        https://raw.githubusercontent.com/cloud-hypervisor/cloud-hypervisor/main/resources/linux-config-x86_64
%endif
%ifarch aarch64
Source1:        https://raw.githubusercontent.com/cloud-hypervisor/cloud-hypervisor/main/resources/linux-config-aarch64
%endif
ExclusiveArch:  x86_64 aarch64

BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  bc
BuildRequires:  bison
BuildRequires:  coreutils
BuildRequires:  flex
%if 0%{?centos_version} && 0%{?centos_version} < 900
BuildRequires:  gcc-toolset-11
%else
BuildRequires:  gcc
%endif
%ifarch x86_64
%if 0%{?suse_version}
BuildRequires:  libelf-devel
%else
BuildRequires:  elfutils-libelf-devel
%endif
%endif

%ifarch x86_64
%define image_fname vmlinux.bin
%define image arch/x86/boot/compressed/%{image_fname}
%if 0%{?centos_version} && 0%{?centos_version} < 900
%define kcflags %{nil}
%else
%define kcflags -Wa,-mx86-used-note=no
%endif
%define arch x86_64
%endif
%ifarch aarch64
%define image_fname Image
%define image arch/arm64/boot/%{image_fname}
%define arch arm64
%endif

%description
Cloud Hypervisor Linux Fork with support for the direct kernel boot.

%prep
# This comes from a github export, thus ignore the root directory as the name won't match.
tar xf %{SOURCE0} --strip-components=1
make mrproper
cp %{SOURCE1} .config
make LC_ALL= ARCH=%{arch} oldconfig

%build
%ifarch x86_64
KCFLAGS="%{kcflags}" make ARCH=%{arch} bzImage -j$(nproc)
%endif
%ifarch aarch64
make ARCH=%{arch} -j$(nproc)
%endif

%install
D=%{buildroot}%{_datadir}/cloud-hypervisor
install -D -m 644 %{image} $D/%{image_fname}

%files
%defattr(-,root,root,-)
%{_datadir}/cloud-hypervisor/%{image_fname}
%dir %{_datadir}/cloud-hypervisor

%changelog
* Sat Mar 18 2023 Anatol Belski <anbelski@linux.microsoft.com> - 6.2.0-1.g9a1660e8
Upgrade to ch-6.2

* Sun Feb 05 2023 Anatol Belski <anbelski@linux.microsoft.com> - 6.1.6-1.g689303de
Upgrade to ch-6.1.6

* Sat Jan 21 2023 Anatol Belski <anbelski@linux.microsoft.com> - 5.15.8-1.g7f1768cd
- Initial import CH kernel sources

