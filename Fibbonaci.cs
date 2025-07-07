public class Fibbonaci
{
    public void CalFibonacci(int n)
    {
        int first = 0, second = 1, next;
        Console.WriteLine("Fibonacci Series (Iterative Method):");
        Console.Write(first + " " + second + " ");
        //Update test

        for (int i = 2; i < n; i++)
        {
            next = first + second;
            Console.Write(next + " ");
            first = second;
            second = next;
        }
    }
}
