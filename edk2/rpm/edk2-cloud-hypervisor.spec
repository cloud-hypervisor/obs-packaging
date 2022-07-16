Summary:        A UEFI firmware to boot UEFI enabled guest image under Cloud Hypervisor
Name:           edk2-cloud-hypervisor
Version:        20220715
Release:        1%{?dist}
License:        BSD-2
Group:          Development/Tools
URL:            https://github.com/tianocore/edk2
Source0:        edk2-482f50252d-ch.tar.gz
%ifarch aarch64
# REV=03d1c51
# wget https://github.com/tianocore/edk2-platforms/tarball/$REV -O edk2-platforms-$REV.tar.gz
Source1:        edk2-platforms-03d1c51.tar.gz 
%endif
Source2:        edk2-submodule-BaseTools-Source-C-BrotliCompress-brotli.tar.gz
Source3:        edk2-submodule-CryptoPkg-Library-OpensslLib-openssl.tar.gz
Source4:        edk2-submodule-MdeModulePkg-Library-BrotliCustomDecompressLib-brotli.tar.gz
Source5:        edk2-submodule-MdeModulePkg-Universal-RegularExpressionDxe-oniguruma.tar.gz
Source6:        edk2-submodule-RedfishPkg-Library-JsonLib-jansson.tar.gz
Source7:        edk2-submodule-SoftFloat.tar.gz
Source8:        edk2-submodule-UnitTestFrameworkPkg-Library-CmockaLib-cmocka.tar.gz
ExclusiveArch:  aarch64 x86_64
#!BuildIgnore:  gcc-PIE

%if 0%{?suse_version}
BuildRequires:  acpica
%else
BuildRequires:  acpica-tools
%endif
BuildRequires:  gcc gcc-c++ make
%ifarch x86_64
BuildRequires:  nasm 
%endif
Buildrequires:  python3-setuptools
BuildRequires:  libuuid-devel
%ifarch aarch64
BuildRequires:  sed
%endif

%ifarch x86_64
%define edk2_arch X64
%define edk2_dsc OvmfPkg/CloudHv/CloudHvX64.dsc
%define edk2_fd_path edk2/Build/CloudHvX64/RELEASE_GCC5/FV/CLOUDHV.fd
%endif
%ifarch aarch64
%define edk2_arch AARCH64
%define edk2_dsc ArmVirtPkg/ArmVirtCloudHv.dsc
%define edk2_fd_path edk2/Build/ArmVirtCloudHv-AARCH64/RELEASE_GCC5/FV/CLOUDHV_EFI.fd
%endif

%description
In order to boot UEFI enabled guest image this firmware is
needed for Cloud-Hypervisor.

%prep
rm -rf edk2
mkdir edk2
tar xf %{SOURCE0} -C edk2
%ifarch aarch64
rm -rf edk2-platforms
mkdir edk2-platforms
tar xf %{SOURCE1} -C edk2-platforms --strip-components=1
%endif
for i in %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} %{SOURCE8}; do
	tar xf $i -C edk2
done

%build
export PACKAGES_PATH="$PWD/edk2"
%ifarch aarch64
export PACKAGES_PATH="$PACKAGES_PATH:$PWD/edk2-platforms"
%endif

cd edk2
source ./edksetup.sh
cd ..

%ifarch x86_64
make -C edk2/BaseTools
%endif
%ifarch aarch64
make -C edk2/BaseTools EXTRA_OPTFLAGS="-Wno-vla-parameter"
# Don't fail on brotli
sed -ie 's,-Werror,,g' edk2/Conf/tools_def.txt
%endif

build -a %{edk2_arch} -t GCC5 -p %{edk2_dsc} -b RELEASE

%check

%install
D=%{buildroot}%{_datadir}/cloud-hypervisor
install -D -m 644 %{edk2_fd_path} $D/CLOUDHV_EFI.fd

%files
%defattr(-,root,root,-)
%{_datadir}/cloud-hypervisor/*
%license edk2/License-History.txt
%license edk2/License.txt

%changelog
* Sat Jul 16 2022 Anatol Belski <anbelski@linux.microsoft.com> - 20220715-1
- Initial import SPEC version, merge x86_64 and AARCH64 target

