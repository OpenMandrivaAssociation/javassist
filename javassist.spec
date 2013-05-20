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

Summary:	Java Programming Assistant:	bytecode manipulation
Name:		javassist
Version:	3.9.0
Release:	2.0.5
License:	MPL and LGPL
Url:		http://www.csg.is.titech.ac.jp/~chiba/javassist/
Group:		Development/Java
Source0:	javassist3.9.GA.zip
# cvs -d:pserver:anonymous@anoncvs.forge.jboss.com:/cvsroot/jboss export -r Javassist_3_5_CR1 javassist
Patch0:		javassist-buildfile-nosource1.4-nosrcjar.patch
%if !%{gcj_support}
BuildArch:	noarch
BuildRequires:	java-devel
%else
BuildRequires:	java-gcj-compat-devel
%endif
BuildRequires:	ant >= 0:1.6
BuildRequires:	java-rpmbuild >= 0:1.6

%description
Javassist (Java Programming Assistant) makes Java
bytecode manipulation simple. It is a class library
for editing bytecodes in Java; it enables Java
programs to define a new class at runtime and to
modify a class file when the JVM loads it. Unlike
other similar bytecode editors, Javassist provides
two levels of API:	source level and bytecode level.
If the users use the source-level API, they can edit
a class file without knowledge of the specifications
of the Java bytecode. The whole API is designed with
only the vocabulary of the Java language. You can even
specify inserted bytecode in the form of source text;
Javassist compiles it on the fly. On the other hand,
the bytecode-level API allows the users to directly
edit a class file as other editors.

%package demo
Summary:	Samples for %{name}
Group:		Development/Java
Requires:	javassist = %{EVRD}

%description demo
%{summary}.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description javadoc
%{summary}.

%package manual
Summary:	Tutorial for %{name}
Group:		Development/Java

%description manual
%{summary}.

%prep
%setup -q
%patch0 -p0
for j in $(find . -name "*.jar"); do
        mv $j $j.no
done
#remove the clas it needs com.sun.jdi to build
rm src/main/javassist/util/HotSwapper.java

%build
%{ant} dist

%install
# jars
mkdir -p %{buildroot}%{_javadir}
cp -p %{name}.jar \
  %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# demo
mkdir -p %{buildroot}%{_datadir}/%{name}-%{version}
cp -pr sample/* %{buildroot}%{_datadir}/%{name}-%{version}

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr html/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name} # ghost symlink

# manual
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}/tutorial
cp -pr tutorial/* %{buildroot}%{_docdir}/%{name}-%{version}/tutorial
cp -p License.html %{buildroot}%{_docdir}/%{name}-%{version}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%doc %{_docdir}/%{name}-%{version}/License.html
%{_javadir}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files demo
%{_datadir}/%{name}-%{version}

%files javadoc
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%files manual
%doc %{_docdir}/%{name}-%{version}/tutorial

