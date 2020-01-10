%define		nkfver	2.0.8

Name:		nkf
Epoch:		1
Version:	2.0.8b
Release:	6.2%{?dist}
License:	BSD
URL:		http://nkf.sourceforge.jp/
Source0:	http://osdn.dl.sourceforge.jp/nkf/26243/%{name}-%{version}.tar.gz
Source3:	nkf.copyright
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	perl(ExtUtils::MakeMaker)

Summary:	A Kanji code conversion filter
Group:		Applications/Text

%description
Nkf is a Kanji code converter for terminals, hosts, and networks. Nkf
converts input Kanji code to 7-bit JIS, MS-kanji (shifted-JIS) or
EUC.

%package -n perl-NKF
Summary:	Perl extension for Network Kanji Filter
Group:		Applications/Text
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description -n perl-NKF
This is a Perl Extension version of nkf (Network Kanji Filter).
It converts the last argument and return converted result.
Conversion details are specified by flags before the last argument.

%prep
%setup -q -n %{name}-%{nkfver}

%build
make CFLAGS="$RPM_OPT_FLAGS" nkf
cp -p %{SOURCE3} .
pushd NKF.mod
CFLAGS="$RPM_OPT_FLAGS" perl Makefile.PL PREFIX=%{_prefix} INSTALLDIRS=vendor
make
popd

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/{man1,ja/man1}

./nkf -e nkf.1j > nkf.1jeuc
iconv -f euc-jp -t utf-8 nkf.1jeuc > nkf.1utf8
install -m 755 -p nkf $RPM_BUILD_ROOT%{_bindir}
install -m 644 -p nkf.1 $RPM_BUILD_ROOT%{_mandir}/man1
install -m 644 -p nkf.1utf8 $RPM_BUILD_ROOT%{_mandir}/ja/man1/nkf.1
pushd NKF.mod
make install DESTDIR=$RPM_BUILD_ROOT
rm -f	$RPM_BUILD_ROOT%{perl_vendorarch}/perllocal.pod		\
	$RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod		\
	$RPM_BUILD_ROOT%{perl_vendorarch}/auto/NKF/NKF.bs	\
	$RPM_BUILD_ROOT%{perl_vendorarch}/auto/NKF/.packlist
popd
chmod 0755 $RPM_BUILD_ROOT%{perl_vendorarch}/auto/NKF/NKF.so

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root, -)
%doc nkf.doc nkf.copyright
%{_bindir}/nkf
%{_mandir}/man1/nkf.1*
%{_mandir}/ja/man1/nkf.1*

%files -n perl-NKF
%defattr (-, root, root, -)
%doc nkf.doc nkf.copyright
%{perl_vendorarch}/NKF.pm
%{perl_vendorarch}/auto/*
%{_mandir}/man3/NKF.3pm.gz

%changelog
* Thu Dec 03 2009 Dennis Gregorovic <dgregor@redhat.com> - 1:2.0.8b-6.2
- Rebuilt for RHEL 6

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1:2.0.8b-6.1
- Rebuilt for RHEL 6

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0.8b-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0.8b-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Nov 21 2008 Akira TAGOH <tagoh@redhat.com> - 1:2.0.8b-4
- Fix a source URL.

* Tue Jul  1 2008 Akira TAGOH <tagoh@redhat.com> - 1:2.0.8b-3
- Add perl(:MODULE_COMPAT_...) deps. (#453413)

* Tue Feb 12 2008 Akira TAGOH <tagoh@redhat.com> - 1:2.0.8b-2
- Rebuild for gcc-4.3.

* Fri Sep 21 2007 Akira TAGOH <tagoh@redhat.com> - 1:2.0.8b-1
- New upstream release.
- clean up the spec file.

* Thu Aug 23 2007 Akira TAGOH <tagoh@redhat.com> - 2.07-3
- Rebuild

* Fri Aug 10 2007 Akira TAGOH <tagoh@redhat.com> - 2.07-2
- Update License tag.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.07-1.1
- rebuild

* Thu Jul  6 2006 Akira TAGOH <tagoh@redhat.com> - 2.07-1
- New upstream release.
- use dist tag.
- clean up the spec file.

* Thu Mar 30 2006 Akira TAGOH <tagoh@redhat.com> - 2.06-1
- New upstream release.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.05-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.05-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Jul  7 2005 Akira TAGOH <tagoh@redhat.com> - 2.05-1
- New upstream release.

* Thu Mar 17 2005 Akira TAGOH <tagoh@redhat.com> - 2.04-5
- rebuilt

* Thu Feb 10 2005 Akira TAGOH <tagoh@redhat.com> - 2.04-4
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 07 2004 Akira TAGOH <tagoh@redhat.com> 2.04-1
- New upstream release.

* Tue Sep 30 2003 Akira TAGOH <tagoh@redhat.com> 2.03-1
- New upstream release.
- converted Japanese nkf.1 to UTF-8. (#105762)
- nkf-1.92-glibc2290.diff: removed.

* Thu Aug  7 2003 Elliot Lee <sopwith@redhat.com> 2.02-4
- Fix unpackaged files

* Fri Jun 27 2003 Akira TAGOH <tagoh@redhat.com> 2.02-3
- had perl-NKF as separated package.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Apr 09 2003 Akira TAGOH <tagoh@redhat.com> 2.02-1
- New upstream release.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Jan 10 2003 Akira TAGOH <tagoh@redhat.com> 2.01-1
- New upstream release.
  it contains UTF-8 support.

* Wed Nov 20 2002 Tim Powers <timp@redhat.com>
- rebbuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 19 2002 Akira TAGOH <tagoh@redhat.com> 1.92-10
- fix the stripped binary.
- s/Copyright/License/

* Mon Jun 03 2002 Yukihiro Nakai <ynakai@redhat.com>
- Add output bug patch for glibc-2.2.90 (#65864)

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Sep  4 2001 SATO Satoru <ssato@redhat.com> - 1.92-6
- attached nkf.1jeuc(euc-jp) instead of nkf.1j(iso-2022-jp) (#53127)

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Wed Feb 28 2001 SATO Satoru <ssato@redhat.com>
- nkf.copyright attached
- use system-defined macros (%%*dir)

* Tue Aug 29 2000 ISHIKAWA Mutsumi <ishikawa@redhat.com>
- adopt FHS

* Mon Aug  7 2000 ISHIKAWA Mutsumi <ishikawa@redhat.com>
- japanese manpages moved ja_JP.eucJP -> ja
- modified to be able to build by normal user.

* Tue Aug 01 2000 Yukihiro Nakai <ynakai@redhat.com>
- Update to 1.92
- rebuild for 7.0J

* Sat Mar 25 2000 Matt Wilson <msw@redhat.com>
- rebuilt for 6.2j
- support compressed man pages

* Wed Mar 22 2000 Chris Ding <cding@redhat.com>
- ja_JP.ujis -> ja_JP.eucJP

* Thu Oct  7 1999 Matt Wilson <msw@redhat.com>
- rebuilt against 6.1

* Sun May 30 1999 FURUSAWA,Kazuhisa <kazu@linux.or.jp>
- 1st Release for i386 (glibc2.1).
- Original Packager: Kazuhiko Mori(COW) <cow@he.mirai.ne.jp>

* Sun Jan 10 1999 Kazuhiko Mori(COW) <cow@he.mirai.ne.jp>
- just rebuilt for glibc TL. (release not changed.)

