***Probabilistic model: Determining roads which are underserved based on
traffic volumes***

**OVERVIEW**

1.  **Data preparation:**

>a\. Deduct 20% from battery range during winter months due to cold
>battery performance.
>
>b\. Adjust traffic volume for rush hours or days, considering
>assumptions.

2.  **Charging probability:**

>a\. For each edge, compute the charging probability using the formula: p
>= edge-length / battery-range.
>
>b\. Consider elevation changes that may affect edge length.

3.  **Charging demand:**

>a\. Compute the number of charging cars on each edge using the formula:
>c = traffic / p.
>
>b\. Calculate the demand for chargers (d) using the formula: d = c /
>(charging time). Use 60 minutes for 50+ KW chargers.

4.  **Charging supply:**

>a\. For each edge, assign the supply of chargers based on the binary
>variable indicating the presence of a charging station.
>
>b\. Compute the satisfied demand for each edge (s_i) using the formula:
>s_i = min(d_i, s_A), where s_A is the total supply from charging
>stations.
>
>c\. Allocate excess supply (s_A - s_i) among edges reachable from the
>center of the edge within a \"meaningful\" radius (e.g., 10km driving
>distance) evenly proportional to their length.

5.  **Identify underserved edges:**

>a\. Find underserved edges (j) where d_j \> s_j for each month.
>
>b\. If needed, aggregate the results across all months, using either the
>maximum traffic for each edge and month or computing everything once per
>month.

6.  **Optimization:**

>a\. Formulate an optimization problem to place a minimum number of
>chargers on each underserved edge (j) such that s_j \>= d_j.
>
>b\. Solve the optimization problem to determine the optimal placement of
>charging stations.

7.  **Sensitivity analysis and model refinement:**

>a\. Evaluate the impact of different assumptions, such as quality of
>service, waiting times, and charger capacities.
>
>b\. Refine the model using additional data or insights, such as hourly
>traffic data, if available.

8.  **Analyze and visualize results:**

>a\.  Analyze the results to identify patterns and trends in the demand
>    and supply of chargers. b. Create visualizations to communicate our
>    findings effectively.
    
    
    
```{=html}
<!--Step by Step Plans-->
```



**Step 1: Data Prep**

1.  **Import and clean the dataset:**

>a\. Load the dataset containing edge information, traffic volume, and
>the presence of charging stations.
>
>b\. Check for missing or inconsistent values and handle them
>appropriately (e.g., remove, impute, or correct).

2.  **Feature engineering:**

>a\. Create a new column for adjusted battery range by deducting 20% from
>the original battery range during winter months. *(assumption)*
>
>b\. Calculate the proportion of traffic during rush hours or days based
>on the provided assumptions, and create a new column to store the
>adjusted traffic volume.
>
>c\. Optionally, derive additional features that may be relevant to the
>analysis, such as elevation changes affecting edge length.

3.  **Data transformation:**

>a\. Normalize or standardize relevant features if necessary, depending
>on the requirements of our analysis or optimization model.

4.  **Temporal data handling:**

>a\. If our dataset is in a time-series format, ensure that the data is
>sorted chronologically.
>
>b\. Divide the dataset into separate subsets for each month, so that you
>can perform the analysis on a monthly basis.

5.  **Data exploration:**

>a\. Perform exploratory data analysis to gain insights into the
>relationships between variables, identify patterns, and detect any
>anomalies.
>
>b\. Create visualizations to better understand the data, such as
>histograms, scatter plots, and heatmaps.

6.  **Save the prepared data:**

>a\. Save the cleaned and transformed dataset in an appropriate format
>(e.g., CSV, Excel, or a database) for further analysis and modelling.
>
>b\. Document the data preparation steps, and any assumptions made, so
>that anyone can easily replicate the process or make adjustments in the
>future.

```{=html}
<!--Next Step-->
```

**Step 2: Charging Probability**

1.  **Define constants and assumptions:**

>a\. Set the battery range based on our research or assumptions, e.g.,
>300 km for an average EV.
>
>b\. Determine the battery range reduction during winter months, e.g.,
>20% reduction.

2.  **Create a new column for adjusted battery range:**

>a\. Calculate the battery range for each month by applying the winter
>reduction when applicable.
>
>b\. Add a new column in our dataset to store the adjusted battery range
>for each edge and month.

3.  **Compute the charging probability:**

>a\. For each edge, calculate the charging probability using the formula:
>p = edge-length / adjusted battery-range.
>
>b\. Store the charging probability in a new column in our dataset for
>each edge and month.

4.  **Consider elevation changes (*optional*):**

>a\. If elevation data is available, calculate the impact of elevation
>changes on edge length.
>
>b\. Adjust the charging probability by incorporating the modified edge
>length due to elevation changes.

5.  **Data validation and exploration:**

>a\. Check the calculated charging probabilities for any unexpected
>values or inconsistencies. b. Perform exploratory data analysis to
>understand the distribution of charging probabilities across the road
>network.
>
>c\. Create visualizations, such as histograms or heatmaps, to explore
>the spatial distribution of charging probabilities.

6.  **Save the results:**

>a\. Save the dataset with the calculated charging probabilities in an
>appropriate format (e.g., CSV, Excel, or a database) for further
>analysis.
>
>b\. Document the steps, constants, and assumptions used in calculating
>charging probabilities for reproducibility and future reference.

```{=html}
<!--Next Step -->
```

**Step 3: Charging Demand**

1.  **Define constants and assumptions:**

> a\. Set the charging time for a 50+ KW charger, e.g., 60 minutes.
>
> b\. Determine the traffic adjustments for rush hours or days, based on
> the assumptions provided in our message or other relevant data.

2.  **Adjust traffic volume for rush hours or days:**

> a\. Create a new column in our dataset to store the adjusted traffic
> volume for each edge and month.
>
> b\. Calculate the adjusted traffic volume by applying the rush hour or
> day multipliers to the average daily traffic volume.

3.  **Compute the number of charging cars on each edge:**

> a\. For each edge, calculate the number of charging cars using the
> formula: c = adjusted traffic / charging probability.
>
> b\. Add a new column in our dataset to store the number of charging
> cars for each edge and month.

4.  **Calculate the demand for chargers:**

> a\. For each edge, compute the demand for chargers (d) using the
> formula: d = number of charging cars / (charging time in hours).
>
> b\. Store the demand for chargers in a new column in our dataset for
> each edge and month.

5.  **Data validation and exploration:**

> a\. Check the calculated charging demand values for any unexpected
> values or inconsistencies.
>
> b\. Perform exploratory data analysis to understand the distribution
> of charging demand across the road network.
>
> c\. Create visualizations, such as histograms or heatmaps, to explore
> the spatial distribution of charging demand.

6.  **Save the results:**

> a\. Save the dataset with the calculated charging demand in an
> appropriate format (e.g., CSV, Excel, or a database) for further
> analysis.
>
> b\. Document the steps, constants, and assumptions used in calculating
> charging demand for reproducibility and future reference.

```{=html}
<!--Next Step -->
```

**Step 4: Charging Supply**

1.  **Define constants and assumptions:**

>a\. Set the \"meaningful\" radius for aggregating edges around a
>charging station, e.g., 10 km driving distance.
>
>b\. Determine the number of chargers at each charging station or make an
>assumption if this information is not available in our dataset.

2.  **Identify edges with charging stations:**

>a\. Filter our dataset to identify edges that have a charging station.
>
>b\. Create a new column in our dataset to store the total supply (s) of
>chargers for each edge.

3.  **Calculate the supply for each edge with a charging station:**

>a\. For each edge with a charging station, set the total supply (s)
>equal to the number of chargers at the station.
>
>b\. Store the supply of chargers in the newly created column for each
>edge and month.

4.  **Aggregate edges within the \"meaningful\" radius:**

>a\. For each edge with a charging station, identify all other edges
>within the defined radius.
>
>b\. Calculate the total demand (d) for chargers within this aggregated
>group of edges.

5.  **Distribute the excess supply to nearby edges:**

>a\. Calculate the excess supply (s_A - s_i) for each edge with a
>charging station.
>
>b\. Distribute the excess supply proportionally to the nearby edges
>within the \"meaningful\" radius based on their length.

6.  **Identify underserved edges:**

>a\. For each edge, compare the charging demand (d_j) to the charging
>supply (s_j).
>
>b\. Create a list or subset of edges where the demand for chargers
>exceeds the available supply (d_j \> s_j).

7.  **Data validation and exploration:**

>a\. Check the calculated charging supply values for any unexpected
>values or inconsistencies. b. Perform exploratory data analysis to
>understand the distribution of charging supply across the road network.
>
>c\. Create visualizations, such as histograms or heatmaps, to explore
>the spatial distribution of charging supply and underserved edges.

8.  **Save the results:**

>a\. Save the dataset with the calculated charging supply in an
>appropriate format (e.g., CSV, Excel, or a database) for further
>analysis.
>
>b\. Document the steps, constants, and assumptions used in calculating
>charging supply for reproducibility and future reference.

```{=html}
<!--Next Step -->
```

**Step 5: Identifying underserved edges**

1.  **Calculate the supply-demand gap:**

>a\. For each edge and month, calculate the supply-demand gap (g) using
>the formula: g = charging demand (d) - charging supply (s).
>
>b\. Add a new column in our dataset to store the supply-demand gap for
>each edge and month.

2.  **Filter underserved edges:**

>a\. Filter our dataset to identify edges where the supply-demand gap (g)
>is greater than 0, indicating an unmet demand for chargers.
>
>b\. Create a subset or list of these underserved edges for further
>analysis and visualization.

3.  **Sort underserved edges by the supply-demand gap:**

>a.  Sort the filtered underserved edges in descending order based on the
>    supply-demand gap (g) to prioritize the edges with the highest unmet
>    demand.

4.  **Explore the characteristics of underserved edges:**

>a\. Analyze the underserved edges to understand their common
>characteristics, such as edge length, location, traffic volume, or other
>relevant factors.
>
>b\. Identify any patterns or trends that may help inform potential
>solutions for addressing the unmet demand.

5.  **Visualize the underserved edges:**

>a\. Create visualizations, such as heatmaps or other spatial
>representations, to display the locations of underserved edges on a map.
>
>b\. Highlight the areas with the highest supply-demand gaps to emphasize
>the priority locations for potential interventions.

6.  **Analyze temporal variations (optional):**

>a\. If our dataset includes monthly data, explore how the underserved
>edges change over time by analyzing the supply-demand gap for each
>month.
>
>b\. Identify any seasonal patterns or trends that may inform the optimal
>timing for adding or adjusting charging infrastructure.

7.  **Save the results:**

>a\. Save the dataset with the identified underserved edges and the
>calculated supply-demand gaps in an appropriate format (e.g., CSV,
>Excel, or a database) for further analysis.
>
>b\. Document the steps, constants, and assumptions used in identifying
>underserved edges for reproducibility and future reference.

```{=html}
<!--Next Step -->
```

**Step 6: Optimization (optional, see if we have time)**

1.  **Formulate the optimization problem:**

>a\. Define the decision variables: The number of chargers to be
>installed on each underserved edge.
>
>b\. Define the objective function: Minimize the total number of chargers
>installed across all underserved edges.
>
>c\. Define the constraints: The installed chargers should satisfy the
>demand on each underserved edge.

2.  **Choose an optimization algorithm or solver:**

>a.Research and choose an appropriate optimization algorithm or solver
>suitable for our problem, such as linear programming, integer
>programming, or metaheuristic algorithms (e.g., genetic algorithms,
>simulated annealing).

3.  **Prepare the input data:**

>a\. Extract the necessary information from our dataset, such as the
>supply-demand gap and edge lengths, for the chosen optimization
>algorithm.
>
>b\. Standardize or preprocess the data as required by the optimization
>algorithm.

4.  **Implement the optimization algorithm:**

>a\. Develop or use existing software to implement the chosen
>optimization algorithm.
>
>b\. Set up the optimization problem using the prepared input data,
>objective function, and constraints.
>
>c\. Configure the algorithm parameters, such as the stopping criteria,
>population size, or other hyperparameters.

5.  **Run the optimization:**

>a\. Execute the optimization algorithm to search for the optimal
>solution.
>
>b\. Monitor the progress of the optimization and adjust the algorithm
>parameters as needed.

6.  **Analyze the results:**

>a\. Evaluate the quality of the optimal solution and its impact on the
>road network in terms of meeting the charging demand.
>
>b\. Analyze the distribution of installed chargers across the
>underserved edges and identify any patterns or trends.

7.  **Validate the solution:**

>a\. Perform sensitivity analysis to evaluate the robustness of the
>solution with respect to changes in the input data or assumptions.
>
>b\. Test the solution on a subset of the data or under different
>scenarios to assess its generalizability.

8.  **Refine the optimization (if necessary):**

>a\. If the solution quality or robustness is unsatisfactory, revisit the
>optimization problem formulation, algorithm choice, or algorithm
>parameters.
>
>b\. Iterate the optimization process until a satisfactory solution is
>found.

9.  **Document and save the results:**

>a\. Document the optimization process, including the problem
>formulation, algorithm choice, and algorithm parameters.
>
>b\. Save the optimal solution and any relevant visualizations or
>analysis in an appropriate format for future reference and reporting.

```{=html}
<!--Next Step -->
```

**Step 7: Sensitivity analysis**

1.  **Identify key parameters and assumptions:**

>a.  Review our optimization model and dataset to identify the key
>    parameters and assumptions that may influence the solution, such as
>    battery range, charging time, traffic volume, and seasonal
>    variations.

2.  **Define the range of variation for each parameter:**

>a.  For each identified key parameter or assumption, define a reasonable
>    range of variation or alternative values that reflect potential
>    changes in the real-world conditions.

3.  **Create scenarios based on parameter variations:**

>a\. Develop a set of scenarios that encompass the defined range of
>variations for each key parameter or assumption.
>
>b\. Consider using a combination of scenarios that involve changes in
>multiple parameters simultaneously to account for potential interactions
>between them.

4.  **Modify the input data for each scenario:**

>a\. For each scenario, adjust our dataset or optimization model to
>reflect the changed parameter values.
>
>b\. Ensure that the modified input data is consistent with the
>optimization model requirements.

5.  **Run the optimization for each scenario:**

>a\. Execute the optimization algorithm with the modified input data for
>each scenario to obtain a solution.
>
>b\. Monitor the progress of the optimization and adjust the algorithm
>parameters as needed for each scenario.

6.  **Compare the solutions across scenarios:**

>a\. Analyze the differences between the optimal solutions obtained for
>each scenario in terms of the total number of chargers, their
>distribution across underserved edges, and other relevant metrics.
>
>b\. Evaluate the robustness of the original solution by comparing its
>performance with the solutions obtained for the different scenarios.

7.  **Identify sensitive parameters:**

>a\. Determine which parameters have the most significant impact on the
>optimization solution by comparing the variation in the solutions across
>different scenarios.
>
>b\. Prioritize these sensitive parameters for further analysis or
>investigation, as they may require more accurate data or estimation
>methods.

8.  **Document and save the results:**

>a\. Document the sensitivity analysis process, including the scenarios,
>parameter variations, and key findings.
>
>b\. Save the sensitivity analysis results, including the solutions and
>performance metrics for each scenario, in an appropriate format for
>future reference and reporting.

```{=html}
<!--Next Step -->
```

**Step 8: Analyze and visualize results**

1.  **Compile the results:**

>a\. Collect the optimal solutions, performance metrics, and other
>relevant information obtained from the optimization and sensitivity
>analysis steps.
>
>b\. Organize the results in a structured format, such as a spreadsheet
>or a database, to facilitate further analysis and visualization.

2.  **Analyze the performance metrics:**

>a\. Calculate summary statistics, such as the mean, median, and standard
>deviation, for the performance metrics across the different scenarios
>and solutions.
>
>b\. Identify any trends, patterns, or outliers in the performance
>metrics that may indicate the robustness of the solutions or the
>influence of specific parameters.

3.  **Visualize the spatial distribution of chargers:**

>a\. Create a map visualization that displays the location of the
>installed chargers on the road network for each solution.
>
>b\. Use color-coded markers or symbols to represent the density of
>chargers on each edge, and consider including the original charging
>station locations for comparison.
>
>c\. Compare the spatial distribution of chargers across the different
>solutions and scenarios to identify any significant differences or
>patterns.

4.  **Visualize the relationship between parameters and performance
    metrics:**

>a\. Create scatter plots, line charts, or other suitable visualizations
>to display the relationship between the key parameters and the
>performance metrics.
>
>b\. Use these visualizations to identify trends or patterns in the data,
>such as a strong correlation between a specific parameter and the total
>number of chargers needed.

5.  **Visualize the sensitivity analysis results:**

>a\. Create visualizations that illustrate the performance of the
>solutions across the different scenarios, such as bar charts or line
>charts displaying the variation in the performance metrics.
>
>b\. Highlight any significant differences or trends in the results that
>may indicate the sensitivity of the solutions to changes in the key
>parameters or assumptions.

6.  **Evaluate the overall performance of the solutions:**

>a\. Review the analysis and visualizations to assess the quality and
>robustness of the optimization solutions.
>
>b\. Determine if the solutions meet the desired objectives, such as
>minimizing the total number of chargers while satisfying the charging
>demand on the road network.

7.  **Refine the optimization model (if necessary):**

>a\. If the analysis and visualizations reveal issues with the
>optimization solutions, such as a lack of robustness or an
>unsatisfactory performance, consider refining the optimization model,
>data, or assumptions to address these issues.
>
>b\. Iterate the optimization, sensitivity analysis, and result analysis
>steps until a satisfactory solution is achieved.

8.  **Document and present the findings:**

>a\. Summarize the key findings from the analysis and visualizations,
>highlighting the most relevant insights, trends, or patterns.
>
>b\. Prepare a report or presentation that effectively communicates the
>results of our research, including the optimization model, methodology,
>analysis, and visualizations.
>
>c\. Consider incorporating interactive visualizations or dashboards to
>allow stakeholders to explore the data and results in more depth.
