using System;
using System.Linq;

/*
alle produkte aus den summanden der summen die man nur aus nicht primzahlen bilden kann
*/

namespace Rätsel
{
    class Program
    {
        
        static void Main()
        {
            int[] primes = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47};
            int[] notprimes = {4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30, 32, 33, 34, 35, 36, 38, 39, 40, 42, 44, 45, 46, 48, 49, 50};
            Console.WriteLine(string.Join(" ", (summen(notprimes, summenprimes(primes)))));
            Console.ReadLine();
        }

        static int[] summen(int[] notprimes, int[] summenprimes)
        {
            int[] summennotprimes = new int[390];
            int[] produkte = new int[1156];
            int anzahl = 0;
            for (int i = 0; i < notprimes.Length; i++)
            {
                for (int i2 = 0; i2 < notprimes.Length; i2++)
                {
                    if (durchsuchen(summenprimes, notprimes[i] + notprimes[i2])==false)
                    {
                        summennotprimes[anzahl] = notprimes[i] + notprimes[i2];
                        produkte[anzahl] = notprimes[i] * notprimes[i2];
                        anzahl++;
                    }
                }
            }
            Console.WriteLine("folgende Summen sind nur durch nicht primzahlen bildbar:");
            Sort(summennotprimes, 0, summennotprimes.Length-1);
            Console.Write(string.Join(" ", summennotprimes));
            Console.Write(" / ");
            Console.WriteLine(summennotprimes.Distinct().ToArray().Length);
            Console.Write("Anzahl der Produkte: ");
            Console.WriteLine(anzahl);
            Console.Write("Anzahl der Produkte(gekürzt): "); 
            Console.WriteLine(produkte.Distinct().ToArray().Length);
            Sort(produkte, 0, produkte.Length -1);
            return produkte.Distinct().ToArray();
        }

        static int[] summenprimes(int[] primes)
        {
            int[] summenprimes = new int[225];
            int anzahl = 0;
            for (int i = 0; i < primes.Length; i++)
            {
                for (int i2 = 0; i2 < primes.Length; i2++)
                {
                    summenprimes[anzahl] = primes[i] + primes[i2];
                    anzahl++;
                }
            }
            Console.WriteLine("Alle Summen die aus Primzahlen gebildet werden können:");
            Sort(summenprimes, 0 , summenprimes.Length-1);
            Console.WriteLine(string.Join(" ", summenprimes));
            Console.WriteLine("Ohne doppelte: ");
            Console.WriteLine(string.Join(" ", summenprimes.Distinct().ToArray()));
            return summenprimes.Distinct().ToArray();
        }

        static bool durchsuchen(int[] summenprimes, int Zahl)
        {
            bool erg = false;
            for (int i = 0; i < summenprimes.Length; i++)
            {
                if (summenprimes[i] == Zahl)
                {
                    erg = true;
                    //Console.Write(summenprimes[i]);
                    //Console.Write(" ");
                    i = summenprimes.Length;
                }
            }
            return erg;
        }

        static int Partition(int[] array, int low,
                                    int high)
    {
        //1. Select a pivot point.
        int pivot = array[high];

        int lowIndex = (low - 1);

        //2. Reorder the collection.
        for (int j = low; j < high; j++)
        {
            if (array[j] <= pivot)
            {
                lowIndex++;

                int temp = array[lowIndex];
                array[lowIndex] = array[j];
                array[j] = temp;
            }
        }

        int temp1 = array[lowIndex + 1];
        array[lowIndex + 1] = array[high];
        array[high] = temp1;

        return lowIndex + 1;
    }

        static void Sort(int[] array, int low, int high)
    {
        if (low < high)
        {
            int partitionIndex = Partition(array, low, high);

            //3. Recursively continue sorting the array
            Sort(array, low, partitionIndex - 1);
            Sort(array, partitionIndex + 1, high);
        }
    }
    
    }
}
