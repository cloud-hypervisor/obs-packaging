# If this flag is set to 1, <arch>-unknown-linux-musl target is required.
%define using_musl_libc 0

Name:           cloud-hypervisor
Summary:        Cloud Hypervisor is a Virtual Machine Monitor (VMM) that runs on top of KVM
Version:        25.0
Release:        1%{?dist}
License:        ASL 2.0 or BSD-3-clause
Group:          Applications/System
Source0:        https://github.com/cloud-hypervisor/cloud-hypervisor/archive/v%{version}.tar.gz
Source1:        vendor.tar.gz
Source2:        config.toml
ExclusiveArch:  x86_64 aarch64

BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  binutils
BuildRequires:  git
BuildRequires:  openssl-devel

BuildRequires:  rust >= 1.60.0
BuildRequires:  cargo >= 1.60.0

Requires: bash
Requires: glibc
Requires: libgcc
Requires: libcap
 
%ifarch x86_64
%define rust_def_target x86_64-unknown-linux-gnu
%if 0%{?using_musl_libc}
%define rust_musl_target x86_64-unknown-linux-musl
%endif
%endif
%ifarch aarch64
%define rust_def_target aarch64-unknown-linux-gnu
%if 0%{?using_musl_libc}
%define rust_musl_target aarch64-unknown-linux-musl
%endif
%endif

%define cargo_offline --offline

%description
Cloud Hypervisor is an open source Virtual Machine Monitor (VMM) that runs on top of KVM. The project focuses on exclusively running modern, cloud workloads, on top of a limited set of hardware architectures and platforms. Cloud workloads refers to those that are usually run by customers inside a cloud provider. For our purposes this means modern Linux* distributions with most I/O handled by paravirtualised devices (i.e. virtio), no requirement for legacy devices and recent CPUs and KVM.

%prep

%setup -q
tar xf %{SOURCE1}
mkdir -p .cargo
cp %{SOURCE2} .cargo/

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_bindir}
install -D -m755  ./target/%{rust_def_target}/release/cloud-hypervisor %{buildroot}%{_bindir}
install -D -m755  ./target/%{rust_def_target}/release/ch-remote %{buildroot}%{_bindir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_libdir}/cloud-hypervisor
install -D -m755 target/%{rust_def_target}/release/vhost_user_block %{buildroot}%{_libdir}/cloud-hypervisor
install -D -m755 target/%{rust_def_target}/release/vhost_user_net %{buildroot}%{_libdir}/cloud-hypervisor

%if 0%{?using_musl_libc}
install -d %{buildroot}%{_libdir}/cloud-hypervisor/static
install -D -m755 target/%{rust_musl_target}/release/cloud-hypervisor %{buildroot}%{_libdir}/cloud-hypervisor/static
install -D -m755 target/%{rust_musl_target}/release/vhost_user_block %{buildroot}%{_libdir}/cloud-hypervisor/static
install -D -m755 target/%{rust_musl_target}/release/vhost_user_net %{buildroot}%{_libdir}/cloud-hypervisor/static
install -D -m755 target/%{rust_musl_target}/release/ch-remote %{buildroot}%{_libdir}/cloud-hypervisor/static
%endif


%build
cargo_version=$(cargo --version)
if [[ $? -ne 0 ]]; then
	echo "Cargo not found, please install cargo. exiting"
	exit 0
fi

export OPENSSL_NO_VENDOR=1
cargo build --release --target=%{rust_def_target} --all %{cargo_offline}
%if 0%{?using_musl_libc}
cargo build --release --target=%{rust_musl_target} --all %{cargo_offline}
%endif

%files
%defattr(-,root,root,-)
%{_bindir}/ch-remote
%caps(cap_net_admin=ep) %{_bindir}/cloud-hypervisor
%dir %{_libdir}/cloud-hypervisor
%{_libdir}/cloud-hypervisor/vhost_user_block
%caps(cap_net_admin=ep) %{_libdir}/cloud-hypervisor/vhost_user_net
%if 0%{?using_musl_libc}
%{_libdir}/cloud-hypervisor/static/ch-remote
%caps(cap_net_admim=ep) %{_libdir}/cloud-hypervisor/static/cloud-hypervisor
%{_libdir}/cloud-hypervisor/static/vhost_user_block
%caps(cap_net_admin=ep) %{_libdir}/cloud-hypervisor/static/vhost_user_net
%endif
%license LICENSE-APACHE
%license LICENSE-BSD-3-Clause


%changelog
*   Sat Jul 16 2022 Anatol Belski <anbelski@linux.microsoft.com> 25.0-1
-   Update to 25.0

*   Sun Jul 03 2022 Anatol Belski <anbelski@linux.microsoft.com> 24.0-2
-   Rework and simplify specs
-   Set version condition for Rust toolchain

*   Wed May 25 2022 Sebastien Boeuf <sebastien.boeuf@intel.com> 24.0-0
-   Update to 24.0

*   Wed May 18 2022 Anatol Belski <anbelski@linux.microsoft.com> - 23.1-0
-   Update to 23.1
-   Add support for aarch64 build
-   Add offline build configuration using vendored crates
-   Fix dependency for openssl-sys

*   Thu Apr 13 2022 Rob Bradford <robert.bradford@intel.com> 23.0-0
-   Update to 23.0

*   Thu Mar 03 2022 Rob Bradford <robert.bradford@intel.com> 22.0-0
-   Update to 22.0

*   Thu Jan 20 2022 Rob Bradford <robert.bradford@intel.com> 21.0-0
-   Update to 21.0

*   Thu Dec 02 2021 Sebastien Boeuf <sebastien.boeuf@intel.com> 20.0-0
-   Update to 20.0

*   Mon Nov 08 2021 Fabiano Fidêncio <fabiano.fidencio@intel.com> 19.0-0
-   Update to 19.0

*   Fri May 28 2021 Muminul Islam <muislam@microsoft.com> 15.0-0
-   Update version to 15.0

*   Wed Jul 22 2020 Muminul Islam <muislam@microsoft.com> 0.8.0-0
-   Initial version
