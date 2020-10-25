import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;

public class triangles {

    public static void main(String[] args) throws IOException {
        InputStreamReader in = new InputStreamReader(System.in);
        BufferedReader input = new BufferedReader(in);

        int n = Integer.parseInt(input.readLine());
        Triangle[] triangleList = new Triangle[n];

        if (n <= 0) {
            return;
        }

        for (int i = 0; i < n; i++) {
            String line = input.readLine();
            String[] splitLine = line.split(" ");
            triangleList[i] = new Triangle(
                    Integer.parseInt(splitLine[0]),
                    Integer.parseInt(splitLine[1]),
                    Integer.parseInt(splitLine[2]),
                    Double.parseDouble(splitLine[3])
            );
        }

        Arrays.sort(triangleList);

        // mem[t][s] represents the length of the longest chain formed that ends with triangle t,
        // where t is joined to the chain using side s.
        int[][] mem = new int[n][3];

        // base cases
        for (int s = 0; s < 3; s++) {
            mem[0][s] = 1;
        }

        for (int t = 1; t < n; t++) {
            for (int s = 0; s < 3; s++) {
                int max = 1;
                for (int prevTriangle = 0; prevTriangle < t; prevTriangle++) {
                    if (triangleList[prevTriangle].shade >= triangleList[t].shade) {
                        continue;
                    }
                    for (int joinedEdge = 0; joinedEdge < 3; joinedEdge++) {
                        if (triangleList[prevTriangle].sides[(joinedEdge + 1) % 3] == triangleList[t].sides[s]
                                || triangleList[prevTriangle].sides[(joinedEdge + 2) % 3] == triangleList[t].sides[s]) {
                            max = Math.max(max, mem[prevTriangle][joinedEdge] + 1);
                        }
                    }
                }
                mem[t][s] = max;
            }
        }

        int max = 0;
        for (int t = 0; t < n; t++) {
            for (int s = 0; s < 3; s++) {
                max = Math.max(max, mem[t][s]);
            }
        }
        System.out.println(max);

    }
}

class Triangle implements Comparable<Triangle> {
    int[] sides = new int[3];
    double shade;

    public Triangle(int side0, int side1, int side2, double shade) {
        this.sides[0] = side0;
        this.sides[1] = side1;
        this.sides[2] = side2;
        this.shade = shade;
    }

    @Override
    public int compareTo(Triangle o) {
        return Double.compare(this.shade, o.shade);
    }

}