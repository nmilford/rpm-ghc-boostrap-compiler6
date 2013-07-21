# An RPM spec file install a Glasgow Haskell Compiler version able to bootstrap
# GHC 7.0.x
#
# We want the latest ghc, 7.6.3, but it's binary release is not compatible with
# glibc on CentOS 5.
#
# We need to build it from source, but you need GHC to build GHC. :/
#
# The latest binary GHC release I could find that worked on CentOS 5 is 6.12.3.
#
# You cannot build ghc-7.6.3 with anything less then ghc-7.* (whose binary
# dists do not work on CentOS 5)
#
# So we need to build ghc-7.0.2 from source with ghc-6.12.3 binaries to allow
# us build our final target of ghc-7.6.3

# To Build:
# sudo yum -y install rpmdevtools gmp-devel && rpmdev-setuptree
# wget http://www.haskell.org/ghc/dist/6.12.3/ghc-6.12.3-x86_64-unknown-linux-n.tar.bz2 -O ~/rpmbuild/SOURCES/ghc-6.12.3-x86_64-unknown-linux-n.tar.bz2
# wget https://raw.github.com/nmilford/rpm-ghc-bootsrap-compiler6/master/ghc-bootsrap-compiler6.spec -O ~/rpmbuild/SPECS/ghc-bootsrap-compiler6.spec
# rpmbuild -bb ~/rpmbuild/SPECS/ghc-bootsrap-compiler6.spec

Name:           ghc-bootstrap-compiler6
Version:        6.12.3
Release:        1
Summary:        Glasgow Haskell Compiler version able to bootstrap GHC 7.0.x
Group:          Development/Languages
License:        The Glasgow Haskell Compiler License
URL:            http://www.haskell.org/ghc/
Source0:        http://www.haskell.org/ghc/dist/%{version}/ghc-%{version}-x86_64-unknown-linux-n.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  gmp-devel

%description
GHC is a state-of-the-art, open source, compiler and interactive environment
for the functional language Haskell.

This package will install %{version}, which is binary compatible with CentOS 5 and
allows for the bootstrapping of newer GHC versions (but not the very latest).

You can use this to build an intermediary GHC version to get you to the latest.

%prep
%setup -q -n ghc-%{version}

%install
install -d -m 755 %{buildroot}/usr/

%configure --docdir=%{buildroot}/usr/share/doc/ghc-%{version}/

%makeinstall
rm -f %{buildroot}/usr/bin/ghc
rm -f %{buildroot}/usr/bin/ghc-pkg
rm -f %{buildroot}/usr/bin/ghci
rm -rf %{buildroot}/usr/share/man/*
mv %{buildroot}/usr/bin/haddock{,-%{version}}
mv %{buildroot}/usr/bin/hp2ps{,-%{version}}
mv %{buildroot}/usr/bin/hpc{,-%{version}}
mv %{buildroot}/usr/bin/hsc2hs{,-%{version}}
mv %{buildroot}/usr/bin/runghc{,-%{version}}
mv %{buildroot}/usr/bin/runhaskell{,-%{version}}

install -d -m 755 %{buildroot}/usr/share/doc/ghc-%{version}
install    -m 644 %{_builddir}/ghc-%{version}/README  %{buildroot}/usr/share/doc/ghc-%{version}
install    -m 644 %{_builddir}/ghc-%{version}/LICENSE %{buildroot}/usr/share/doc/ghc-%{version}

for file in ghc-%{version} ghci-%{version} ghc-pkg-%{version} haddock-%{version} hp2ps-%{version} hpc-%{version} hsc2hs-%{version} runghc-%{version}; do
  sed -i -e  's|%{buildroot}||g' %{buildroot}%{_bindir}/$file
done

rm -f %{buildroot}/%{_libdir}/ghc-%{_bindir}/package.conf.d/package.cache


cd %{buildroot}/%{_libdir}/ghc-%{version}/package.conf.d/
for pkg in *; do
  sed -i -e  's|%{buildroot}||g' $pkg
done
cd -

%post
%{_bindir}/ghc-pkg-%{version} recache

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/ghc*
%{_bindir}/*
/usr/share/doc/ghc-%{version}/*

%changelog
* Mon Jul 08 2013 Nathan Milford <nathan@milford.io> 6.12.3-1
- Initial spec.
- This is specifically meant to build newer versions of GHC.
