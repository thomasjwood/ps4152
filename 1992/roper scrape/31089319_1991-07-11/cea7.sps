file handle cea7  /name="c:\USAIPOSPGO1991-USCEA7\CEA7.DAT". 
data list file=cea7 records=1
  /1
	ID	1-4
	D1	5
	D2	6
	D3	7
	D4	8-9
	D5	10
	D6	11
	D8	12
	Q13	19
	Q14A	20
	Q14B	21
	Q15	22
	Q16	23
	S1	13
	S2	14-15
	REGION	16
	S3	17-18.
Variable Labels
	D1 "Education"
	D2 "Race"
	D3 "Ethnicity"
	D4 "Occupation"
	D5 "Marital Status"
	D6 "Marital Status 2"
	D8 "Income"
	Q13 " How important a role should nuclear energy play in meeting this nation's future energy needs? Should nuclear energy play a very important role, a somewhat important role, not too important a role, or not an important role at all? "
	Q14A "Agree-Disagree: Using nuclear energy to generate electricity cuts greenhouse gas emissions and air pollution?"
	Q14B "Agree-Disagree: We should use more nuclear energy if that will cut greenhouse gas emissions and air pollution?"
	Q15 "Using a scale from one to seven, where 1 means do not identify with at all, and 7 means strongly identify with, please tell me how much you identify yourself with the label environmentalist?"
	Q16 "In the past year, have you or has anyone in your household donated to or been active in a group or organization working to protect the environment?"
	S1 "Sex"
	S2 "State"
	REGION "Region"
	S3 "Age".
Value Labels
  D1 1 "Less than high school graduate" 2 "High school graduate" 3 "Some college" 4 "Trade-Technical-Vocational Training" 5 "College graduate" 6 "Post-graduate work" 7 "DK" 8 "Refused" /
  D2 1 "White" 2 "Black" 3 "Some other" 4 "DK" 5 "Refused"/
  D3 1 "Yes" 2 "No" 3 "DK" 4 "Refused"/
  D4 1 "Other" 2 "DK" 3 "Refused" 4 "Unemployed" 6 "Student" 7 "Housewife" 8 "Retired-Disabled" 9 "Professional-Managerial" 10 "Secretarial-Labor" 11 "Services-Labor" 12 "Sales-Retail sales" 13 "Farmer-Rancher" 14 "Military" 15 "Self-employed"/
  D5 1 "Single" 2 "Married" 3 "Separated" 4 "Divorced" 5 "Widowed" 6 "Refused"/
  D6 1 "Divorced" 2 "Widowed" 3 "Separated" 4 "Never been married" 5 "Refused"/
  D8 1 "Under $10,000" 2 "$10,000 to $19,999" 3 "$20,000 to $29,999" 4 "$30,000 to $39,999" 5 "$40,000 to $59,999" 6 "$60,000 to $74,999" 7 "$75,000 to $99,999" 8 "$100,000 or more" 9 "DK" 0 "Refused"/
  Q13 1 "Very important role" 2 "Somewhat important role" 3 "Not too important role" 4 "Not an important role at all" 5 "DK" 6 "Refused"/
  Q14A 1 "Agree" 2 "Disagree" 3 "DK" 4 "Refused"/
  Q14B 1 "Agree" 2 "Disagree" 3 "DK" 4 "Refused"/
  Q15 1 "Do not identify" 7 "Strongly identify with" 8 "DK" 9 "Refused"/
  Q16 1 "Yes" 2 "No" 3 "DK" 4 "Refused"/
  S1 1 "Male" 2 "Female"/
  S2 01 "Alabama" 02 "Alaska" 04 "Arizona" 05 "Arkansas" 06 "California" 08 "Colorado" 09 "Connecticut" 10 "Delaware" 11 "Washington DC" 12 "Florida" 13 "Georgia" 15 "Hawaii" 16 "Idaho" 17 "Illinois" 18 "Indiana" 19 "Iowa" 20 "Kansas" 21 "Kentucky" 22 "Louisiana" 23 "Maine" 24 "Maryland" 25 "Massachusetts" 26 "Michigan" 27 "Minnesota" 28 "Mississippi" 29 "Missouri" 30 "Montana" 31 "Nebraska" 32 "Nevada" 33 "New Hampshire" 34 "New Jersey" 35 "New Mexico" 36 "New York" 37 "North Carolina" 38 "North Dakota" 39 "Ohio" 40 "Oklahoma" 41 "Oregon" 42 "Pennsylvania" 44 "Rhode Island" 45 "South Carolina" 46 "South Dakota" 47 "Tennessee" 48 "Texas" 49 "Utah" 50 "Vermont" 51 "Virginia" 53 "Washington" 54 "West Virginia" 55 "Wisconsin" 56 "Wyoming"/
  REGION 1 "East" 2 "Midwest" 3 "South" 4 "West"/
  S3 00 "Refused" 99 "99+".
Execute. 