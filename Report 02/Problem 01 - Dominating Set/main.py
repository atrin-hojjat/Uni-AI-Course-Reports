from tests.RunSamples import Test
from tests.TestIterations import TestByN, TestByP, TestSuccessByRandStart

if __name__ == "__main__":
    #  TestByP(start=0.2, end=.3, diff=0.04, tries=10, nodes=20)
    #  TestByN()
    #  TestSuccessByRandStart()
    Test(save=True)
