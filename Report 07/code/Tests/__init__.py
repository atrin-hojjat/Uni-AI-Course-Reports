from . import (TestMushrooms, TestDecisionMushrooms, 
        TestRandomForestMushrooms, TestPerceptronMushrooms, )

tests = [
        ("Compare perceptron/decision tree/random forest for Mushrooms dataset",
            TestMushrooms),
        ("Test Decision Trees on Mushroom dataset",
            TestDecisionMushrooms),
        ("Test Random Forest on Mushroom dataset",
            TestRandomForestMushrooms),
        ("Test Perceptron on Mushroom dataset",
            TestPerceptronMushrooms)
        ]
