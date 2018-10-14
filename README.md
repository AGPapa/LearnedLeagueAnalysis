# LearnedLeagueAnalysis

LearnedLeague is an online trivia competition where players compete against one opponent each day to answer six questions.

This project looked to use machine learning to predict whether or not a player would get a specific question correct based on their answers to past questions. A stocastic gradient descent algorithm with one hidden layer and L2 weight regulation. This was implemented using Pytorch only as a linear algebra library (and not for its machine learning capabilites) since this was meant as an educational refresher exercise for me.

The question chosen to predict was `'Beale fired - Obscentities Prokoke Record Calls' is the hedline of a fictional 1975 edition of the New Work Daily News that appears in what film?` (the answer is, of course, <i>Network</i>). This question was chosen since  close to half (53%) of players got the answer correctly, meaning that any testing accuracy over 53% would be better than random guessing. Ultimatley, the algorithm produced a testing accuracy of 81%, meaning that based on a player's answers to 599 other, totally unrelated questions, we can get a pretty good idea if they would have known the answer to this question about <i>Network</i>.
