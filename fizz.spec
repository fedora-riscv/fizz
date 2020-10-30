# shared build links against static folly if both are installed on armv7hl
%ifarch armv7hl
%bcond_with static
%else
%bcond_without static
%endif

# Some tests fail on 32-bit arches
%ifarch armv7hl i686
%bcond_with tests
%else
%bcond_without tests
%endif

%global _static_builddir static_build

Name:           fizz
Version:        2020.10.26.00
Release:        2%{?dist}
Summary:        A C++14 implementation of the TLS-1.3 standard

License:        BSD
URL:            https://github.com/facebookincubator/fizz
Source0:        %{url}/releases/download/v%{version}/fizz-v%{version}.tar.gz
Patch0:         %{url}/commit/66de2b986f81ee8fc9a8a06661ee78d9f4088094.patch#/%{name}-%{version}-maybe_uninitialized.patch
Patch1:         %{url}/commit/22b5d4635f79e614693e55d81dce983da953589c.patch#/%{name}-%{version}-fix_fizz_test_support_dest.patch
Patch2:         %{url}/commit/505cbc78dd98f04915220e3d2796bc026f79c066.patch#/%{name}-%{version}-allow_overriding_version.patch

# Folly is known not to work on big-endian CPUs
# https://bugzilla.redhat.com/show_bug.cgi?id=1892152
ExcludeArch:    s390x

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  folly-devel
%if %{with static}
BuildRequires:  folly-static
%endif

%description
Fizz is a TLS 1.3 implementation.

Fizz currently supports TLS 1.3 drafts 28, 26 (both wire-compatible with the
final specification), and 23. All major handshake modes are supported, including
PSK resumption, early data, client authentication, and HelloRetryRequest.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%if %{with static}
%package        static
Summary:        Static development libraries for %{name}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description    static
The %{name}-static package contains static libraries for
developing applications that use %{name}.
%endif


%prep
%autosetup -c -p1


%build
%cmake fizz \
  -DCMAKE_INSTALL_DIR=%{_libdir}/cmake/%{name} \
  -DFOLLY_ROOT=%{_libdir}/cmake/folly \
  -DPACKAGE_VERSION=%{version} \
  -DSO_VERSION=%{version}
%cmake_build


%if %{with static}
# static build
# apply patch to build against static folly
#cat {SOURCE1} | patch -p1
mkdir %{_static_builddir}
cd %{_static_builddir}
%cmake ../fizz \
  -DBUILD_SHARED_LIBS=OFF \
  -DBUILD_TESTS=OFF \
  -DCMAKE_INSTALL_DIR=%{_libdir}/cmake/%{name}-static \
  -DFOLLY_ROOT=%{_libdir}/cmake/folly-static \
  -DPACKAGE_VERSION=%{version}
%cmake_build
%endif


%install
%cmake_install

%if %{with static}
# static build
pushd %{_static_builddir}
%cmake_install
popd
%endif

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%if %{with tests}
%check
%ctest
%endif


%files
%license LICENSE
%{_libdir}/*.so.*

%files devel
%doc CODE_OF_CONDUCT.md CONTRIBUTING.md README.md
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/cmake/%{name}

%if %{with static}
%files static
%{_libdir}/*.a
%{_libdir}/cmake/%{name}-static
%endif


%changelog
* Thu Oct 29 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.10.26.00-2
- Add static subpackage

* Mon Oct 26 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.10.26.00-1
- Update to 2020.10.26.00

* Thu Oct 22 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.10.19.00-1
- Initial package
