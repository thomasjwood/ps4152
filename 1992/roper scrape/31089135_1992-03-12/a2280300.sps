set width=80.
file handle datain name='h:\demi\USAIPOGO1992-2280300\version1\2280300.bin' /mode=multipunch.
file handle out name='h:\demi\USAIPOGO1992-2280300\version2\22810300.sav'.
set compression=yes.
set format=F8.0.
set mxwarns=99999.
 
DATA LIST FILE=datain RECORDS=1 TABLE
 		/1
Respid		1-6(a)
Surveyid	7-9
no_01		10-11
Weight		13-15
Section		16-24(a)
Intvr		25-26
Q01		27
q901		29
q901a		30
q902		31
q902a		32(a)
q903		33
q904		34(a)
q904a_1	35:4
q904a_2	35:5
q904a_3	35:6
q904a_4	35:7
q904a_5	35:8
q904a_0	35:3
q905		36
q906		37
q907c1		38(a)
q907c2		39(a)
q908		40
q909		41
q910c1		42(a)
q910c2		43(a)
OCWE		44-45(a)
q911		46
q911a		47
q912		48(a)
q913		49
q914		50-51
q915		54
q916a		55(a)
q916b		56
q917		57(a)
q918		58(a)
q918a		59(a)
q919a		60(a)
q919b		61-62
q920		63
spot#		77-80.








