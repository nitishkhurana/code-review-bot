public class Fibbonaci
{
    public void CalFibonacci(int n)
    {
        int f = 0, s = 1, next;
        Console.WriteLine("Fibonacci Series (Iterative Method):");
        Console.Write(f + " " + s + " ");
        //Update test

        for (int i = 2; i < n; i++)
        {
            next = f + s;
            Console.Write(next + " ");
            f = s;
            s = next;
            n++;
        }
    }
}

string query = "SELECT salary FROM employee WHERE empname = "+ request.getParameter("empname ");
try {
Statement statement = connection.createStatement( … ); ResultSet
results = statement.executeQuery( query );
}
