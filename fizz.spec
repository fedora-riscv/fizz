%if 0%{?fedora} == 36
# Folly is compiled with Clang
%bcond_without toolchain_clang
%else
%bcond_with toolchain_clang
%endif

%if %{with toolchain_clang}
%global toolchain clang
%endif

%if 0%{?el8}
%ifarch ppc64le
# tests often stall after this
# 64/66 Test #60: SlidingBloomReplayCacheTest 
%bcond_with check
%else
# tests don't currently compile with el8's gmock
# error: use of deleted function
%bcond_with check
%endif
%else
%bcond_without check
%endif

Name:           fizz
Version:        2022.03.14.00
Release:        %autorelease
Summary:        A C++14 implementation of the TLS-1.3 standard

License:        BSD
URL:            https://github.com/facebookincubator/fizz
Source0:        %{url}/archive/v%{version}/fizz-%{version}.tar.gz
# Disable failing tests
Patch0:         %{name}-no_failed_tests.patch
Patch1:         %{name}-no_32bit_failed_tests.patch

# Folly is known not to work on big-endian CPUs
# https://bugzilla.redhat.com/show_bug.cgi?id=1892152
ExcludeArch:    s390x
%if 0%{?fedora} == 36
# fmt code breaks: https://bugzilla.redhat.com/show_bug.cgi?id=2061022
ExcludeArch:    ppc64le
%endif

BuildRequires:  cmake
%if %{with toolchain_clang}
BuildRequires:  clang
%else
BuildRequires:  gcc-c++
%endif
BuildRequires:  folly-devel = %{version}
%if %{with check}
BuildRequires:  gmock-devel
BuildRequires:  gtest-devel
%endif

%global _description %{expand:
Fizz is a TLS 1.3 implementation.

Fizz currently supports TLS 1.3 drafts 28, 26 (both wire-compatible with the
final specification), and 23. All major handshake modes are supported, including
PSK resumption, early data, client authentication, and HelloRetryRequest.}

%description %{_description}
Fizz is a TLS 1.3 implementation.

Fizz currently supports TLS 1.3 drafts 28, 26 (both wire-compatible with the
final specification), and 23. All major handshake modes are supported, including
PSK resumption, early data, client authentication, and HelloRetryRequest.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      %{name}-static < 2022.02.28.00-1

%description    devel %{_description}

The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1 -b .no_failed_tests
%ifarch armv7hl i686
%patch1 -p1 -b .no_32bit_failed_tests
%endif


%build
cd fizz
%cmake \
%if %{without tests}
  -DBUILD_TESTS=OFF \
%endif
  -DCMAKE_INSTALL_DIR=%{_libdir}/cmake/%{name} \
  -DFOLLY_ROOT=%{_libdir}/cmake/folly \
  -DPACKAGE_VERSION=%{version} \
  -DSO_VERSION=%{version}
%cmake_build
cd -


%install
cd fizz
%cmake_install
cd -


%if %{with check}
%check
cd fizz
%ctest
cd -
%endif


%files
%license LICENSE
%{_bindir}/fizz
%{_bindir}/fizz-bogoshim
%{_libdir}/*.so.%{version}

%files devel
%doc CODE_OF_CONDUCT.md CONTRIBUTING.md README.md
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/cmake/%{name}


%changelog
%autochangelog
