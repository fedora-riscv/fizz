# Some tests fail on 32-bit arches
%ifarch armv7hl i686
%bcond_with tests
%else
%bcond_without tests
%endif

Name:           fizz
Version:        2020.10.26.00
Release:        1%{?dist}
Summary:        A C++14 implementation of the TLS-1.3 standard

License:        BSD
URL:            https://github.com/facebookincubator/fizz
Source0:        https://github.com/facebookincubator/fizz/releases/download/v%{version}/fizz-v%{version}.tar.gz
Patch0:         https://github.com/facebookincubator/fizz/commit/66de2b986f81ee8fc9a8a06661ee78d9f4088094.patch#/fizz-%{version}-maybe_uninitialized.patch
Patch1:         https://github.com/facebookincubator/fizz/commit/22b5d4635f79e614693e55d81dce983da953589c.patch#/fizz-%{version}-fix_fizz_test_support_dest.patch
Patch2:         https://github.com/facebookincubator/fizz/commit/505cbc78dd98f04915220e3d2796bc026f79c066.patch#/fizz-%{version}-allow_overriding_version.patch

# Folly is known not to work on big-endian CPUs
# will file a proper blocking bug once this is imported
ExcludeArch:    s390x

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  folly-devel

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


%prep
%autosetup -c -p1


%build
%cmake fizz \
  -DCMAKE_INSTALL_DIR=%{_libdir}/cmake/%{name} \
  -DPACKAGE_VERSION=%{version} \
  -DSO_VERSION=%{version}
%cmake_build


%install
%cmake_install
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


%changelog
* Mon Oct 26 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.10.26.00-1
- Update to 2020.10.26.00

* Thu Oct 22 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.10.19.00-1
- Initial package
