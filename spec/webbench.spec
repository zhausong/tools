Name:	        webbench	
Version:	1.5
Release:	1%{?dist}
Summary:	webbench tool

Group:          system administration tools
License:	GPL
uRL:	        http://home.tiscali.cz	
Source0:	http://home.tiscali.cz/~cz210552/distfiles/webbench-1.5.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	gcc,make

%description
system administration tools


%prep
%setup -q


%build
make
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
mkdir %{buildroot}/usr/local/man/man1 -p
mkdir %{buildroot}/usr/bin
make install DESTDIR=%{buildroot}
mv %{buildroot}/usr/local/bin %{buildroot}/usr/bin/webbench

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc
/usr/bin/webbench
/usr/local/man/man1/webbench.1
/usr/local/share/doc/webbench/changelog
/usr/local/share/doc/webbench/copyright


%changelog
* Fri Jul 12 2013        change config file<itnihao@qq.com>
- 1.5

