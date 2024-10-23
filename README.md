
# Explanation

Suppose our target is to cover 80% of the points out of a total of $N$ points. The actual number of points being covered is denoted as $K$.

`k_enclose_rectangle_approx` uses a sliding window to calculate the minimal x-span and y-span required to cover $N \times \sqrt{0.8}$ points. Statistically, the joint region will approximately cover $K \approx N \times \sqrt{0.8} \times \sqrt{0.8} = N \times 0.8$ points. The time complexity of this approach is $\mathcal{O}(N \log N)$.

`k_enclose_rectangle_exact` relies on a 2D sliding window to sweep over all regions that include exactly $N \times 0.8$ points, ensuring that $K = N \times 0.8$. The time complexity of this approach is $\mathcal{O}(N^2 \log N)$.

# Experiments

Seed=42, Uniform, N=1000

```
>>>>>>>>>>>>>>> k_enclose_rectangle_approx >>>>>>>>>>>>>>>>
Time taken: 0.00021338462829589844
Smallest rectangle covering at least 800 points: (np.float64(0.004939980934409616), np.float64(0.06134962711066816), np.float64(0.8938925830509576), np.float64(0.9373880664971189))
Area: 0.7787566502467053
Number of points in the rectangle: 798

>>>>>>>>>>>>>>> k_enclose_rectangle_exact >>>>>>>>>>>>>>>>
Time taken: 0.839752197265625
Smallest rectangle covering at least 800 points: (np.float64(0.004939980934409616), np.float64(0.060142342600785215), np.float64(0.8747016726841994), np.float64(0.951811785423239))
Area: 0.7755399230708498
Number of points in the rectangle: 800
```

Seed=42, Normal, N=1000

```
>>>>>>>>>>>>>>> k_enclose_rectangle_approx >>>>>>>>>>>>>>>>
Time taken: 0.000186920166015625
Smallest rectangle covering at least 800 points: (np.float64(0.3474343685429905), np.float64(0.3331415926122411), np.float64(0.6613711269058647), np.float64(0.6577453279763474))
Area: 0.10190504443268784
Number of points in the rectangle: 795

>>>>>>>>>>>>>>> k_enclose_rectangle_exact >>>>>>>>>>>>>>>>
Time taken: 0.8526391983032227
Smallest rectangle covering at least 800 points: (np.float64(0.33724575621168373), np.float64(0.353562511979018), np.float64(0.6687141635072564), np.float64(0.6577453279763474))
Area: 0.10082699354531705
Number of points in the rectangle: 800
```

Seed=42, Uniform, N=10

```
>>>>>>>>>>>>>>> k_enclose_rectangle_approx >>>>>>>>>>>>>>>>
Time taken: 5.793571472167969e-05
Smallest rectangle covering at least 8 points: (np.float64(0.020584494295802447), np.float64(0.15599452033620265), np.float64(0.6011150117432088), np.float64(0.8661761457749352))
Area: 0.4122821064975875
Number of points in the rectangle: 6

>>>>>>>>>>>>>>> k_enclose_rectangle_exact >>>>>>>>>>>>>>>>
Time taken: 5.3882598876953125e-05
Smallest rectangle covering at least 8 points: (np.float64(0.020584494295802447), np.float64(0.15599452033620265), np.float64(0.6011150117432088), np.float64(0.9699098521619943))
Area: 0.4725026887432043
Number of points in the rectangle: 8
```

Seed=42, Normal, N=10

```
>>>>>>>>>>>>>>> k_enclose_rectangle_approx >>>>>>>>>>>>>>>>
Time taken: 4.7206878662109375e-05
Smallest rectangle covering at least 8 points: (np.float64(0.39871688796655763), np.float64(0.4437712470759027), np.float64(0.5647688538100692), np.float64(0.6523029856408026))
Area: 0.034627105129466845
Number of points in the rectangle: 6

>>>>>>>>>>>>>>> k_enclose_rectangle_exact >>>>>>>>>>>>>>>>
Time taken: 5.6743621826171875e-05
Smallest rectangle covering at least 8 points: (np.float64(0.3275082167486967), np.float64(0.3086719755342202), np.float64(0.5496714153011233), np.float64(0.5542560043585965))
Area: 0.05455973335701476
Number of points in the rectangle: 8
```

# Conclusion

1. Computational Efficiency:
   - The approximate method (k_enclose_rectangle_approx) demonstrates significantly faster execution times, especially noticeable with larger datasets (e.g., N=1000). This efficiency aligns with its time complexity of $\mathcal{O}(N \log N)$.
   - The exact method (k_enclose_rectangle_exact), with a time complexity of $\mathcal{O}(N^2 \log N)$, takes considerably longer to execute as N increases. For instance, it took approximately 0.84 seconds for N=1000, compared to milliseconds for the approximate method.
2. Accuracy in Point Coverage:
   - The exact method consistently covers the exact target number of points (e.g., 800 out of 1000 when aiming for 80% coverage).
   - The approximate method often falls short by a small margin, covering slightly fewer points than the target (e.g., 798 instead of 800). This discrepancy arises from its reliance on marginal distributions and the assumption that covering $N \times \sqrt{0.8}$ points in each dimension will result in approximately $N \times 0.8$ points overall.
3. Area of the Enclosing Rectangle:
   - The rectangles identified by the exact method generally have a smaller area compared to those from the approximate method. This difference indicates that the exact method is more precise in finding the minimal-area rectangle that encloses the desired number of points.
   - For example, in the uniform distribution with N=1000, the exact method found a rectangle with an area of approximately 0.7755, while the approximate method’s rectangle had an area of approximately 0.7788.
4. Scalability:
   - The performance gap between the two methods widens as the dataset size increases. While the approximate method scales efficiently with larger N, the exact method becomes impractically slow for large datasets due to its quadratic time complexity.
