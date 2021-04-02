from tests.RunSamples import Test
from tests.TestIterations import TestByN, TestByP, TestSuccessByRandStart
from visualizers.DataPlot import plot_data, SetupLibraries

if __name__ == "__main__":
    SetupLibraries()
    #  plot_data("this is a test", "test", "test", [{'X': [0, 1], 'Y': [1, 0], 'name':
    #      "test"}], 'test_do_nut_mind_this')
    #  TestByP(start=0.12, end=.36, diff=0.04, tries=10, nodes=20)
    #  TestByN(start=5, end=25, diff=2, tries=10, p=0.2)
    #  TestSuccessByRandStart(start=0.0, end=0.36, diff=0.04, tries=10, p=0.2,
    #          nodes=20)
    Test(save=True)
