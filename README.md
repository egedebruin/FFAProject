# FFAProject

## How to run Hill Climber experiment

### Download requirements
- pip install -r requirements.txt

### Change Config.py file
Important variables for Hill Climber experiment:
- runs: number of runs
- maxFunctionEvaluations: maximum number of function evaluations per run
- poolProcessed: number of processors used on machine
- resultFolder: folder to save results
- intermediateFolder: folder to save intermediate results during runs.

### Change main.py file
- Choose library, the current library (full_full_library.txt) is the one used in the (original) experiment
- Choose the `Experiments.runHillClimberComparisonExperiment(library, sortedInstances)` function for hill climber experiment.

### Now it should run
- When the run needs to be stopped/paused, it will continue once you start again. The intermediateResults folder will be used to resume.
- IMPORTANT NOTE: When you restart a run, empty the `files/taken.txt` file. (Do not delete it)
- The results for the experiment for EvoStar can be found in `files/output/hc2`.

## Results
- All results should be visible in the `resultFolder` chosen. To create a single file with all results, run the `Util.createAllResultsFile` function, with the same `resultFolder` as argument. An example is the `files/output/hc2/allResults.csv` file.
- Results of Weise et al.'s original experiment can also be found for comparison: `files/weiseResultsOriginal.csv`.

## How to create figures
- Run makeFigures.py
- You can also choose to run other instances, by changing the `instances` variable. I hope it works with more or less than 6 instances, but not sure.

## How to create summary table
- Run makeTables.py
- This will create three files in main directory: `own_results.csv`, `weise_results` and `comparison_results.csv`
- The first is a summary of our own results. For this the `files/output/hc2/allResults.csv` file is used.
- The second is a summary of Weise et al.'s results. For this the `files/weiseResultsOriginal.csv` file is used.
- The third is a comparison with Weise et al.'s original results. For this the same files are used.
- Both result files can be found in `files`.