\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{practice}[2024/01/31 Practice tasks template]

\LoadClass[parskip=half]{scrartcl}

\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{amsthm}

\RequirePackage{tcolorbox}
\tcbuselibrary{listings,skins,breakable}
\RequirePackage{fancyvrb}

\newtcblisting{cmdblock}{
  colback=black!5,
  colframe=black!20,
  listing only,
  listing options={
    basicstyle=\small\ttfamily,
    columns=flexible,
    breaklines=true,
    breakindent=1em,
    aboveskip=0pt,
    belowskip=0pt,
  },
  left=3pt, right=3pt, top=3pt, bottom=3pt,
  arc=3pt,
  boxrule=0.5pt,
}

\RequirePackage[hidelinks]{hyperref}

\RequirePackage{fontspec}
\RequirePackage{unicode-math}
\RequirePackage{microtype}

\setmainfont{Stix Two Text}
%\setsansfont[BoldFont = *-Semibold]{Source Sans 3}
\setsansfont{TeX Gyre Heros}
\setmathfont{Stix Two Math}
\setmonofont{Courier New}

\RequirePackage{csquotes}
\setquotestyle{british}

\RequirePackage{bookmark}

\RequirePackage{datetime2}
\DTMsetdatestyle{ddmmyy}
\DTMsetup{datesep=.}

\RequirePackage{booktabs}

\makeatletter
\def\@maketitle{%
  \newpage
  \begin{center}%
    {Practice session \@title{} --- \@date\par}%
  \end{center}%
  \par}
\makeatother

\newcounter{task}[section]
\newenvironment*{task}[1]{%
  \refstepcounter{task}%
  \vspace*{1em}
  \textbf{Task~\thetask{} --- {#1}}\par}{}

\newenvironment*{demo}[1]{%
  \refstepcounter{task}%
  \vspace*{1em}
  \textbf{Demo~\thetask{} --- {#1}}\par}{}

\newenvironment*{challenge}[1]{%
  \vspace*{1em}
  \textbf{Challenge --- {#1}}\par}{}

%\makeatletter
%\newcommand\task{\@startsection {task}{1}{\z@}%
%                                {0pt}%
%                                {0pt}%
%                                {\normalfont\bfseries\par}}
%\newcommand{\taskmark}[1]{}
%\newcounter{task}
%\let\l@task\l@section
