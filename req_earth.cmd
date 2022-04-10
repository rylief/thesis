
SETLOCAL 

GOTO :start

:next_day

SET /A numhour=0
SET /A mod=%numyear% %% 4
SET /A numday=%numday%+1

IF %numday% EQU 32 ( SET/A numday=1 & SET /A nummonth=%nummonth%+1)
IF %numday% EQU 31 ( IF %nummonth% EQU 4 ( SET /A numday=1 & SET /A nummonth=%nummonth%+1)
		     IF %nummonth% EQU 6 ( SET /A numday=1 & SET /A nummonth=%nummonth%+1)
		     IF %nummonth% EQU 9 ( SET /A numday=1 & SET /A nummonth=%nummonth%+1)
		     IF %nummonth% EQU 11 ( SET /A numday=1 & SET /A nummonth=%nummonth%+1) )

IF %numday% EQU 30 ( IF %nummonth% EQU 2 ( SET /A numday=1 & SET /A nummonth=%nummonth%+1) )

IF %numday% EQU 29 ( IF %nummonth% EQU 2 ( IF %mod% NEQ 0 (SET /A numday=1 & SET /A nummonth=%nummonth%+1) ) )

IF %nummonth% EQU 13 (SET /A numyear=%numyear%+1)
IF %nummonth% EQU 13 (SET /A nummonth=1)

SET year=%numyear%
SET month=%nummonth%
SET day=%numday%

IF %nummonth% LSS 10 (SET month=0%month%)
IF %numday% LSS 10 (SET day=0%day%)

GOTO :build_req

:start

SET sattelite=GOE-8
SET type=IR

SET year=%1
SET endyear=%4
SET /A numyear=%year%

SET month=%2
SET /A nummonth=%month%
IF %nummonth% LSS 10 (SET month=0%month%)

SET endmonth=%5
SET /A numendmonth=%endmonth%
IF %numendmonth% LSS 10 (SET endmonth=0%endmonth%)

SET day=%3
SET /A numday=%day%
IF %numday% LSS 10 (SET day=0%day%)

SET endday=%6
SET /A numendday=%endday%
IF %numendday% LSS 10 (SET endday=0%endday%)

SET startday=%day%
SET startmonth=%month%
SET startyear=%year%

SET filename=%startyear%-%startmonth%-%startday%_%endyear%-%endmonth%-%endday%-%type%

IF NOT EXIST C:\Users\DELL\PycharmProjects\thesisIdeas\earth_pics\%filename% (mkdir C:\Users\DELL\PycharmProjects\thesisIdeas\earth_pics\%filename%)

SET /A numhour=0

SET crop=%7

:build_req

SET hour=%numhour%
IF %numhour% LSS 10 (SET hour=0%hour%)

SET stamp=%year%-%month%-%day%-%hour%
SET req=%sattelite%/%type%/%stamp%

curl "https://www.ncdc.noaa.gov/gibbs/image/%req%" -O 
magick %stamp% -crop %crop% %stamp%.jpg
del %stamp% 
move %stamp%.jpg C:\Users\DELL\PycharmProjects\thesisIdeas\earth_pics\%filename%

IF %numhour% LSS 21 (
	SET /A numhour=%numhour%+3
	GOTO :build_req
)

IF /I %year%-%month%-%day% NEQ %endyear%-%endmonth%-%endday% (
	GOTO :next_day
)
