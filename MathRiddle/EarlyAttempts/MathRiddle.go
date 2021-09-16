package main

var primes = [15]int{2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47}

//{2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47}
var notprimes = [34]int{4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30, 32, 33, 34, 35, 36, 38, 39, 40, 42, 44, 45, 46, 48, 49, 50}

//{4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30, 32, 33, 34, 35, 36, 38, 39, 40, 42, 44, 45, 46, 48, 49, 50}

func main() {
	var produkte []int
	var summen []int
	produkte = produkt()
	möglicheSummen(summen, summenprime())
}

func möglicheSummen(summen []int, summenprime []int) {
	for i := 0; i < len(summen); i++ {
		for i := 0; i < len(summen); i++ {

		}
	}
}

func summenprime() []int {
	var ergebnisse []int
	ergebnisse = make([]int, 225)
	var anzahl int = 0
	for i := 0; i < len(primes); i++ {
		for i2 := 0; i2 < len(primes); i2++ {

			ergebnisse[anzahl] = primes[i] + primes[i2]
			anzahl++
		}
	}
	//fmt.Println(anzahl)
	return quickSort(ergebnisse)
}

func summen() []int {
	var ergebnisse []int
	ergebnisse = make([]int, 1156)
	var anzahl int = 0
	for i := 0; i < len(notprimes); i++ {
		for i2 := 0; i2 < len(notprimes); i2++ {
			ergebnisse[anzahl] = notprimes[i] + notprimes[i2]
			anzahl++
		}
	}
	//fmt.Println(anzahl)
	return quickSort(ergebnisse)
}

func produkt() []int {
	var ergebnisse []int
	ergebnisse = make([]int, 1156)
	var anzahl int = 0
	for i := 0; i < len(primes); i++ {
		for i2 := 0; i2 < len(primes); i2++ {
			ergebnisse[anzahl] = primes[i] * primes[i2]
			anzahl++
		}
	}
	//fmt.Println(anzahl)
	return quickSort(ergebnisse)
}

func durchsuchen(array []int, zahl int) bool {
	var erg bool = false
	for i := 0; i < len(array); i++ {
		if array[i] == zahl {
			erg = true
		}
	}
	return erg
}

func quickSort(data []int) []int {
	if len(data) > 1 {
		pivot := data[0]
		smaller := make([]int, 0, len(data))
		equal := make([]int, 1, len(data))
		equal[0] = pivot
		larger := make([]int, 0, len(data))
		for i := 1; i < len(data); i++ {
			if data[i] > pivot {
				larger = append(larger, data[i])
			} else if data[i] < pivot {
				smaller = append(smaller, data[i])
			} else {
				equal = append(equal, data[i])
			}
		}
		return append(append(quickSort(smaller), equal...), quickSort(larger)...)
	} else {
		return data
	}
}
