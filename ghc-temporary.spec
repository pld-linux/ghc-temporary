#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	temporary
Summary:	Portable temporary file and directory support for Windows and Unix
Summary(pl.UTF-8):	Przenośna obsługa plików i katalogów tymczasowych dla Windows i Uniksa
Name:		ghc-%{pkgname}
Version:	1.3
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/temporary
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	3f2d619133f19080886b8aa81da7f419
URL:		http://hackage.haskell.org/package/temporary
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 3
BuildRequires:	ghc-directory >= 1.0
BuildRequires:	ghc-filepath >= 1.1
BuildRequires:	ghc-transformers >= 0.2.0.0
BuildRequires:	ghc-exceptions >= 0.6
BuildRequires:	ghc-random >= 1.1
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 3
BuildRequires:	ghc-directory-prof >= 1.0
BuildRequires:	ghc-filepath-prof >= 1.1
BuildRequires:	ghc-transformers-prof >= 0.2.0.0
BuildRequires:	ghc-exceptions-prof >= 0.6
BuildRequires:	ghc-random-prof >= 1.1
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 3
Requires:	ghc-directory >= 1.0
Requires:	ghc-filepath >= 1.1
Requires:	ghc-transformers >= 0.2.0.0
Requires:	ghc-exceptions >= 0.6
Requires:	ghc-random >= 1.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
The functions for creating temporary files and directories in the base
library are quite limited. The unixutils package contains some good
ones, but they aren't portable to Windows. This library just
repackages the Cabal implementations of its own temporary file and
folder functions so that you can use them without linking against
Cabal or depending on it being installed.

%description -l pl.UTF-8
Funkcje do tworzenia plików i katalogów tymczasowych w bibliotece
podstawowej są nieco ograniczone. Pakiet unixutils zawiera kilka
dobrych, ale nie są one przenośne na Windows. Ta biblioteka zawiera
przepakietowane implementacje funkcji i katalogów tymczasowych z
pakietu Cabal, dzięki czemu można ich używać bez zależności od
Cabala.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-prof >= 6.12.3
Requires:	ghc-base-prof >= 3
Requires:	ghc-directory-prof >= 1.0
Requires:	ghc-filepath-prof >= 1.1
Requires:	ghc-transformers-prof >= 0.2.0.0
Requires:	ghc-exceptions-prof >= 0.6
Requires:	ghc-random-prof >= 1.1

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.lhs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHStemporary-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHStemporary-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHStemporary-%{version}-*_p.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/IO
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/IO/Temp.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/IO/Temp.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHStemporary-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/IO/Temp.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
