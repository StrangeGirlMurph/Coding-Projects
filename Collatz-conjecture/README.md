# Collatz-conjecture

Code to calculate the tree of the collatz conjecture in python with numba.

## Explanation/thought process for myself (German)

Eine Startnummer
- ist sie gerade teile durch 2 (n -> n/2)
- ist sie ungerade multipiziere sie mit 3 und addiere 1 hinzu (n -> 3n+1)

sobald n eins wird ist die dauerschleife erreicht

jede ungerade Zahl wird durch 3n+1 gerade und muss direkt durch 2 geteilt werden

wenn n auf dem Baum der vorherigen Verläufe gefunden wird kann man dem einfach folgen