* Roper Center SPSS Syntax File for:
* Study Number: USAIPOSPGONEW1992-305073
* Title: Gallup/Newsweek Poll
* Organization: Gallup Organization
* Field Dates: 12/17/92-12/18/92
* Generated: 5/23/02 11:40:37 AM
* ----------------------------------------------------------- *.
file handle datain  name='H:\25-ds-149\usaipospgonew1992-305073\305073.dat' .
file handle dataout name='H:\25-ds-149\usaipospgonew1992-305073\305073.sav'.
set compression=yes.
set format=F8.0.
set mxwarns=99999.
 
DATA LIST FILE=datain RECORDS=4 TABLE
  			/1
 respid	 3-6	
 states	 7-8	
 age	 9	
 card#	10-11	
 weight	13-15		
 d1	44
 d2	45-46	
 d3	47	
 d4	48	
 d5	52	
 d6	53-54	
 			/4
 q01	12	
 q02	13	
 q03	14 	
 q04	15	
 q05	16 	
 q06	17	
 q07	18	
 q08	19	
 q09	20 	
 q10a	21	
 q10b	22	
 q10c	23	
 q10d	24	
 q11a	25	
 q11b	26	
 q11c	27	
 q11d	28	
 q12	29	
 q13	30	
 q14	31	
 q15 	32	
 q16a	33	
 q16b	34	
 q16c	35	
 q17	36	
 q18	37	
 q19	38 	
 q20a	39	
 q20b	40 	
 q20c	41	
 q20d 	42		.


VARIABLE LABELS 
  Q01      'Did things come up that kept you from voting in the election on November 3rd, or did you happen to vote?'
  Q02      'On November 3rd, did you happen to vote for Bill Clinton, George Bush or Ross Perot?'
  Q03      'From what you know about Bill Clinton''s wife Hillary, do you have a favorable or unfavorable opinion of her?'
  Q04      'Would you like to see Hillary Clinton play an active role in policy-making in the Clinton administration, or not?'
  Q05      'Would you favor or oppose having Congress pass the Freedom of Choice Act, which would guarantee a woman''s legal right to an abortion in most circumstances?'
  Q06      'In general, do you think that 1992 has been a year in which women made progress, basically held their positions, or lost ground?'
  Q07      'Do you think most men in the United States today understand the issues that concern women most, or not?'
  Q08      'Have the men you know in your personal life become more sensitive to the needs and problems of women in the past year, or not?'
  Q09      'I have some questions about the women''s movement and feminism.... Do you consider yourself a feminist, or not?'
  Q10A     'We''d like to know how you think the women''s movement has affected certain groups. Do you think the women''s movement has done very well, fairly well or not well in improving the lives of... professional women?'
  Q10B     'We''d like to know how you think the women''s movement has affected certain groups. Do you think the women''s movement has done very well, fairly well or not well in improving the lives of... working class women?'
  Q10C     'We''d like to know how you think the women''s movement has affected certain groups. Do you think the women''s movement has done very well, fairly well or not well in improving the lives of... poor women?'
  Q10D     'We''d like to know how you think the women''s movement has affected certain groups. Do you think the women''s movement has done very well, fairly well or not well in improving the lives of... woman like yourself?'
  Q11A     'Please tell me whether or not you think women are better off now than they were 10 years ago in each of the following areas.... Income and economic resources'
  Q11B     '(Please tell me whether or not you think women are better off now than they were 10 years ago in each of the following areas.)... Legal rights'
  Q11C     '(Please tell me whether or not you think women are better off now than they were 10 years ago in each of the following areas.)... Their status in society'
  Q11D     '(Please tell me whether or not you think women are better off now than they were 10 years ago in each of the following areas.)... The burden from housework and child-rearing'
  Q12      'Thinking about the job opportunities and pay available to you, yourself--are they better, worse, or about the same as those available to equally qualified men?'
  Q13	   'Do you now have a full-time job for pay, a part time job, or do you not now work at a paying job?'
  Q14	   'Do you happen to have any children living at home?'
  Q15      'Do you work mostly for the money or mostly for other reasons?'
  Q16A     'In the past year, have you seen the following changes in your workplace or not?... Have men become more sensitive to the problem of sexual harassment?'
  Q16B     '(In the past year, have you seen the following changes in your workplace or not?)... Have bosses become more sensitive to the problem of sexual harassment?'
  Q16C     '(In the past year, have you seen the following changes in your workplace or not?)... Have bosses become more sensitive to the problems of working mothers?'
  Q17      'Thinking about the charges of sexual harassment that Anita Hill made against Supreme Court Justice Clarence Thomas one year ago...From what you have heard or read, do you think Thomas sexually harassed Hill, or not?'
  Q18      'Do you think the women that President-elect (Bill) Clinton has appointed to office will make a big difference, a small difference or no difference in the way the government operates?'
  Q19      'Do you think that the increased number of women elected to political office this year will make a big difference, a small difference or no difference in the way the government operates?'
  Q20A     'Please tell me whether or not you have done each of the following in the past twelve months.... Become more politically active'
  Q20B     '(Please tell me whether or not you have done each of the following in the past twelve months.)... Given money to a feminist groups or a group dealing with women''s problems'
  Q20C     '(Please tell me whether or not you have done each of the following in the past twelve months.)... Given money to a political candidate'
  Q20D     '(Please tell me whether or not you have done each of the following in the past twelve months.)... Changed your job or career goals'
  D1	   'Gender'
  D2	   'What is your age?'
  D3	   'What is the last grade or class that you completed in school?'
  D4	   'What is your race?  Are you white, black, Asian or some other?'
  D5	   'What is your marital status?  Are you currently married, widowed, divorces, separated, or have you never been married?'
  D6	   'Is your total annual household income before taxes $20,000 or more or is it less that $20,000?...'

 .  
    
* End of Variable Labels 
 
VALUE LABELS
  States
  	11  'Maine'
  	12  'New Hampshire'
  	13  'Vermont'
  	14  'Massachusetts'
  	15  'Rhode Island'
  	16  'Connecticut'
  	21  'New York'
  	22  'New Jersey'
  	23  'Pennsylvania'
  	24  'Maryland'
  	25  'Delaware'
  	26  'West Virginia'
  	27  'District of Columbia'
  	31  'Ohio'
  	32  'Michigan'
  	33  'Indiana'
  	34  'Illinois'
  	41  'Wisconsin'
  	42  'Minnesota'
  	43  'Iowa'
  	44  'Missouri'
  	45  'North Dakota'
  	46  'South Dakota'
  	47  'Nebraska'
  	48  'Kansas'
  	51  'Virginia'
  	52  'North Carolina'
  	53  'South Carolina'
  	54  'Gerogia'
  	55  'Florida'
  	56  'Kentucky'
  	57  'Tennessee'
  	58  'Alabama'
  	59  'Mississippi'
	61  'Arkansas'
  	62   'Louisiana'
  	63  'Oklahoma'
  	64  'Texas'
  	71  'Montana'
  	72  Arizona'
  	73  'Colorado'
  	74  'Idaho'
  	75  'Wyoming'
  	76  'Utah'
  	77  'Nevada'
  	78  'New Mexico'
  	81  'California'
  	82  'Oregon'
  	83  'Washington'
  	/        
  Q01
  1  'Yes, voted'
  2  'No, did not'
  3  'Too young (vol.)'
  4  'Don''t know'
  5  'Refused'
  / 
  Q02
  1  'Clinton'
  2  'Bush'
  3  'Perot'
  4  'Other'
  5  'Don''t remember'
  6  'Refused'
  / 
  Q03
  1  'Favorable'
  2  'Unfavorable'
  3  'Don''t know/Refused'
  / 
  Q04
  1  'Yes, active role'
  2  'No'
  3  'Don''t know/Refused'
  / 
  Q05
  1  'Favor'
  2  'Oppose'
  3  'Don''t know/Refused'
  / 
  Q06
  1  'Made progress'
  2  'Held position'
  3  'Lost ground'
  4  'Don''t know/Refused'
  / 
  Q07
  1  'Yes'
  2  'No'
  3  'Don''t know/Refused'
  / 
  Q08
  1  'Yes'
  2  'No'
  3  'Don''t know/Refused'
  / 
  Q09
  1  'Yes'
  2  'No'
  3  'Don''t know/Refused'
  / 
  Q10A
  1  'Very well'
  2  'Fairly well'
  3  'Not well'
  4  'Don''t know/Refused'
  / 
  Q10B
  1  'Very well'
  2  'Fairly well'
  3  'Not well'
  4  'Don''t know/Refused'
  / 
  Q10C
  1  'Very well'
  2  'Fairly well'
  3  'Not well'
  4  'Don''t know/Refused'
  / 
  Q10D
  1  'Very well'
  2  'Fairly well'
  3  'Not well'
  4  'Don''t know/Refused'
  / 
  Q11A
  1  'Better off'
  2  'Not better off'
  3  'Don''t know/Refused'
  / 
  Q11B
  1  'Better off'
  2  'Not better off'
  3  'Don''t know/Refused'
  / 
  Q11C
  1  'Better off'
  2  'Not better off'
  3  'Don''t know/Refused'
  / 
  Q11D
  1  'Better off'
  2  'Not better off'
  3  'Don''t know/Refused'
  / 
  Q12
  1  'Better'
  2  'Worse'
  3  'Same'
  4  'Don''t know/Refused'
  / 
  Q13
  1  'Full-time'
  2  'Part-time'
  3  'Not employed'
  4  'Retired'
  5  'Don''t know/Refused'
  /
  Q14
  1  'Yes'
  2  'No'
  3  'Don''t know/Refused'
  /
  Q15
  1  'Money'
  2  'Other reasons'
  3  'Can''t say'
  / 
  Q16A
  1  'Yes'
  2  'No'
  3  'Don''t know/Refused'
  / 
  Q16B
  1  'Yes'
  2  'No'
  3  'Don''t know/Refused'
  / 
  Q16C
  1  'Yes'
  2  'No'
  3  'Don''t know/Refused'
  / 
  Q17
  1  'Yes'
  2  'No'
  3  'Don''t know/Refused'
  / 
  Q18
  1  'Big difference'
  2  'Small difference'
  3  'No difference'
  4  'Don''t know/Refused'
  / 
  Q19
  1  'Big difference'
  2  'Small difference'
  3  'No difference'
  4  'Don''t know/Refused'
  / 
  Q20A
  1  'Yes'
  2  'No'
  3  'Don''t know/Refused'
  / 
  Q20B
  1  'Yes'
  2  'No'
  3  'Don''t know/Refused'
  / 
  Q20C
  1  'Yes'
  2  'No'
  3  'Don''t know/Refused'
  / 
  Q20D
  1  'Yes'
  2  'No'
  3  'Don''t know/Refused'
  /
  D1
  1  'Male'
  2  'Female'
  /
  D2
  1  '1'
  2  '2'
  3  '3'
  4  '4'
  5  '5'
  6  '6'
  7  '7'
  8  '8'
  9  '9'
  0  '0'
  11 'Don"t know'
   /
  D3
  1  'None, or grade 1-4'
  2  'Grade 5, 6 or 7'
  3  'Grade 8'
  4  'High school incomplate (grade 9-11)'
  5  'High school graduate, grade 12'
  6  'Technical, trade or business after high school'
  7  'Collage/university imcomplete'
  8  'College/university graduate or more'
  9  'Don"t know/no answer'
  /
  D4
  1  'White'
  2  'Black'
  3  'Asian'
  4  'Other'
  5  'Don"t know'
  6  'Refused'
  /
  D5
  1  'Married'
  2  'Widowed'
  3  'Divorced'
  4  'Separated'
  5  'Never married'
  6  'Refused'
  /
  D6
  1  'Less than $10,000'
  2  '$10,000 - 14,999'
  3  '$15,000 - 19,999'
  4  '$20,000 - 29,999'
  5  '$30,000 - 49,999'
  6  '$50,000 - 74,999'
  7  '$75,000 and over'
  8  'Don"t know'
  9  'Refused'
 .  
    
* End of Value Labels .
* End of file .
COMPUTE weight = weight / 100 .
EXECUTE .
