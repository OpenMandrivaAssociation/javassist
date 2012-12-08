# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support 0

Summary:        Java Programming Assistant: bytecode manipulation
Name:           javassist
Version:        3.9.0
Release:        %mkrel 2.0.5
Epoch:          0
License:        MPL and LGPL
URL:            http://www.csg.is.titech.ac.jp/~chiba/javassist/
Group:          Development/Java
Source0:        javassist3.9.GA.zip
# cvs -d:pserver:anonymous@anoncvs.forge.jboss.com:/cvsroot/jboss export -r Javassist_3_5_CR1 javassist

Patch0:         javassist-buildfile-nosource1.4-nosrcjar.patch
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  ant >= 0:1.6
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Javassist (Java Programming Assistant) makes Java
bytecode manipulation simple. It is a class library
for editing bytecodes in Java; it enables Java
programs to define a new class at runtime and to
modify a class file when the JVM loads it. Unlike
other similar bytecode editors, Javassist provides
two levels of API: source level and bytecode level.
If the users use the source-level API, they can edit
a class file without knowledge of the specifications
of the Java bytecode. The whole API is designed with
only the vocabulary of the Java language. You can even
specify inserted bytecode in the form of source text;
Javassist compiles it on the fly. On the other hand,
the bytecode-level API allows the users to directly
edit a class file as other editors.

%package demo
Summary:        Samples for %{name}
Group:          Development/Java
Requires:       javassist = 0:%{version}-%{release}

%description demo
%{summary}.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
%{summary}.

%package manual
Summary:        Tutorial for %{name}
Group:          Development/Java

%description manual
%{summary}.

%prep
%setup -q # -n %{name}-%{version}
%patch0 -p0
for j in $(find . -name "*.jar"); do
        mv $j $j.no
done
#remove the clas it needs com.sun.jdi to build
rm src/main/javassist/util/HotSwapper.java

%build
%{ant} dist

%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p %{name}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# demo
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
cp -pr sample/* $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr html/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

# manual
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/tutorial
cp -pr tutorial/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/tutorial
cp -p License.html $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc %{_docdir}/%{name}-%{version}/License.html
%{_javadir}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif


%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}-%{version}

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%files manual
%defattr(0644,root,root,0755)
%doc %{_docdir}/%{name}-%{version}/tutorial


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0:3.9.0-2.0.3mdv2011.0
+ Revision: 665818
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:3.9.0-2.0.2mdv2011.0
+ Revision: 606074
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:3.9.0-2.0.1mdv2010.1
+ Revision: 523065
- rebuilt for 2010.1

* Wed Feb 18 2009 Jérôme Soyer <saispo@mandriva.org> 0:3.9.0-2.0.0mdv2009.1
+ Revision: 342372
- Fix Version
- New upstream release

* Wed Aug 13 2008 Helio Chissini de Castro <helio@mandriva.com> 0:3.5-1.cr1.2.0.3mdv2009.0
+ Revision: 271402
- We need update all the toolchain to maven, now using openjdk

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0:3.5-0.cr1.2.0.3mdv2009.0
+ Revision: 136503
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:3.5-0.cr1.2.0.3mdv2008.1
+ Revision: 120930
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:3.5-0.cr1.2.0.2mdv2008.0
+ Revision: 87426
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Thu Aug 02 2007 David Walluck <walluck@mandriva.org> 0:3.5-0.cr1.2.0.1mdv2008.0
+ Revision: 58356
- Import javassist



* Wed Jul 18 2007 Alexander Kurtakov <akurtakov@active-lynx.com> - 0:3.5-0.cr1.2.0.1mdv2008.0
- Adapt for Mandriva
- Remove class referencing com.sun.jdi

* Sat Feb 17 2007 Fernando Nasser <fnasser@redhat.com> - 0:3.5-0.cr1.2jpp
- Remove vendor and distribution tags
- Remove tabs

* Sat Feb 17 2007 Fernando Nasser <fnasser@redhat.com> - 0:3.5-0.cr1.1jpp
- Upgrade to 3.5.CR1

* Tue Jun 13 2006 Ralph Apel <r.apel@r-apel.de> - 0:3.2-0.cr2.1jpp
- Upgrade to 3.2.CR2

* Tue May 02 2006 Ralph Apel <r.apel@r-apel.de> - 0:3.1-1jpp
- Upgrade to 3.1

* Fri Feb 24 2006 Fernando Nasser <fnasser@redhat.com> - 0:3.0-2jpp
- First JPP 1.7 build

* Fri Mar 04 2005 Ralph Apel <r.apel at r-apel.de> - 0:3.0-1jpp
- Upgrade to 3.0 final
- Fixed _docdir ownership

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:3.0-0.beta.2jpp
- Rebuild with ant-1.6.2

* Fri Jun 04 2004 Ralph Apel <r.apel at r-apel.de> - 0:3.0-0.beta.1jpp
- preview of 3.0

* Fri Mar 05 2004 Ralph Apel <r.apel at r-apel.de> - 0:2.6-1jpp
- First JPackage release
