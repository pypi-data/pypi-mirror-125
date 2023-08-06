import plotly.graph_objects as go
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import logging as log
import scipy


class BaseOptimizationAlgorithm(ABC):

    def __init__(self,
                 objective_function,
                 n_iteration: int = 1000,
                 timeout: int = None,
                 population_size=50,
                 minimize=True):
        self.objective_function = objective_function
        self.minimize = minimize
        self.population_size = population_size
        self.n_iteration = n_iteration
        self.timeout = timeout

    @abstractmethod
    def fit(self):
        pass

    def sigmoid(self, x):
        return 1/(1+np.exp(-x))

    def _evaluate_fitness(self, model, x_train, y_train, x_valid, y_valid):
        scores = []
        for i, individual in enumerate(self.individuals):
            chosen_features = [index for index in range(
                x_train.shape[1]) if individual[index] == 1]
            x_train_copy = x_train.iloc[:, chosen_features]
            x_valid_copy = x_valid.iloc[:, chosen_features]

            feature_hash = '_*_'.join(
                sorted(self.feature_list[chosen_features]))
            if feature_hash in self.feature_score_hash.keys():
                score = self.feature_score_hash[feature_hash]
            else:
                score = self.objective_function(
                    model, x_train_copy, y_train, x_valid_copy, y_valid)
                if not(self.minimize):
                    score = -score
                self.feature_score_hash[feature_hash] = score

            if score < self.best_score:
                self.best_score = score
                self.best_dim = individual
            scores.append(score)
        return scores

    def iteration_objective_score_monitor(self, i):
        if self.minimize:
            self.best_results_per_iteration[i] = {'best_score': self.best_score,
                                                  'objective_score': np.array(self.fitness_scores).min(),
                                                  'selected_features': list(self.feature_list[
                                                      np.where(self.individuals[np.array(self.fitness_scores).argmin()])[0]])}
        else:
            self.best_results_per_iteration[i] = {'best_score': -self.best_score,
                                                  'objective_score': -np.array(self.fitness_scores).min(),
                                                  'selected_features': list(self.feature_list[
                                                      np.where(self.individuals[np.array(self.fitness_scores).argmin()])[0]])}

    def initialize_population(self, x):
        self.individuals = np.random.randint(
            0, 2, size=(self.population_size, x.shape[1]))

    def _check_params(self, model, x_train, y_train, x_valid, y_valid):
        if (self.n_iteration <= 0):
            raise ValueError(
                f"n_init should be > 0, got {self.n_iteration} instead.")

        if (self.population_size <= 0):
            raise ValueError(
                f"population_size should be > 0, got {self.population_size} instead.")

        if (not (callable(self.objective_function))):
            raise TypeError(f"objective_function should be a callable function that returns\
                            metric value, got {type(self.objective_function)} instead")

        if y_train is None:
            raise ValueError(
                f"requires y_train to be passed, but the target y is None.")

        if x_train is None:
            raise ValueError(
                f"requires X_train to be passed, but the target X_train is None.")

        if (type(x_train) != pd.core.frame.DataFrame):
            raise TypeError(f" X_train should be of type pandas.core.frame.DataFrame,\
                            got {type(x_train)} instead.")

        if (type(x_valid) != pd.core.frame.DataFrame):
            raise TypeError(f" X_valid should be of type pandas.core.frame.DataFrame,\
                            got {type(x_valid)} instead.")

        if x_train.shape[1] != x_valid.shape[1]:
            raise ValueError(f" X_train and X_valid should have same number of features,\
                             got { x_train.shape[1]},{x_valid.shape[1]} instead.")

        if x_valid is None:
            raise ValueError(
                f"requires X_valid to be passed, but the target X_train is None.")

        if y_valid is None:
            raise ValueError(
                f"requires X_valid to be passed, but the target y_valid is None.")

        return_val = self.objective_function(
            model, x_train, y_train, x_valid, y_valid)
        if (not (isinstance(return_val, (int, float)))):
            raise TypeError(
                f"objective_function should return int/float value , got {type(return_val)} instead.")

    def plot_history(self):
        """
        Plot objective score history
        """
        res = pd.DataFrame.from_dict(self.best_results_per_iteration).T
        res.reset_index(inplace=True)
        res.columns = ['iteration', 'best_score',
                       'objective_score', 'selected_features']
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=res['iteration'], y=res['objective_score'],
                                 mode='markers', name='objective_score'))
        fig.add_trace(go.Scatter(x=res['iteration'], y=res['best_score'],
                                 mode='lines+markers',
                                 name='best_score'))
        fig.update_xaxes(title_text='Iteration')
        fig.update_yaxes(title_text='objective_score')
        fig.update_layout(
            title="Optimization History Plot")
        fig.show()

    def _check_individuals(self):
        if (self.individuals.sum(axis=1) == 0).sum() > 0:
            log.warning(str((self.individuals.sum(axis=1) ==
                        0).sum())+' individuals went zero')
            self.individuals[self.individuals.sum(axis=1) == 0] = np.random.randint(0, 2,
                                                                                    (self.individuals[self.individuals.sum(axis=1) == 0].shape[0],
                                                                                     self.individuals[self.individuals.sum(axis=1) == 0].shape[1]))

    def verbose_results(self, verbose, i):
        if verbose:
            if i == 0:
                print(
                    "\t\t Best value of metric across iteration \t Best value of metric across population  ")
            if self.minimize:
                print(
                    f"Iteration {i} \t {np.array(self.fitness_scores).min()} \t\t\t\t\t {self.best_score} ")
            else:
                print(
                    f"Iteration {i} \t {-np.array(self.fitness_scores).min()} \t\t\t\t\t {-self.best_score} ")
