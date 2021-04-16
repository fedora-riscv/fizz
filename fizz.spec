# link issues on some platforms:
# https://bugzilla.redhat.com/show_bug.cgi?id=1893332
%ifarch i686 x86_64
%bcond_without static
%else
%bcond_with static
%endif

%bcond_without tests

%global _static_builddir static_build

Name:           fizz
Version:        2021.04.12.00
Release:        1%{?dist}
Summary:        A C++14 implementation of the TLS-1.3 standard

License:        BSD
URL:            https://github.com/facebookincubator/fizz
Source0:        %{url}/archive/v%{version}/fizz-%{version}.tar.gz

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
%autosetup -p1


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
* Fri Apr 16 2021 Michel Alexandre Salim <salimma@fedoraproject.org> - 2021.04.12.00-1
- Update to 2021.04.12.00

* Mon Mar 29 2021 Michel Alexandre Salim <michel@michel-slm.name> - 2021.03.29.00-1
- Update to 2021.03.29.00

* Wed Mar 24 2021 Michel Alexandre Salim <michel@michel-slm.name> - 2021.03.22.00-1
- Update to 2021.03.22.00

* Mon Mar 15 2021 Michel Alexandre Salim <salimma@fedoraproject.org> - 2021.03.15.00-1
- Update to 2021.03.15.00

* Wed Feb 03 2021 Michel Alexandre Salim <salimma@fedoraproject.org> - 2021.02.01.00-1
- Update to 2021.02.01.00

* Tue Jan 26 17:49:18 PST 2021 Michel Alexandre Salim <salimma@fedoraproject.org> - 2021.01.25.00-1
- Update to 2021.01.25.00

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2020.12.28.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 29 12:14:58 PST 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.12.28.00-1
- Update to 2020.12.28.00

* Tue Dec 22 16:56:06 PST 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.12.21.00-1
- Update to 2020.12.21.00

* Mon Nov 30 10:42:44 PST 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.11.30.00-1
- Update to 2020.11.30.00

* Mon Nov 23 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.11.23.00-1
- Update to 2020.11.23.00

* Mon Nov 16 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.11.16.00-2
- Fix tests on 32-bit architectures

* Mon Nov 16 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.11.16.00-1
- Update to 2020.11.16.00

* Mon Nov  9 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.11.09.00-1
- Update to 2020.11.09.00

* Mon Nov  2 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.11.02.00-1
- Update to 2020.11.02.00

* Fri Oct 30 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.10.26.00-3
- Only enable static subpackage on x86/x86_64 architectures for now (bz #1893332)

* Thu Oct 29 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.10.26.00-2
- Add static subpackage

* Mon Oct 26 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.10.26.00-1
- Update to 2020.10.26.00

* Thu Oct 22 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.10.19.00-1
- Initial package
