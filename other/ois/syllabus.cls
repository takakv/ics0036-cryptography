\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{syllabus}[2026/08/14 TalTech extended syllabus]

\newif\ifsyl@estonian
\DeclareOption{estonian}{\syl@estoniantrue}
\DeclareOption{english}{\syl@estonianfalse}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{scrartcl}}
\ExecuteOptions{english}
\ProcessOptions\relax

\LoadClass[parskip=half,fontsize=11pt]{scrartcl}
\KOMAoptions{usegeometry}

\RequirePackage[
  a4paper,
  top=25mm,
  bottom=25mm,
  left=25mm,
  right=25mm,
  footskip=10mm
]{geometry}

\RequirePackage{microtype}
\RequirePackage{fontspec}
\RequirePackage{unicode-math}

\IfFontExistsTF{Calibri}{%
  \setmainfont{Calibri}%
  \setsansfont{Calibri}%
}{%
  \setmainfont{Carlito}%
  \setsansfont{Carlito}%
}

% Hide the class options from babel
\let\syl@classoptions\@classoptionslist
\let\@classoptionslist\@empty
\ifsyl@estonian
  \RequirePackage[estonian]{babel}
\else
  \RequirePackage[british]{babel}
\fi
\let\@classoptionslist\syl@classoptions

\RequirePackage[autostyle]{csquotes}
\RequirePackage{xcolor}
\RequirePackage{hyperref}

\definecolor{taltech}{HTML}{870042}
\hypersetup{colorlinks=true,urlcolor=blue,linkcolor=blue}

\RequirePackage{scrlayer-scrpage}
\clearpairofpagestyles
\rofoot*{\pagemark}
\pagestyle{scrheadings}

\newcommand{\syl@s}[3]{%
  \expandafter\newcommand\csname syl@s@#1\endcsname{\ifsyl@estonian #3\else #2\fi}%
}

\syl@s{university}{Tallinn University of Technology}{Tallinna Tehnikaülikool}
\syl@s{faculty}{School of Information Technologies}{Infotehnoloogia teaduskond}
\syl@s{doctype}{Extended syllabus}{Laiendatud ainekava}
\syl@s{autumn}{Autumn}{Sügis}
\syl@s{spring}{Spring}{Kevad}

\syl@s{objectives}{Course aims:}{Õppeaine eesmärgid:}
\syl@s{outcomes}{Learning outcomes:}{Õpiväljundid:}
\syl@s{description}{Brief description of the course:}{Õppeaine sisu lühikirjeldus (teemad):}
\syl@s{language}{Language of instruction:}{Õppeaine keel:}
\syl@s{eap}{ECTS credits:}{EAP-d:}
\syl@s{students}{Target group:}{Üliõpilased:}
\syl@s{specialneeds}{Special needs:}{Erivajadused:}
\syl@s{registration}{Registration:}{Registreerumine:}
\syl@s{prerequisites}{Prerequisite subjects and/or required prior knowledge:}{Eeldusained ja/või nõutavad eelteadmised:}
\syl@s{resources}{Necessary resources and technical requirements:}{Vajalikud ressursid:}
\syl@s{lecturers}{Lecturers:}{Õppejõud:}
\syl@s{contact}{Contact details:}{Õppejõuga kontakti saamine:}
\syl@s{timetable}{Schedule of contact learning:}{Kontaktõppe ajagraafik:}
\syl@s{process}{Studies and description of the learning process:}{Õppeprotsessi kirjeldus:}
\syl@s{esupport}{E-support:}{Õppeaine e-tugi:}
\syl@s{literature}{Study materials and literature:}{Õppekirjandus:}
\syl@s{illustrative}{Illustrative material:}{Illustreeriv materjal:}
\syl@s{ongoing}{Ongoing evaluation:}{Jooksev hindamine:}
\syl@s{assessment}{Assessment:}{Hindamine:}
\syl@s{ongoingcriteria}{Evaluation criteria related to ongoing evaluation:}{Jooksva hindamisega seotud hindamiskriteeriumid:}
\syl@s{exam}{Exam:}{Eksam:}
\syl@s{examcriteria}{Assessment criteria for the exam:}{Eksami hindamiskriteeriumid:}
\syl@s{finalgrade}{Final grade:}{Lõpphinne:}
\syl@s{practices}{Academic practices:}{Akadeemilised tavad:}
\syl@s{ai}{Use of AI:}{TI kasutamine:}

\syl@s{scheduletitle}{Schedule and topics}{Detailne ajakava ning teemad}
\syl@s{week}{Week}{Nädal}
\syl@s{before}{Before contact lessons:}{Enne kontakttundi:}
\syl@s{during}{In contact hours:}{Kontakttunnis:}
\syl@s{after}{After the contact lesson:}{Peale kontakttundi:}
\syl@s{inmoodle}{In Moodle:}{Moodle'is:}
\syl@s{note}{Note:}{Märkus:}

\syl@s{specialneedstext}{%
  % Taken from GUIDELINE FOR DESCRIBING EXTENDED SYLLABUS
  Students with special needs can participate in the course.
  Please inform the lecturer at the beginning of the course of any special needs that may affect your participation in the study activities or assessment activities.%
}{%
  Erivajadustega üliõpilastel on võimalik õppeaines osaleda.  Palun
  informeerige kohe õppeaine alguses õppejõudu erivajadustest, mis võivad
  mõjutada teie osalemist õppetegevuses või hindamistegevuses.%
}

\syl@s{registrationtext}{%
  Students wishing to complete the course must declare the course in SIS
  according to the deadlines specified in the academic calendar.%
}{%
  Õppeainet läbida soovivad õppurid peavad deklareerima õppeaine ÕIS-is
  vastavalt akadeemilises kalendris määratud tähtaegadele.%
}

\syl@s{practicestext}{%
  % Taken from GUIDELINE FOR DESCRIBING EXTENDED SYLLABUS
  As a student of Tallinn University of Technology, you are obliged to follow the academic practices of the university in your studies.
  It is assumed that you do the work you submit under your name.
  Plagiarism and cheating are not acceptable.
  If it is confirmed that you have engaged in such activities, it will be followed by a grade of \enquote{0} for the specific work/assessment and a proposal will be submitted to the programme director.
  Depending on the proposal, this may result in a reprimand from the dean or, in the case of a very significant violation, expulsion from the university.%
}{%
  Tallinna Tehnikaülikooli õppurina on teil kohustus järgida õppetöös ülikooli
  akadeemilisi tavasid.  Eeldatakse, et töö, mille te esitate oma nime all, on
  teie enda tehtud.  Plagiaat ning spikerdamine ei ole aktsepteeritavad.  Kui
  leiab kinnitust, et te olete sellist tegevust harrastanud, siis sellele
  järgneb konkreetse töö/eksami hinne \enquote{0} ning esitatakse esildis
  teaduskonna \enquote{Akadeemiliste tavade ja vääritu käitumise menetlemise
  komisjonile}.  Sõltuvalt komisjoni ettepanekust, võib see tuua kaasa dekaani
  noomituse või, väga olulise rikkumise korral, ülikoolist
  eksmatrikuleerimise.%
}

\syl@s{aitext}{%
  AI may not be used in the exam.
  It may be used for homework assignments only if the use aligns with TalTech's AI policies, and any restrictions that are explicitly stated in the assignments.
  That is, the use of AI may be restricted, or even forbidden, for specific tasks during the semester.
  The use of AI must always be mentioned if used to solve a task, including when rewording, as it may insert important things not originally part of the student's own input.%
}{}

\syl@s{scaletext}{%
  The sum of the points will be converted into the final grade based on the
  following principles:%
}{%
  Punktide summa muudetakse lõpphindeks järgmiste põhimõtete alusel:%
}

\syl@s{gradefive}{excellent}{suurepärane}
\syl@s{gradefour}{very good}{väga hea}
\syl@s{gradethree}{good}{hea}
\syl@s{gradetwo}{satisfactory}{rahuldav}
\syl@s{gradeone}{poor}{kasin}
\syl@s{gradezero}{fail}{puudulik}
\syl@s{lessthan}{less than}{vähem kui}

\syl@s{scheduledisclaimer}{%
  The semester plan is preliminary and subject to change due to cancellation of
  appointments, changes to materials, and more.%
}{%
  Semestri plaan on esialgne ning võib muutuda seoses kohtumiste tühistamise,
  materjalide muutmise ja muu osas.%
}

\newcommand{\coursecode}[1]{\def\syl@code{#1}}
\newcommand{\coursetitle}[1]{\def\syl@title{#1}}
\newcommand{\semester}[2]{\def\syl@season{#1}\def\syl@year{#2}}
\newcommand{\lecturers}[1]{\def\syl@s@lecturerstext{#1}}
\newcommand{\email}[1]{\href{mailto:#1}{#1}}

\coursecode{XXX0000}
\coursetitle{Xxxxxxxxx}
\semester{autumn}{2026}
\lecturers{Taaniel Kraavi, \email{taaniel.kraavi@taltech.ee}}

\newcommand{\makesyllabustitle}{%
  \begingroup
    \raggedright
    \syl@s@university\\
    \syl@s@faculty\par
    \bigskip
    {\color{taltech}\bfseries\Large\syl@code\ \syl@title\par}
    \smallskip
    {\color{taltech}\large
      \syl@s@doctype\\
      \csname syl@s@\syl@season\endcsname\ \syl@year\par}
  \endgroup
  \bigskip
  \hypersetup{pdftitle={\syl@code\ \syl@title\ -- \syl@s@doctype}}%
}

\newlength{\syl@labelwidth}
\newlength{\syl@labelsep}
\newlength{\syl@bodyindent}
\newbox\syl@labelbox
\newbox\syl@bodybox
\newdimen\syl@labelht
\newdimen\syl@bodyht

\AtBeginDocument{%
  \setlength{\syl@labelwidth}{0.23\textwidth}%
  \setlength{\syl@labelsep}{0.02\textwidth}%
  \setlength{\syl@bodyindent}{\dimexpr\syl@labelwidth+\syl@labelsep\relax}%
}

\newcommand{\field}[2]{%
  \par\vskip\dimexpr\medskipamount+\baselineskip\relax
  \begingroup
    \setbox\syl@labelbox=\hbox{%
      \textcolor{taltech}{%
        \parbox[t]{\syl@labelwidth}{\raggedright\bfseries
          \csname syl@s@#1\endcsname}}}%
    \syl@labelht=\dimexpr\ht\syl@labelbox+\dp\syl@labelbox\relax
    \dp\syl@labelbox=\z@
    \setbox\syl@bodybox=\vbox{%
      \leftskip=\syl@bodyindent
      \@totalleftmargin=\syl@bodyindent
      \linewidth=\dimexpr\textwidth-\syl@bodyindent\relax
      \noindent\llap{\box\syl@labelbox\hspace{\syl@labelsep}}\ignorespaces #2\par}%
    \syl@bodyht=\dimexpr\ht\syl@bodybox+\dp\syl@bodybox\relax
    \unvbox\syl@bodybox
    \ifdim\syl@bodyht<\syl@labelht
      \vskip\dimexpr\syl@labelht-\syl@bodyht\relax
    \fi
  \endgroup
}

\newcommand{\stdfield}[1]{%
  \field{#1}{\csname syl@s@#1text\endcsname}%
}

\newcommand{\gradescale}{%
  \par\medskip\noindent\syl@s@scaletext\par\nobreak
  \begin{center}
    \begin{tabular}{@{}rll@{}}
      \enquote{5} & \syl@s@gradefive  & 91--100\\
      \enquote{4} & \syl@s@gradefour  & 81--90\\
      \enquote{3} & \syl@s@gradethree & 71--80\\
      \enquote{2} & \syl@s@gradetwo   & 61--70\\
      \enquote{1} & \syl@s@gradeone   & 51--60\\
      \enquote{0} & \syl@s@gradezero  & \syl@s@lessthan\ 51\\
    \end{tabular}
  \end{center}
}

\newcommand{\makescheduletitle}{%
  \par\bigskip
  {\color{taltech}\bfseries\Large\syl@s@scheduletitle\par}
  \medskip
  \syl@s@scheduledisclaimer\par
}

\newcommand{\week}[3]{%
  \par\medskip
  {\color{taltech}\bfseries\syl@s@week\ #1\par}\nobreak
  #3\par
  \edef\syl@date{\detokenize{#2}}%
  \ifx\syl@date\empty\else #2\par\fi
}

\newcommand{\syl@item}[2]{\par\noindent\textbf{#1}\ #2\par}
\newcommand{\note}[1]{\syl@item{\syl@s@note}{#1}}

\endinput
