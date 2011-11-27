Name:           javassist
Version:        3.14.0
Release:        5
Summary:        The Java Programming Assistant provides simple Java bytecode manipulation
Group:          Development/Java
License:        MPLv1.1 or LGPLv2+
URL:            http://www.csg.is.titech.ac.jp/~chiba/javassist/
Source0:        http://downloads.sourceforge.net/jboss/%{name}-%{version}-GA.zip
BuildArch:      noarch

BuildRequires:     java-devel >= 0:1.6.0
BuildRequires:     jpackage-utils

BuildRequires:     maven2
BuildRequires:     maven-compiler-plugin
BuildRequires:     maven-install-plugin
BuildRequires:     maven-jar-plugin
BuildRequires:     maven-javadoc-plugin
BuildRequires:     maven-resources-plugin
BuildRequires:     maven-surefire-plugin
BuildRequires:     maven-source-plugin
BuildRequires:     maven-antrun-plugin
BuildRequires:     maven-doxia
BuildRequires:     maven-doxia-sitetools

Requires:          java >= 0:1.6.0
Requires:          jpackage-utils

Requires(post): jpackage-utils
Requires(postun): jpackage-utils

%description
Javassist enables Java programs to define a new class at runtime and to
modify a class file when the JVM loads it. Unlike other similar
bytecode editors, Javassist provides two levels of API: source level
and bytecode level. If the users use the source-level API, they can
edit a class file without knowledge of the specifications of the Java
bytecode. The whole API is designed with only the vocabulary of the
Java language. You can even specify inserted bytecode in the form of
source text; Javassist compiles it on the fly. On the other hand, the
bytecode-level API allows the users to directly edit a class file as
other editors.

%package javadoc
Summary:           Javadocs for javassist
Group:             Development/Java
Requires:          jpackage-utils

%description javadoc
javassist development documentation.

%prep
%setup -q -n %{name}-%{version}-GA

find . -name \*.jar -type f -delete

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mvn-jpp \
-Dmaven.repo.local=$MAVEN_REPO_LOCAL \
install javadoc:javadoc

%install
rm -rf $RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_datadir}/maven2/poms/JPP-%{name}.pom
%add_to_maven_depmap %{name} %{name} %{version}%{ext_ver} JPP %{name}

# jar
install -d $RPM_BUILD_ROOT%{_javadir}
install -m644 target/%{name}-%{version}-GA.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -rp target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%doc License.html Readme.html
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%doc License.html
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}
%{_javadocdir}/%{name}-%{version}/*

