# Similarity Checker
This Python Module is used for comparing string values on similarity. The output is a list which is filled with the string values that are within the similarity requirements.
V.0.1.0 | Made by: Jekkow

## How does it work:
The module creates string-sets of 2 of every string value it is compared with. These sets will be created by taking the first index character with the adjacent index. The following set is the previous index+1 and the adjacent index. These sets will be compared with the string-sets of the master string value.

Due to possible human error there is extra space for margin. The possible scenarios of human error are:
-Wrong character(s)
-Extra character(s)
-Less character(s)

To manage these alternative scenarios, the module takes into consideration the set difference position index offset and also the length difference count value. While comparing string-sets it takes these values to check if the string and string-sets are valid to be compared. If these are not valid these will be excluded from the similarity check.

These Variables are changeable to the limit value of preference:
*Set_Difference*
Set_Difference is the position index offset. With this variable the module will exclude string sets that are beyond the index offset of the master string set index.
*Length_Difference*
Length_Difference is the total length of the string values to be compared to the master string. When the string value is beyond the master string length it will be excluded from the comparison.
*Minimum_Percentage*
Minimum_Percentage is the minimum percentage of similarity required to be included in the output of the module.

### Example:
Neon Trees is the master string value, which will be created in the following string-sets of 2
NE - EO - ON - NT - TR - RE - EE - ES >>> 8 sets  ORIGINAL

Nean Trees
NE - EA - AN - NT - TR - RE - EE - ES >>> 8 sets  1 Letter misspelled, SimilarityScore of 0,75
Neon Tres
NE - EO - ON - NT - TR - RE – ES >>> 7 sets  1 Letter missing, SimilarityScore of 0,75
Neon Treees
NE - EO - ON - NT - TR - RE - EE - EE - ES >>> 9 sets  1 additional Letter typed, SimilarityScore of 0,875
Neonn Treees
NE - EO - ON - NN - TR - RE - EE - EE – ES >>> 9 sets  2 additional Letters typed, wont be included in the output due to the length

Neonas
NE – EO – ON – NA – AS >>> 5 sets

Due to the length count of Neonas is 6, Neonas wont be included in the check due to the master string length being 9. Which means that only string values with an length of 8,9,10 will be used.

### EXAMPLE 2
String value 1: ABCDEFGHI
String-sets 1: AB-BC-CD-DE-EF-FG-GH-HI
String value 2: HILMNOPQR
String-sets 2: HI-IL-LM-MN-NO-OP-PQ-QR

(set.count + set_difference) or (set.count - set_difference) != master_set.count
In the first string-set [HI] is the last index while in the second string-set [HI] is in the first index. Therefore, these cannot be similar to each other and will be excluded from the check.

## How to Use:
```py
#Import the module
from similaritychecker import checker

#Create the Constructor:
SC = checker()

#Set the values:
SC.Set_Difference = 
#(Default = 1)
SC.Length_Difference = 
#(Default = 1)
SC.Minumum_Percentage = 
#(Default = 0.75)

#Use the check method:
SC.Check(“string*”, [“List*”]
#String* = the string that need to be compared with
#List* = The List that contains the word(s) that the master string value will be compared with
 ```