import LoadTSP
import LoadSAT
from visualizers import SetupLibraries


if __name__ == '__main__':
    SetupLibraries()

    #  print("Loading TSP")
    #  LoadTSP.load_samples()

    print("Running TSP tests")
    LoadTSP.run_tests()

    #  print("Loading SAT")
    #  LoadSAT.load_samples()
    

